"""Second 07.09 keyboard test: proposal review, cancel and native validation flow.

Restricted to the offline Chromium demonstration. No real votes or invitations.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
checks=[]

def check(page,width,name,condition):
    checks.append({'width':width,'case':name,'passed':bool(condition),'focus':page.evaluate('document.activeElement?.outerHTML?.slice(0,120)')})

def at(page,css):return page.locator(css).evaluate('(el)=>document.activeElement===el')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (390,768):
        page=browser.new_page(viewport={'width':width,'height':860})
        errors=[]
        page.on('pageerror',lambda err: errors.append(str(err)))
        page.goto('about:blank?demo=1');page.set_content(HTML)
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').focus()
        page.keyboard.press('Enter')
        page.wait_for_function('location.hash==="#/compose" && document.activeElement?.id==="main-content"')
        check(page,width,'compose Enter route focus main',at(page,'#main-content'))
        page.keyboard.press('Tab')
        check(page,width,'Tab from main enters editor title',at(page,'#draft-title'))
        page.keyboard.type('Rascunho de teste do teclado')
        page.keyboard.press('Tab')
        check(page,width,'Tab follows title into body',at(page,'#draft-body'))
        page.keyboard.type('Redação demonstrativa com mais de vinte caracteres para a folha de revisão.')
        page.keyboard.press('Tab')
        check(page,width,'Tab from body to conclude button',at(page,'button[name="intent"][value="conclude"]'))
        page.keyboard.press('Enter')
        page.wait_for_function('location.hash==="#/review" && document.activeElement?.id==="main-content"')
        check(page,width,'review navigation focus main',at(page,'#main-content'))
        page.keyboard.press('Tab')
        check(page,width,'review Tab reaches section selector',at(page,'#confirm-proposal-form select[name="sectionId"]'))
        page.keyboard.press('Tab')
        check(page,width,'review Tab reaches type selector',at(page,'#confirm-proposal-form select[name="type"]'))
        page.keyboard.press('Tab')
        check(page,width,'review Tab reaches Cancel',at(page,'[data-route="compose"]'))
        page.keyboard.press('Shift+Tab')
        check(page,width,'review Shift+Tab returns to selector',at(page,'#confirm-proposal-form select[name="type"]'))
        page.locator('[data-route="compose"]').focus()
        page.keyboard.press('Enter')
        page.wait_for_function('location.hash==="#/compose" && document.activeElement?.id==="main-content"')
        check(page,width,'review cancel returns focus to editor main',at(page,'#main-content'))
        check(page,width,'editor preserved title after cancel',page.locator('#draft-title').input_value()=='Rascunho de teste do teclado')
        check(page,width,'no JS error',not errors)
        page.close()
    browser.close()
report={'checks':checks,'passed':sum(x['passed'] for x in checks),'failures':[x for x in checks if not x['passed']]}
(ROOT/'dist'/'stage7_keyboard_workflows_v0139_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'07.09 workflows: {report["passed"]}/{len(checks)}')
for f in report['failures']: print('FAIL',f['width'],f['case'],f['focus'])
assert not report['failures']
