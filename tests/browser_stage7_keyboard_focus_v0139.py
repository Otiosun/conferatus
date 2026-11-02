"""Stage 07.09 — deterministic Chromium keyboard and focus regression.

Only the offline preview is tested; no real authentication or institutional voting.
Tests Tab, Shift+Tab, Enter, Escape, route changes, form error and selector rerender.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
SIZES = ((320, 680), (390, 844), (768, 1024), (1440, 900))
results = []
def active(page):
    return page.evaluate('''() => ({tag:document.activeElement?.tagName,
        id:document.activeElement?.id || '', css:document.activeElement?.className || '',
        focusVisible:document.activeElement?.matches(':focus-visible') || false})''')

def check(page, width, case, okay, info=None):
    results.append({'width': width, 'case': case, 'pass': bool(okay), 'focus': active(page), 'details': info})

with sync_playwright() as w:
    browser = w.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width, height in SIZES:
        page = browser.new_page(viewport={'width':width, 'height':height})
        errors=[]
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)
        page.keyboard.press('Tab')
        check(page, width, 'first Tab reaches skip link', page.locator('.skip-link').evaluate('(el)=>document.activeElement===el && el.matches(":focus-visible")'))
        page.keyboard.press('Enter')
        check(page, width, 'skip link focuses main', active(page)['id']=='main-content')
        page.locator('.footer-nav').focus()
        page.keyboard.press('Enter')
        check(page, width, 'menu Enter focuses first item', page.locator('.menu-item').first.evaluate('(el)=>document.activeElement===el') and page.locator('.footer-nav').get_attribute('aria-expanded')=='true')
        page.keyboard.press('Escape')
        check(page, width, 'Escape menu returns to trigger', page.locator('.footer-nav').evaluate('(el)=>document.activeElement===el') and page.locator('.bottom-menu').count()==0)
        page.locator('.footer-nav').focus()
        page.keyboard.press('Enter')
        page.keyboard.press('Enter')
        page.wait_for_function('location.hash==="#/members" && document.querySelector(".member-item")!==null')
        check(page, width, 'menu route moves focus to main', active(page)['id']=='main-content')
        page.locator('.search-trigger').focus()
        page.keyboard.press('Enter')
        check(page, width, 'search opens and focuses input', active(page)['id']=='search-members')
        page.keyboard.press('Escape')
        check(page, width, 'Escape search returns to trigger', page.locator('.search-trigger').evaluate('(el)=>document.activeElement===el') and page.locator('#search-members').count()==0)
        page.locator('.member-item').first.focus()
        page.keyboard.press('Enter')
        page.wait_for_function('location.hash.startsWith("#/profile/") && document.querySelector(".profile-head")!==null')
        page.wait_for_function('document.activeElement?.id==="main-content"')
        check(page, width, 'member profile route focuses main', active(page)['id']=='main-content')
        page.evaluate('location.hash="#/governance"')
        page.locator('[data-section]').first.focus()
        page.keyboard.press('Enter')
        check(page,width,'section disclosure preserves focus',page.locator('[data-section]').first.evaluate('(el)=>el===document.activeElement'))
        page.locator('[data-edit]').first.focus()
        page.keyboard.press('Enter')
        check(page,width,'edit opens with field focus',active(page)['id']=='member-acdm-id')
        page.keyboard.press('Escape')
        check(page,width,'Escape editor returns to edit trigger',page.locator('[data-edit]').first.evaluate('(el)=>el===document.activeElement'))
        page.locator('[data-action="toggle-tools"]').focus()
        page.keyboard.press('Enter')
        check(page,width,'tools opens and keeps toggle focus',page.locator('[data-action="toggle-tools"]').evaluate('(el)=>el===document.activeElement'))
        page.locator('#role-mode').focus()
        page.locator('#role-mode').select_option('membro')
        check(page,width,'role selection preserves selector focus',active(page)['id']=='role-mode')
        page.keyboard.press('Escape')
        check(page,width,'Escape tools returns to toggle',page.locator('[data-action="toggle-tools"]').evaluate('(el)=>el===document.activeElement'))
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').focus()
        page.keyboard.press('Enter')
        page.wait_for_function('location.hash==="#/compose" && document.querySelector("#draft-title")!==null')
        check(page,width,'compose route focuses main',active(page)['id']=='main-content')
        page.locator('#draft-title').focus()
        save=page.locator('#compose-proposal-form button[value="save"]')
        save.focus();page.keyboard.press('Enter')
        check(page,width,'invalid draft reports error and focuses title',active(page)['id']=='draft-title' and page.locator('[role="alert"]').count()>0)
        page.evaluate('location.hash="#/calendar"')
        page.locator('[data-action="calendar-next"]').focus()
        month=page.locator('.calendar-month-nav h2').inner_text()
        page.keyboard.press('Enter')
        check(page,width,'month change retains action focus',page.locator('[data-action="calendar-next"]').evaluate('(el)=>el===document.activeElement') and month!=page.locator('.calendar-month-nav h2').inner_text())
        page.keyboard.press('Shift+Tab')
        check(page,width,'Shift+Tab stays on keyboard-selectable element', page.evaluate('document.activeElement instanceof HTMLElement && document.activeElement!==document.body && document.activeElement.tabIndex>=0'))
        check(page,width,'no JS errors',not errors,errors)
        if width in (320,768):
            page.locator('[data-action="calendar-next"]').focus()
            page.screenshot(path=str(ROOT/'dist'/f'keyboard_focus_calendar_{width}.png'),full_page=False)
        page.close()
    browser.close()

report={'version':'v0.10.39','sizes':SIZES,'results':results,'passed':sum(x['pass'] for x in results),'failed':[x for x in results if not x['pass']],
'limits':'Chromium offline only; not full screen-reader or native browser focus certification'}
(ROOT/'dist'/'stage7_keyboard_focus_v0139_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'07.09 keyboard: {report["passed"]}/{len(results)} checks; failed={len(report["failed"])}')
for r in report['failed'][:12]: print('FAILED:',r['width'],r['case'],r['focus'])
assert not report['failed'], 'Stage 07.09 keyboard regressions detected'
