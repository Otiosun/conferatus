"""Megalos profile layout: one member, five metrics, proposals and working routes."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        page.set_default_timeout(4000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('[data-route="proposals"]').first.click()
        profile = page.locator('.workflow-profile')
        profile.wait_for()
        assert profile.locator('.profile-head').count() == 1, width
        assert profile.locator('.profile-identity strong').inner_text() == 'Helena Avelar', width
        assert profile.locator('.metric-cell').count() == 5, width
        assert profile.locator('.profile-summary .metrics').evaluate(
            'el => getComputedStyle(el).gridTemplateColumns.split(" ").length') == 5, width
        assert profile.locator('.workflow-tabs [aria-current=page]').inner_text().casefold() == 'proposições e socii', width
        assert profile.locator('.workflow-tabs button').count() == 1, width  # No inert selected button
        rows = page.locator('.workflow-proposals-layout .activity-proposal')
        assert rows.count() == 4, width
        assert page.locator('.workflow-record-heading').inner_text().casefold() == 'histórico demonstrativo', width
        rows.first.locator('[data-activity]').click()
        rows.first.locator('.proposal-expansion').wait_for()
        assert rows.first.locator('.proposal-tag').inner_text() == 'PDR', width
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        profile.get_by_role('button', name='Consultar histórico de votação').click()
        page.locator('.profile-head').wait_for()
        assert page.evaluate('location.hash').startswith('#/profile'), width
        assert not errors, (width, errors)
        page.close()
    browser.close()
print('Profile proposal layout, real author filtering, expandable records and tabs: OK')
