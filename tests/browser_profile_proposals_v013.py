from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html)
  page.locator('.footer-nav').click();page.locator('[data-route=proposals]').first.click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Rascunho de comunicação')
  page.locator('#draft-body').fill('Primeiro parágrafo ainda incompleto.')
  page.locator('#compose-proposal-form [value=save]').click()
  page.locator('.footer-nav').click();page.locator('[data-route=members]').first.click()
  page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  page.locator('.session-proposals-heading').first.wait_for()
  page.get_by_text('Rascunho de comunicação').first.wait_for()
  page.locator('.session-proposal-link').click()
  assert page.locator('#draft-title').input_value()=='Rascunho de comunicação'
  assert page.locator('#draft-body').input_value()=='Primeiro parágrafo ainda incompleto.'
  page.locator('#draft-body').fill('Esta é a versão final consolidada do documento para consulta e revisão institucional.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.footer-nav').click();page.locator('[data-route=members]').first.click()
  page.locator('.profile-name-button').click();page.locator('[data-tab=proposicoes]').click()
  page.locator('.session-proposal-link').click()
  page.get_by_text('Proposição concluída',exact=True).wait_for()
  assert page.locator('#confirm-proposal-form').count()==0
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('Author profile ↔ draft and finished proposal: OK')
