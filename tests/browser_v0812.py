"""Regression checks for subversions v0.8.9-v0.8.12, self-contained preview."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'publish/index.html').read_text(encoding='utf-8')
SHOTS=ROOT/'docs/checkpoints'
SHOTS.mkdir(exist_ok=True,parents=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':390,'height':844})
    errors=[]
    page.on('pageerror',lambda exc:errors.append(str(exc)))
    page.set_content(HTML,wait_until='load')
    page.evaluate("location.hash='#/members'")
    page.locator('[data-action=search]').click()
    field=page.locator('#search-members')
    field.evaluate('(el)=>window.__searchElement = el')
    for value in ['l','li','lí','LÍA','Mia','caio']:
        field.fill(value)
        assert field.input_value()==value
        assert page.evaluate('window.__searchElement === document.querySelector("#search-members")'), 'Rebuilt keyboard input during typing'
        assert page.evaluate('document.activeElement.id === "search-members"'), 'Lost typing focus'
    field.fill('LÍa')
    assert page.locator('#member-results .member-item').count()==1
    assert 'Lia' in page.locator('#member-results').inner_text()
    assert page.locator('#member-count').inner_text()=='1 membro encontrado'
    field.fill('não tem')
    assert page.locator('#member-results .member-item').count()==0
    assert page.locator('#member-count').inner_text()=='0 membros encontrados'
    page.locator('[data-action=clear-search]').click()
    assert page.locator('#member-results .member-item').count()>=6
    assert page.locator('.clear-search[hidden]').count()==1
    page.screenshot(path=str(SHOTS/'C1-v0812-busca.png'),full_page=True)
    # A keyboard-only user can skip to main content, without breaking hash routes.
    page.keyboard.press('Tab')
    page.locator('.skip-link').focus()
    route_before=page.evaluate('location.hash')
    page.keyboard.press('Enter')
    assert page.evaluate('document.activeElement.id')=='main-content'
    assert page.evaluate('location.hash')==route_before
    # Invalid identifiers must get an inline error instead of being ignored.
    page.evaluate("location.hash='#/governance'")
    page.locator('[data-section=coordenacao]').click()
    page.locator('[data-edit=m01]').first.click()
    field=page.locator('#member-acdm-id')
    field.fill(' ')  # whitespace only
    page.locator('#edit-member-form button[type=submit]').click()
    assert '3 a 40 caracteres' in page.locator('#edit-error').inner_text()
    assert field.get_attribute('aria-invalid')=='true'
    assert page.evaluate('document.activeElement.id')=='member-acdm-id'
    field.fill('ABC?')
    page.locator('#edit-member-form button[type=submit]').click()
    assert '3 a 40 caracteres' in page.locator('#edit-error').inner_text()
    field.fill('DEMO-0002')
    page.locator('#edit-member-form button[type=submit]').click()
    assert 'já pertence' in page.locator('#edit-error').inner_text()
    field.fill('DEMO-9123')
    page.locator('#edit-member-form button[type=submit]').click()
    assert page.locator('#edit-error').count()==0
    assert page.locator('[data-action=undo]').count()==1
    page.locator('[data-action=undo]').click()
    assert 'desfeita' in page.locator('.status-line').last.inner_text()
    # No overflow or page script exception across supported widths.
    for width,height in [(320,720),(390,844),(740,1600),(1280,900)]:
        page.set_viewport_size({'width':width,'height':height})
        for route in ['ballot','members','profile/m01','overview','governance']:
            page.evaluate('(route)=>{ location.hash=`#/${route}` }',route)
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),(width,route)
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate("location.hash='#/governance'")
    page.locator('[data-section=coordenacao]').click()
    page.screenshot(path=str(SHOTS/'C1-v0812-admin.png'),full_page=True)
    page.evaluate("location.hash='#/ballot'")
    page.screenshot(path=str(SHOTS/'C1-v0812-votacao.png'),full_page=True)
    assert not errors,errors
    browser.close()
    print('PASS v0.8.12: stable mobile input, search live count, accessible skip link, invalid/duplicate ID, undo, five views at four widths, zero JS exceptions')
