from pathlib import Path
from playwright.sync_api import sync_playwright

# Optional browser regression: python tests/browser_calendar_v012.py
html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="calendar"]').click()
        page.locator('.calendar-grid').wait_for()
        for _ in range(18):
            if 'novembro de 2026' in page.locator('.calendar-month-nav h2').inner_text().lower():
                break
            page.locator('[data-action=calendar-prev]').click()
        assert 'novembro de 2026' in page.locator('.calendar-month-nav h2').inner_text().lower()
        page.locator('[data-calendar-day="2026-11-22"]').click()
        assert page.locator('.calendar-item').count() == 1
        assert page.evaluate('document.activeElement?.dataset.calendarDay') == '2026-11-22'
        page.locator('[data-calendar-day="2026-11-25"]').click()
        page.get_by_text('Nenhuma programação nesta data.').wait_for()
        page.locator('[data-action=calendar-all]').click()
        assert page.locator('.calendar-item').count() == 1
        page.locator('[data-action=open-schedule]').click()
        assert page.locator('#schedule-deliberation-form button[type=submit]').is_disabled()
        form = page.locator('#schedule-deliberation-form')
        form.locator('[name="title"]').fill('Programação em elaboração')
        form.locator('[name="objective"]').fill('Descrição ainda não enviada no protótipo.')
        form.locator('[name="start"]').fill('2026-11-26T09:00')
        form.locator('[name="end"]').fill('2026-11-26T10:00')
        page.locator('[data-calendar-day="2026-11-22"]').click()
        page.locator('[data-action="calendar-next"]').click()
        page.locator('[data-action="calendar-prev"]').click()
        assert form.locator('[name="title"]').input_value() == 'Programação em elaboração'
        assert form.locator('[name="objective"]').input_value() == 'Descrição ainda não enviada no protótipo.'
        assert form.locator('[name="start"]').input_value() == '2026-11-26T09:00'
        assert form.locator('[name="end"]').input_value() == '2026-11-26T10:00'
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        page.close()
    browser.close()
print('Calendar navigation, filtering and empty state: OK')
