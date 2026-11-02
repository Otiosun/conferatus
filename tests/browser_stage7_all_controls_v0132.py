"""Stage 07.03 closure gate for interactive targets in the offline preview.

Exhaustive over the *mapped* routes/states and nine CSS viewports, not real
hardware or full WCAG conformance. Calendar days keep a documented 24px width
exception (seven-column layout) while retaining >=44px height.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 360, 390, 540, 740, 768, 1024, 1440)
STATES = ('ballot-base', 'vote-expanded', 'members-default', 'members-empty',
          'profile', 'profile-tab2', 'overview', 'overview-tab2',
          'governance', 'governance-expanded', 'governance-edit',
          'governance-tools', 'calendar', 'calendar-form', 'calendar-expanded',
          'proposals', 'socii-invite', 'compose', 'review')
all_targets = []
issues = []
page_errors = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True,
        executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width': width, 'height': 800},
                                has_touch=True, is_mobile=True)
        page.set_default_timeout(8500)
        page.on('pageerror', lambda err: page_errors.append({'width': width, 'error': str(err)}))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)
        visited = []

        def inspect(state):
            visited.append(state)
            targets = page.evaluate('''() => [...document.querySelectorAll(
              'button,a,select,input,textarea,[role="button"]')]
              .filter(el => {const b=el.getBoundingClientRect(),s=getComputedStyle(el);
                return b.width>0 && b.height>0 && !el.disabled &&
                  s.display!=='none' && s.visibility!=='hidden' &&
                  (!el.matches('.skip-link') || document.activeElement===el)})
              .map(el => {const b=el.getBoundingClientRect(); return {
                cls:String(el.className||'').slice(0,80),
                label:(el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,50),
                width:Math.round(b.width*10)/10,height:Math.round(b.height*10)/10}})''')
            for target in targets:
                item = {'viewport': width, 'state': state, **target}
                all_targets.append(item)
                calendar = target['cls'].split(' ')[0] == 'calendar-day'
                minimum_width = 24 if calendar else 44
                if target['width'] < minimum_width-0.5 or target['height'] < 43.5:
                    issues.append(item)
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+1'), (
                width, state, 'horizontal overflow')

        def navigate(route):
            page.locator('.footer-nav').click()
            page.locator(f'.menu-item[data-route="{route}"]').click()

        inspect('ballot-base')
        page.locator('[data-action="toggle-demo"]').click()
        inspect('vote-expanded')
        navigate('members')
        inspect('members-default')
        page.locator('.search-trigger').click()
        page.locator('#search-members').fill('mxyz_missing')
        inspect('members-empty')
        page.locator('[data-action="clear-search"]').click()
        page.locator('.member-item').first.click()
        inspect('profile')
        page.locator('[data-tab="proposicoes"]').click()
        inspect('profile-tab2')
        navigate('overview')
        inspect('overview')
        page.locator('[data-overview-tab="proposicoes"]').click()
        inspect('overview-tab2')
        page.locator('[data-route="governance"]').first.click()
        inspect('governance')
        page.locator('.section-toggle').first.click()
        inspect('governance-expanded')
        page.locator('.icon-button--edit').first.click()
        inspect('governance-edit')
        page.locator('.panel-button').first.click()
        inspect('governance-tools')
        navigate('calendar')
        inspect('calendar')
        page.locator('[data-action="open-schedule"]').click()
        inspect('calendar-form')
        page.locator('[data-action="open-schedule"]').click()
        page.locator('[data-schedule="sample-1"]').click()
        inspect('calendar-expanded')
        navigate('proposals')
        inspect('proposals')
        page.locator('[data-action="invite-socii"]').click()
        inspect('socii-invite')
        page.locator('[data-action="new-proposal"]').click()
        inspect('compose')
        page.locator('#draft-title').fill('Título de teste')
        page.locator('#draft-body').fill('Texto de teste com comprimento suficiente para a revisão.')
        page.locator('#compose-proposal-form [value="conclude"]').click()
        inspect('review')
        assert tuple(visited) == STATES, (width, 'missing test state', visited)
        page.close()
    browser.close()

result = {'viewport_widths': WIDTHS, 'tested_states': STATES,
          'observations': len(all_targets), 'issues': issues, 'page_errors': page_errors,
          'calendar_narrow_targets': sum(1 for x in all_targets if x['width'] < 43.5
                                         and x['cls'].startswith('calendar-day'))}
(ROOT/'dist/stage7_all_controls_v0132_report.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
assert len(all_targets) >= 2000, ('missing interactive inventory', len(all_targets))
assert not issues, f'{len(issues)} undersized controls in mapped states: {issues[:10]}'
assert not page_errors, page_errors
print(f"Stage 07.03 inventory: PASS {len(all_targets)} controls / {len(STATES)} states × {len(WIDTHS)} CSS widths; "
      f"calendar narrow exception {result['calendar_narrow_targets']}, no undersized targets, page errors or overflow")
