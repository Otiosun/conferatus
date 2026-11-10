"""Natural Socii-to-calendar journey; all data synthetic."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text()
D={'id':'d-socii','title':'Proposição Socii','body':'Texto fictício para testar o percurso completo.','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[{'id':'m02','complete':False}],'status':'revisao'}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=b.new_page(viewport={'width':width,'height':850});p.set_default_timeout(6000)
  errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto('about:blank')
  p.evaluate("""draft=>{const db=new Map([['conferatus:proposals-v010',JSON.stringify([draft])]]);Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>db.get(k)??null,setItem:(k,v)=>db.set(k,String(v)),removeItem:k=>db.delete(k)}})}""",D)
  p.set_content(HTML);p.evaluate("location.hash='#/proposals'")
  record=p.locator('.workflow-record').filter(has_text='Proposição Socii')
  expect(p.locator('.workflow-proposals-layout > .workflow-socii-help')).to_have_count(1)
  expect(p.locator('.workflow-proposals-layout > .workflow-socii-help')).to_contain_text('Nenhuma outra conta')
  expect(record.locator('.workflow-socii-help')).to_have_count(0)
  action=record.locator('[data-confirm-partner]')
  expect(action).to_contain_text('Marcar etapa')
  assert 'Simular conclusão' not in record.inner_text(),width
  action.click();expect(record).to_contain_text('Concluída')
  assert record.locator('[data-confirm-partner]').count()==0,width
  record.locator('[data-schedule-draft]').click()
  form=p.locator('#schedule-deliberation-form')
  expect(form).to_be_visible()
  assert form.locator('[name=proposalId]').input_value()=='d-socii',width
  assert not errors,(width,errors)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS synthetic Socii and calendar',width);p.close()
 b.close()
