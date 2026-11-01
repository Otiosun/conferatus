from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (390, 740):
        page = browser.new_page(viewport={'width': width, 'height': 844}, timezone_id='UTC')
        page.clock.install(time=datetime(2026, 11, 1, 23, 55, tzinfo=timezone.utc))
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('[data-route="calendar"]').first.click()
        page.clock.fast_forward('10:00')
        page.locator('[data-action="calendar-today"]').click()
        selected = page.locator('[data-calendar-day][aria-pressed="true"]').get_attribute('data-calendar-day')
        assert selected == '2026-11-02', (width, selected)
        assert page.locator('.calendar-month-nav h2').inner_text().lower() == 'novembro de 2026'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        page.close()
    browser.close()
print('Today switches to actual local date after midnight: OK')
