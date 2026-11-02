"""Stage 07.08 desktop: real navigation, intentional 740px column and pointer feedback.

Chromium offline only; simulates CSS desktop viewports, not a desktop-screen reader.
Never infers Megalos approval from passing tests.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
SIZES = ((1280,720),(1366,768),(1440,900),(1600,900),(1920,1080),(1920,720),(2560,1440))
ROUTES = ('ballot','members','overview','governance','calendar','proposals','compose','profile')
records=[]; journeys=[]; hovers=[]; issues=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width,height in SIZES:
        page=browser.new_page(viewport={'width':width,'height':height})
        page.set_default_timeout(7500)
        errors=[]
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto('about:blank?demo=1');page.set_content(HTML)
        for route in ROUTES:
            if route=='profile':
                page.evaluate('location.hash="#/members"');page.locator('.member-item').first.click()
            elif route=='compose':
                page.evaluate('location.hash="#/proposals"');page.locator('[data-action="new-proposal"]').click()
            else:
                page.evaluate('(r)=>location.hash="#/"+r',route)
                if route=='governance':page.locator('.panel-button').click()
            m=page.evaluate('''()=>{
              const box=s=>{const el=document.querySelector(s);if(!el)return null;const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}};
              const shell=box('.app-shell'),foot=box('.app-footer'),logo=box('.app-footer > img'),menu=box('.footer-nav'),home=box('.footer-home');
              const intersection=(a,b)=>Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y));
              const bodyOverflow=document.documentElement.scrollWidth-innerWidth;
              const childOverflows=[...document.querySelectorAll('main *,footer *')].filter(el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0&&(r.right>shell.x+shell.w+1||r.left<shell.x-1)}).slice(0,5).map(el=>String(el.className));
              return {viewport:[innerWidth,innerHeight],shell,foot,logo,menu,home,bodyOverflow,childOverflows,
                centerError:shell.x+shell.w/2-innerWidth/2,logoLoaded:document.querySelector('.app-footer>img').naturalWidth>0,
                logoHomeCollision:intersection(logo,home),menuHomeCollision:intersection(menu,home)};
            }''')
            records.append({'route':route,**m})
            if m['bodyOverflow']>1 or m['childOverflows'] or abs(m['centerError'])>1 or not 739<=m['shell']['w']<=741 or not m['logoLoaded'] or m['logoHomeCollision']>1 or m['menuHomeCollision']>1:
                issues.append((width,height,route,m))
            if width in (1280,1920) and route in ('ballot','members','overview','calendar','compose') and height!=720 or width==1280 and route in ('ballot','overview'):
                page.screenshot(path=str(ROOT/'dist'/f'desktop_v0138_{route}_{width}.png'),full_page=False)
        # Functional pointer/keyboard smoke: menu, search, change tab, calendar, draft.
        page.locator('.footer-nav').click()
        assert page.locator('.menu-item[data-route="members"]').count()==1
        page.locator('.menu-item[data-route="members"]').click()
        page.locator('.search-trigger').click()
        page.locator('#search-members').fill('bruno')
        assert page.locator('.member-item').count()==1,(width,'search result')
        page.locator('[data-action="clear-search"]').click()
        assert page.locator('.member-item').count()>1,(width,'search reset')
        page.evaluate('location.hash="#/overview"')
        active=page.locator('.overview-tabs .tab:not([aria-pressed="true"])').first
        before=active.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        active.hover();page.wait_for_timeout(220)
        after=active.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        hovers.append((width,'overview-tab',before,after))
        if (width,height)==(1920,1080):
            page.screenshot(path=str(ROOT/'dist'/'desktop_v0138_overview_hover_1920.png'),full_page=False)
        assert after!=before,(width,'overview tab has no pointer feedback')
        tab_id=active.get_attribute('data-overview-tab')
        active.click()
        selected=page.locator(f'[data-overview-tab="{tab_id}"]')
        assert selected.get_attribute('aria-pressed')=='true',(width,'tab failed')
        selected_before=selected.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        selected.hover();page.wait_for_timeout(220)
        assert selected.evaluate('(e)=>getComputedStyle(e).backgroundColor')==selected_before,(width,'selected state changed on hover')
        page.evaluate('location.hash="#/members"')
        member_tab=page.locator('.profile-head .tabs .tab:not([aria-pressed="true"])').first
        before=member_tab.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        member_tab.hover();page.wait_for_timeout(220)
        after=member_tab.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        hovers.append((width,'member-tab',before,after))
        assert after!=before,(width,'member tab has no pointer feedback')
        page.evaluate('location.hash="#/calendar"')
        month=page.locator('.calendar-month-nav h2').inner_text()
        nxt=page.locator('[data-action="calendar-next"]')
        before=nxt.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        nxt.hover();page.wait_for_timeout(220)
        after=nxt.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        hovers.append((width,'calendar-next',before,after))
        assert after!=before,(width,'month navigation has no pointer feedback')
        nxt.click()
        assert month!=page.locator('.calendar-month-nav h2').inner_text(),(width,'next month')
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Teste desktop — prévia')
        page.locator('#draft-body').fill('Conteúdo fictício para verificar campos e foco.')
        assert page.locator('#draft-title').input_value()=='Teste desktop — prévia'
        # Focus indicator is checked without asserting the entire 07.09 keyboard matrix.
        page.keyboard.press('Tab')
        journeys.append((width,height,'search/tab/calendar/draft/hover'))
        if errors:issues.append((width,height,'javascript',errors))
        page.close()
    touch_page=browser.new_page(viewport={'width':740,'height':1024},has_touch=True,is_mobile=True)
    touch_page.goto('about:blank?demo=1');touch_page.set_content(HTML)
    touch_page.evaluate('location.hash="#/overview"')
    assert touch_page.evaluate('matchMedia("(hover:hover) and (pointer:fine)").matches') is False, 'touch wrongly classified as fine pointer'
    touch_page.close()
    browser.close()

report={'sizes':SIZES,'routes':ROUTES,'layouts':len(records),'journeys':journeys,'hovers':hovers,'issues':issues,
        'limits':'Chromium only; not a native desktop accessibility / focus order certification; Megalos D1–D6 pending'}
(ROOT/'dist'/'stage7_desktop_v0138_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
assert len(records)==len(SIZES)*len(ROUTES)
assert not issues, f'{len(issues)} layout defects: {issues[:3]}'
print(f'07.08 DESKTOP PASS: {len(records)} layouts, {len(journeys)} journeys, {len(hovers)} hover checks, no clipping/JS errors')
