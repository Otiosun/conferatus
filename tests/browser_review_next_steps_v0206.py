"""PF-13: review metadata, Socii participants, next steps and contextual scheduling.
Only synthetic preview records. No institutional identity, approval or delivery.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT_KEY='conferatus:proposals-v010'
WAITING={
 'id':'draft-review-pending','title':'Revisão com Socii','body':'Texto fictício da proposição esperando a participação do Socii.',
 'sectionId':'integridade','type':'PR','authorComplete':False,
 'partners':[{'id':'m02','complete':True},{'id':'m03','complete':False}],
 'status':'revisao'
}
DONE={
 'id':'draft-review-finished','title':'Revisão já concluída',
 'body':'Proposição fictícia concluída e pronta para criar uma programação local.',
 'sectionId':'integridade','type':'Ofício','authorComplete':True,
 'partners':[{'id':'m02','complete':True}], 'status':'concluida'
}

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(6500)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank')
  page.evaluate("""drafts=>{
   const records=new Map([['conferatus:proposals-v010',JSON.stringify(drafts)],['conferatus:deliberations-v010','[]']]);
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>records.get(k)??null,
    setItem:(k,v)=>records.set(k,String(v)),
    removeItem:k=>records.delete(k)
   }});
  }""",[WAITING,DONE])
  page.set_content(HTML)
  page.evaluate("location.hash='#/proposals'")
  waiting=page.locator('.workflow-record').filter(has_text='Revisão com Socii')
  waiting.locator('[data-draft]').click()
  expect(page.locator('.workflow-editor-head h1')).to_contain_text('Revisão com Socii')
  expect(page.locator('.workflow-review-body')).to_contain_text('esperando a participação do Socii')
  expect(page.locator('#confirm-proposal-form [name=type]')).to_have_value('PR')
  expect(page.locator('#confirm-proposal-form [name=sectionId]')).to_have_value('integridade')
  guide=page.locator('.workflow-review-guidance')
  expect(guide).to_have_count(1)
  expect(guide).to_contain_text('Autoria:')
  expect(guide).to_contain_text('Socii:')
  expect(guide).to_contain_text('(concluiu)')
  expect(guide).to_contain_text('(pendente)')
  expect(guide).to_contain_text('aguardando')
  assert page.locator('[data-schedule-draft]').count()==0,width
  assert page.locator('#d3-review-dialog').count()==0,width
  page.locator('#confirm-proposal-form button[type=submit]').click()
  expect(waiting).to_contain_text('Aguardando Socii')
  assert waiting.locator('[data-schedule-draft]').count()==0,width

  finished=page.locator('.workflow-record').filter(has_text='Revisão já concluída')
  finished.locator('[data-draft]').click()
  expect(page.locator('.workflow-finished')).to_be_visible()
  expect(page.locator('.workflow-editor-head h1')).to_contain_text('Revisão já concluída')
  expect(page.locator('.workflow-review-body')).to_contain_text('pronta para criar uma programação')
  expect(page.locator('.workflow-finished')).to_contain_text('Ofício')
  expect(page.locator('.workflow-finished')).to_contain_text('Integridade')
  finalGuide=page.locator('.workflow-finished .workflow-review-guidance')
  expect(finalGuide).to_contain_text('Socii:')
  expect(finalGuide).to_contain_text('(concluiu)')
  expect(finalGuide).to_contain_text('pode ser vinculada a uma programação')
  nextAction=page.locator('.workflow-finished [data-schedule-draft]')
  expect(nextAction).to_be_visible()
  nextAction.click()
  expect(page.locator('#schedule-deliberation-form')).to_be_visible()
  expect(page.locator('#schedule-deliberation-form [name=proposalId]')).to_have_value('draft-review-finished')
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS review participants and schedule continuation',width)
  page.close()
 browser.close()
