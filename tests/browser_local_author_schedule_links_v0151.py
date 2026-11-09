"""Bidirectional local-only author/proposal/schedule navigation.

Only synthetic current-session data; never assumes real Academy identity or permissions.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (280, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 850})
        page.set_default_timeout(6000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(HTML)
        def menu(route):
            page.locator('.footer-nav').click()
            page.locator(f'.menu-item[data-route="{route}"]').click()

        menu('proposals')
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Proposição do vínculo local')
        page.locator('#draft-body').fill('A redação de demonstração deve permanecer vinculada ao perfil e à programação locais.')
        page.locator('#compose-proposal-form [value="conclude"]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()

        menu('calendar')
        page.locator('[data-action="open-schedule"]').click()
        form = page.locator('#schedule-deliberation-form')
        form.locator('[name="title"]').fill('Programação do vínculo local')
        form.locator('[name="objective"]').fill('Vincular proposta e calendário sem criar atividade institucional.')
        form.locator('[name="proposalId"]').select_option(index=1)
        form.locator('[name="method"]').select_option('binaria')
        form.locator('[name="start"]').fill('2026-12-12T09:00')
        form.locator('[name="end"]').fill('2026-12-12T12:00')
        form.locator('button[type=submit]').click()
        page.locator('.calendar-item--expanded').filter(has_text='Programação do vínculo local').wait_for()
        # From the schedule, open the DEMO author's local proposals profile.
        page.locator('[data-open-proposal-author]').click()
        assert page.evaluate('location.hash').startswith('#/profile/'), width
        page.locator('.session-proposals-heading').first.wait_for()
        assert page.locator('.session-proposal-link').filter(has_text='Proposição do vínculo local').count() == 1, width
        link = page.locator('.session-schedule-link').filter(has_text='Programação do vínculo local')
        assert link.count() == 1, (width, 'profile lacks linked scheduled deliberation')
        assert link.bounding_box()['height'] >= 44, (width, 'touch target too short')
        if width == 390:
            page.screenshot(path=str(ROOT/'dist/local_author_schedule_profile_390.png'), full_page=True)
        link.click()
        assert page.evaluate('location.hash') == '#/calendar', width
        assert page.locator('[data-calendar-day="2026-12-12"]').get_attribute('aria-pressed') == 'true', width
        item = page.locator('.calendar-item--expanded').filter(has_text='Programação do vínculo local')
        assert item.count() == 1, (width, 'linked calendar item did not expand')
        if width == 390:
            page.screenshot(path=str(ROOT/'dist/local_author_schedule_calendar_390.png'), full_page=True)
        # Link to proposal remains usable after jumping from author profile.
        item.locator('[data-open-schedule-proposal]').click()
        page.locator('.workflow-finished').wait_for()
        assert page.locator('.session-schedule-link').filter(has_text='Programação do vínculo local').count() == 1, (width, 'finished document missing return link')
        page.locator('.session-schedule-link').click()
        page.locator('.calendar-item--expanded').filter(has_text='Programação do vínculo local').wait_for()

        # Cancellation is respected by the profile and no longer offers the cancelled schedule.
        page.locator('.calendar-item--expanded [data-cancel-schedule]').click()
        page.locator('.calendar-item--expanded [data-confirm-cancel-schedule]').click()
        menu('members')
        page.locator('.profile-name-button').click()
        page.locator('[data-tab="proposicoes"]').click()
        assert page.locator('.session-schedule-link').count() == 0, (width, 'cancelled schedule still advertised as active')
        # Other synthetic people never inherit the first demo author's documents.
        menu('members')
        page.locator('.member-item[data-member]').first.click()
        if page.locator('[data-tab="proposicoes"]').count():
            page.locator('[data-tab="proposicoes"]').click()
        assert page.locator('.session-proposal-link').count() == 0, (width, 'another member attributed the draft')
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        page.close()
    browser.close()
print('Local author / proposal / schedule navigation: PASS 4 widths, active/cancelled and owner isolation')
