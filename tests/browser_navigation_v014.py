from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,320,360,375,390,430,540,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html)
  for dest,expected in [('calendar','.calendar-grid'),('proposals','.workflow-actions'),('overview','.overview-content'),('members','.member-list')]:
   page.locator('.footer-nav').click()
   page.locator(f'.menu-item[data-route="{dest}"]').click()
   page.locator(expected).wait_for()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,dest)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-body').wait_for()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'compose')
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('Four menu routes and editor: nine viewport widths OK')
