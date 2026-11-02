"""Stage 07: verify every main demo route without document-level horizontal clipping.

This is a Chromium baseline, not a claim about all browsers or WCAG compliance.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
widths=(280,320,360,390,540,740,768,1024,1440)
routes=('ballot','members','overview','calendar','proposals','profile','governance')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in widths:
        page=browser.new_page(viewport={'width':width,'height':740})
        page.set_default_timeout(6500)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('about:blank?demo=1');page.set_content(html)
        for route in routes:
            if route!='ballot':
                page.locator('.footer-nav').click()
                target="members" if route=="profile" else "overview" if route=="governance" else route
                page.locator(f'.menu-item[data-route="{target}"]').click()
                if route=='profile':page.locator('.member-item').first.click()
                if route=='governance':page.locator('.panel-button').click()
            measurements=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,
              outer:[...document.querySelectorAll('main *, footer *')].filter(el=>{
                const s=getComputedStyle(el),r=el.getBoundingClientRect();
                return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0&&r.left<innerWidth&&r.right>innerWidth+1;
              }).slice(0,4).map(el=>({tag:el.tagName,cl:String(el.className).slice(0,60)}))})''')
            assert measurements['scroll']<=measurements['width']+1,(width,route,measurements)
            assert not measurements['outer'],(width,route,measurements['outer'])
        assert not errors,(width,errors)
        page.close()
    browser.close()
print(f'Stage 07 main-route reflow: {len(widths)*len(routes)} cases in Chromium OK')
