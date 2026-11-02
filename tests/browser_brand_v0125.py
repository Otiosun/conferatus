"""Canonical visible brand is CONFFRATUS; legacy file and storage remain compatible."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
canonical=(root/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
legacy=(root/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
assert legacy==canonical,'legacy offline file is not synchronized with canonical brand'
assert '<title>CONFFRATUS</title>' in canonical

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':844})
        page.set_default_timeout(8000)
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(canonical)
        assert page.title()=='CONFFRATUS',width
        assert page.locator('.footer-home').inner_text()=='CONFFRATUS',width
        assert 'CONFFRATUS' in page.locator('.app-shell').get_attribute('aria-label'),width
        assert page.locator('.footer-demo').inner_text()=='DADOS FICTÍCIOS · PRÉVIA',width
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=proposals]').click()
        page.locator('[data-action=new-proposal]').click()
        assert page.locator('.workflow-editor-head span').inner_text()=='CONFFRATUS',width
        if width in (390,740):
            page.screenshot(path=f'/mnt/data/conffratus_v0125_brand_{width}.png',full_page=True)
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),width
        page.close()
    browser.close()
print('Canonical UI + legacy offline alias: OK in four widths')
