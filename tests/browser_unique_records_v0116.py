"""Duplicate workflow IDs or repeated Socii participants cannot ambiguously bind buttons."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
base={'id':'p-primary','title':'Proposição original','body':'Proposição previamente concluída por todas as pessoas vinculadas à demonstração.', 'sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
draft_duplicate={**base,'title':'Proposição duplicada incorreta','body':'Outra redação com o mesmo identificador da proposta original.'}
partner_duplicate={**base,'id':'p-repeated-partners','title':'Socii repetido','partners':[{'id':'m02','complete':True},{'id':'m02','complete':True}]}
sched={'id':'s-primary','title':'Programação original','objective':'Programação associada à versão correta da proposição.', 'proposalId':'p-primary','sectionId':'integridade','start':'2026-11-22T10:00','end':'2026-11-22T11:00','type':'PDR','status':'programada'}
sched_duplicate={**sched,'title':'Programação duplicada incorreta','proposalId':'missing-proposal'}
sched_second={**sched,'id':'s-secondary','title':'Programação secundária','start':'2026-11-23T12:00','end':'2026-11-23T13:00'}

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  page.set_default_timeout(6000)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1')
  page.evaluate('''data=>{const store=new Map(Object.entries(data));Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)}})}''',{'conferatus:proposals-v010':json.dumps([base,draft_duplicate,partner_duplicate]), 'conferatus:deliberations-v010':json.dumps([sched,sched_duplicate,sched_second])})
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('.workflow-record').filter(has_text='Proposição original').wait_for()
  assert page.locator('.workflow-record').filter(has_text='Proposição original').count()==1,width
  assert page.locator('.workflow-record').filter(has_text='Proposição duplicada incorreta').count()==0,(width,'duplicated draft ID accepted')
  assert page.locator('.workflow-record').filter(has_text='Socii repetido').count()==0,(width,'duplicated partner IDs accepted')
  assert 'registros incompletos' in page.locator('.workflow-form-error').inner_text().lower(),width
  if width in (390,740):
   page.screenshot(path=f'/mnt/data/conferatus_v0116_id_quarantine_{width}.png',full_page=True)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=calendar]').click()
  page.locator('.calendar-item').filter(has_text='Programação original').wait_for()
  assert page.locator('.calendar-item').filter(has_text='Programação original').count()==1,width
  assert page.locator('.calendar-item').filter(has_text='Programação duplicada incorreta').count()==0,(width,'duplicated schedule ID accepted')
  assert page.locator('.calendar-item').filter(has_text='Programação secundária').count()==1,width
  original=page.locator('.calendar-item').filter(has_text='Programação original')
  original.locator('[data-schedule]').click()
  assert original.locator('[data-open-schedule-proposal="p-primary"]').count()==1,width
  original.locator('[data-open-schedule-proposal="p-primary"]').click()
  page.get_by_text('Proposição concluída',exact=True).wait_for()
  page.locator('.workflow-finished [data-route=calendar]').click()
  assert page.evaluate('location.hash')=='#/calendar',width
  secondary=page.locator('.calendar-item').filter(has_text='Programação secundária')
  secondary.locator('[data-schedule]').click()
  secondary.locator('[data-cancel-schedule]').click()
  backup=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:invalid-session-backup-v0114"))')
  assert [d['title'] for d in backup['drafts']]==['Proposição duplicada incorreta','Socii repetido'],(width,backup)
  assert [s['title'] for s in backup['schedule']]==['Programação duplicada incorreta'],(width,backup)
  saved_drafts=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
  saved_schedule=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
  assert [d['id'] for d in saved_drafts]==['p-primary'],(width,saved_drafts)
  assert [s['id'] for s in saved_schedule]==['s-primary','s-secondary'],(width,saved_schedule)
  journal=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:quarantined-session-backups-v0116"))')
  assert journal==[backup],(width,journal)
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
  if width==390:
   # An existing v0114 backup must not be overwritten or cause new rejects to vanish.
   older={'drafts':[{'id':'old-damaged','title':'Registro anterior'}],'schedule':[]}
   more=browser.new_page(viewport={'width':390,'height':844})
   more.goto('about:blank?demo=1')
   more.evaluate('''data=>{const store=new Map(Object.entries(data));Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)}})}''',{'conferatus:proposals-v010':json.dumps([base,draft_duplicate]),'conferatus:deliberations-v010':json.dumps([sched,sched_duplicate]),'conferatus:invalid-session-backup-v0114':json.dumps(older)})
   more.set_content(html)
   more.locator('.footer-nav').click()
   more.locator('.menu-item[data-route=calendar]').click()
   more.locator('.calendar-item').filter(has_text='Programação original').wait_for()
   row=more.locator('.calendar-item').filter(has_text='Programação original')
   row.locator('[data-schedule]').click()
   row.locator('[data-cancel-schedule]').click()
   assert more.evaluate('JSON.parse(sessionStorage.getItem("conferatus:invalid-session-backup-v0114"))')==older
   second=more.evaluate('JSON.parse(sessionStorage.getItem("conferatus:quarantined-session-backups-v0116"))')
   assert len(second)==1 and second[0]['drafts'][0]['title']=='Proposição duplicada incorreta',second
   assert second[0]['schedule'][0]['title']=='Programação duplicada incorreta',second
   more.close()
 browser.close()
print('Unique workflow IDs, partner IDs and cumulative quarantine with prior legacy backup: OK')
