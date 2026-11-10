"""Cross-screen local-only scenario: profile -> compose -> Socii -> review -> calendar -> ballot.
Only fictional actors and temporary in-memory browser state; no Academy accounts.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(6000)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank')
  # Opaque origin: deterministic in-memory stand-in. No reload-persistence claim.
  page.evaluate("""() => {
    const records=new Map();
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
      getItem:k=>records.get(k)??null,
      setItem:(k,v)=>records.set(k,String(v)),
      removeItem:k=>records.delete(k)
    }});
  }""")
  page.set_content(html)
  def nav(route):
   page.locator('.footer-nav').click()
   page.locator(f'.menu-item[data-route="{route}"]').click()
  nav('members')
  page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  actions=page.locator('.profile-workflow-actions')
  actions.wait_for(state='visible')
  assert actions.locator('button').count()==2,width
  actions.locator('[data-action=new-proposal]').click()
  title=page.locator('#draft-title');title.wait_for(state='visible')
  title.fill('Proposta original da autoria')
  page.locator('#draft-body').fill('Uma nova redação institucional de teste que será revisada com o Socii e agendamento. Mais informações de teste.')
  page.locator('.footer-nav').click()
  assert title.input_value()=='Proposta original da autoria',width
  page.keyboard.press('Escape')
  page.locator('#compose-proposal-form [value=save]').click()
  page.locator('[data-action=new-proposal]').wait_for(state='visible')
  nav('members');page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  page.locator('.session-proposal-link').first.wait_for(state='visible')
  page.locator('.profile-workflow-actions [data-action=invite-socii-from-profile]').click()
  invite=page.locator('#invite-socii-form')
  invite.wait_for(state='visible')
  member=invite.locator('[name=memberId]')
  assert member.input_value()=='',width
  member.select_option(index=1)
  invite.locator('button.workflow-primary').click()
  record=page.locator('.workflow-record').filter(has_text='Proposta original da autoria')
  record.locator('.workflow-partners').wait_for(state='visible')
  record.locator('[data-draft]').click()
  page.locator('#draft-title').wait_for(state='visible')
  page.locator('[data-action=enable-rich-editor]').click()
  editor=page.locator('#draft-rich-body')
  editor.click()
  page.keyboard.press('End')
  page.keyboard.insert_text(' Acrescento uma linha de justificativa.')
  assert 'Acrescento uma linha' in editor.inner_text(),width
  page.locator('.footer-nav').click()
  assert 'Acrescento uma linha' in editor.inner_text(),width
  page.keyboard.press('Escape')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  assert 'Acrescento uma linha' in page.locator('.workflow-review-body').inner_text(),width
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-record').first.wait_for(state='visible')
  assert 'Aguardando Socii' in page.locator('.workflow-record').inner_text(),width
  # The full fictional demo must allow a session partner to complete their role
  # without requiring the hidden test-only ?demo=1 switch.
  partner=page.locator('[data-confirm-partner]')
  assert partner.count()==1,width
  partner.click()
  assert 'Concluída' in page.locator('.workflow-record').inner_text(),width
  nav('calendar')
  page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  form.locator('[name=title]').fill('Programação mensal')
  form.locator('[name=objective]').fill('Programação local ligada à proposição concluída.')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=method]').select_option('nominal')
  form.locator('[name=choices]').fill('Opção A\nOpção B')
  form.locator('[name=start]').fill('2026-12-13T10:00')
  form.locator('[name=end]').fill('2026-12-13T09:00')
  form.locator('button[type=submit]').click()
  assert form.locator('[role=alert]').count()==1,width
  assert form.locator('[name=title]').input_value()=='Programação mensal',width
  form.locator('[name=end]').fill('2026-12-13T11:00')
  form.locator('button[type=submit]').click()
  linked=page.locator('.calendar-item').filter(has_text='Programação mensal')
  linked.wait_for(state='visible')
  linked.locator('[data-preview-schedule]').click()
  page.locator('#preview-vote-method').wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/ballot',width
  assert page.locator('#preview-vote-method').input_value()=='nominal',width
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('PASS: linked profile/proposal/Socii/review/calendar/ballot workflow, four widths')
