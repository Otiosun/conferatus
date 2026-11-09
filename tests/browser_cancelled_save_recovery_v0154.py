"""Cancellation write failures must never masquerade as durable local history.

Synthetic records, deterministic sessionStorage failure; no external Academy data.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT = {'id': 'synthetic-draft', 'title': 'Proposta sintética concluída',
         'body': 'Proposta inteiramente fictícia usada para exercitar a gravação local.',
         'sectionId': 'integridade', 'type': 'PDR', 'authorComplete': True,
         'partners': [], 'status': 'concluida'}
SCHEDULE = {'id': 'synthetic-schedule', 'title': 'Agenda sintética cancelável',
            'objective': 'Testar falha transitória de gravação de cancelamentos.',
            'proposalId': 'synthetic-draft', 'sectionId': 'integridade',
            'start': '2026-12-15T09:00', 'end': '2026-12-15T11:00',
            'type': 'PDR', 'status': 'programada'}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (280, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 860})
        page.set_default_timeout(6000)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('about:blank?demo=1')
        page.evaluate('''records => {
          const items = new Map([
            ['conferatus:proposals-v010', JSON.stringify([records.draft])],
            ['conferatus:deliberations-v010', JSON.stringify([records.schedule])]
          ]);
          let fails = 1;
          Object.defineProperty(window, 'sessionStorage', {configurable: true, value: {
            getItem: k => items.get(k) ?? null,
            setItem: (k,v) => {
              if(k === 'conferatus:deliberations-v010' && fails-- > 0)
                throw new Error('Simulated quota error on schedule save');
              items.set(k,v);
            },
            removeItem: k => items.delete(k)
          }});
          window.__failNextSaves = count => { fails = count; };
        }''', {'draft': DRAFT, 'schedule': SCHEDULE})
        page.set_content(HTML)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="calendar"]').click()
        row = page.locator('.calendar-item').filter(has_text=SCHEDULE['title'])
        row.locator('[data-schedule]').click()
        row.locator('[data-cancel-schedule]').click()
        row.locator('[data-confirm-cancel-schedule]').click()
        # Must be honest about failed persistence and offer a recovery action.
        assert page.locator('.workflow-status').count() == 1, width
        assert 'não foi possível salvar' in page.locator('.workflow-status').inner_text().lower(), width
        retry = page.locator('[data-action="retry-cancellation-save"]')
        assert retry.count() == 1, (width, 'missing retry action after transient storage failure')
        assert retry.bounding_box()['height'] >= 44, width
        stored = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
        assert stored[0]['status'] == 'programada', (width, 'mock persistence did not fail as expected')
        assert page.locator('.calendar-item').filter(has_text=SCHEDULE['title']).count() == 0, width
        assert page.locator('.calendar-cancelled-record').count() == 0, width  # archive collapsed
        assert page.locator('[data-action="toggle-cancelled-history"]').count() == 1, width
        # Opening another calendar control must not hide an unresolved save failure.
        page.locator('[data-action="open-schedule"]').click()
        assert 'não foi possível salvar' in page.locator('.workflow-status').inner_text().lower(), width
        assert page.locator('[data-action="retry-cancellation-save"]').count() == 1, width
        page.locator('[data-action="open-schedule"]').click()
        # Even other workflows that reset ordinary notices must not hide an
        # unsaved cancellation when we return to the calendar.
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="proposals"]').click()
        page.locator('[data-action="new-proposal"]').click()
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="calendar"]').click()
        assert 'não foi possível salvar' in page.locator('.workflow-status').inner_text().lower(), width
        assert page.locator('[data-action="retry-cancellation-save"]').count() == 1, width
        # Repeated storage failure preserves the warning and recovery button.
        page.evaluate('window.__failNextSaves(1)')
        if width == 390:
            page.screenshot(path=str(ROOT/'dist/cancellation_save_failed_390.png'), full_page=True)
        retry.focus()
        page.keyboard.press('Enter')
        assert page.locator('[data-action="retry-cancellation-save"]').count() == 1, width
        assert 'não foi possível salvar' in page.locator('.workflow-status').inner_text().lower(), width
        assert page.locator('[data-action="retry-cancellation-save"]:focus').count() == 1, width
        assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))[0].status') == 'programada', width
        page.keyboard.press('Enter')
        stored = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
        assert stored[0]['status'] == 'cancelada', (width, 'retry failed to save cancellation')
        assert page.locator('[data-action="retry-cancellation-save"]').count() == 0, width
        assert 'salvo nesta sessão' in page.locator('.workflow-status').inner_text().lower(), width
        assert page.locator('[data-action="toggle-cancelled-history"]').count() == 1, width
        assert page.evaluate('document.activeElement !== document.body'), (width,'lost keyboard focus on disappearing retry')
        if width == 390:
            page.screenshot(path=str(ROOT/'dist/cancellation_save_recovered_390.png'), full_page=True)
        page.set_content(HTML)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="calendar"]').click()
        assert page.locator('.calendar-item').filter(has_text=SCHEDULE['title']).count() == 0, width
        page.locator('[data-action="toggle-cancelled-history"]').click()
        assert page.locator('.calendar-cancelled-record').count() == 1, width
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), width
        page.close()
    browser.close()
print('Cancellation persistence recovery: PASS 4 widths; failed save warned, retry persisted, restore remained cancelled')
