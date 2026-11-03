"""Cancelled schedules remain readable, never active, in the local-only calendar.

Only synthetic drafts and program entries; no institution, authentication or shared DB.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (280, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 820})
        page.set_default_timeout(6000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.evaluate('''() => {
            const records = new Map();
            Object.defineProperty(window, 'sessionStorage', { configurable: true, value: {
                getItem: key => records.get(key) ?? null,
                setItem: (key, value) => records.set(key, value),
                removeItem: key => records.delete(key)
            }});
        }''')
        page.set_content(HTML)

        def menu(route):
            page.locator('.footer-nav').click()
            page.locator(f'.menu-item[data-route="{route}"]').click()

        menu('proposals')
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Documento local para histórico')
        page.locator('#draft-body').fill('Documento fictício concluído para programações ativas e canceladas no calendário.')
        page.locator('#compose-proposal-form [value="conclude"]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        menu('calendar')

        def schedule(title, start, end):
            page.locator('[data-action="open-schedule"]').click()
            form = page.locator('#schedule-deliberation-form')
            form.locator('[name="title"]').fill(title)
            form.locator('[name="objective"]').fill('Motivação fictícia para demonstrar preservação de histórico de cancelamento.')
            form.locator('[name="proposalId"]').select_option(index=1)
            form.locator('[name="start"]').fill(start)
            form.locator('[name="end"]').fill(end)
            form.locator('button[type=submit]').click()

        schedule('Agenda ativa da sessão', '2026-12-12T09:00', '2026-12-12T11:00')
        schedule('Agenda cancelada da sessão', '2026-12-13T09:00', '2026-12-13T11:00')
        item = page.locator('.calendar-item').filter(has_text='Agenda cancelada da sessão')
        if 'calendar-item--expanded' not in (item.get_attribute('class') or ''):
            item.locator('[data-schedule]').click()
        item.locator('[data-cancel-schedule]').click()

        saved = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
        assert {x['title']: x['status'] for x in saved} == {
            'Agenda ativa da sessão': 'programada',
            'Agenda cancelada da sessão': 'cancelada'
        }, (width, 'cancelled status not saved')
        assert page.locator('.calendar-item').filter(has_text='Agenda cancelada da sessão').count() == 0, (width, 'cancelled schedule still active')
        assert page.locator('[data-action="toggle-cancelled-history"]').count() == 1, (width, 'no cancelled history disclosure')
        toggle = page.locator('[data-action="toggle-cancelled-history"]')
        assert toggle.get_attribute('aria-expanded') == 'false', width
        assert toggle.bounding_box()['height'] >= 44, (width, 'touch target')
        toggle.focus()
        page.keyboard.press('Enter')
        assert page.locator('[data-action="toggle-cancelled-history"]').get_attribute('aria-expanded') == 'true'
        history = page.locator('#cancelled-schedule-history')
        assert history.count() == 1, width
        archived = history.locator('.calendar-cancelled-record')
        assert archived.count() == 1, (width, 'wrong number of cancellations')
        assert 'Agenda cancelada da sessão' in archived.inner_text(), width
        assert 'Cancelada' in archived.inner_text(), width
        assert 'Documento local para histórico' in archived.inner_text(), (width, 'linked proposal reference missing')
        assert archived.locator('[data-cancel-schedule]').count() == 0, (width, 'archived record can be cancelled again')
        assert archived.locator('[data-schedule]').count() == 0, (width, 'archived record has active schedule control')
        assert history.locator('button, a').count() == 0, (width, 'archive should be read-only')
        assert page.locator('[data-action="toggle-cancelled-history"]:focus').count() == 1, (width, 'toggle lost keyboard focus')
        # The calendar markers reflect only ACTIVE records, even on archived dates.
        archived_day = page.locator('[data-calendar-day="2026-12-13"]')
        if archived_day.get_attribute('aria-pressed') != 'true':
            archived_day.click()
        assert page.locator('.calendar-empty-message').count() == 1, (width, 'cancelled day appears as active')
        assert 'programação' not in (page.locator('[data-calendar-day="2026-12-13"]').get_attribute('aria-label') or '').lower(), width
        # Global archive remains readable regardless of the selected day.
        assert history.locator('.calendar-cancelled-record').count() == 1, width
        if width == 390:
            page.screenshot(path=str(ROOT / 'dist/cancelled_schedule_history_390.png'), full_page=True)
        # Even after a complete application redraw/reinitialization, cancelled entries are still records.
        page.set_content(HTML)
        menu('calendar')
        assert page.locator('[data-action="toggle-cancelled-history"]').count() == 1, (width, 'archive disappeared after restore')
        page.locator('[data-action="toggle-cancelled-history"]').click()
        assert page.locator('.calendar-cancelled-record').count() == 1, (width, 'archive record lost after restore')
        assert page.locator('.calendar-item').filter(has_text='Agenda ativa da sessão').count() == 1, width
        assert page.locator('.calendar-item').filter(has_text='Agenda cancelada da sessão').count() == 0, width
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        page.close()
    browser.close()
print('Cancelled schedule history: PASS 4 widths, read-only archive, active isolation, day markers, session restoration')
