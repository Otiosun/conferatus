"""Local workflow IDs must remain unique even when the clock does not advance.

This prevents one draft or schedule from silently replacing another in a session.
The fixtures are synthetic. No Academy identity, vote or server is involved.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (280, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 850})
        page.set_default_timeout(6500)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        # Explicit in-memory session storage lets us inspect persistence deterministically.
        page.evaluate('''() => {
          const records = new Map();
          Object.defineProperty(window, 'sessionStorage', {configurable: true, value: {
            getItem: key => records.get(key) ?? null,
            setItem: (key, value) => records.set(key, value),
            removeItem: key => records.delete(key)
          }});
          Date.now = () => 1765000000000;
        }''')
        page.set_content(HTML)
        def menu(route):
            page.locator('.footer-nav').click()
            page.locator(f'.menu-item[data-route="{route}"]').click()
        def draft(title, conclude):
            menu('proposals')
            page.locator('[data-action="new-proposal"]').click()
            page.locator('#draft-title').fill(title)
            page.locator('#draft-body').fill(f'Texto de teste local relacionado à {title}; sem dados de qualquer instituição real.')
            if conclude:
                page.locator('#compose-proposal-form [value="conclude"]').click()
                page.locator('#confirm-proposal-form button[type=submit]').click()
            else:
                page.locator('#compose-proposal-form [value="save"]').click()
        draft('Primeiro rascunho no mesmo milissegundo', False)
        draft('Segundo rascunho no mesmo milissegundo', False)
        drafts = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
        assert len(drafts) == 2, (width, 'draft records lost', drafts)
        assert len({item['id'] for item in drafts}) == 2, (width, 'duplicate draft ID', drafts)
        draft('Proposição aprovada para duas programações', True)
        menu('calendar')
        def schedule(title, start):
            page.locator('[data-action="open-schedule"]').click()
            form = page.locator('#schedule-deliberation-form')
            form.locator('[name="title"]').fill(title)
            form.locator('[name="objective"]').fill('Programação demonstrativa com vínculo local íntegro e histórico preservado.')
            form.locator('[name="proposalId"]').select_option(index=1)
            form.locator('[name="method"]').select_option('aprovacao')
            form.locator('[name=choices]').fill('Primeira alternativa\nSegunda alternativa')
            form.locator('[name="start"]').fill(start)
            form.locator('[name="end"]').fill(start[:11] + '14:00')
            form.locator('button[type=submit]').click()
        schedule('Primeira programação sob mesmo relógio', '2026-12-12T09:00')
        schedule('Segunda programação sob mesmo relógio', '2026-12-13T09:00')
        items = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
        assert len(items) == 2, (width, 'schedule records lost', items)
        assert len({item['id'] for item in items}) == 2, (width, 'duplicate schedule ID', items)
        # Actions resolve only their own schedule; the remaining record keeps its link.
        target = page.locator('.calendar-item').filter(has_text='Segunda programação sob mesmo relógio')
        if 'calendar-item--expanded' not in (target.get_attribute('class') or ''):
            target.locator('[data-schedule]').click()
        target.locator('[data-cancel-schedule]').click()
        updated = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
        assert {item['title']: item['status'] for item in updated} == {
            'Primeira programação sob mesmo relógio': 'programada',
            'Segunda programação sob mesmo relógio': 'cancelada',
        }, (width, 'cancellation affected the wrong historical record', updated)
        menu('proposals')
        page.locator('.workflow-record').filter(has_text='Primeiro rascunho no mesmo milissegundo').wait_for()
        assert page.locator('.workflow-record').filter(has_text='Primeiro rascunho no mesmo milissegundo').count() == 1
        assert page.locator('.workflow-record').filter(has_text='Segundo rascunho no mesmo milissegundo').count() == 1
        assert page.locator('.session-schedule-link').count() == 1, (width, 'cancelled schedule link shown as active')
        if width == 390:
            page.screenshot(path=str(ROOT/'dist/workflow_unique_id_390.png'), full_page=True)
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), width
        page.close()
    browser.close()
print('Workflow IDs: PASS four widths, frozen clock, independent drafts, schedules and cancellation')
