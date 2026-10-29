from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
shots=root/'docs/checkpoints'
shots.mkdir(exist_ok=True,parents=True)
html=(root/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf8')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 # Navigation to localhost and file:// is blocked in this container, so use
 # content injection with a small in-memory sessionStorage stand-in.
 page.evaluate('''() => {
   const entries=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
     getItem:k=>entries.has(k)?entries.get(k):null,
     setItem:(k,v)=>entries.set(k,String(v)),
     removeItem:k=>entries.delete(k)
   }});
 }''')
 def refresh():
  page.set_content(html)
  page.wait_for_selector('.result-row') if page.url.endswith('/ballot') or not page.url.endswith('/governance') else page.wait_for_selector('.governance-list')
 refresh()
 page.screenshot(path=str(shots/'C1-v06-01-votacao.png'),full_page=True)
 page.get_by_role('button',name='Abrir menu').click()
 page.get_by_role('button',name='Como testar esta prévia').click()
 assert page.get_by_role('dialog').count()==1
 assert 'Nenhum voto ou cadastro real' in page.get_by_role('dialog').inner_text()
 page.screenshot(path=str(shots/'C1-v06-02-guia.png'),full_page=True)
 assert page.evaluate('document.activeElement.classList.contains("guide-close")')
 page.keyboard.press('Shift+Tab')
 assert page.evaluate('document.activeElement.classList.contains("guide-ok")')
 page.keyboard.press('Tab')
 assert page.evaluate('document.activeElement.classList.contains("guide-close")')
 page.keyboard.press('Escape')
 assert page.get_by_role('dialog').count()==0
 page.get_by_role('button',name='Abrir menu').click()
 page.locator('[data-route=members]').click()
 page.get_by_role('button',name='Buscar membros').click()
 page.locator('#search-members').fill('Helena')
 assert page.locator('.member-item').count()==1
 page.locator('.member-item').first.click()
 assert page.locator('.profile-identity').count()==1
 page.get_by_role('button',name='Abrir menu').click()
 page.locator('[data-route=overview]').click()
 page.locator('[data-route=governance]').click()
 page.locator('[data-section=coordenacao]').click()
 assert page.locator('.section-member').count()==5
 page.locator('[data-demote=m01]').click()
 assert page.locator('.section-member').count()==4
 assert page.get_by_role('button',name='Desfazer').count()==1
 page.screenshot(path=str(shots/'C1-v06-03-desfazer.png'),full_page=True)
 page.get_by_role('button',name='Desfazer').click()
 assert page.locator('.section-member').count()==5
 page.locator('[data-edit=m01]').first.click()
 page.locator('#member-acdm-id').fill('DEMO-UPDATED')
 page.get_by_role('button',name='Salvar').click()
 # Soft-refresh via document rewrite preserves mocked session store, like a tab reload.
 refresh()
 page.locator('[data-section=coordenacao]').click()
 page.locator('[data-edit=m01]').first.click()
 assert page.locator('#member-acdm-id').input_value()=='DEMO-UPDATED'
 page.get_by_role('button',name='Abrir ferramentas de demonstração').click()
 page.get_by_role('button',name='Reiniciar dados fictícios').click()
 refresh()
 page.locator('[data-section=coordenacao]').click()
 page.locator('[data-edit=m01]').first.click()
 assert page.locator('#member-acdm-id').input_value()=='DEMO-0001'
 page.evaluate('location.hash="#/ballot"')
 page.locator('[data-action=toggle-demo]').click()
 page.locator('[data-vote=o2]').click()
 assert page.locator('.result-row--chosen').count()==1
 refresh()
 assert page.locator('.result-row--chosen').count()==1
 page.locator('[data-action=reset-vote]').click()
 assert page.locator('.result-row--chosen').count()==0
 for width in (320,360,390,740,1280):
  page.set_viewport_size({'width':width,'height':844})
  for route in ('ballot','members','overview','governance'):
   page.evaluate('route=>location.hash="#/"+route',route)
   page.wait_for_timeout(40)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,route)
 assert not errors,errors
 print('v0.6 browser PASSED: guide, search, undo, persistence simulation, reset, voting, responsive. JS errors:',errors)
 browser.close()
