"""Run without network; executes the exact bundled HTML using Playwright's set_content."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'publish/index.html').read_text()
OUT=ROOT/'docs/checkpoints'
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
 browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width,height in [(320,740),(390,844),(740,900),(1280,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(HTML,wait_until='load')
  page.get_by_text('Objeto 01').first.wait_for()
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'Overflow width {width}'
  if width==390:
   page.screenshot(path=str(OUT/'C1-v07-votacao.png'),full_page=True)
   page.get_by_role('button',name='Simular voto').click()
   page.locator('button[data-vote="o2"]').click()
   assert '21 Votos' in page.locator('.result-row--chosen').inner_text()
   page.screenshot(path=str(OUT/'C1-v07-voto.png'),full_page=True)
   page.locator('button[data-action="menu"]').click()
   page.locator('button[data-action="guide"]').click()
   assert page.get_by_role('dialog').count()==1
   page.keyboard.press('Escape')
   assert page.get_by_role('dialog').count()==0
   page.locator('button[data-action="menu"]').click()
   page.locator('[data-route="members"]').click()
   page.locator('[data-action="search"]').click()
   page.locator('#search-members').fill('Bruno')
   assert page.get_by_role('button',name='Bruno Leal').count()==1
   page.screenshot(path=str(OUT/'C1-v07-busca.png'),full_page=True)
   page.get_by_role('button',name='Bruno Leal').click()
   assert 'Bruno Leal' in page.locator('body').inner_text()
   page.locator('button[data-tab="proposicoes"]').click()
   page.locator('button[data-activity]').first.click()
   assert page.locator('.proposal-expansion').count()==1
   page.locator('button[data-action="menu"]').click()
   page.locator('[data-route="overview"]').click()
   page.locator('[data-route="governance"]').click()
   page.locator('[data-section="coordenacao"]').click()
   page.screenshot(path=str(OUT/'C1-v07-painel.png'),full_page=True)
   page.locator('[data-edit="m02"]').first.click()
   page.locator('#member-acdm-id').fill('DEMO-2048')
   page.get_by_role('button',name='Salvar').click()
   assert 'atualizado' in page.locator('.status-line').inner_text()
   page.get_by_role('button',name='Desfazer').click()
   assert 'desfeita' in page.locator('.status-line').inner_text()
  assert not errors, f'JS exceptions at width {width}: {errors}'
  print(f'OK viewport {width}x{height} no overflow / JS exceptions')
  page.close()
 browser.close()
print('OK interactive demo: vote, guide, search, profile, proposals, governance, edit, undo')
