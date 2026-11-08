"""Multiple proposals must require an explicit Socii invitation target.

With exactly one unfinished proposal, keep the quick one-step selection.
With more than one, never silently assign the participant to the first draft.
No real participants or Academy data are used.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  page.set_default_timeout(6000)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html)
  page.locator('.footer-nav').click();page.locator('[data-route=proposals]').click()
  def draft(title):
   page.locator('[data-action=new-proposal]').click()
   page.locator('#draft-title').fill(title)
   page.locator('#draft-body').fill('Texto da proposta de teste salvo nesta sessão, para conferir o destino correto do convite.')
   page.locator('#compose-proposal-form [value=save]').click()
   page.locator('[data-action=new-proposal]').wait_for(state='visible')
  draft('Primeiro rascunho')
  page.locator('[data-action=invite-socii]').click()
  select=page.locator('#invite-socii-form [name=draftId]')
  assert select.input_value()!='',(width,'single proposal should remain easy to choose')
  page.locator('[data-action=invite-socii]').click()
  draft('Segundo rascunho')
  page.locator('[data-action=invite-socii]').click()
  select=page.locator('#invite-socii-form [name=draftId]')
  assert select.input_value()=='',(width,'multiple proposals must require choice')
  assert not select.evaluate('(el)=>el.checkValidity()'),width
  page.locator('#invite-socii-form [name=memberId]').select_option(index=1)
  page.locator('#invite-socii-form button.workflow-primary').click()
  assert page.locator('.workflow-partners').count()==0,(width,'invite accepted without proposal choice')
  select.select_option(label='Segundo rascunho')
  page.locator('#invite-socii-form button.workflow-primary').click()
  first=page.locator('.workflow-record').filter(has_text='Primeiro rascunho')
  second=page.locator('.workflow-record').filter(has_text='Segundo rascunho')
  assert first.locator('.workflow-partners').count()==0,width
  assert second.locator('.workflow-partners').count()==1,width
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('PASS: Socii draft selection with one versus multiple drafts, 4 widths')
