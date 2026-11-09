"""Bad legacy session entries must not break healthy proposal and schedule records."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
valid_draft={'id':'local-valid','title':'Proposta íntegra de teste','body':'Texto válido da proposta preservada entre recarregamentos.', 'sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
invalid_draft={'id':'broken-draft','title':'Proposta incompleta'}
valid_schedule={'id':'local-sched','title':'Reunião da proposta íntegra','objective':'Programação ligada a uma proposição salva corretamente.', 'proposalId':'local-valid','sectionId':'integridade','start':'2026-12-18T09:00','end':'2026-12-18T11:00','type':'PDR','status':'programada'}
invalid_schedule={'id':'broken-sched','title':'Programação incompleta', 'status':'programada'}
orphan_schedule={**valid_schedule,'id':'orphan-sched','title':'Reunião com vínculo ausente','proposalId':'missing-draft'}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  errors=[]
  page.set_default_timeout(4000)
  page.on('pageerror',lambda e: errors.append(str(e)))
  page.goto('about:blank?demo=1')
  page.evaluate('''(items)=>{const data=new Map([['conferatus:proposals-v010',JSON.stringify(items[0])],['conferatus:deliberations-v010',JSON.stringify(items[1])]]);Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:(k)=>data.get(k)??null,setItem:(k,v)=>{data.set(k,v)},removeItem:(k)=>{data.delete(k)}}})}''',[[valid_draft,invalid_draft],[valid_schedule,invalid_schedule,orphan_schedule]])
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('.workflow-record').filter(has_text=valid_draft['title']).wait_for()
  assert page.locator('.workflow-record').filter(has_text=invalid_draft['title']).count()==0, width
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=calendar]').click()
  page.locator('.calendar-item').filter(has_text=valid_schedule['title']).wait_for()
  assert page.locator('.calendar-item').filter(has_text=invalid_schedule['title']).count()==0,width
  row=page.locator('.calendar-item').filter(has_text=orphan_schedule['title'])
  assert row.count()==1,width
  row.locator('[data-schedule]').click()
  assert row.get_by_text('Proposição vinculada indisponível nesta sessão.').count()==1,width
  assert row.locator('[data-open-schedule-proposal]').count()==0,width
  # Saving a valid user action must back up, rather than silently discard, skipped records.
  row.locator('[data-cancel-schedule]').click()
  row.locator('[data-confirm-cancel-schedule]').click()
  backup=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:invalid-session-backup-v0114"))')
  assert [d['id'] for d in backup['drafts']]==['broken-draft'],(width,backup)
  assert [d['id'] for d in backup['schedule']]==['broken-sched'],(width,backup)
  current=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
  assert [d['id'] for d in current]==['local-valid'],(width,current)
  page.locator('.calendar-item').filter(has_text=valid_schedule['title']).locator('[data-schedule]').click()
  assert page.locator('[data-open-schedule-proposal="local-valid"]').count()==1,width
  page.locator('[data-open-schedule-proposal="local-valid"]').click()
  page.get_by_text('Proposição concluída',exact=True).wait_for()
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('Restored sessions: invalid records skipped, healthy links kept, orphan clearly labeled (4 widths): OK')
