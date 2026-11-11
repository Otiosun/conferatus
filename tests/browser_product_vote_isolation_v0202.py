"""Isolate fictional ballots, drafts and historic fixture numbers. No Academy records."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect

H=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text()
D={'id':'draft-isolate','title':'Proposição isolada','body':'Conteúdo sintético','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
def schedule(id,method):
 a={'id':id,'title':'Sessão '+id,'objective':'Teste isolado','proposalId':D['id'],'sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'programada','method':method}
 if method!='binaria':a['choices']=[{'id':'opt-1','label':'Alternativa A'},{'id':'opt-2','label':'Alternativa B'}]
 return a
S=[schedule('sched-iso-a','nominal'),schedule('sched-iso-b','aprovacao')]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=b.new_page(viewport={'width':width,'height':850});p.set_default_timeout(6000)
  errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto('about:blank')
  p.evaluate('''([draft,schedules])=>{const store=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010',JSON.stringify(schedules)]]);Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)}})}''',[D,S])
  p.set_content(H)
  baseline=p.locator('.results').inner_text()
  p.locator('[data-action=enter-ballot]').click()
  p.locator('[name=selected]').nth(1).check()
  p.evaluate("location.hash='#/members'")
  p.evaluate("location.hash='#/ballot'")
  expect(p.locator('[name=selected]:checked')).to_have_count(1)
  p.locator('.preview-vote-submit').click()
  expect(p.locator('.preview-vote-receipt')).to_contain_text('Calendário quinzenal')
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(p.locator('.results')).to_be_visible()
  assert p.locator('.results').inner_text()==baseline,(width,'historical fixture total changed')
  def enter(id):
   p.evaluate("location.hash='#/calendar'")
   p.locator('.calendar-list').wait_for(state='visible')
   if p.locator(f'[data-preview-schedule="{id}"]').count()==0:
    p.locator(f'[data-schedule="{id}"]').click()
   p.locator(f'[data-preview-schedule="{id}"]').click()
  enter('sched-iso-a')
  p.locator('[name=selected]').first.check()
  p.evaluate("location.hash='#/members'")
  p.evaluate("location.hash='#/ballot'")
  expect(p.locator('[name=selected]:checked')).to_have_count(1)
  enter('sched-iso-b')
  assert p.locator('[name=approved]:checked').count()==0,width
  p.locator('[name=approved]').first.check()
  enter('sched-iso-a')
  assert p.locator('[name=selected]:checked').count()==0,(width,'draft leaked across schedules')
  p.locator('.preview-vote-submit').click()
  expect(p.locator('#preview-vote-error')).to_be_visible()
  p.locator('[name=selected]').first.check()
  p.locator('.preview-vote-submit').click()
  expect(p.locator('.preview-vote-receipt')).to_contain_text('Alternativa A')
  p.locator('[data-action=reset-preview-vote]').click()
  assert p.locator('[name=selected]:checked').count()==0,width
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(p.locator('.calendar-list')).to_be_visible()
  p.locator('.footer-home').click()
  expect(p.locator('.results')).to_be_visible()
  assert p.locator('.results').inner_text()==baseline,width
  assert not errors,(width,errors)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS isolated historic totals, receipt and drafts',width)
  p.close()
 b.close()
