"""Schedule keeps the source proposal's initial section/type, while keeping both editable."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DONE={'id':'draft-schedule-origin','title':'Proposição concluída para agenda',
 'body':'Documento fictício concluído para demonstrar preenchimento contextual do formulário.',
 'sectionId':'coordenacao','type':'Ofício','authorComplete':True,'partners':[],
 'status':'concluida'}
def boot(browser,width):
 p=browser.new_page(viewport={'width':width,'height':850});p.set_default_timeout(6000)
 p.goto('about:blank')
 p.evaluate("""draft=>{
   const m=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010','[]']]);
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>m.get(k)??null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k)}});
 }""",DONE)
 p.set_content(HTML)
 return p
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=boot(b,width)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.evaluate("location.hash='#/proposals'")
  page.locator('.workflow-record').filter(has_text='Proposição concluída para agenda').locator('[data-draft]').click()
  expect(page.locator('.workflow-finished')).to_be_visible()
  page.locator('.workflow-finished [data-schedule-draft]').click()
  form=page.locator('#schedule-deliberation-form')
  expect(form).to_be_visible()
  expect(form.locator('[name=proposalId]')).to_have_value('draft-schedule-origin')
  expect(form.locator('[name=sectionId]')).to_have_value('coordenacao')
  expect(form.locator('[name=type]')).to_have_value('Ofício')
  # The proposal provides initial context, not a locked institution rule.
  form.locator('[name=sectionId]').select_option('integridade')
  form.locator('[name=type]').select_option('PR')
  form.locator('[name=method]').select_option('binaria')
  expect(form.locator('[name=sectionId]')).to_have_value('integridade')
  expect(form.locator('[name=type]')).to_have_value('PR')
  form.locator('[name=title]').fill('Programação contextual')
  form.locator('[name=objective]').fill('Objetivo fictício de uma programação a partir do documento.')
  form.locator('[name=start]').fill('2026-12-21T10:00')
  form.locator('[name=end]').fill('2026-12-21T11:00')
  form.locator('button[type=submit]').click()
  expect(page.locator('.calendar-item').filter(has_text='Programação contextual')).to_be_visible()
  saved=page.evaluate("""()=>JSON.parse(sessionStorage.getItem('conferatus:deliberations-v010'))""")
  assert len(saved)==1,(width,saved)
  assert saved[0]['proposalId']=='draft-schedule-origin',(width,saved)
  assert saved[0]['sectionId']=='integridade' and saved[0]['type']=='PR',(width,saved)
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()

  # Starting a new schedule from calendar has no source proposal to preselect.
  page=boot(b,width)
  page.evaluate("location.hash='#/calendar'")
  page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  expect(form.locator('[name=proposalId]')).to_have_value('')
  expect(form.locator('[name=sectionId]')).to_have_value('integridade')
  expect(form.locator('[name=type]')).to_have_value('PDR')
  print('PASS contextual schedule defaults and independent calendar',width)
  page.close()
 b.close()
