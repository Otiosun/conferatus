"""Stage 07.04: sample visible leaf text for exceptionally small type.

10 CSS px is an internal legibility heuristic; WCAG does not mandate this
minimum font size. The sampled routes/widths must not be overstated as a
whole-product WCAG audit or a physical-device validation.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from collections import Counter
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
records=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (280,390,740):
        page=browser.new_page(viewport={'width':width,'height':820})
        page.goto('about:blank?stage7=type-audit')
        page.set_content(HTML)
        for route in ('ballot','members','profile','overview','governance','calendar','proposals','compose'):
            page.evaluate('(r)=>location.hash="#/"+r',route)
            page.wait_for_timeout(25)
            spans=page.evaluate('''() => [...document.querySelectorAll('main *, .app-footer *')].filter(el=>{
                if(el.children.length>0 || !el.textContent?.trim())return false;
                const style=getComputedStyle(el),r=el.getBoundingClientRect();
                return r.width>0&&r.height>0&&style.visibility==='visible'&&style.display!=='none';
            }).map(el=>({className:String(el.className||''),text:el.textContent.trim().slice(0,55),
                        font:parseFloat(getComputedStyle(el).fontSize)}))''')
            for span in spans:
                if span['font']<10:
                    records.append({'width':width,'route':route,**span})
        page.close()
    browser.close()
report={'routes':8,'widths':3,'text_under_10px':records,'count':len(records)}
(ROOT/'dist'/'stage7_readability_inventory_v0134.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Stage 07.04 small-text inventory: 8 routes × 3 widths, under-10px:',len(records))
for record in records[:12]: print('ISSUE',record)
assert not records
