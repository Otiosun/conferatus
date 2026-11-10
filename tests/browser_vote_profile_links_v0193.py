"""Prototype route linking author profile, proposals, active schedules and back.
All data fictional. No Academy identity, authorization or official voting.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
PROPOSALS=[
 {'id':'draft-alpha','title':'Proposta Alfa de demonstração','body':'Conteúdo sintético suficientemente detalhado da proposta Alfa.','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[], 'status':'concluida'},
 {'id':'draft-beta','title':'Proposta Beta de demonstração','body':'Conteúdo sintético suficientemente detalhado da proposta Beta.','sectionId':'coordenacao','type':'PDR','authorComplete':True,'partners':[], 'status':'concluida'}]
SCHEDULES=[
 {'id':'sched-alpha','title':'Programação Alfa fictícia','objective':'Teste de vínculo.', 'proposalId':'draft-alpha','sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'programada','method':'nominal','choices':[{'id':'opt-1','label':'Alternativa A'},{'id':'opt-2','label':'Alternativa B'}]},
 {'id':'sched-beta','title':'Programação Beta fictícia','objective':'Teste de vínculo.', 'proposalId':'draft-beta','sectionId':'coordenacao','start':'2026-12-22T09:00','end':'2026-12-22T11:00','type':'PDR','status':'programada','method':'binaria'},
 {'id':'sched-cancelled','title':'Programação cancelada fictícia','objective':'Cancelada.', 'proposalId':'draft-alpha','sectionId':'integridade','start':'2026-12-23T09:00','end':'2026-12-23T11:00','type':'PDR','status':'cancelada','method':'nominal','choices':[{'id':'opt-1','label':'Sim'},{'id':'opt-2','label':'Não'}]},
]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850});page.set_default_timeout(5000)
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank')
  page.evaluate('''([drafts,schedules])=>{
   const store=new Map([
    ['conferatus:proposals-v010',JSON.stringify(drafts)],
    ['conferatus:deliberations-v010',JSON.stringify(schedules)]
   ]);
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)}});
  }''',[PROPOSALS,SCHEDULES])
  page.set_content(HTML)
  page.evaluate("location.hash='#/profile/m01'")
  page.locator('[data-tab=proposicoes]').click()
  expect(page.locator('.session-proposal')).to_have_count(2)
  assert page.locator('.session-schedule-link').count()==2,width
  assert 'cancelada' not in page.locator('.section-body').inner_text().lower(),width
  first=page.locator('.session-proposal').filter(has_text='Proposta Alfa')
  expect(first.locator('[data-linked-schedule="sched-alpha"]')).to_be_visible()
  assert first.locator('[data-linked-schedule="sched-beta"]').count()==0,width
  first.locator('[data-linked-schedule="sched-alpha"]').click()
  assert page.evaluate('location.hash')=='#/calendar',width
  expect(page.locator('#schedule-details-sched-alpha')).to_be_visible()
  assert 'PROGRAMAÇÃO ALFA FICTÍCIA' in page.locator('main').inner_text(),width
  page.locator('[data-open-schedule-proposal="draft-alpha"]').click()
  assert page.evaluate('location.hash')=='#/review',width
  expect(page.locator('.workflow-review-body')).to_contain_text('Conteúdo sintético suficientemente detalhado da proposta Alfa.')
  page.locator('.workflow-finished [data-route="calendar"]').click()
  # Allow the application's hashchange listener to finish before interacting.
  page.wait_for_timeout(150)
  if not page.locator('#schedule-details-sched-alpha').count():
   page.locator('[data-schedule="sched-alpha"]').click()
  expect(page.locator('[data-open-proposal-author]')).to_be_visible()
  page.locator('[data-open-proposal-author]').click()
  assert page.evaluate('location.hash')=='#/profile/m01',width
  expect(page.locator('.session-proposal')).to_have_count(2)
  page.evaluate("location.hash='#/profile/m02'")
  assert page.locator('.session-proposal').count()==0,width
  assert page.locator('.session-schedule-link').count()==0,width
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  assert not errors,(width,errors)
  page.close();print('PASS profile/proposition/schedule/author cross-links',width)
 browser.close()
