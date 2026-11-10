"""Cancelled local schedule cannot silently turn into a different voting form.

Reproduced before the fix at 320/390/740/1280px. Fictional records only.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

H=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT={'id':'draft-one','title':'Proposta um','body':'Texto ficticio','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
SCHEDULE={'id':'sched-one','title':'Sessão de revisão','objective':'Escolha fictícia','proposalId':'draft-one','sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'programada','method':'nominal','choices':[{'id':'opt-1','label':'Alternativa A'},{'id':'opt-2','label':'Alternativa B'}]}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=b.new_page(viewport={'width':width,'height':850})
  p.set_default_timeout(4500)
  errs=[]
  p.on('pageerror',lambda e:errs.append(str(e)))
  p.goto('about:blank')
  p.evaluate('''([draft,sched])=>{const store=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010',JSON.stringify([sched])]]);Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)}})}''',[DRAFT,SCHEDULE])
  p.set_content(H)
  p.evaluate("location.hash='#/calendar'")
  p.locator('[data-schedule=sched-one]').click()
  p.locator('[data-preview-schedule=sched-one]').click()
  expect(p.locator('#preview-vote-form')).to_be_visible()
  expect(p.locator('[name=selected]')).to_have_count(2)
  p.locator('[name=selected]').first.check()
  p.evaluate("location.hash='#/calendar'")
  if p.locator('[data-cancel-schedule=sched-one]').count()==0:
   p.locator('[data-schedule=sched-one]').click()
  p.locator('[data-cancel-schedule=sched-one]').click()
  p.locator('[data-confirm-cancel-schedule=sched-one]').click()
  p.evaluate("location.hash='#/ballot'")
  assert p.locator('#preview-vote-form').count()==0,(width,'cancelled scheduled form still active')
  expect(p.locator('#preview-vote-title')).to_contain_text('Sessão de revisão')
  expect(p.locator('#preview-vote-lab')).to_contain_text('Programação cancelada')
  assert p.locator('.results').count()==0,(width,'unrelated home totals visible')
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(p.locator('#cancelled-schedule-history')).to_contain_text('Sessão de revisão')
  p.locator('.footer-home').click()
  expect(p.locator('[data-action=enter-ballot]')).to_be_visible()
  p.locator('[data-action=enter-ballot]').click()
  expect(p.locator('[name=selected]')).to_have_count(2)
  assert p.locator('[name=selected]:checked').count()==0,width
  assert not errs,(width,errs)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS cancelled program closes vote without leaking choices',width)
  p.close()
 b.close()
