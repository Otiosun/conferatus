"""Browser regression: unfinished draft can be saved and separate compositions do not overwrite it."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = (Path(__file__).resolve().parents[1] / 'dist' / 'CONFERATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in [320, 390, 740, 1280]:
        page = browser.new_page(viewport={'width': width, 'height': 800})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.set_content(HTML)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="proposals"]').click()
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Primeiro documento')
        page.locator('#draft-body').fill('Texto provisório.')
        page.get_by_role('button', name='Salvar rascunho').click()
        page.locator('.workflow-status').filter(has_text='Rascunho mantido somente enquanto a página estiver aberta.').wait_for()
        page.locator('[data-action="new-proposal"]').click()
        assert page.locator('#draft-title').input_value() == ''
        assert page.locator('#draft-body').input_value() == ''
        page.locator('#draft-title').fill('Segundo documento')
        page.locator('#draft-body').fill('Texto finalizado do segundo documento com conteúdo suficiente para revisão.')
        page.get_by_role('button', name='Concluir redação').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        page.locator('.workflow-status').filter(has_text='Proposição concluída.').wait_for()
        first = page.locator('.workflow-record').filter(has_text='Primeiro documento')
        second = page.locator('.workflow-record').filter(has_text='Segundo documento')
        assert first.count() == 1 and second.count() == 1
        first.locator('[data-draft]').click()
        assert page.locator('#draft-title').input_value() == 'Primeiro documento'
        assert page.locator('#draft-body').input_value() == 'Texto provisório.'
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), width
        page.close()
    browser.close()

print('Rascunhos independentes: OK (320, 390, 740, 1280 px)')
