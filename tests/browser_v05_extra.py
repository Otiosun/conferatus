from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':360,'height':760})
 errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 page.set_content(html)
 page.evaluate('location.hash="#/governance"')
 page.locator('[data-section="coordenacao"]').click()
 # Duplicate identifier must be rejected
 page.locator('[data-edit="m01"]').first.click()
 page.locator('#member-acdm-id').fill('DEMO-0002')
 page.get_by_role('button',name='Salvar').click()
 assert 'já utilizado' in page.locator('.status-line').inner_text()
 # Demotion removes only membership and keeps the historical voting record
 page.locator('[data-demote="m01"]').click()
 assert 'Vínculo removido' in page.locator('.status-line').inner_text()
 page.evaluate('location.hash="#/profile/m01"')
 page.wait_for_selector('.profile-identity')
 assert 'Helena Avelar' in page.locator('.profile-identity').inner_text()
 assert page.locator('.activity-vote').count()>=1
 # Esc closes the menu without navigating away
 page.get_by_role('button',name='Abrir menu').click()
 assert page.locator('.bottom-menu').count()==1
 page.keyboard.press('Escape')
 assert page.locator('.bottom-menu').count()==0
 # Expanded proposal's disclosure target exists in both states.
 page.locator('[data-tab="proposicoes"]').click()
 trigger=page.locator('.proposal-trigger').first
 target_id=trigger.get_attribute('aria-controls')
 assert page.locator(f'#{target_id}').count()==1
 trigger.click()
 assert page.locator(f'#{target_id}.proposal-expansion').count()==1
 assert errors==[], errors
 browser.close()
 print('v0.5 extra checks PASSED: duplicate ID, historical integrity, Escape, disclosure attributes; errors:',errors)
