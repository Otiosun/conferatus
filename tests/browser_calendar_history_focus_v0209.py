"""PF-18: cancelled calendar rows remain discoverable without appearing active."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
D={'id':'d-history','title':'Documento do calendário','body':'Texto fictício concluído para o calendário.','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
ACTIVE={'id':'sched-active','title':'Agenda ativa para cancelar','objective':'Programação fictícia de trabalho.','proposalId':'d-history','sectionId':'integridade','start':'2026-12-12T09:00','end':'2026-12-12T11:00','type':'PDR','method':'binaria','status':'programada'}
OLD={**ACTIVE,'id':'sched-old','title':'Agenda anteriormente cancelada','start':'2026-12-13T09:00','end':'2026-12-13T11:00','status':'cancelada'}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=b.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(6500);errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank')
  page.evaluate("""([draft,active,old])=>{
   const db=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010',JSON.stringify([active,old])]]);
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>db.get(k)??null,setItem:(k,v)=>db.set(k,String(v)),removeItem:k=>db.delete(k)}});
  }""",[D,ACTIVE,OLD])
  page.set_content(HTML)
  page.evaluate("location.hash='#/calendar'")
  expect(page.locator('.calendar-item').filter(has_text='Agenda ativa para cancelar')).to_have_count(1)
  expect(page.locator('.calendar-item').filter(has_text='Agenda anteriormente cancelada')).to_have_count(0)
  history=page.locator('[data-action=toggle-cancelled-history]')
  expect(history).to_have_attribute('aria-expanded','false')
  expect(history).to_contain_text('(1)')
  for _ in range(4):
   if 'dezembro de 2026' in page.locator('.calendar-month-nav h2').inner_text().lower():break
   page.locator('[data-action=calendar-next]').click()
  assert '1 programação' in page.locator('[data-calendar-day="2026-12-12"]').get_attribute('aria-label'),width
  assert 'programação' not in page.locator('[data-calendar-day="2026-12-13"]').get_attribute('aria-label'),width
  page.locator('[data-calendar-day="2026-12-12"]').click()
  row=page.locator('.calendar-item').filter(has_text='Agenda ativa para cancelar')
  row.locator('[data-schedule]').click()
  row.locator('[data-cancel-schedule]').click()
  row.locator('[data-confirm-cancel-schedule]').click()
  expect(row).to_have_count(0)
  expect(page.locator('.calendar-empty-message')).to_contain_text('Nenhuma programação nesta data')
  expect(page.locator('.workflow-status')).to_contain_text('Consulte o histórico de cancelamentos')
  expect(history).to_be_focused()
  expect(history).to_have_attribute('aria-expanded','false')
  expect(history).to_contain_text('(2)')
  assert 'programação' not in page.locator('[data-calendar-day="2026-12-12"]').get_attribute('aria-label'),width
  history.click()
  region=page.locator('#cancelled-schedule-history')
  expect(region.locator('.calendar-cancelled-record')).to_have_count(2)
  expect(region).to_contain_text('Agenda ativa para cancelar')
  expect(region).to_contain_text('Agenda anteriormente cancelada')
  assert region.locator('[data-cancel-schedule]').count()==0,width
  saved=page.evaluate("JSON.parse(sessionStorage.getItem('conferatus:deliberations-v010'))")
  assert len(saved)==2 and all(s['status']=='cancelada' for s in saved),(width,saved)
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS calendar cancellation history/focus',width)
  page.close()
 b.close()
