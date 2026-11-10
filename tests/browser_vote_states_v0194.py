"""Fixed ballot methods, validation and receipts for scheduled fictional deliberations."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
MODES=('binaria','nominal','ordenada','aprovacao','escalar','cumulativa')
DRAFT={'id':'draft-vote-states','title':'Proposta de estados','body':'Proposta fictícia.','sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  for mode in MODES:
   schedule={'id':'sched-'+mode,'title':'Deliberação '+mode,'objective':'Voto demonstrativo.', 'proposalId':DRAFT['id'],'sectionId':'integridade','start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'programada','method':mode}
   if mode!='binaria':schedule['choices']=[{'id':'opt-1','label':'Alternativa A'},{'id':'opt-2','label':'Alternativa B'}]
   page=browser.new_page(viewport={'width':width,'height':850});page.set_default_timeout(6000)
   errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto('about:blank')
   page.evaluate('''([draft,sched])=>{const data=new Map([['conferatus:proposals-v010',JSON.stringify([draft])],['conferatus:deliberations-v010',JSON.stringify([sched])]]);Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,String(v)),removeItem:k=>data.delete(k)}})}''',[DRAFT,schedule])
   page.set_content(HTML)
   page.evaluate("location.hash='#/calendar'")
   page.locator('[data-schedule="sched-'+mode+'"]').click()
   page.locator('[data-preview-schedule="sched-'+mode+'"]').click()
   assert page.locator('#preview-vote-method').count()==0,(mode,width)
   expect(page.locator('.preview-vote-detail').first).to_contain_text('Modalidade:')
   page.locator('.preview-vote-submit').click()
   expect(page.locator('#preview-vote-error')).to_be_visible()
   if mode in ('binaria','nominal'):page.locator('#preview-vote-form [name=selected]').first.check()
   elif mode=='ordenada':
    for i,field in enumerate(page.locator('select[name^="rank-"]').all()):field.select_option(index=i+1)
   elif mode=='aprovacao':page.locator('input[name=approved]').first.check()
   elif mode=='escalar':
    for field in page.locator('select[name^="score-"]').all():field.select_option('7')
   else:page.locator('input[name^="alloc-"]').first.fill('2')
   page.locator('.preview-vote-submit').click()
   expect(page.locator('.preview-vote-receipt')).to_be_visible()
   page.locator('[data-action=reset-preview-vote]').click()
   expect(page.locator('#preview-vote-form')).to_be_visible()
   assert not errors,(width,mode,errors)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,mode)
   page.close()
  print('PASS six fixed voting methods, errors and receipts',width)
 browser.close()
print('PASS 24 scheduled validations, receipts and resets')