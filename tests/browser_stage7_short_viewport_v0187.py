"""Short-height route, drawer and keyboard checks for offline CONFFRATUS preview.

This tests CSS viewports, not native browser zoom or a phone's virtual keyboard.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
SIZES = ((280, 256), (320, 256), (390, 256), (280, 320), (320, 360), (640, 256))
ROUTES = ('ballot', 'members', 'overview', 'governance', 'calendar', 'proposals', 'compose', 'profile/m01')
EVIDENCE = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width, height in SIZES:
        page = browser.new_page(viewport={'width': width, 'height': height}, reduced_motion='reduce')
        page.set_default_timeout(6000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)
        for route in ROUTES:
            page.evaluate('(route) => {location.hash = "#/" + route}', route)
            expect(page.locator('#main-content')).to_be_visible()
            # This measure is a necessary reflow check but not full WCAG compliance.
            data = page.evaluate("""() => ({width: innerWidth,
                scrollWidth: document.documentElement.scrollWidth,
                footerHeight: document.querySelector('.footer-nav')?.getBoundingClientRect().height,
                mainVisible: !!document.querySelector('#main-content'),
                route:location.hash})""")
            assert data['scrollWidth'] <= width + 1, (width, height, route, data)
            assert data['footerHeight'] >= 44, (width, height, route, data)
            assert data['mainVisible'] and data['route'] == '#/' + route, (width, height, route, data)
            assert not errors, (width, height, route, errors)
            EVIDENCE.append({'viewport': [width, height], 'route': route, 'scrollWidth': data['scrollWidth'], 'errors': len(errors)})
        # The drawer must remain operable with only 256 CSS px of height.
        page.locator('.footer-nav').focus()
        assert page.evaluate('document.activeElement.classList.contains("footer-nav")')
        page.keyboard.press('Enter')
        expect(page.locator('.footer-nav')).to_have_attribute('aria-expanded', 'true')
        expect(page.locator('.menu-item')).to_have_count(4)
        last = page.locator('.menu-item[data-route="proposals"]')
        last.scroll_into_view_if_needed()
        expect(last).to_be_visible()
        last.click()
        expect(page.locator('.footer-nav')).to_have_attribute('aria-expanded', 'false')
        assert page.evaluate('location.hash') == '#/proposals'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
        assert not errors, (width, height, 'menu', errors)
        if (width, height) in ((280, 256), (390, 256)):
            page.screenshot(path=str(ROOT / f'dist/short_viewport_{width}x{height}_v0187.png'), full_page=False)
        page.close()
    browser.close()

(ROOT / 'dist/short_viewport_v0187_results.json').write_text(json.dumps(EVIDENCE, indent=2), encoding='utf-8')
print(f'SHORT VIEWPORT PASS: {len(EVIDENCE)} route/viewport checks, {len(SIZES)} keyboard-operated drawer journeys, no horizontal overflow or JS errors. Physical phone, virtual keyboard and native zoom NOT tested.')
