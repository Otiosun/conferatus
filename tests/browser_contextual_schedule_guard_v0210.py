"""Fictional PF-19/PF-20 schedule context and unsaved-editor continuity."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
D={'id':'draft-pf20','title':'Proposição de encaminhamento','body':'Documento fictício finalizado para agendamento.','sectionId':'coordenacao','type':'Ofício','authorComplete':True,'partners':[],'status':'concluida'}
S={'id':'sched-pf20','title':'Sessão de encaminhamento','objective':'Consulta fictícia relacionada ao documento.',
   'proposalId':'draft-pf20','sectionId':'coordenacao','start':'2026-12-21T09:00','end':'2026-12-21T11:00',
   'type':'Ofício','status':'programada','method':'nominal',
   'choices':[{'id':'opt-1','label':'Alternativa Primeira'},{'id':'opt-2','label':'Alternativa Segunda'}]}

def setup(browser,width):
 p=browser.new_page(viewport={'width':width,'height':850});p.set_default_timeout(6500)
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('about:blank')
 p.evaluate("""([draft,schedule])=>{
  const items=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],
                       ['conferatus:deliberations-v010',JSON.stringify([schedule])]]);
  Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>items.get(k)??null,setItem:(k,v)=>items.set(k,String(v)),
    removeItem:k=>items.delete(k)}});
 }""",[D,S])
 p.set_content(HTML);p.evaluate("location.hash='#/proposals'")
 p.locator('.workflow-record').filter(has_text='Proposição de encaminhamento').locator('[data-draft]').click()
 p.locator('.workflow-finished [data-schedule-draft]').click()
 form=p.locator('#schedule-deliberation-form')
 expect(form).to_be_visible()
 expect(form.locator('[name=proposalId]')).to_have_value('draft-pf20')
 expect(form.locator('[name=sectionId]')).to_have_value('coordenacao')
 expect(form.locator('[name=type]')).to_have_value('Ofício')
 return p,form,errors

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p,form,errors=setup(browser,width)
  prompts=[]
  p.on('dialog',lambda d:(prompts.append(d.message),d.dismiss()))
  # No false confirmation when prefilled values have not been edited.
  p.locator('[data-action=open-schedule]').click()
  expect(form).to_have_count(0)
  assert not prompts,(width,prompts)
  assert not errors,(width,errors)
  p.close()

  # Decline leaving the unfinished form to participate in an existing schedule.
  p,form,errors=setup(browser,width)
  form.locator('[name=title]').fill('Agendamento em andamento')
  p.locator('[data-schedule="sched-pf20"]').click()
  participate=p.locator('[data-preview-schedule="sched-pf20"]')
  expect(participate).to_contain_text('Participar')
  seen=[]
  p.once('dialog',lambda d:(seen.append(d.message),d.dismiss()))
  participate.click()
  assert len(seen)==1,(width,'expected one leave confirmation',seen)
  assert p.evaluate('location.hash')=='#/calendar',width
  expect(form.locator('[name=title]')).to_have_value('Agendamento em andamento')
  p.once('dialog',lambda d:d.accept())
  p.locator('[data-action=open-schedule]').click()
  expect(form).to_have_count(0)
  p.locator('.footer-home').click()
  expect(p.locator('.results')).to_be_visible()
  assert p.locator('#preview-vote-title').count()==0,(width,'abandoned contextual state')
  assert not errors,(width,errors)
  p.close()

  # Accept leaving and keep the intended program, its choices and return focus.
  p,form,errors=setup(browser,width)
  form.locator('[name=title]').fill('Outro rascunho de agendamento')
  p.locator('[data-schedule="sched-pf20"]').click()
  p.once('dialog',lambda d:d.accept())
  p.locator('[data-preview-schedule="sched-pf20"]').click()
  expect(p.locator('#preview-vote-title')).to_contain_text('Sessão de encaminhamento')
  expect(p.locator('.preview-vote-context')).to_contain_text('Proposição de encaminhamento')
  expect(p.locator('.preview-vote-detail')).to_contain_text('Nominal')
  expect(p.locator('[name=selected]')).to_have_count(2)
  p.locator('[name=selected]').nth(1).check()
  p.locator('.preview-vote-submit').click()
  expect(p.locator('.preview-vote-receipt')).to_contain_text('Alternativa Segunda')
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(p.locator('[data-schedule="sched-pf20"]')).to_be_focused()
  assert p.locator('#schedule-deliberation-form').count()==0,width
  assert not errors,(width,errors)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS contextual participation and schedule guard',width)
  p.close()
 browser.close()
