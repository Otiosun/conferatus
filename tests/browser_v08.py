"""Offline HTML smoke. Browser navigation is blocked in this environment;
checks reload with a controlled sessionStorage shim rather than a real HTTP request."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'publish/index.html').read_text()
SCREEN=ROOT/'docs/checkpoints'
SCREEN.mkdir(parents=True,exist_ok=True)
STORAGE='''(snapshot) => { const values={...snapshot}; Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:key=>values[key]??null,setItem:(key,value)=>{values[key]=String(value)},removeItem:key=>{delete values[key]},clear:()=>{for(const key of Object.keys(values))delete values[key]}}}); window.__demoStore=values; }'''
def launch_page(browser, width, height, stored=None):
 page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
 errs=[]; page.on('pageerror',lambda e:errs.append(str(e)))
 page.evaluate(STORAGE,stored or {})
 page.set_content(HTML,wait_until='load')
 page.get_by_text('Objeto 01').first.wait_for()
 return page,errs
def saved(page):
 return page.evaluate('window.__demoStore')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width,height in [(320,720),(390,844),(740,1600),(1280,900)]:
  page,errors=launch_page(browser,width,height)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow width {width}'
  assert page.locator('meta[name="robots"]').get_attribute('content')=='noindex,nofollow,noarchive'
  if width==390:
   page.screenshot(path=str(SCREEN/'C1-v08-votacao.png'),full_page=True)
   page.get_by_role('button',name='Abrir menu').click()
   page.locator('[data-action=guide]').click()
   guide=page.get_by_role('dialog')
   assert guide.locator('button[data-guide-route]').count()==3
   page.screenshot(path=str(SCREEN/'C1-v08-guia.png'),full_page=True)
   guide.locator('[data-guide-route=ballot]').click()
   page.locator('[data-action=toggle-demo]').click()
   page.locator('[data-vote=o2]').click()
   assert '21 Votos' in page.locator('.result-row--chosen').inner_text()
   store=saved(page)
   assert store['conferatus:demo-vote']=='o2'
   assert not errors, errors
   page.close()
   page,errors=launch_page(browser,width,height,store)
   assert '21 Votos' in page.locator('.result-row--chosen').inner_text()
   page.get_by_role('button',name='Abrir menu').click()
   page.locator('[data-action=guide]').click()
   page.locator('[data-guide-route=members]').click()
   page.locator('[data-action=search]').click()
   page.locator('#search-members').fill('Lia')
   assert page.locator('[data-member=m03]').count()==1
   page.locator('[data-member=m03]').click()
   page.locator('[data-tab=proposicoes]').click()
   page.locator('[data-activity]').first.click()
   assert page.locator('.proposal-expansion').count()==1
   page.get_by_role('button',name='Abrir menu').click()
   page.locator('[data-action=guide]').click()
   page.locator('[data-guide-route=governance]').click()
   page.locator('.section-member').first.wait_for(timeout=2500)
   page.screenshot(path=str(SCREEN/'C1-v08-gerenciamento.png'),full_page=True)
   page.locator('[data-edit=m02]').first.click()
   page.locator('#member-acdm-id').fill('DEMO-2048')
   page.get_by_role('button',name='Salvar').click()
   store=saved(page)
   assert 'DEMO-2048' in store['conferatus:demo-members-v07']
   assert not errors, errors
   page.close()
   page,errors=launch_page(browser,width,height,store)
   page.locator('[data-action=menu]').click()
   page.locator('[data-action=guide]').click()
   page.locator('[data-guide-route=governance]').click()
   page.locator('[data-edit=m02]').first.click()
   assert page.locator('#member-acdm-id').input_value()=='DEMO-2048'
   page.get_by_role('button',name='Abrir menu').click()
   page.locator('[data-action=guide]').click()
   page.locator('[data-action=reset-all]').click()
   page.locator('[data-action=toggle-demo]').wait_for(timeout=2500)
   assert page.locator('.result-row--chosen').count()==0
   assert 'conferatus:demo-vote' not in saved(page)
   assert 'conferatus:demo-members-v07' not in saved(page)
   page.get_by_role('button',name='Abrir menu').click()
   page.locator('[data-action=guide]').click()
   page.locator('[data-guide-route=governance]').click()
   page.locator('[data-edit=m02]').first.click()
   assert page.locator('#member-acdm-id').input_value()=='DEMO-0002'
  assert not errors,f'JS exceptions width {width}: {errors}'
  print(f'PASS offline Chromium viewport {width}x{height}')
  page.close()
 browser.close()
print('PASS guided navigation, voting, search, proposals, administration, simulated reload and reset')
