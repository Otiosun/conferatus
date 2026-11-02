from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':820})
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Regimento de comunicação interna')
  page.locator('#draft-body').fill('Documento consolidado para discutir as etapas de comunicação interna da Academy.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=calendar]').click()
  page.locator('[data-action=open-schedule]').click()
  page.locator('[name=title]').fill('Reunião da proposta')
  page.locator('[name=objective]').fill('Avaliar o documento de comunicação em reunião deliberativa.')
  page.locator('[name=proposalId]').select_option(index=1)
  page.locator('[name=start]').fill('2026-12-12T09:00')
  page.locator('[name=end]').fill('2026-12-12T12:00')
  page.locator('#schedule-deliberation-form button[type=submit]').click()
  page.locator('[data-calendar-day="2026-12-12"]').wait_for()
  assert page.locator('[data-calendar-day="2026-12-12"]').get_attribute('aria-pressed')=='true'
  page.locator('[data-open-schedule-proposal]').click()
  page.get_by_text('Proposição concluída',exact=True).wait_for()
  assert page.locator('#confirm-proposal-form').count()==0
  page.locator('.workflow-finished [data-route=calendar]').click()
  assert page.evaluate('location.hash')=='#/calendar',width
  assert page.locator('[data-calendar-day="2026-12-12"]').get_attribute('aria-pressed')=='true',width
  assert page.locator('.calendar-item--expanded').filter(has_text='Reunião da proposta').count()==1,width
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('Calendar → finished proposal: OK')
