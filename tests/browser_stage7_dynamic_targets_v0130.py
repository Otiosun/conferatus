"""Stage 07.03, dynamic states: test small controls appearing only after user actions.

Run with STAGE7_FIXED=0 to reproduce defects; after scoped CSS repair run default.
No external APIs, real accounts, institutional changes, or browser extensions.
"""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 360, 390, 540, 740, 768, 1024, 1440)
FIXED = os.getenv('STAGE7_FIXED','1') == '1'
all_results=[]
issues=[]

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page=browser.new_page(viewport={'width':width,'height':780},has_touch=True,is_mobile=True)
        page.set_default_timeout(6500)
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)

        def measure(key, locator, *, minimum=44):
            locator.wait_for(state='visible')
            rect=locator.bounding_box()
            assert rect,(width,key,'no rectangle')
            hit=locator.evaluate('''e => {
              let r=e.getBoundingClientRect(); let x=Math.min(innerWidth-1,Math.max(1,r.x+r.width/2));
              let y=Math.min(innerHeight-1,Math.max(1,r.y+r.height/2));
              // Measure after browser scrollIntoView so center hit is genuinely on screen
              e.scrollIntoView({block:'center',inline:'nearest'}); r=e.getBoundingClientRect();
              x=Math.min(innerWidth-1,Math.max(1,r.x+r.width/2));
              y=Math.min(innerHeight-1,Math.max(1,r.y+r.height/2));
              let top=document.elementFromPoint(x,y);
              return !!top && (top===e || e.contains(top));
            }''')
            record={'width':width,'state':key,'w':round(rect['width'],2),'h':round(rect['height'],2),'center_hit':hit}
            all_results.append(record)
            if rect['height']<minimum-.5 or rect['width']<minimum-.5 or not hit:
                issues.append(record)
            return record

        def navigate(route):
            page.locator('.footer-nav').tap()
            page.locator(f'.menu-item[data-route="{route}"]').tap()

        navigate('members')
        page.locator('.search-trigger').tap()
        page.locator('#search-members').fill('INEXISTENTE_XY_2026')
        assert 'Nenhum membro encontrado' in page.locator('#member-results').inner_text()
        clear=page.locator('[data-action="clear-search"]')
        measure('members-clear-search-in-empty-state',clear)
        if width in (280,390):page.screenshot(path=str(ROOT/f'dist/stage7_dynamic_empty_{width}.png'),full_page=True)
        clear.tap()
        assert page.locator('.member-item').count()>0, (width,'clear search did not restore members')
        assert page.locator('[data-action="clear-search"]').is_hidden(), (width,'clear search did not hide')

        navigate('governance') if False else None  # governance is reachable through overview shortcut
        navigate('overview')
        page.locator('[data-route="governance"]').first.tap()
        page.locator('.section-toggle').first.tap()
        demote=page.locator('[data-demote]').first
        assert demote.count()>0,(width,'demote unavailable in demo fixture')
        demote.tap()
        undo=page.locator('[data-action="undo"]')
        assert undo.count()==1,(width,'undo unavailable')
        measure('governance-undo-after-demotion',undo)
        undo.tap()
        assert page.locator('[data-action="undo"]').count()==0,(width,'undo did not restore')
        page.locator('.panel-button').tap()
        reset=page.locator('[data-action="reset-admin"]')
        measure('preview-reset-tools',reset)
        reset.tap()
        assert not page.locator('.demo-tools').count(),(width,'preview reset tools did not close')

        page.evaluate('location.hash="#/profile/no-such-member-stage7"')
        page.wait_for_function('location.hash.includes("no-such-member")')
        page.locator('.missing-profile').wait_for(state='visible')
        back=page.locator('.missing-profile button')
        measure('missing-profile-return',back)
        back.tap()
        assert '#/members' in page.url,(width,'missing profile return broken')

        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,'overflow')
        assert not errors,(width,'javascript pageerrors',errors)
        page.close()
    browser.close()

report=ROOT/'dist'/'stage7_dynamic_target_measurements.json'
report.write_text(json.dumps({'measurements':all_results,'problems':issues},indent=2,ensure_ascii=False))
print('Dynamic actions measured:',len(all_results),'across',len(WIDTHS),'widths')
for problem in issues[:30]:print('ISSUE',json.dumps(problem,ensure_ascii=False))
print('problems total:',len(issues))
if FIXED: assert not issues, f'{len(issues)} dynamic touch target defects'
