"""Stage 07.06: real interaction and no clipping in short/landscape CSS viewports.

Chromium + offline static preview; keyboard height reduction is *simulated*, not
Android/iOS virtual keyboard, safe-area cutouts, or physical-device approval.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text('utf-8')
SIZES=((280,320),(320,280),(360,320),(390,430),(568,320),(667,375),(740,360),(812,375),(390,667))
ROUTES=('ballot','members','overview','governance','calendar','proposals','compose')
records=[];failures=[]

with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in SIZES:
  page=browser.new_page(viewport={'width':w,'height':h},is_mobile=True,has_touch=True)
  js=[];page.on('pageerror',lambda err:js.append(str(err)))
  page.goto('about:blank?demo=1');page.set_content(HTML)
  for route in ROUTES:
   if route=='compose':
    page.evaluate('location.hash="#/proposals"')
    page.locator('[data-action="new-proposal"]').click()
   else:page.evaluate('(r)=>location.hash="#/"+r',route)
   rec=page.evaluate('''() => {
     const body=document.documentElement,footer=document.querySelector('.app-footer');
     const nav=document.querySelector('.footer-nav');
     const a=footer.getBoundingClientRect(),n=nav.getBoundingClientRect();
     const crest=document.querySelector('.app-footer>img');
     return {viewport:[innerWidth,innerHeight],scrollWidth:body.scrollWidth,
       scrollHeight:body.scrollHeight,footerHeight:a.height,menuWidth:n.width,
       menuHeight:n.height,logoLoaded:crest.complete&&crest.naturalWidth>0,
       menuInsideFooter:n.left>=a.left-1&&n.right<=a.right+1&&n.top>=a.top-1&&n.bottom<=a.bottom+1};
   }''')
   records.append({'width':w,'height':h,'route':route,**rec})
   if rec['scrollWidth']>w+1:failures.append((w,h,route,'horizontal overflow'))
   if rec['menuHeight']<43.5 or not rec['menuInsideFooter']:failures.append((w,h,route,'menu outside footer'))
   if not rec['logoLoaded']:failures.append((w,h,route,'official crest failed'))
  # Menu must remain operable when footer is below the first screen.
  page.locator('.footer-nav').click()
  assert page.locator('.menu-item').count()==4,(w,h,'menu cannot open')
  page.locator('.menu-item[data-route="members"]').click()
  page.locator('.member-item').first.wait_for()
  assert page.locator('.member-item').count()>0,(w,h,'navigation to members failed')
  # A simulated reduced visual viewport: scroll, focus, type, then navigate.
  page.locator('.search-trigger').click()
  search=page.locator('#search-members')
  search.click()
  page.set_viewport_size({'width':w,'height':max(210,h-125)})
  search.fill('bruno')
  # The operating system keyboard is not present in Chromium headless; measure
  # whether the focused control can be scrolled fully into view after resize.
  search.scroll_into_view_if_needed()
  active=page.evaluate('''() => {const el=document.activeElement;const r=el.getBoundingClientRect();
    return {id:el.id,top:r.top,bottom:r.bottom,visualHeight:innerHeight,
      scrollWidth:document.documentElement.scrollWidth};}''')
  if active['id']!='search-members' or active['scrollWidth']>w+1:
   failures.append((w,h,'search','keyboard-height layout/focus lost',active))
  if active['bottom']>active['visualHeight']+2 or active['top']< -2:
   failures.append((w,h,'search','focused field off visual viewport',active))
  # Check buttons still reachable after keyboard closes and height recovers.
  page.set_viewport_size({'width':w,'height':h})
  page.locator('[data-action="clear-search"]').click()
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="proposals"]').click()
  page.locator('[data-action="new-proposal"]').click()
  title=page.locator('#draft-title');body=page.locator('#draft-body')
  title.fill('Teste compacto')
  body.fill('Esta é uma redação longa para testar rolagem com o teclado virtual simulado no modo compacto.')
  body.focus()
  page.set_viewport_size({'width':w,'height':max(210,h-125)})
  body.scroll_into_view_if_needed()
  focus=page.evaluate('''() => {const r=document.activeElement.getBoundingClientRect();return {
    tag:document.activeElement.tagName,top:r.top,bottom:r.bottom,
    visibleHeight:innerHeight,scrollWidth:document.documentElement.scrollWidth};}''')
  if focus['tag']!='TEXTAREA' or focus['scrollWidth']>w+1:
   failures.append((w,h,'compose','textarea focus lost or overflow',focus))
  # Textarea is taller than the small viewport by design; require at least one
  # visible segment and reachable submit controls by scroll, not full visibility.
  if focus['bottom']<=0 or focus['top']>=focus['visibleHeight']:
   failures.append((w,h,'compose','textarea completely off screen',focus))
  page.set_viewport_size({'width':w,'height':h})
  page.locator('button[name="intent"][value="save"]').click()
  
  page.wait_for_function('document.body.innerText.includes("TESTE COMPACTO")')
  if js: failures.append((w,h,'javascript',js))
  if w in (320,568,740):
   page.screenshot(path=str(ROOT/'dist'/f'stage7_compact_editor_{w}x{h}.png'),full_page=True)
  page.close()
 browser.close()
report={'sizes':SIZES,'cases':len(records),'routes':ROUTES,'failures':failures,
 'keyboard_note':'viewport height shrink only; NOT actual OS keyboard/safe-area/orientation sensor'}
(ROOT/'dist'/'stage7_compact_v0136_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(records)==len(SIZES)*len(ROUTES),(len(records),'incomplete')
assert not failures,f'{len(failures)} compact failures: {failures[:9]}'
print('07.06 compact/landscape Chromium PASS:',len(records),'route-size combinations +',len(SIZES),'keyboard-height interaction flows')
