"""Synthetic proposal editing and Socii progress messaging."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
OLD='Redação original fictícia com participantes do Socii.'
NEW='Redação alterada com bastante conteúdo fictício para revisar o documento.'
D={'id':'draft-revision','title':'Texto com Socii','body':OLD,'sectionId':'integridade','type':'PR','authorComplete':True,
   'partners':[{'id':'m02','complete':True},{'id':'m03','complete':False}],'status':'revisao'}
def boot(browser,width):
 page=browser.new_page(viewport={'width':width,'height':850});page.set_default_timeout(6500)
 page.goto('about:blank')
 page.evaluate("""draft=>{
  const db=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010','[]']]);
  Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
   getItem:k=>db.get(k)??null,setItem:(k,v)=>db.set(k,String(v)),removeItem:k=>db.delete(k)}});
 }""",D)
 page.set_content(HTML);page.evaluate("location.hash='#/proposals'")
 return page
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=boot(b,width);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  rec=p.locator('.workflow-record').filter(has_text='Texto com Socii')
  rec.locator('[data-draft]').click()
  p.locator('#confirm-proposal-form [data-route=compose]').click()
  p.locator('#compose-proposal-form [value=conclude]').click()
  expect(p.locator('.workflow-revision-feedback')).to_have_count(0)
  p.locator('#confirm-proposal-form [data-route=compose]').click()
  p.locator('#draft-body').fill(NEW)
  p.locator('#compose-proposal-form [value=conclude]').click()
  expect(p.locator('.workflow-revision-feedback')).to_contain_text('etapas de autoria e Socii')
  expect(p.locator('.workflow-review-guidance')).to_contain_text('(pendente)')
  state=p.evaluate("""()=>{const d=JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))[0];
   return [d.status,d.authorComplete,d.partners.map(x=>x.complete),d.body]}""")
  assert state==['redacao',False,[False,False],NEW],(width,state)
  p.locator('#confirm-proposal-form button[type=submit]').click()
  expect(rec.locator('.workflow-partners')).to_contain_text('Concluíram 1 de 3')
  assert rec.locator('[data-schedule-draft]').count()==0,width
  for progress in ('Concluíram 2 de 3','Concluíram 3 de 3'):
   rec.locator('[data-confirm-partner]').first.click()
   expect(rec.locator('.workflow-partners')).to_contain_text(progress)
  expect(rec.locator('[data-schedule-draft]')).to_be_visible()
  assert not errors,(width,errors)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  p.close()
  p=boot(b,width)
  rec=p.locator('.workflow-record').filter(has_text='Texto com Socii')
  rec.locator('[data-draft]').click()
  p.locator('#confirm-proposal-form [data-route=compose]').click()
  p.locator('#draft-body').fill(NEW)
  p.locator('#compose-proposal-form [value=save]').click()
  expect(p.locator('.workflow-status')).to_contain_text('confirmações anteriores foram reiniciadas')
  expect(rec.locator('.workflow-partners')).to_contain_text('Concluíram 0 de 3')
  p.close();print('PASS local Socii revision UX',width)
 b.close()
