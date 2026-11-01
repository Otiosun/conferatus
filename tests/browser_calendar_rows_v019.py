from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('[data-route="calendar"]').first.click()
        row = page.locator('.calendar-item').first
        title = row.locator('button[data-schedule] strong')
        assert title.text_content() == 'Revisão do calendário de reuniões'
        assert title.evaluate('el => getComputedStyle(el).textTransform') == 'uppercase'
        assert row.locator('.calendar-status-type').inner_text() == 'PDR'
        assert row.locator('.calendar-status strong').inner_text() == 'PROPOSIÇÃO EM DELIBERAÇÃO'
        assert row.locator('.calendar-socii').count() == 0  # No invented participant data
        assert row.get_attribute('class').endswith('calendar-item--expanded')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        row.locator('[data-schedule]').click()
        assert page.locator('.calendar-expanded').count() == 0
        row.locator('[data-schedule]').click()
        assert page.locator('.calendar-expanded').count() == 1
        assert page.evaluate('document.activeElement?.dataset.schedule') == 'sample-1', width
        if width in (390, 740):
            page.locator('.calendar-list').screenshot(path=str(Path(__file__).resolve().parents[2] / f'conferatus_v019_programacoes_{width}.png'))

        # Link a real local-demo Socii participant to a newly scheduled proposal.
        page.locator('.footer-nav').click()
        page.locator('[data-route="proposals"]').first.click()
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Plano colaborativo do conselho')
        page.locator('#draft-body').fill('Proposta redigida de maneira colaborativa para teste visual de participantes do Socii.')
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('.footer-nav').click()
        page.locator('[data-route="proposals"]').first.click()
        page.locator('[data-action="invite-socii"]').click()
        name = page.locator('[name=memberId] option').nth(1).inner_text()
        page.locator('[name=memberId]').select_option(index=1)
        page.locator('#invite-socii-form button.workflow-primary').click()
        page.locator('[data-draft]').first.click()
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        page.locator('[data-confirm-partner]').click()
        page.locator('.footer-nav').click()
        page.locator('[data-route="calendar"]').first.click()
        page.locator('[data-action="open-schedule"]').click()
        page.locator('[name=title]').fill('Reunião do plano colaborativo')
        page.locator('[name=objective]').fill('Debate do plano colaborativo com participantes cadastrados nesta sessão.')
        page.locator('[name=proposalId]').select_option(index=1)
        page.locator('[name=start]').fill('2026-12-12T09:00')
        page.locator('[name=end]').fill('2026-12-12T12:00')
        page.locator('#schedule-deliberation-form button[type=submit]').click()
        scheduled = page.locator('.calendar-item').filter(has_text='Reunião do plano colaborativo')
        assert scheduled.count() == 1, width
        assert scheduled.locator('.calendar-socii').inner_text() == f'Socii: {name}', width
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        page.close()
    browser.close()
print('Calendar row visual parity, focus, known Socii only and scheduling: OK')
