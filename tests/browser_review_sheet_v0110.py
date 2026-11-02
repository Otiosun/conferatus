from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('[data-route="proposals"]').first.click()
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Regulamento de colaboração')
        draft_text = 'Texto técnico de revisão da proposta. ' * 20
        page.locator('#draft-body').fill(draft_text)
        page.locator('[value="conclude"]').click()
        sheet = page.locator('#confirm-proposal-form')
        sheet.wait_for()
        assert sheet.locator('.workflow-review-sheet').is_visible(), width
        assert sheet.locator('.workflow-review-crest').count() == 1, width
        assert sheet.locator('[name="sectionId"]').count() == 1, width
        assert sheet.locator('[name="type"]').count() == 1, width
        assert sheet.locator('button[type="submit"]').inner_text() == 'Confirmar', width
        assert sheet.locator('.workflow-review-buttons button').count() == 2, width
        assert sheet.locator('.workflow-review-buttons').evaluate(
            'el => getComputedStyle(el).gridTemplateColumns.split(" ").length') == 2, width
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
        sheet.get_by_role('button', name='Cancelar confirmação e voltar à redação').click()
        page.locator('#draft-body').wait_for()
        assert page.locator('#draft-body').input_value() == draft_text.strip(), width
        page.locator('[value="conclude"]').click()
        page.locator('#confirm-proposal-form').wait_for()
        page.locator('#confirm-proposal-form button[type="submit"]').click()
        page.locator('.workflow-status').filter(has_text='Proposição concluída.').wait_for()
        assert not errors, (width, errors)
        page.close()
    browser.close()
print('Review sheet: confirm, cancel-to-editor, responsive layout and draft preserved: OK')
