"""Linked completed proposal returns to its calendar schedule, not the proposal list."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        page.set_default_timeout(6500)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=proposals]').click()
        page.locator('[data-action=new-proposal]').click()
        page.locator('#draft-title').fill('Proposição de navegação para agenda')
        page.locator('#draft-body').fill('Documento de teste que precisa permanecer vinculado à programação da sessão local.')
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        record = page.locator('.workflow-record').filter(has_text='Proposição de navegação para agenda')
        record.locator('[data-draft]').click()
        assert page.locator('.workflow-finished [data-route=proposals]').inner_text() == 'Voltar às proposições', width
        page.locator('.workflow-finished [data-route=proposals]').click()

        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=calendar]').click()
        page.locator('[data-action=open-schedule]').click()
        form = page.locator('#schedule-deliberation-form')
        form.locator('[name=title]').fill('Programação ligada à proposição')
        form.locator('[name=objective]').fill('Revisar em sessão demonstrativa a proposição de navegação.')
        form.locator('[name=proposalId]').select_option(index=1)
        form.locator('[name=method]').select_option('nominal')
        form.locator('[name=choices]').fill('Calendário mensal\nCalendário quinzenal')
        form.locator('[name=start]').fill('2026-12-12T09:00')
        form.locator('[name=end]').fill('2026-12-12T12:00')
        form.locator('button[type=submit]').click()
        day = page.locator('[data-calendar-day="2026-12-12"]')
        assert day.get_attribute('aria-pressed') == 'true', width
        item = page.locator('.calendar-item').filter(has_text='Programação ligada à proposição')
        assert item.locator('[data-open-schedule-proposal]').is_visible(), width
        item.locator('[data-preview-schedule]').click()
        assert page.evaluate('location.hash') == '#/ballot', (width,'did not navigate to linked sandbox ballot')
        assert page.locator('#preview-vote-method').input_value() == 'nominal', width
        assert page.locator('#preview-vote-method').is_disabled(), width
        labels=page.locator('#preview-vote-form [name=selected]').evaluate_all('(nodes)=>nodes.map(node=>node.parentElement.innerText.trim())')
        assert labels==['Calendário mensal','Calendário quinzenal'], (width,labels)
        page.locator('#preview-vote-form [name=selected][value=opt-2]').check()
        page.locator('.preview-vote-submit').click()
        assert 'Calendário quinzenal' in page.locator('.preview-vote-receipt').inner_text(), width
        assert 'amostras nesta aba (1)' in page.locator('.preview-vote-summary').inner_text(),width
        assert page.locator('.result-row--chosen').count()==0, (width,'sample altered legacy voting results')
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=calendar]').click()
        page.locator('.calendar-list').wait_for(state='visible')
        item=page.locator('.calendar-item').filter(has_text='Programação ligada à proposição')
        if not item.locator('[data-open-schedule-proposal]').is_visible(): item.locator('[data-schedule]').click()
        item.locator('[data-open-schedule-proposal]').click()
        assert page.locator('.workflow-finished strong').inner_text() == 'Proposição concluída', width
        back = page.locator('.workflow-finished [data-route=calendar]')
        assert back.inner_text() == 'Voltar à programação', (width, 'contextual return missing')
        back.click()
        assert page.evaluate('location.hash') == '#/calendar', width
        assert page.locator('[data-calendar-day="2026-12-12"]').get_attribute('aria-pressed') == 'true', width
        assert page.locator('.calendar-item--expanded').filter(has_text='Programação ligada à proposição').count() == 1, width
        page.locator('.calendar-item--expanded').filter(has_text='Programação ligada à proposição').locator('[data-cancel-schedule]').click()
        assert page.locator('.calendar-item').filter(has_text='Programação ligada à proposição').count()==0,width
        page.locator('.footer-home').click()
        assert page.locator('.preview-vote-summary').count()==0,(width,'cancelled schedule leaked a sample into the fixture ballot')
        assert page.locator('#preview-vote-method').is_enabled(),width
        assert page.locator('.preview-vote-context').count()==0,width
        if width in (390, 740):
            page.screenshot(path=f'/mnt/data/conferatus_v0120_calendar_return_{width}.png', full_page=True)
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), width
        page.close()
    browser.close()
print('Context-aware return from linked proposal to schedule in 4 widths: OK')
