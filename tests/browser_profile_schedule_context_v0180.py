"""Profile → scheduling context must retain the correct completed proposal.

No new vote logic, Academy accounts or admin permission is asserted. The
profile merely opens the existing local calendar form with a preselection.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
probe="""() => {
 const e=new Event('beforeunload',{cancelable:true});
 window.dispatchEvent(e);
 return e.defaultPrevented;
}"""

with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width in (280,320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(7000)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1')
  page.evaluate("""() => {
   const store=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>store.get(k)??null,
    setItem:(k,v)=>store.set(k,String(v)),
    removeItem:k=>store.delete(k)
   }});
  }""")
  page.set_content(html)
  def menu(route):
   page.locator('.footer-nav').click()
   page.locator(f'.menu-item[data-route="{route}"]').click()
  menu('proposals')
  def make_draft(title,complete=True):
   page.locator('[data-action=new-proposal]').click()
   page.locator('#draft-title').fill(title)
   page.locator('#draft-body').fill(
      'Texto local fictício em revisão, sem valor institucional nem informação de membros reais.')
   if complete:
    page.locator('#compose-proposal-form [value=conclude]').click()
    page.locator('#confirm-proposal-form button[type=submit]').click()
   else:
    page.locator('#compose-proposal-form [value=save]').click()
   page.locator('[data-action=new-proposal]').wait_for(state='visible')
  make_draft('Proposta contextual A')
  make_draft('Proposta contextual B')
  make_draft('Rascunho ainda em redação',complete=False)
  ids=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010")).map(d=>[d.title,d.id,d.status])')
  chosen=next(x[1] for x in ids if x[0]=='Proposta contextual B')
  assert len(ids)==3,width
  menu('members')
  page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  a=page.locator('.session-proposal').filter(has_text='Proposta contextual A')
  b=page.locator('.session-proposal').filter(has_text='Proposta contextual B')
  unfinished=page.locator('.session-proposal').filter(has_text='Rascunho ainda em redação')
  assert a.locator('[data-schedule-draft]').count()==1,width
  assert b.locator('[data-schedule-draft]').count()==1,width
  assert unfinished.locator('[data-schedule-draft]').count()==0,width
  btn=b.locator('[data-schedule-draft]')
  assert btn.bounding_box()['height']>=44,(width,'tiny contextual action')
  btn.click()
  form=page.locator('#schedule-deliberation-form')
  form.wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/calendar',(width,'context route')
  select=form.locator('[name=proposalId]')
  assert select.input_value()==chosen,(width,'wrong proposal linked')
  assert not page.evaluate(probe),(width,'untouched contextual preselection triggers an unnecessary leave warning')
  assert select.evaluate('(e)=>document.activeElement===e'),(width,'contextual form missing focus')
  # Closing an unmodified contextual form should be quick and quiet.
  unexpected=[]
  page.on('dialog',lambda dlg:(unexpected.append(dlg.message),dlg.dismiss()))
  page.locator('[data-action=open-schedule]').click()
  assert form.count()==0,width
  assert not unexpected,(width,'false leave warning',unexpected)
  # Entry from the independent Proposições page is available too.
  menu('proposals')
  shortcut=page.locator('.workflow-record').filter(has_text='Proposta contextual B').locator('[data-schedule-draft]')
  shortcut.click()
  form=page.locator('#schedule-deliberation-form')
  form.wait_for(state='visible')
  assert form.locator('[name=proposalId]').input_value()==chosen,width
  form.locator('[name=title]').fill('Deliberação vinculada a B')
  form.locator('[name=objective]').fill('A segunda proposta deve ser o único documento vinculado nesta simulação.')
  form.locator('[name=method]').select_option('binaria')
  form.locator('[name=start]').fill('2027-03-18T09:00')
  form.locator('[name=end]').fill('2027-03-18T11:00')
  form.locator('button[type=submit]').click()
  item=page.locator('.calendar-item').filter(has_text='Deliberação vinculada a B')
  item.wait_for(state='visible')
  records=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
  assert len(records)==1 and records[0]['proposalId']==chosen,(width,records)
  assert not page.evaluate(probe),(width,'saved form still guarded')
  menu('members')
  page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  b=page.locator('.session-proposal').filter(has_text='Proposta contextual B')
  assert b.locator('.session-schedule-link').count()==1,width
  a=page.locator('.session-proposal').filter(has_text='Proposta contextual A')
  assert a.locator('.session-schedule-link').count()==0,width
  menu('members')
  page.locator('.member-item[data-member=m04]').click()
  page.locator('[data-tab=proposicoes]').click()
  assert page.locator('[data-schedule-draft]').count()==0,(width,'another fixture member inherited local author controls')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'overflow')
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('PASS: completed author proposal context, prefill/keyboard, draft isolation and correct schedule link; '+engine)
