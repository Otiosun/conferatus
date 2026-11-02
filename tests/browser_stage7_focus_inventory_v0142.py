"""Chromium-only keyboard focus inventory for the stage 07.10 sample.

Enumerates Tab stops (actual keyboard modality), tests visible CSS focus outlines,
records potential contrast concerns for manual review; not a screen-reader audit.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf8')
SIZES=(320,740,1440)
SCENARIOS=('ballot','members','governance','calendar','proposals','compose','review')
JS='''() => {
 const e=document.activeElement; if (!e || e===document.body || e===document.documentElement) return null;
 const s=getComputedStyle(e),r=e.getBoundingClientRect();
 return {tag:e.tagName,id:e.id,role:e.getAttribute('role'),label:e.getAttribute('aria-label')||e.innerText?.trim()?.slice(0,36)||e.getAttribute('name')||'',focusVisible:e.matches(':focus-visible'),outlineStyle:s.outlineStyle,outlineWidth:parseFloat(s.outlineWidth)||0,outlineColor:s.outlineColor,width:r.width,height:r.height};
}'''
rows=[];failed=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'],headless=True)
 for width in SIZES:
  for scenario in SCENARIOS:
   page=browser.new_page(viewport={'width':width,'height':900})
   page.goto('about:blank?demo=1');page.set_content(HTML)
   if scenario=='review':
    page.evaluate('location.hash="#/proposals"')
    page.locator('[data-action=new-proposal]').click()
    page.locator('#draft-title').fill('Teste demonstrativo')
    page.locator('#draft-body').fill('Texto suficiente para ir à revisão com teclado.')
    page.locator('[value=conclude]').click()
   else:
    page.evaluate('(route)=>location.hash="#/"+route',scenario)
    if scenario=='calendar':page.locator('[data-action=open-schedule]').click()
    if scenario=='governance':page.locator('[data-action=toggle-tools]').click()
   # Start from an unfocused document and navigate via real keyboard Tab.
   page.locator('body').click(position={'x':2,'y':2})
   seen=set()
   for index in range(36):
    page.keyboard.press('Tab')
    m=page.evaluate(JS)
    if not m:continue
    key=(m['tag'],m['id'],m['label'],m['outlineColor'])
    if key in seen:break
    seen.add(key)
    if m['tag'] not in ('BUTTON','INPUT','TEXTAREA','SELECT','A'):continue
    ok=m['focusVisible'] and m['outlineStyle']!='none' and m['outlineWidth']>=2
    row={'width':width,'state':scenario,'ordinal':index,'passed':ok,**m}
    rows.append(row)
    if not ok:failed.append(row)
   page.close()
 browser.close()
report={'sampled':len(rows),'failed':len(failed),'failures':failed,'rows':rows}
(ROOT/'dist/stage7_focus_inventory_v0142_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'Keyboard focus outline: {len(rows)-len(failed)}/{len(rows)} visible, {len(failed)} missing')
for f in failed[:15]:print(f['width'],f['state'],f['tag'],f['id'],f['label'],f['outlineStyle'],f['outlineWidth'])
assert not failed
