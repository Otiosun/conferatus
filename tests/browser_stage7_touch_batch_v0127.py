"""Stage 07.03 (first batch): test actual click/touch rectangles and navigation.

Checks the member profile link, footer home, demonstration-vote toggle,
plus desktop directory search. This is a focused batch, not a full audit.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = (Path(__file__).resolve().parents[1] / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 360, 390, 540, 740, 768, 1024, 1440)

def bounds(locator, width, label):
    rect = locator.bounding_box()
    assert rect, (width, label, 'missing rectangle')
    assert rect['height'] >= 44, (width, label, 'height under 44px', round(rect['height'], 2))
    assert rect['width'] >= 44, (width, label, 'width under 44px', round(rect['width'], 2))
    return rect

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width': width, 'height': 740}, has_touch=True, is_mobile=True)
        page.set_default_timeout(6500)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)

        toggle = page.locator('.demo-toggle')
        bounds(toggle, width, 'demo-toggle')
        toggle.tap()
        page.locator('.demo-ballot').wait_for(state='visible')
        toggle.tap()
        assert not page.locator('.demo-ballot').count(), (width, 'demo toggle did not close')

        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="members"]').click()
        page.locator('.profile-name-button').wait_for(state='visible')
        profile_button = page.locator('.profile-name-button')
        bounds(profile_button, width, 'member profile')

        search = page.locator('.search-trigger')
        sr = bounds(search, width, 'directory search')
        first = page.locator('.member-item').first.bounding_box()
        assert first and sr['y'] + sr['height'] <= first['y'] + 1, (width, 'search overlaps row')
        search.tap()
        page.locator('#search-members').fill('Bruno')
        assert page.locator('.member-item').count() == 1, (width, 'search filter')
        page.locator('#search-members').fill('')
        assert page.locator('.member-item').count() > 1, (width, 'search reset')

        profile_button.tap()
        page.wait_for_url('**#/profile/*')
        page.locator('.profile-identity strong').first.wait_for(state='visible')
        home = page.locator('.footer-home')
        hr = bounds(home, width, 'footer home')
        menu = page.locator('.footer-nav').bounding_box()
        assert menu and hr['x'] + hr['width'] <= menu['x'] + 1, (width, 'footer controls collide')
        home.tap()
        page.wait_for_url('**#/ballot')
        page.locator('.demo-toggle').wait_for(state='visible')

        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), (width, 'overflow')
        assert not errors, (width, errors)
        if width in (320, 390, 740):
            page.screenshot(path=f'/mnt/data/conffratus_source/after_ballot_{width}.png', full_page=True)
        page.close()
    browser.close()
print(f'Stage 07.03 batch: {len(WIDTHS)} widths; four controls, interactions and overlap OK')
