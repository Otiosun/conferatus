from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'dist/CONFERATUS_demo_offline.html').read_text()
shots=root/'docs/checkpoints'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':390,'height':844})
 page.set_default_timeout(3000)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html)
 page.wait_for_selector('.result-row')
 page.screenshot(path=str(shots/'C1-v04-votacao.png'),full_page=True)
 page.get_by_role('button',name='Abrir menu').click()
 page.locator('[data-route="members"]').click()
 page.wait_for_selector('.member-item')
 page.screenshot(path=str(shots/'C1-v04-membros.png'),full_page=True)
 page.locator('[data-member="m04"]').click()
 assert 'Bruno Leal' in page.locator('.profile-identity').inner_text()
 assert page.locator('.activity').count()>0, 'Member still empty'
 assert page.evaluate('location.hash')=='#/profile/m04'
 page.screenshot(path=str(shots/'C1-v04-perfil.png'),full_page=True)
 page.reload() if False else None
 page.locator('[data-tab="proposicoes"]').click()
 assert page.locator('.activity-proposal').count()>0
 page.screenshot(path=str(shots/'C1-v04-propostas.png'),full_page=True)
 # Browser direct deeplink
 page.evaluate("location.hash='#/profile/m06'")
 page.wait_for_function("document.querySelector('.profile-identity')?.textContent?.includes('Daniel Freitas')")
 assert 'Daniel Freitas' in page.locator('.profile-identity').inner_text()
 page.get_by_role('button',name='Abrir menu').click()
 page.locator('[data-route="overview"]').click()
 page.wait_for_selector('.overview-stats')
 page.screenshot(path=str(shots/'C1-v04-historico.png'),full_page=True)
 page.locator('[data-overview-tab="proposicoes"]').click()
 assert page.locator('.activity-proposal').count()>4
 page.locator('.panel-button').click()
 page.wait_for_selector('.governance-list')
 page.locator('[data-section="coordenacao"]').click()
 page.screenshot(path=str(shots/'C1-v04-admin.png'),full_page=True)
 page.locator('[data-edit="m01"]').click()
 page.get_by_label('Nome fictício').fill('Helena Revisada')
 page.get_by_role('button',name='Salvar').click()
 assert 'Helena Revisada' in page.locator('main').inner_text()
 page.get_by_role('button',name='Reiniciar').click()
 assert 'Helena Avelar' in page.locator('main').inner_text()
 page.get_by_label('Simular perfil').select_option('membro')
 assert 'Acesso negado' in page.locator('main').inner_text()
 page.get_by_label('Simular perfil').select_option('diretor')
 assert not errors, errors
 print('v0.4 browser smoke passed, screenshots created, js errors:',errors)
 browser.close()
