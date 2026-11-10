"""P0 complete local-only proposal, Socii and schedule flow.
Fictional collaborators only: never a real invitation, identity, signature or vote.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(6000)
  errors=[]
  page.on('pageerror',lambda e: errors.append(str(e)))
  page.goto('about:blank')
  page.evaluate('''() => {const store=new Map();Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:key=>store.get(key)??null,setItem:(key,val)=>store.set(key,String(val)),removeItem:key=>store.delete(key)}});}''')
  page.set_content(HTML)
  def nav(route):
   page.locator('.footer-nav').click()
   page.locator('.menu-item[data-route="'+route+'"]').click()
  def invite(index):
   page.locator('[data-action=invite-socii]').click()
   form=page.locator('#invite-socii-form');expect(form).to_be_visible()
   form.locator('[name=memberId]').select_option(index=index)
   form.locator('button.workflow-primary').click()
  def record():
   return page.locator('.workflow-record').filter(has_text='Proposta Socii de teste')
  def progress(text):
   expect(record().locator('.workflow-partners')).to_contain_text(text)
  # A pending/absent proposal cannot be scheduled.
  nav('calendar');page.locator('[data-action=open-schedule]').click()
  expect(page.locator('#schedule-deliberation-form button[type=submit]')).to_be_disabled()
  expect(page.locator('#schedule-deliberation-form')).to_contain_text('conclua uma proposição')
  nav('proposals')
  page.locator('[data-action=new-proposal]').click()
  page.locator('#compose-proposal-form [value=save]').click()
  expect(page.locator('#compose-save-error')).to_be_visible()
  page.locator('#draft-title').fill('Proposta Socii de teste')
  page.locator('#draft-body').fill('Texto local para demonstrar a revisão e a integridade do Socii durante uma deliberação, sem conta institucional.')
  page.locator('#compose-proposal-form [value=save]').click()
  expect(record()).to_contain_text('Em redação')
  invite(1);invite(2)
  progress('Concluíram 0 de 3')
  assert record().locator('[data-confirm-partner]').count()==2,width
  assert record().locator('[data-schedule-draft]').count()==0,width
  record().locator('[data-draft]').click()
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  page.locator('#confirm-proposal-form button[type=submit]').click()
  expect(record()).to_contain_text('Aguardando Socii')
  progress('Concluíram 1 de 3')
  first=record().locator('[data-confirm-partner]').first
  assert first.evaluate('(el)=>el.getBoundingClientRect().height')>=44,width
  first.click()
  progress('Concluíram 2 de 3')
  assert record().locator('[data-schedule-draft]').count()==0,width
  # Editing the text invalidates both the author's and the Socii confirmation.
  record().locator('[data-draft]').click()
  page.locator('#confirm-proposal-form [data-route=compose]').click()
  page.locator('#draft-body').fill('Texto materialmente ALTERADO para exigir novas confirmações de autoria e participantes fictícios do Socii.')
  page.locator('#compose-proposal-form [value=save]').click()
  progress('Concluíram 0 de 3')
  expect(record()).to_contain_text('Em redação')
  assert record().locator('[data-confirm-partner]').count()==2,width
  # Restore author and both fictional partners, then schedule the completed draft.
  record().locator('[data-draft]').click()
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  progress('Concluíram 1 de 3')
  record().locator('[data-confirm-partner]').first.click()
  progress('Concluíram 2 de 3')
  record().locator('[data-confirm-partner]').first.click()
  progress('Concluíram 3 de 3')
  expect(record()).to_contain_text('Concluída')
  expect(record().locator('[data-schedule-draft]')).to_be_visible()
  nav('calendar');page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  expect(form.locator('button[type=submit]')).to_be_enabled()
  form.locator('[name=title]').fill('Votação Socii vinculada')
  form.locator('[name=objective]').fill('Descrição objetiva para uma programação fictícia vinculada à proposta concluída.')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=sectionId]').select_option('coordenacao')
  form.locator('[name=type]').select_option('PR')
  form.locator('[name=method]').select_option('nominal')
  form.locator('[name=choices]').fill('Mesma\nMesma')
  form.locator('[name=start]').fill('2026-12-21T10:00')
  form.locator('[name=end]').fill('2026-12-21T09:00')
  form.locator('button[type=submit]').click()
  expect(form.locator('[role=alert]')).to_be_visible()
  form.locator('[name=end]').fill('2026-12-21T11:00')
  form.locator('button[type=submit]').click()
  expect(form.locator('[role=alert]')).to_be_visible()
  form.locator('[name=choices]').fill('Alternativa A\nAlternativa B')
  form.locator('button[type=submit]').click()
  linked=page.locator('.calendar-item').filter(has_text='Votação Socii vinculada')
  expect(linked).to_be_visible()
  expect(linked).to_contain_text('Coordenação')
  assert linked.locator('.calendar-socii').count()>0,width
  expect(linked.locator('[data-preview-schedule]')).to_be_visible()
  linked.locator('[data-preview-schedule]').click()
  expect(page.locator('#preview-vote-method')).to_have_value('nominal')
  expect(page.locator('.preview-vote-context')).to_contain_text('Proposta Socii de teste')
  nav('calendar')
  linked=page.locator('.calendar-item').filter(has_text='Votação Socii vinculada')
  linked.locator('[data-cancel-schedule]').click()
  expect(linked.locator('[data-keep-schedule]')).to_be_visible()
  linked.locator('[data-keep-schedule]').click()
  expect(page.locator('.calendar-item').filter(has_text='Votação Socii vinculada')).to_be_visible()
  linked=page.locator('.calendar-item').filter(has_text='Votação Socii vinculada')
  linked.locator('[data-cancel-schedule]').click()
  linked.locator('[data-confirm-cancel-schedule]').click()
  assert page.locator('.calendar-item').filter(has_text='Votação Socii vinculada').count()==0,width
  page.locator('[data-action=toggle-cancelled-history]').click()
  expect(page.locator('.calendar-cancelled-record')).to_contain_text('Votação Socii vinculada')
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print(f'PASS 04.05/04.09/04.13 combined normal preview — {width}px')
  page.close()
 browser.close()
print('PASS: all 4 widths; draft, 2 Socii, reapproval, invalid schedule, valid schedule, kept/cancelled history')
