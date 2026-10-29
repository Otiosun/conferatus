"""Focused regression of the v0.8.5–v0.8.8 micro-updates."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 page.set_content(html,wait_until='load')
 # Search filter with the new clear action.
 page.evaluate("location.hash='#/members'")
 page.locator('[data-action=search]').click()
 page.locator('#search-members').fill('inexistente')
 assert 'Nenhum membro encontrado' in page.locator('.member-list').inner_text()
 page.locator('[data-action=clear-search]').click()
 assert page.locator('#search-members').input_value()==''
 assert page.evaluate("document.activeElement.id==='search-members'")
 # Proposal expansion must preserve scroll position, rather than jump to the hero.
 page.evaluate("location.hash='#/profile/m01'")
 page.locator('[data-tab=proposicoes]').click()
 assert page.locator('[data-activity]').count()>1
 page.evaluate('window.scrollTo(0, 250)')
 before=page.evaluate('window.scrollY')
 page.locator('[data-activity]').first.click()
 after=page.evaluate('window.scrollY')
 assert abs(after-before)<=2,(before,after)
 # Invalid member IDs are explained immediately near the form; editing stays open.
 page.evaluate("location.hash='#/governance'")
 page.locator('[data-section=coordenacao]').click()
 page.locator('[data-edit=m01]').first.click()
 page.locator('#member-acdm-id').fill('DEMO-0002')
 page.locator('#edit-member-form button[type=submit]').click()
 assert page.locator('.edit-error').count()==1
 assert page.locator('#member-acdm-id').get_attribute('aria-invalid')=='true'
 assert page.evaluate("document.activeElement.id==='member-acdm-id'")
 assert page.locator('.edit-error').inner_text().startswith('Este identificador')
 page.locator('#member-acdm-id').fill('DEMO-9090')
 page.locator('#edit-member-form button[type=submit]').click()
 assert page.locator('.edit-error').count()==0
 assert page.locator('[data-action=undo]').count()==1
 assert page.evaluate("document.activeElement.getAttribute('data-action')==='undo'")
 page.locator('[data-action=undo]').click()
 assert 'desfeita' in page.locator('[role=status]').last.inner_text().lower()
 # Demotion action removes exactly one section association; Undo restores it.
 count_before=page.locator('[data-demote=m01]').count()
 assert count_before>0
 page.locator('[data-demote=m01]').first.click()
 assert page.evaluate("document.activeElement.getAttribute('data-action')==='undo'")
 page.locator('[data-action=undo]').click()
 assert page.locator('[data-demote=m01]').count()==count_before
 assert not errors, errors
 page.screenshot(path=str(ROOT/'docs/checkpoints/C1-v088-admin.png'),full_page=True)
 for w,h in [(320,720),(390,844),(740,1600),(1280,900)]:
  page.set_viewport_size({'width':w,'height':h})
  page.evaluate("location.hash='#/ballot'")
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),w
  page.evaluate("location.hash='#/members'")
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),w
  page.evaluate("location.hash='#/governance'")
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),w
 page.set_viewport_size({'width':390,'height':844})
 page.evaluate("location.hash='#/ballot'")
 page.screenshot(path=str(ROOT/'docs/checkpoints/C1-v088-votacao.png'),full_page=True)
 page.evaluate("location.hash='#/members'")
 page.screenshot(path=str(ROOT/'docs/checkpoints/C1-v088-membros.png'),full_page=True)
 assert not errors,errors
 browser.close()
 print('PASS v0.8.8: clear search, scroll position, inline ID validation, edit/demotion undo, four responsive widths, zero JS exceptions')
