from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('[data-route="calendar"]').first.click()
        page.locator('[data-action="open-schedule"]').click()
        form = page.locator('#schedule-deliberation-form')
        assert form.is_visible(), width
        assert form.evaluate("el => getComputedStyle(el).backgroundColor") == 'rgb(81, 93, 199)', width
        for name in ('title', 'objective', 'proposalId', 'sectionId', 'start', 'end', 'type', 'method'):
            assert form.locator(f'[name="{name}"]').count() == 1, (width, name)
        assert form.locator('[name="title"]').evaluate(
            "el => getComputedStyle(el).color") == 'rgb(255, 255, 255)', width
        form.locator('[name="title"]').fill('Reunião em preparação')
        page.locator('[data-action="calendar-next"]').click()
        assert form.locator('[name="title"]').input_value() == 'Reunião em preparação', width
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        assert not errors, (width, errors)
        page.close()
    browser.close()
print('Schedule visual palette, controls, rerender, responsive layout: OK')
