from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':820})
  page.goto('about:blank?demo=1')
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Revisão coletiva do regulamento')
  page.locator('#draft-body').fill('Texto inicial consolidado para revisão e conclusão pelas pessoas participantes do Socii.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=invite-socii]').click()
  page.locator('[name=memberId]').select_option(index=1)
  page.locator('#invite-socii-form button.workflow-primary').click()
  page.get_by_text('Concluíram 0 de 2').wait_for()
  page.locator('[data-draft]').first.click()
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.get_by_text('Concluíram 1 de 2').wait_for()
  page.locator('[data-confirm-partner]').click()
  page.get_by_text('Concluíram 2 de 2').wait_for()
  assert page.locator('[data-confirm-partner]').count()==0
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('Socii progress 0/2 → 1/2 → 2/2 across four viewport widths')
