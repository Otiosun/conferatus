"""Mobile legibility of key navigation actions, with no horizontal overflow.

Sizes and text only: automated browser checks cannot certify actual visual comfort
or assistive-technology behavior on the user's device.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 cases={
  'members':['.profile-head .tabs .tab','.search-trigger'],
  'proposals':['.workflow-profile .workflow-tabs .tab','.proposal-trigger'],
  'overview':['.overview-tabs .tab'],
  'governance':['.section-toggle']
 }
 for width in (280,320,390,540,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844},has_touch=True,is_mobile=True)
  page.set_default_timeout(6500)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html)
  for route,selectors in cases.items():
   page.evaluate('(r)=>location.hash="#/"+r',route)
   for selector in selectors:
    locator=page.locator(selector).first
    locator.wait_for(state='visible')
    if width<=540:
     size=locator.evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)')
     assert size>=12,(width,route,selector,size)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('PASS: 24 route-width samples, >=12px key mobile controls, no overflow')
