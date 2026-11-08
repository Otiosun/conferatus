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
  page.locator('.workflow-status').filter(has_text='Rascunho mantido somente enquanto a página estiver aberta.').wait_for()
  page.locator('.footer-nav').click();page.locator('[data-route=members]').first.click()
  page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  page.locator('.session-proposals-heading').first.wait_for()
  page.get_by_text('Rascunho de comunicação').first.wait_for()
  page.locator('.session-proposal-link').click()
  assert page.locator('#draft-title').input_value()=='Rascunho de comunicação'
  assert page.locator('#draft-body').input_value()=='Primeiro parágrafo ainda incompleto.'
  page.locator('#compose-proposal-form [data-route=profile]').click()
  assert page.evaluate('location.hash')=='#/profile/m01',width
  page.locator('.session-proposal-link').wait_for(state='visible')
  assert page.locator('.session-proposal-link').count()==1,width
  page.locator('.session-proposal-link').click()
  page.locator('#draft-body').fill('Esta é a versão final consolidada do documento para consulta e revisão institucional.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.footer-nav').click();page.locator('[data-route=members]').first.click()
  page.locator('.profile-name-button').click();page.locator('[data-tab=proposicoes]').click()
  page.locator('.session-proposal-link').click()
  page.get_by_text('Proposição concluída',exact=True).wait_for()
  assert page.locator('#confirm-proposal-form').count()==0
  page.locator('.workflow-finished [data-route=profile]').click()
  assert page.evaluate('location.hash')=='#/profile/m01',width
  page.locator('.session-proposal-link').wait_for(state='visible')
  assert page.locator('.session-proposal-link').count()==1,width
  page.locator('.footer-nav').click();page.locator('[data-route=members]').first.click()
  page.locator('.member-item[data-member="m04"]').click()
  page.locator('.footer-nav').click();page.locator('[data-route=proposals]').first.click()
  page.locator('.workflow-tabs button[data-route=profile]').click()
  assert page.evaluate('location.hash')=='#/profile/m01',(width,'wrong member selected for author history')
  # Original Megalos profile composition: two real actions on the author's
  # Proposições tab, not inert copies of the separate proposals buttons.
  page.locator('[data-tab=proposicoes]').click()
  actions=page.locator('.profile-workflow-actions')
  actions.wait_for(state='visible')
  assert actions.locator('button').count()==2,width
  assert all(button.bounding_box()['height']>=44 for button in actions.locator('button').all()),width
  actions.locator('[data-action=invite-socii-from-profile]').click()
  page.locator('#invite-socii-form').wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/proposals',width
  page.locator('.workflow-tabs button[data-route=profile]').click()
  page.locator('[data-tab=proposicoes]').click()
  page.locator('.profile-workflow-actions [data-action=new-proposal]').click()
  page.locator('#draft-title').wait_for(state='visible')
  assert page.locator('.workflow-editor-actions [data-route=profile]').inner_text()=='Voltar ao perfil',width
  page.locator('.workflow-editor-actions [data-route=profile]').click()
  page.locator('.profile-workflow-actions').wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/profile/m01',width
  # A different fictitious person's profile cannot expose authoring privileges.
  page.locator('.footer-nav').click();page.locator('[data-route=members]').first.click()
  page.locator('.member-item[data-member="m04"]').click()
  page.locator('[data-tab=proposicoes]').click()
  assert page.locator('.profile-workflow-actions').count()==0,width
  # Calendar day targets gain an ergonomic 44px footprint on 320px+ screens.
  page.locator('.footer-nav').click();page.locator('[data-route=calendar]').first.click()
  day=page.locator('.calendar-day').first
  day.wait_for(state='visible')
  rect=day.bounding_box()
  assert rect['width']>=44 and rect['height']>=44,(width,rect)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('Author profile ↔ draft and finished proposal: OK')
