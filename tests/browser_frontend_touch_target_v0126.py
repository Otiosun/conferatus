"""Stage 07: Search must have a usable touch target without covering directory rows."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (280,320,360,390,540):
        page=browser.new_page(viewport={'width':width,'height':740},has_touch=True,is_mobile=True)
        page.set_default_timeout(6500)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('about:blank?demo=1');page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=members]').click()
        trigger=page.locator('.search-trigger')
        rect=trigger.bounding_box()
        first=page.locator('.member-item').first.bounding_box()
        assert rect and first, width
        assert rect['height']>=44,(width,'Touch target too short',rect['height'])
        assert rect['y']+rect['height']<=first['y']+1,(width,'Touch target covers first member',rect,first)
        trigger.tap()
        field=page.locator('#search-members')
        field.wait_for(state='visible')
        field.fill('Bruno')
        assert page.locator('.member-item').count()==1,width
        field.fill('')
        assert page.locator('.member-item').count()>1,width
        if width in (320,390):
            page.screenshot(path=f'/mnt/data/conffratus_stage7_search_{width}.png',full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        assert not errors,(width,errors)
        page.close()
    browser.close()
print('Stage 07 touch target, directory row safety, and search at five widths: OK')
