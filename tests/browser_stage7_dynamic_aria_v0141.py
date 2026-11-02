"""Stage 07.10 — auditable ARIA disclosure relationships in the offline preview.

The test deliberately fails on the existing UI before changes. It does NOT
certify WCAG nor simulate an actual screen reader. It checks concrete DOM
contracts, keyboard operability and live-region continuity.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(320,390,740,1440)
results=[]

def check_references(page, width, case):
    missing=page.evaluate(r'''() => [...document.querySelectorAll('[aria-controls],[aria-describedby],[aria-labelledby]')].flatMap(el => ['aria-controls','aria-describedby','aria-labelledby'].flatMap(attr => (el.getAttribute(attr)||'').split(/\s+/).filter(Boolean).filter(id=>!document.getElementById(id)).map(id=>({attr,id,tag:el.tagName}))));''')
    assert not missing,(width,case,'broken ARIA ID references',missing)

def check(page, selector, expected, label, width):
    element=page.locator(selector).first
    assert element.count(),(width,label,'trigger missing')
    assert element.get_attribute('aria-expanded')==expected,(width,label,'expanded state mismatch')
    target_id=element.get_attribute('aria-controls')
    ok=bool(target_id) and page.locator('#'+target_id).count()==1
    results.append({'width':width,'case':label,'controls':target_id,'valid':ok})
    assert ok,(width,label,'expanded disclosure has no resolvable aria-controls')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in WIDTHS:
        page=browser.new_page(viewport={'width':width,'height':860})
        errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto('about:blank?demo=1');page.set_content(HTML)
        page.locator('.footer-nav').click()
        check(page,'.footer-nav','true','open navigation',width)
        check_references(page,width,'navigation')
        page.keyboard.press('Escape')
        assert page.locator('.footer-nav').get_attribute('aria-expanded')=='false'
        page.locator('[data-action=toggle-demo]').click()
        check(page,'[data-action=toggle-demo]','true','open demonstration voting',width)
        page.locator('[data-action=toggle-demo]').click()
        page.evaluate('location.hash="#/members"')
        page.wait_for_timeout(30)
        page.locator('[data-action=search]').click()
        check(page,'[data-action=search]','true','open member search',width)
        assert page.locator('.member-list').get_attribute('role')=='region'
        assert page.locator('.metrics').first.get_attribute('role')=='group'
        check_references(page,width,'member search')
        count=page.locator('#member-count')
        assert count.count() and count.get_attribute('role')=='status'
        page.locator('#search-members').fill('inexistente-um-nome-xxxx')
        assert '0 membros' in count.inner_text(),(width,'search live count')
        page.evaluate('location.hash="#/governance"');page.wait_for_timeout(30)
        sections=page.locator('.section-toggle')
        assert sections.count()>0
        sections.first.click()
        check(page,'.section-toggle[aria-expanded=true]','true','expanded governance section',width)
        page.locator('[data-action=toggle-tools]').click()
        check(page,'[data-action=toggle-tools]','true','open demonstration tools',width)
        check_references(page,width,'governance tools')
        page.evaluate('location.hash="#/calendar"');page.wait_for_timeout(30)
        page.locator('[data-action=open-schedule]').click()
        check(page,'[data-action=open-schedule]','true','open calendar form',width)
        calendar_item=page.locator('.calendar-item [data-schedule]').first
        if calendar_item.get_attribute('aria-expanded')!='true':
            calendar_item.click()
        check(page,'.calendar-item [data-schedule][aria-expanded=true]','true','expanded calendar item',width)
        check_references(page,width,'calendar')
        page.evaluate('location.hash="#/overview"');page.wait_for_timeout(25)
        assert page.locator('.overview-stats').get_attribute('role')=='group'
        check_references(page,width,'overview')
        assert not errors,(width,'JS errors',errors)
        page.close()
    browser.close()
report={'total':len(results),'passed':sum(x['valid'] for x in results),'results':results}
(ROOT/'dist/stage7_dynamic_aria_v0141.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"ARIA relationships: {report['passed']}/{report['total']}")
