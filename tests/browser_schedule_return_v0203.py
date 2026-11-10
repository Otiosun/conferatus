"""Calendar-return UI regression using synthetic data only."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text()
D={'id':'draft-return','title':'Proposição fictícia','body':'Conteúdo fictício','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
S={'id':'sched-return','title':'Sessão de retorno','objective':'Percurso contextual','proposalId':'draft-return','sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'programada','method':'nominal','choices':[{'id':'opt-1','label':'Alternativa A'},{'id':'opt-2','label':'Alternativa B'}]}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=b.new_page(viewport={'width':width,'height':850});p.set_default_timeout(6000)
  errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto('about:blank')
  p.evaluate("""([draft,schedule])=>{
    const store=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010',JSON.stringify([schedule])]]);
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
      getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)}});
  }""",[D,S])
  p.set_content(HTML);p.evaluate("location.hash='#/calendar'")
  p.locator('[data-schedule="sched-return"]').click()
  p.locator('[data-preview-schedule="sched-return"]').click()
  expect(p.locator('#preview-vote-title')).to_contain_text('Sessão de retorno')
  p.locator('[name=selected]').first.check();p.locator('.preview-vote-submit').click()
  expect(p.locator('.preview-vote-receipt')).to_contain_text('Alternativa A')
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(p.locator('[data-schedule="sched-return"]')).to_be_focused()
  p.locator('[data-cancel-schedule="sched-return"]').click()
  p.locator('[data-confirm-cancel-schedule="sched-return"]').click()
  p.evaluate("location.hash='#/ballot'")
  expect(p.locator('#preview-vote-title')).to_contain_text('Sessão de retorno')
  expect(p.locator('#preview-vote-lab')).to_contain_text('Programação cancelada')
  expect(p.locator('#preview-vote-form')).to_have_count(0)
  expect(p.locator('.results')).to_have_count(0)
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(p.locator('[data-action=toggle-cancelled-history]')).to_be_focused()
  expect(p.locator('#cancelled-schedule-history')).to_contain_text('Sessão de retorno')
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  assert not errors,(width,errors)
  print('PASS calendar return/cancellation',width);p.close()
 b.close()
