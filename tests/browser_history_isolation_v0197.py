"""Personal/institutional fixture history versus local proposals and vote samples.

All records are synthetic; no Academy session or official participation is asserted.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT=[
 {'id':'draft-history-01','title':'Proposta da sessão do autor','body':'Texto fictício que só deve aparecer no perfil da autoria de demonstração.','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'},
 {'id':'draft-history-02','title':'Proposição incompleta privada','body':'Outro registro local sem informações institucionais.','sectionId':'integridade','type':'PDR','authorComplete':False,'partners':[],'status':'redacao'}
]
SCHEDULE=[
 {'id':'schedule-history-01','title':'Programação ativa da sessão','objective':'Objetivo demonstrativo','proposalId':'draft-history-01','sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'programada','method':'nominal','choices':[{'id':'opt-1','label':'Opção A'},{'id':'opt-2','label':'Opção B'}]},
 {'id':'schedule-history-cancel','title':'Programação cancelada da sessão','objective':'Objetivo de cancelamento','proposalId':'draft-history-01','sectionId':'integridade','start':'2026-12-22T09:00','end':'2026-12-22T11:00','type':'PDR','status':'cancelada','method':'nominal','choices':[{'id':'opt-1','label':'Opção A'},{'id':'opt-2','label':'Opção B'}]}
]

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(5000)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank')
  page.evaluate('''([drafts,schedules])=>{
   const store=new Map([
    ['conferatus:proposals-v010',JSON.stringify(drafts)],
    ['conferatus:deliberations-v010',JSON.stringify(schedules)]
   ]);
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:key=>store.get(key)??null,setItem:(key,value)=>store.set(key,String(value)),removeItem:key=>store.delete(key)
   }});
  }''',[DRAFT,SCHEDULE])
  page.set_content(HTML)
  page.evaluate("location.hash='#/overview'")
  # Institutional sample metrics are fixture-derived, not local authorship or samples.
  baseline=page.locator('.overview-stats').inner_text()
  assert 'Proposta da sessão do autor' not in baseline,width
  page.locator('[data-overview-tab=proposicoes]').click()
  expect(page.locator('.overview-local-history')).to_contain_text('Proposta da sessão do autor')
  expect(page.locator('.overview-local-history')).to_contain_text('Proposição incompleta privada')
  assert page.locator('.overview-content .activity-proposal').count()>0,width
  assert page.locator('.overview-stats').inner_text()==baseline,width
  assert page.locator('.overview-local-history .session-schedule-link').count()==1,width
  assert 'Programação cancelada da sessão' not in page.locator('.overview-local-history').inner_text(),width
  page.evaluate("location.hash='#/profile/m01'")
  page.locator('[data-tab=proposicoes]').click()
  expect(page.locator('.session-proposal')).to_have_count(2)
  expect(page.locator('.session-proposal').first).to_contain_text('Proposta da sessão do autor')
  assert page.locator('.session-schedule-link').count()==1,width
  page.locator('[data-tab=votos]').click()
  personal_count=page.locator('.activity-vote').count()
  assert personal_count>0,width
  assert page.locator('.session-proposal').count()==0,width
  page.evaluate("location.hash='#/profile/m02'")
  assert page.locator('.session-proposal').count()==0,width
  assert page.locator('.session-schedule-link').count()==0,width
  page.locator('[data-tab=proposicoes]').click()
  assert page.locator('.activity-proposal').count()>0,width
  assert 'Proposta da sessão do autor' not in page.locator('.section-body').inner_text(),width
  page.evaluate("location.hash='#/ballot'")
  page.locator('[data-action=toggle-voting-forms]').click()
  page.locator('#preview-vote-method').select_option('nominal')
  page.locator('#preview-vote-form [name=selected]').first.check()
  page.locator('#preview-vote-form .preview-vote-submit').click()
  expect(page.locator('.preview-vote-receipt')).to_be_visible()
  page.evaluate("location.hash='#/overview'")
  assert page.locator('.overview-stats').inner_text()==baseline,(width,'a sample vote changed institution-style metrics')
  page.locator('[data-overview-tab=votos]').click()
  assert page.locator('.overview-local-history').count()==0,width
  assert 'Voto simulado conferido' not in page.locator('.overview-content').inner_text(),width
  page.evaluate("location.hash='#/profile/m01'")
  page.locator('[data-tab=votos]').click()
  assert page.locator('.activity-vote').count()==personal_count,(width,'sample ballot wrongly attributed to an author')
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS history separation, fictional author, institution totals, vote samples',width)
  page.close()
 browser.close()
print('PASS all four widths: personal/institutional demo history remains separate from local-only records')
