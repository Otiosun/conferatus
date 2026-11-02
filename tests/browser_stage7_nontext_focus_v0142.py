"""Stage 07.10, batch 3: measurable non-text control boundaries and focus.

Chromium offline demo only. Measure actual rendered border against control surface;
contrast of 3:1 is used for the sampled visible UI component boundaries. This is
not a complete WCAG 2.2 audit or a real assistive technology test.
"""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf8')
FIXED=os.environ.get('STAGE7_FIXED','1')=='1'
WIDTHS=(320,390,740,1440)
records=[]
failures=[]
MEASURE=r'''el => {
 function parse(input){let s=input.match(/rgba?\(([^)]+)\)/);if(!s)return null;
  let a=s[1].split(/[, ]+/).filter(Boolean).map(Number);return [a[0],a[1],a[2],a.length>3?a[3]:1];}
 function blend(f,b){return [0,1,2].map(i=>f[i]*f[3]+b[i]*(1-f[3])).concat([1]);}
 function lum(c){const x=c.slice(0,3).map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4});return .2126*x[0]+.7152*x[1]+.0722*x[2]}
 function ratio(a,b){let x=lum(a),y=lum(b);return +((Math.max(x,y)+.05)/(Math.min(x,y)+.05)).toFixed(3)}
 let s=getComputedStyle(el),stack=[];
 for(let p=el.parentElement;p;p=p.parentElement)stack.push(p);
 let outside=[255,255,255,1];
 for(let i=stack.length-1;i>=0;i--){const bg=parse(getComputedStyle(stack[i]).backgroundColor);if(bg)outside=blend(bg,outside)}
 let inside=outside;const eb=parse(s.backgroundColor);if(eb)inside=blend(eb,inside);
 const bc=parse(s.borderTopColor),oc=parse(s.outlineColor),box=el.getBoundingClientRect();
 return {border:s.borderTopWidth,borderColor:s.borderTopColor,borderAgainstInside:bc?ratio(blend(bc,inside),inside):null,borderAgainstOutside:bc?ratio(blend(bc,outside),outside):null,
 surfaceVsOutside:ratio(inside,outside),focusOutline:s.outlineStyle,focusWidth:s.outlineWidth,outlineColor:s.outlineColor,
 focusVsOutside:oc?ratio(blend(oc,outside),outside):null,focusVsInside:oc?ratio(blend(oc,inside),inside):null,
 width:box.width,height:box.height,visible:box.width>0&&box.height>0,css:s.cssText,background:s.backgroundColor,parentBackground:outside};
}'''
def note(width,name,case,m,ok):
  rec={'viewport':width,'name':name,'case':case,'passed':ok,**m}
  records.append(rec)
  if not ok:failures.append(rec)

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in WIDTHS:
  page=browser.new_page(viewport={'width':width,'height':900})
  page.goto('about:blank?demo=1');page.set_content(HTML)
  # Create a concluded local draft so the schedule proposal select is ENABLED.
  page.evaluate('location.hash="#/proposals"')
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Revisão demonstrativa dos controles')
  page.locator('#draft-body').fill('Texto com tamanho suficiente para criar uma proposta fictícia e ativar o seletor.')
  page.locator('[value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.evaluate('location.hash="#/calendar"')
  page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  for name,locator in [('schedule-title',form.locator('input[name=title]')),('schedule-start',form.locator('input[name=start]')),('schedule-proposal',form.locator('select[name=proposalId]'))]:
   m=locator.evaluate(MEASURE)
   # A sufficiently contrasting control boundary or surface is essential for perceiving an empty input.
   ok=max(m['borderAgainstInside'] or 0,m['surfaceVsOutside'])>=3
   note(width,name,'non-text field boundary',m,ok)
   if name=='schedule-proposal':
    form.locator('[name=objective]').focus()
    page.keyboard.press('Tab')
    assert locator.evaluate('e=>document.activeElement===e'),(width,'keyboard traversal not reaching schedule select')
   else: locator.focus()
   m=locator.evaluate(MEASURE)
   ok=m['focusOutline'] not in ('none','hidden') and float(m['focusWidth'].replace('px',''))>=2 and max(m['focusVsInside'] or 0,m['focusVsOutside'] or 0)>=3
   note(width,name,'keyboard focus indicator',m,ok)
  page.evaluate('location.hash="#/proposals"')
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Título demonstrativo para revisar contornos')
  page.locator('#draft-body').fill('Descrição representativa com conteúdo suficiente para revisão sem recursos remotos.')
  page.locator('[value=conclude]').click()
  panel=page.locator('.workflow-review-sheet')
  for name,locator in [('review-section',panel.locator('select').nth(0)),('review-type',panel.locator('select').nth(1))]:
   m=locator.evaluate(MEASURE)
   ok=max(m['borderAgainstInside'] or 0,m['surfaceVsOutside'])>=3
   note(width,name,'non-text field boundary',m,ok)
   locator.focus()
   m=locator.evaluate(MEASURE)
   ok=m['focusOutline'] not in ('none','hidden') and float(m['focusWidth'].replace('px',''))>=2 and max(m['focusVsInside'] or 0,m['focusVsOutside'] or 0)>=3
   note(width,name,'keyboard focus indicator',m,ok)
  page.close()
 browser.close()
report={'total':len(records),'passed':len(records)-len(failures),'failed':len(failures),'failures':failures,'records':records}
(ROOT/'dist/stage7_nontext_focus_v0142_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'Non-text and focus: {report["passed"]}/{report["total"]}, {report["failed"]} failures')
for f in failures[:15]:print('FAIL',f['width'],f['name'],f['case'],'border',f.get('borderAgainstInside'),'surface',f.get('surfaceVsOutside'),'focus',f.get('focusVsInside'),f.get('focusVsOutside'))
if FIXED:assert not failures
