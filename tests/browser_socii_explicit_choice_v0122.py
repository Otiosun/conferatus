"""Opening Socii invitation must not silently select its first candidate."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page = browser.new_page(viewport={'width':width,'height':844})
        page.set_default_timeout(5000)
        errors=[]
        page.on('pageerror', lambda err:errors.append(str(err)))
        page.goto('about:blank?demo=1')
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=proposals]').click()
        page.locator('[data-action=new-proposal]').click()
        page.locator('#draft-title').fill(f'Socii escolha consciente {width}')
        page.locator('#draft-body').fill('Texto demonstrativo construído para verificar o consentimento explícito de seleção no formulário local de Socii.')
        page.locator('#compose-proposal-form [value=save]').click()
        page.locator('[data-action=invite-socii]').click()
        select=page.locator('#invite-socii-form [name=memberId]')
        assert select.input_value()=='',f'{width}: first participant was selected without user interaction'
        assert select.evaluate('(el)=>el.required && !el.checkValidity()'),width
        page.locator('#invite-socii-form button.workflow-primary').click()
        assert page.locator('#invite-socii-form').count()==1,width
        assert page.locator('.workflow-record .workflow-partners').count()==0,width
        candidates=select.locator('option').evaluate_all('(nodes)=>nodes.filter(o=>o.value).map(o=>o.value)')
        assert candidates,(width,'No demo members')
        select.select_option(candidates[0])
        assert select.evaluate('(el)=>el.checkValidity()'),width
        page.locator('#invite-socii-form button.workflow-primary').click()
        assert page.locator('.workflow-record .workflow-partners').count()==1,width
        assert 'concluíram 0 de 2' in page.locator('.workflow-record').inner_text().casefold(),(width,page.locator('.workflow-record').inner_text())
        if width in (390,740):
            page.locator('[data-action=invite-socii]').click()
            page.screenshot(path=f'/mnt/data/conferatus_v0122_socii_choice_{width}.png',full_page=True)
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        page.close()
    browser.close()
print('Socii explicit candidate choice and no accidental invite: four viewports OK')
