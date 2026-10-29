"""Microversion browser checks using the built single-file demo, no live backend."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda err: errors.append(str(err)))
    page.set_content(html,wait_until='load')
    page.get_by_role('button',name='Abrir menu').click()
    page.locator('[data-action=guide]').click()
    assert page.get_by_role('dialog').count()==1
    assert page.locator('main').get_attribute('inert') is not None
    assert page.evaluate('document.activeElement.classList.contains("guide-close")')
    page.keyboard.press('Escape')
    assert page.get_by_role('dialog').count()==0
    assert page.evaluate('document.activeElement.classList.contains("footer-nav")')
    page.locator('[data-action=menu]').click()
    page.locator('[data-route=members]').click()
    page.locator('[data-action=search]').click()
    page.locator('#search-members').fill('lia')
    assert page.get_by_text('Lia Batista').count()==1
    page.keyboard.press('Escape')
    assert page.locator('#search-members').count()==0
    assert page.evaluate('document.activeElement.getAttribute("data-action")==="search"')
    page.evaluate("location.hash='#/profile/unknown-user'")
    page.get_by_text('Perfil não encontrado').wait_for(timeout=2500)
    page.get_by_role('button',name='Voltar aos membros').click()
    page.locator('[data-action=search]').wait_for(timeout=2500)
    page.evaluate("location.hash='#/governance'")
    page.locator('[data-section=coordenacao]').click()
    first=page.locator('[data-edit=m01]').first
    first.click()
    assert page.evaluate('document.activeElement?.id==="member-acdm-id"')
    page.keyboard.press('Escape')
    assert page.locator('#edit-member-form').count()==0
    assert not errors,errors
    print('PASS modal inertia/focus, Escape dismissal, accent search, invalid profile recovery, edit focus')
    browser.close()
