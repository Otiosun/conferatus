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
        page.set_content(html)
        # The normal preview must never present a simulated choice as an official vote.
        assert page.locator('.preview-vote-lab').count() == 0, width
        note = page.locator('.ballot-preview-disclosure[role="note"]')
        assert note.is_visible(), width
        assert 'nenhum voto é enviado à Academy' in note.inner_text(), width
        before = page.evaluate("Object.keys(sessionStorage).sort()")
        page.locator('[data-action="toggle-demo"]').click()
        assert 'Votação fictícia aberta' in page.locator('.demo-ballot').inner_text(), width
        page.locator('[data-vote]').first.click()
        assert 'Nenhum voto foi enviado' in page.locator('.vote-feedback').inner_text(), width
        assert 'Escolha simulada' in page.locator('.result-row--chosen').inner_text(), width
        assert page.evaluate("Object.keys(sessionStorage).sort()") == before, width
        page.locator('[data-action="reset-vote"]').click()
        assert page.locator('.result-row--chosen').count() == 0, width
        page.locator('.footer-nav').click()
        page.locator('[data-route="calendar"]').first.click()
        action=page.locator('[data-action="open-schedule"]')
        assert action.inner_text()=='Iniciar uma Votação',width  # Megalos' prototype wording stays intact
        note=page.locator('.calendar-preview-disclosure[role="note"]')
        assert note.count()==1,width
        assert note.is_visible(),width
        assert 'não inicia uma votação real' in note.inner_text(),width
        assert action.get_attribute('aria-expanded')=='false',width
        if width in (390,740):
            page.screenshot(path=f'/mnt/data/conferatus_v0117_disclosure_{width}.png',full_page=True)
        action.click()
        assert action.get_attribute('aria-expanded')=='true',width
        assert page.locator('#schedule-deliberation-form').is_visible(),width
        assert page.locator('.calendar-preview-disclosure').is_visible(),width
        assert page.locator('#schedule-deliberation-form').get_by_text('Programar deliberação').count()==1,width
        assert 'votação real' in page.locator('.calendar-preview-disclosure').inner_text(),width
        action.click()
        assert action.get_attribute('aria-expanded')=='false',width
        assert page.locator('#schedule-deliberation-form').count()==0,width
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        page.close()
    browser.close()
print('Schedule-only disclosure and expandable form in four widths: OK')
