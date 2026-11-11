"""Current, offline CONFERATUS smoke: actual UI actions, no institutional accounts.

Run after `npm run build` with `python tests/browser_smoke.py`.
This is a browser check of the static demo, not a test of Academy authentication.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')


def open_menu(page, route):
    page.locator('.footer-nav').click()
    page.locator(f'.menu-item[data-route="{route}"]').click()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        page.set_default_timeout(5500)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        # The sandbox prohibits localhost/file navigation. Demo-only tools are enabled
        # by a URL search flag, while the HTML is loaded as a real parsed document.
        page.goto('about:blank?demo=1')
        page.set_content(html)
        assert page.locator('.result-row').count() == 2, width
        assert page.get_by_text('DADOS FICTÍCIOS').count() >= 1, width

        # All six form families belong to an opt-in, non-institutional laboratory.
        modes=page.locator('#preview-vote-method')
        assert modes.locator('option').count()==6,width
        page.locator('.preview-vote-submit').click()
        assert 'Selecione exatamente uma' in page.locator('.preview-vote-error').inner_text(),width
        page.locator('[name=selected][value=sim]').check()
        page.locator('.preview-vote-submit').click()
        assert 'Escolha: Sim' in page.locator('.preview-vote-receipt').inner_text(),width
        assert 'amostras nesta aba (1)' in page.locator('.preview-vote-summary').inner_text(),width
        assert page.locator('.preview-vote-summary-row').count()==2,width
        page.locator('[data-action=reset-preview-vote]').click()
        assert page.locator('.preview-vote-summary-row').count()==2,width
        page.locator('[name=selected][value=nao]').check()
        page.locator('.preview-vote-submit').click()
        assert 'amostras nesta aba (2)' in page.locator('.preview-vote-summary').inner_text(),width
        page.once('dialog',lambda dialog: dialog.dismiss())
        page.locator('[data-action=clear-preview-samples]').click()
        assert page.locator('.preview-vote-summary').count()==1,width
        page.once('dialog',lambda dialog: dialog.accept())
        page.locator('[data-action=clear-preview-samples]').click()
        assert page.locator('.preview-vote-summary').count()==0,width

        modes.select_option('nominal')
        page.locator('[name=selected][value=b]').check()
        page.locator('.preview-vote-submit').click()
        assert 'Alternativa B' in page.locator('.preview-vote-receipt').inner_text(),width

        modes.select_option('ordenada')
        page.locator('[name=rank-0]').select_option('a')
        page.locator('[name=rank-1]').select_option('a')
        page.locator('[name=rank-2]').select_option('c')
        page.locator('.preview-vote-submit').click()
        assert 'sem repetir' in page.locator('.preview-vote-error').inner_text(),width
        page.locator('[name=rank-1]').select_option('b')
        page.locator('.preview-vote-submit').click()
        assert '3º Alternativa C' in page.locator('.preview-vote-receipt').inner_text(),width

        modes.select_option('aprovacao')
        page.locator('[name=approved][value=a]').check()
        page.locator('[name=approved][value=c]').check()
        page.locator('.preview-vote-submit').click()
        assert 'Alternativa A, Alternativa C' in page.locator('.preview-vote-receipt').inner_text(),width
        assert 'aprovações por alternativa' in page.locator('.preview-vote-summary').inner_text(),width

        modes.select_option('escalar')
        for option,value in (('a','1'),('b','7'),('c','10')):
            page.locator(f'[name=score-{option}]').select_option(value)
        page.locator('.preview-vote-submit').click()
        assert 'Alternativa C: 10/10' in page.locator('.preview-vote-receipt').inner_text(),width
        assert 'Distribuição de notas 1 a 10' in page.locator('.preview-vote-summary').inner_text(),width

        modes.select_option('cumulativa')
        assert 'Nenhum membro deliberativo fictício' in page.locator('.preview-vote-fieldset').inner_text(),width
        assert page.locator('.preview-vote-submit').is_disabled(),width

        # Only a fictional ballot is selectable; the original UI labels have changed.
        page.locator('[data-action="toggle-demo"]').click()
        page.locator('[data-vote="o2"]').click()
        assert page.locator('.result-row--chosen').count() == 1, width
        assert page.locator('.result-row--chosen .result-count').inner_text() == '21 Votos', width
        page.locator('[data-action="reset-vote"]').click()
        assert page.locator('.result-row--chosen').count() == 0, width
        page.locator('[data-action="toggle-demo"]').click()

        # Escape closes the menu and returns keyboard focus to the opener.
        page.locator('.footer-nav').click()
        assert page.locator('.bottom-menu').count() == 1, width
        page.keyboard.press('Escape')
        assert page.locator('.bottom-menu').count() == 0, width
        assert page.locator('.footer-nav').evaluate('(el) => document.activeElement === el'), width

        open_menu(page, 'members')
        page.locator('.member-item').first.wait_for()
        page.locator('[data-action="search"]').click()
        page.locator('#search-members').fill('Bruno')
        assert page.locator('.member-item').count() == 1, width
        page.locator('.member-item').click()
        page.locator('.profile-identity').get_by_text('Bruno Leal').wait_for()
        assert page.evaluate('location.hash') == '#/profile/m04', width
        page.locator('[data-tab="proposicoes"]').click()
        page.locator('.activity-proposal').first.wait_for()

        # Deep links resolve to the requested fictional member in a fresh document.
        direct = browser.new_page(viewport={'width': width, 'height': 844})
        direct.on('pageerror', lambda error: errors.append(str(error)))
        direct.goto('about:blank')
        direct.evaluate("location.hash='#/profile/m06'")
        direct.set_content(html)
        direct.locator('.profile-identity').get_by_text('Daniel Freitas').wait_for()
        direct.close()

        open_menu(page, 'overview')
        page.locator('.overview-content').wait_for()
        page.locator('[data-overview-tab="proposicoes"]').click()
        page.locator('.activity-proposal').first.wait_for()
        page.locator('.panel-button').click()
        page.locator('.governance-list').wait_for()
        page.locator('[data-action="toggle-tools"]').click()
        page.locator('#role-mode').select_option('membro')
        assert 'exclusivo da diretoria' in page.locator('main').inner_text(), width
        page.locator('#role-mode').select_option('diretor')
        page.locator('[data-action="toggle-tools"]').click()
        page.locator('[data-section="coordenacao"]').click()
        page.locator('[data-edit="m01"]').first.click()
        page.locator('#member-acdm-id').fill('DEMO-5012')
        page.locator('#edit-member-form button[type="submit"]').click()
        assert 'Dados de Helena Avelar atualizados.' in page.locator('main').inner_text(), width
        page.locator('[data-action="undo"]').click()
        assert 'Alteração desfeita' in page.locator('main').inner_text(), width

        open_menu(page, 'calendar')
        assert 'A programação ficará disponível após concluir uma proposição.' in page.locator('.calendar-preview-disclosure').inner_text(), width
        page.locator('[data-action="open-schedule"]').click()
        page.locator('#schedule-deliberation-form').wait_for()
        page.locator('[data-action="open-schedule"]').click()
        assert page.locator('#schedule-deliberation-form').count() == 0, width

        open_menu(page, 'proposals')
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-body').wait_for()
        assert page.locator('#draft-title').is_visible(), width
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), width
        assert not errors, (width, errors)
        page.close()
    browser.close()
print('BROWSER SMOKE PASSED: 4 viewports; simulated vote, menu focus, profiles, deep links, history, role preview, edit/undo, calendar and editor')
