from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
html=(root/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
shots=root/'docs/checkpoints'
shots.mkdir(exist_ok=True, parents=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 page.set_default_timeout(5000)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html)
 page.wait_for_selector('.result-row')
 page.screenshot(path=str(shots/'C1-v05-01-votacao.png'),full_page=True)
 page.get_by_role('button',name='Abrir menu').click()
 page.locator('[data-route="members"]').click()
 page.locator('[data-member="m04"]').click()
 page.locator('[data-tab="proposicoes"]').click()
 assert page.locator('.activity-proposal').count()>=3, 'profile should have several synthetic proposals'
 page.screenshot(path=str(shots/'C1-v05-02-propostas.png'),full_page=True)
 target=page.locator('.proposal-trigger').first
 assert target.get_attribute('aria-expanded')=='false'
 target.click()
 assert page.locator('.proposal-expansion').count()==1
 assert page.locator('.proposal-meta-row').count()==1
 page.screenshot(path=str(shots/'C1-v05-03-proposta-expandida.png'),full_page=True)
 page.locator('.proposal-trigger').first.press('Enter')
 assert page.locator('.proposal-expansion').count()==0
 # go to governance from overview
 page.get_by_role('button',name='Abrir menu').click()
 page.locator('[data-route="overview"]').click()
 page.locator('[data-overview-tab="proposicoes"]').click()
 page.locator('.proposal-trigger').first.click()
 assert page.locator('.proposal-expansion').count()==1
 page.screenshot(path=str(shots/'C1-v05-04-historico.png'),full_page=True)
 page.locator('[data-route="governance"]').click()
 page.wait_for_selector('.governance-list')
 assert page.locator('.governance-list').count()==1
 assert page.locator('.status-line').count()==0, 'no technical notice on the base canvas'
 page.screenshot(path=str(shots/'C1-v05-05-admin.png'),full_page=True)
 page.locator('[data-section="coordenacao"]').click()
 assert page.locator('.section-member').count()>2
 page.screenshot(path=str(shots/'C1-v05-06-secao.png'),full_page=True)
 # editing a row opens the same editor as in source reference
 page.locator('[data-edit="m01"]').first.click()
 assert page.locator('#member-acdm-id').count()==1
 page.screenshot(path=str(shots/'C1-v05-07-edicao.png'),full_page=True)
 page.locator('#member-acdm-id').fill('DEMO-NOVO')
 page.get_by_role('button',name='Salvar').click()
 assert 'atualizado' in page.locator('.status-line').inner_text()
 # tools popover supports add member, reset, role preview
 page.get_by_role('button',name='Abrir ferramentas de demonstração').click()
 assert page.locator('.demo-tools').count()==1
 page.screenshot(path=str(shots/'C1-v05-08-ferramentas.png'),full_page=True)
 page.get_by_label('Simular perfil').select_option('membro')
 assert 'Acesso restrito' in page.locator('main').inner_text()
 page.get_by_label('Simular perfil').select_option('diretor')
 page.locator('#add-member').select_option('m06')
 page.locator('[data-action="add-member"]').click()
 assert page.locator('.section-member').count()>4
 page.get_by_role('button',name='Abrir ferramentas de demonstração').click()
 page.get_by_role('button',name='Reiniciar dados fictícios').click()
 assert page.locator('.section-member').count()==5
 # test responsive overflow, accessibility basics
 for width in [320,360,390,740,1280]:
  page.set_viewport_size({'width':width,'height':850})
  for route in ['ballot','members','overview','governance']:
   page.evaluate('route => {location.hash = "#/"+route}',route)
   page.wait_for_timeout(35)
   overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
   assert not overflow, f'horizontal overflow {width} at {route}'
 assert not errors, errors
 print('v0.5 browser smoke PASSED; screenshots, proposal states, admin controls, responsive widths; JavaScript errors:',errors)
 browser.close()
