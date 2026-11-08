"""A scheduling-only preview must never imply that clicking launches a real vote."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':844})
        page.set_default_timeout(5000)
        errors=[]
        page.on('pageerror',lambda error: errors.append(str(error)))
        # The initial about:blank document has an opaque origin in Chromium.
        # Provide an isolated sessionStorage spy rather than reading inaccessible storage.
        page.evaluate("""() => {
          const writes = [];
          Object.defineProperty(window, 'sessionStorage', {configurable: true, value: {
            getItem: () => null,
            setItem: key => writes.push(key),
            removeItem: () => {}
          }});
          window.__previewStorageWrites = writes;
        }""")
        page.set_content(html)
        # The normal preview must never present a simulated choice as an official vote.
        assert page.locator('.preview-vote-lab').count() == 0, width
        # A single permanent disclosure is clearer than two adjacent labels.
        assert page.locator('.ballot-preview-disclosure').count() == 0, width
        footer = page.locator('.footer-demo')
        assert footer.is_visible(), width
        assert 'DADOS FICTÍCIOS' in footer.inner_text().upper(), width
        before = page.evaluate("window.__previewStorageWrites.length")
        page.locator('[data-action="toggle-demo"]').click()
        assert 'Selecione uma opção para testar a votação.' in page.locator('.demo-ballot').inner_text(), width
        page.locator('[data-vote]').first.click()
        assert 'Opção selecionada' in page.locator('.vote-feedback').inner_text(), width
        assert 'Sua escolha' in page.locator('.result-row--chosen').inner_text(), width
        writes = page.evaluate("window.__previewStorageWrites.slice()")
        assert writes[before:] == ["conferatus:demo-vote"], (width, "vote should only write the local demo key", writes)
        page.locator('[data-action="reset-vote"]').click()
        assert page.locator('.result-row--chosen').count() == 0, width
        page.locator('.footer-nav').click()
        page.locator('[data-route="overview"]').first.click()
        page.locator('[data-route="governance"]').first.click()
        warning=page.locator('.governance-preview-disclosure[role="note"]')
        warning.wait_for(state="visible",timeout=5000)
        assert warning.is_visible(),width
        assert warning.inner_text().strip() == 'Alterações nesta página não afetam cadastros oficiais.',width
        assert page.locator('[data-action="toggle-tools"]').count()==0,width
        page.locator('.footer-nav').click()
        page.locator('[data-route="calendar"]').first.click()
        # The fixed sample predates per-deliberation methods: do not present
        # its missing field as a real legacy record or invent a voting mode.
        sample = page.locator('[data-schedule="sample-1"]')
        if sample.get_attribute('aria-expanded') != 'true':
            sample.click()
        sample_details = page.locator('#schedule-details-sample-1').inner_text()
        assert 'Modalidade:' not in sample_details, (width, sample_details)
        assert 'Não informada (registro anterior)' not in sample_details, width
        action=page.locator('[data-action="open-schedule"]')
        assert action.inner_text()=='Iniciar uma Votação',width  # Megalos' prototype wording stays intact
        note=page.locator('.calendar-preview-disclosure[role="note"]')
        assert note.count()==1,width
        assert note.is_visible(),width
        assert note.inner_text().strip() == 'Defina a data e a modalidade da deliberação.',width
        assert action.get_attribute('aria-expanded')=='false',width
        if width in (390,740):
            page.screenshot(path=f'/mnt/data/conferatus_v0117_disclosure_{width}.png',full_page=True)
        action.click()
        assert action.get_attribute('aria-expanded')=='true',width
        assert page.locator('#schedule-deliberation-form').is_visible(),width
        assert page.locator('.calendar-preview-disclosure').is_visible(),width
        assert page.locator('#schedule-deliberation-form').get_by_text('Programar deliberação').count()==1,width
        assert 'data e a modalidade' in page.locator('.calendar-preview-disclosure').inner_text(),width
        action.click()
        assert action.get_attribute('aria-expanded')=='false',width
        assert page.locator('#schedule-deliberation-form').count()==0,width
        # The normal view must not expose advanced testing tools or local
        # archive operations; retain useful Socii controls and the disclaimer.
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="proposals"]').click()
        # Hash navigation renders asynchronously. First wait for the target
        # screen so absence checks cannot pass on the previous calendar view.
        page.wait_for_function('location.hash==="#/proposals" && document.querySelector("[data-action=invite-socii]")!==null')
        assert page.locator('.local-archive-actions').count()==0,width
        assert page.locator('[data-action="export-local-archive"],[data-action="import-local-archive"]').count()==0,width
        assert page.locator('[data-action="toggle-tools"],.preview-vote-lab').count()==0,width
        assert page.locator('[data-action="invite-socii"]').is_visible(),width
        page.locator('[data-action="invite-socii"]').click()
        assert 'primeiro redija e salve uma proposição' in page.locator('#invite-socii-form').inner_text(),width
        assert page.locator('#invite-socii-form button.workflow-primary').is_disabled(),width
        assert 'DADOS FICTÍCIOS' in page.locator('.footer-demo').inner_text().upper(),width
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        page.close()
    browser.close()
print('Normal-mode preview controls and disclosures: 4 widths OK; no advanced voting, debug or archive operations')
