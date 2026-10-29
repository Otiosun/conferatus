"""Executable demo smoke tests; no network and no personal records."""
from pathlib import Path
from playwright.sync_api import sync_playwright

project = Path(__file__).resolve().parents[1]
preview = project / 'dist' / 'CONFERATUS_demo_offline.html'
html = preview.read_text()
shots = project / 'docs' / 'checkpoints'

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    page = browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    page.set_default_timeout(3500)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    # Browser sandbox blocks file:// and localhost; inject the standalone HTML directly.
    page.set_content(html)
    page.wait_for_selector('.result-row')
    assert page.locator('.result-row').count() == 2
    page.screenshot(path=str(shots / 'C1-v04-01-votacao.png'), full_page=True)

    # Exercise changing and resetting the demonstration vote.
    page.get_by_role('button', name='Simular voto').click()
    page.get_by_role('button', name='Objeto 02').click()
    assert page.get_by_text('21 Votos').count() == 1
    assert page.locator('.result-row--chosen').count() == 1
    page.get_by_role('button', name='Reiniciar simulação').click()
    assert page.locator('.result-row--chosen').count() == 0
    page.get_by_role('button', name='Fechar simulação').click()

    page.get_by_role('button', name='Abrir menu').click()
    page.screenshot(path=str(shots / 'C1-v04-02-menu.png'), full_page=True)
    page.keyboard.press('Escape')
    assert page.locator('.bottom-menu').count() == 0
    assert page.get_by_role('button', name='Abrir menu').evaluate('(el) => document.activeElement === el')
    page.get_by_role('button', name='Abrir menu').click()
    page.locator('[data-route="members"]').click()
    page.wait_for_selector('.member-item')
    assert page.locator('.member-item').count() == 6
    assert page.locator('.profile-head [aria-pressed="true"]').count() == 0, 'Directory tabs should be neutral'
    page.screenshot(path=str(shots / 'C1-v04-03-membros.png'), full_page=True)

    page.get_by_role('button', name='Buscar membros').click()
    page.get_by_role('searchbox', name='Buscar membro').fill('Bruno')
    assert page.locator('.member-item').count() == 1
    page.locator('.member-item').click()
    page.wait_for_function("document.querySelector('.profile-identity')?.textContent?.includes('Bruno Leal')")
    assert page.locator('.activity').count() >= 1
    assert page.evaluate('location.hash') == '#/profile/m04'
    page.screenshot(path=str(shots / 'C1-v04-04-perfil-votos.png'), full_page=True)
    page.locator('[data-tab="proposicoes"]').click()
    assert page.locator('.activity-proposal').count() >= 1
    page.screenshot(path=str(shots / 'C1-v04-05-perfil-propostas.png'), full_page=True)

    # A direct link should resolve to a particular member, even on a fresh load.
    direct = browser.new_page(viewport={'width':390,'height':844})
    direct.on('pageerror', lambda error: errors.append(str(error)))
    direct.evaluate("location.hash='#/profile/m06'")
    direct.set_content(html)
    direct.wait_for_function("document.querySelector('.profile-identity')?.textContent?.includes('Daniel Freitas')")
    assert direct.locator('.activity').count() >= 1
    direct.close()

    page.get_by_role('button', name='Abrir menu').click()
    page.screenshot(path=str(shots / 'C1-v04-06-perfil-menu.png'), full_page=True)
    page.locator('[data-route="overview"]').click()
    page.wait_for_selector('.overview-stats')
    assert page.locator('.stat-chip').count() == 4
    page.screenshot(path=str(shots / 'C1-v04-07-historico.png'), full_page=True)
    page.locator('[data-overview-tab="proposicoes"]').click()
    assert page.locator('.activity-proposal').count() >= 7
    page.screenshot(path=str(shots / 'C1-v04-08-historico-propostas.png'), full_page=True)

    page.locator('.panel-button').click()
    page.wait_for_selector('.governance-list')
    page.screenshot(path=str(shots / 'C1-v04-09-admin.png'), full_page=True)
    page.get_by_label('Simular perfil').select_option('membro')
    assert 'Acesso negado' in page.locator('main').inner_text()
    page.get_by_label('Simular perfil').select_option('diretor')
    page.locator('[data-section="coordenacao"]').click()
    page.screenshot(path=str(shots / 'C1-v04-10-secao.png'), full_page=True)
    page.locator('[data-edit="m01"]').click()
    page.screenshot(path=str(shots / 'C1-v04-11-edicao.png'), full_page=True)
    page.get_by_label('ACDM ID (demo)').fill('DEMO-5012')
    page.get_by_role('button', name='Salvar').click()
    assert 'ACDM ID fictício de Helena Avelar atualizado' in page.locator('main').inner_text()
    page.locator('[data-demote="m01"]').click()
    assert 'os registros de atividades anteriores permanecem intactos' in page.locator('main').inner_text()
    page.get_by_role('button', name='Reiniciar').click()
    assert 'Helena Avelar' in page.locator('main').inner_text()
    assert page.locator('[data-demote="m01"]').count() == 1

    # No overflow and no JS exceptions on common mobile / desktop viewports.
    for width,height in [(320,700),(360,780),(390,844),(740,900),(1280,900)]:
        page.set_viewport_size({'width':width,'height':height})
        page.wait_for_timeout(30)
        overflow = page.evaluate('document.documentElement.scrollWidth - window.innerWidth')
        assert overflow <= 1, f'Unexpected horizontal overflow at {width}px: {overflow}'
        if width==1280:
            page.screenshot(path=str(shots / 'C1-v04-12-desktop.png'), full_page=True)
    assert errors == [], errors
    print('BROWSER SMOKE PASSED: mobile + desktop, 11 reference states, deep links, voting, access role, edit/reset; 0 JS errors')
    browser.close()
