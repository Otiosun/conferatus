"""Prototype-only check: demotion preserves fictional personal voting history.

No account data, institutional permissions or official audit records are used.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML = (Path(__file__).resolve().parents[1] / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox']
    )
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 850})
        page.set_default_timeout(6000)
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto('about:blank')
        page.set_content(HTML)
        page.evaluate("location.hash = '#/profile/m01'")
        expect(page.locator('.profile-identity')).to_contain_text('Helena Avelar')
        expect(page.locator('[data-tab=votos]')).to_be_visible()
        assert page.locator('.activity-vote').count() > 0, width
        before = page.locator('.activity-vote').count()
        before_metric = page.locator('.metric-cell').first.inner_text()
        # The governance screen is reached via the panel shortcut, not footer menu.
        page.evaluate("location.hash = '#/governance'")
        page.locator('[data-section=coordenacao]').click()
        page.locator('[data-demote=m01]').click()
        expect(page.locator('main')).to_contain_text('O histórico foi preservado')
        page.evaluate("location.hash = '#/profile/m01'")
        expect(page.locator('.profile-identity')).to_contain_text('Membro da Academy')
        expect(page.locator('[data-tab=votos]')).to_be_visible()
        assert page.locator('.activity-vote').count() == before, width
        assert page.locator('.metric-cell').first.inner_text() == before_metric, width
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        assert not errors, (width, errors)
        print('PASS preserved fictional history after demotion:', width, 'px')
        page.close()
    browser.close()
