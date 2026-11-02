"""Stage 07.06: CSS safe-area bottom padding survives the mobile grid-footer.

This injects a KNOWN CSS env() value into a cloned offline HTML page to
exercise the author's actual rule in Chromium. It is not an iPhone/notch
emulator, and cannot certify native OS inset handling.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1]
HTML=(R/'dist/CONFFRATUS_demo_offline.html').read_text('utf-8')
CSS=(R/'src/styles.css').read_text('utf-8')
assert 'padding-bottom:env(safe-area-inset-bottom,0px)' in CSS, 'safe-area padding declaration absent'
assert 'viewport-fit=cover' in HTML, 'mobile viewport metadata absent'
records=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,320,390,540):
  for inset in (24,34,48):
   page=b.new_page(viewport={'width':width,'height':600})
   page.goto('about:blank?demo=1')
   simulated=HTML.replace('env(safe-area-inset-bottom,0px)',f'{inset}px')
   assert simulated!=HTML,'env substitution did not reach bundled CSS'
   page.set_content(simulated)
   m=page.evaluate('''() => {
    const el=document.querySelector('.app-footer'),r=el.getBoundingClientRect();
    const logo=document.querySelector('.app-footer>img').getBoundingClientRect();
    const nav=document.querySelector('.footer-nav').getBoundingClientRect();
    const sty=getComputedStyle(el);return {padding:parseFloat(sty.paddingBottom),
       overflow:document.documentElement.scrollWidth-innerWidth,
       footerBottom:r.bottom,logoBottom:logo.bottom,menuBottom:nav.bottom};
   }''')
   records.append({'width':width,'inset':inset,**m})
   assert m['padding']>=inset-.5,(width,inset,'safe area lost',m)
   assert m['overflow']<=1,(width,inset,'horizontal overflow',m)
   assert m['logoBottom']<m['footerBottom']-inset+2,(width,inset,'crest crosses safe area',m)
   assert m['menuBottom']<m['footerBottom']-inset+2,(width,inset,'menu crosses safe area',m)
   page.close()
 b.close()
(R/'dist/stage7_safe_area_v0136_report.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('07.06 synthetic bottom-safe-area CSS PASS:',len(records),'cases')
