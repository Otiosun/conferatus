"""Normal-route six fictional ballot forms and a contextual calendar navigation.
No Academy identity, backend, institutional persistence, or official vote.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT = {'id':'draft-imported','title':'Proposta fictícia do calendário',
         'body':'Documento de demonstração.', 'sectionId':'integridade',
         'type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
SCHEDULE = {'id':'sched-demo-2026','title':'Votação fictícia programada',
            'objective':'Ensaio de programação local.','proposalId':'draft-imported',
            'sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00',
            'type':'PDR','status':'programada','method':'nominal',
            'choices':[{'id':'opt-1','label':'Simulação A'},{'id':'opt-2','label':'Simulação B'}]}

def vote(page,mode):
 page.locator('#preview-vote-method').select_option(mode)
 expect(page.locator('#preview-vote-form')).to_be_visible()
 if mode in ('binaria','nominal'):
  page.locator('#preview-vote-form [name=selected]').first.check()
 elif mode=='ordenada':
  for i,field in enumerate(page.locator('#preview-vote-form select[name^=rank-]').all()):
   field.select_option(index=i+1)
 elif mode=='aprovacao':
  page.locator('#preview-vote-form [name=approved]').first.check()
 elif mode=='escalar':
  for field in page.locator('#preview-vote-form select[name^=score-]').all():
   field.select_option('7')
 else:
  assert page.locator('#preview-vote-member').count()==0
  weights=page.locator('#preview-vote-form [name^=alloc-]')
  weights.first.fill('6')
  page.locator('#preview-vote-form .preview-vote-submit').click()
  expect(page.locator('#preview-vote-error')).to_be_visible()
  weights.first.fill('2')
 page.locator('#preview-vote-form .preview-vote-submit').click()
 expect(page.locator('.preview-vote-receipt')).to_be_visible()
 if mode=='cumulativa':
  expect(page.locator('.preview-vote-receipt')).to_contain_text('distribuídos 2 de 5')
 page.locator('[data-action=reset-preview-vote]').click()
 expect(page.locator('#preview-vote-form')).to_be_visible()

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(7000)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank')
  page.set_content(HTML)
  assert page.locator('.preview-vote-lab').count()==0,width
  trigger=page.locator('[data-action=toggle-voting-forms]')
  region=page.locator('#preview-vote-lab')
  expect(trigger).to_be_visible()
  assert trigger.get_attribute('aria-controls')=='preview-vote-lab',width
  assert region.count()==1,width
  expect(region).to_be_hidden()
  expect(trigger).to_have_attribute('aria-expanded','false')
  trigger.press('Enter')
  expect(region).to_be_visible()
  expect(trigger).to_have_attribute('aria-expanded','true')
  assert page.locator('#preview-vote-method option').count()==6,width
  for method in ('binaria','nominal','ordenada','aprovacao','escalar','cumulativa'):
   vote(page,method)
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  if width==390:
   page.locator('#preview-vote-method').select_option('nominal')
   page.screenshot(path=str(ROOT/'dist/voting_normal_390_v0190.png'),full_page=True)
  trigger.press('Space')
  expect(region).to_be_hidden()
  expect(trigger).to_have_attribute('aria-expanded','false')
  assert region.count()==1,width
  trigger.press('Enter')
  expect(region).to_be_visible()
  trigger.click()
  expect(region).to_be_hidden()
  assert page.locator('.preview-vote-lab').count()==0,width
  page.close()

  scheduled=browser.new_page(viewport={'width':width,'height':850})
  scheduled.set_default_timeout(7000)
  scheduled.goto('about:blank')
  scheduled.evaluate('''([draft,schedule])=>{
    const state=new Map([
      ['conferatus:proposals-v010',JSON.stringify([draft])],
      ['conferatus:deliberations-v010',JSON.stringify([schedule])]
    ]);
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
      getItem:key=>state.get(key)??null,
      setItem:(key,value)=>state.set(key,String(value)),
      removeItem:key=>state.delete(key)
    }});
  }''',[DRAFT,SCHEDULE])
  scheduled.set_content(HTML)
  scheduled.locator('.footer-nav').click()
  scheduled.locator('.menu-item[data-route="calendar"]').click()
  scheduled.locator('[data-schedule="sched-demo-2026"]').click()
  scheduled.locator('[data-preview-schedule="sched-demo-2026"]').click()
  assert scheduled.evaluate('location.hash')=='#/ballot',width
  expect(scheduled.locator('#preview-vote-lab')).to_be_visible()
  expect(scheduled.locator('#preview-vote-method')).to_have_value('nominal')
  expect(scheduled.locator('.preview-vote-context')).to_contain_text('Votação fictícia programada')
  assert scheduled.locator('.results').count()==0,(width,'unrelated sample results on scheduled ballot')
  assert scheduled.locator('.description-panel').count()==0,width
  scheduled.locator('#preview-vote-form [name=selected]').first.check()
  scheduled.locator('#preview-vote-form .preview-vote-submit').click()
  expect(scheduled.locator('.preview-vote-receipt')).to_be_visible()
  assert scheduled.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  scheduled.close()
  print('PASS normal ballot six modes and scheduled navigation',width)

 advanced=browser.new_page()
 advanced.goto('about:blank?demo=1')
 advanced.set_content(HTML)
 expect(advanced.locator('#preview-vote-lab')).to_be_visible()
 assert advanced.locator('[data-action="toggle-voting-forms"]').count()==0
 assert 'Apenas em ?demo=1' in advanced.locator('.preview-vote-disclaimer').inner_text()
 advanced.close()
 browser.close()
print('PASS: normal six voting modes across 4 widths, 4 calendar contexts, advanced lab preserved')
