"""07.04: stress real preview DOM with long names, unbroken words, titles and labels.

The fixtures are synthetic text *only*, inserted into existing rendered elements;
no institutional records are altered. The member-list ellipsis is intentionally
allowed because its complete accessible button name remains in the DOM.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 360, 390, 540, 740, 768, 1024, 1440)
LONG_WORD = 'CONSELHEIROEXTRAORDINARIO' * 6
LONG_LABEL = 'PROPOSICAOINSTITUCIONAL-' + LONG_WORD
STATES = (
    ('ballot', '.result-label'),
    ('ballot', '.description-panel p'),
    ('members', '.member-name'),  # intentional visual ellipsis; accessible name is not truncated
    ('profile', '.activity-title'),
    ('profile', '.activity-code'),
    ('overview', '.activity-title'),
    ('overview', '.activity-code'),
    ('governance', '.section-toggle > span'),
    ('governance-expanded', '.section-member-name'),
    ('calendar', '.calendar-item > button strong'),
    ('proposals', '.activity-title'),
    ('compose', '.workflow-editor-head h1'),
)
records = []
failures = []
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True,
                                executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width':width,'height':800})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)
        for state, selector in STATES:
            route = 'governance' if state == 'governance-expanded' else state
            page.evaluate('(route) => { location.hash = "#/" + route; }', route)
            if state == 'governance-expanded':
                page.locator('.section-toggle').first.click()
            elif route != 'ballot':
                page.wait_for_timeout(30)
            element = page.locator(selector)
            assert element.count(), (width, state, selector, 'selector not rendered')
            target = element.first
            target.evaluate('(el,text) => { el.textContent=text; }', LONG_LABEL)
            geometry = page.evaluate('''(selector) => {
              const el=document.querySelector(selector), rect=el.getBoundingClientRect();
              const root=document.documentElement;
              return {scrollWidth:root.scrollWidth,viewWidth:innerWidth,
                targetWidth:Math.round(rect.width),targetHeight:Math.round(rect.height),
                fullText:el.textContent};
            }''', selector)
            item={'width':width,'state':state,'selector':selector,
                  'scrollWidth':geometry['scrollWidth'],'targetWidth':geometry['targetWidth']}
            records.append(item)
            if geometry['scrollWidth'] > width + 1:
                failures.append(item)
            if state=='members':
                assert target.evaluate('(el) => el.closest("button").textContent.includes(el.textContent)'), (
                    width, 'member ellipsis must preserve full accessible button name')
            if width in (280,390,740) and state in ('profile','governance','calendar','compose') and selector in (
                '.activity-title','.section-toggle > span','.calendar-item > button strong','.workflow-editor-head h1'):
                path=ROOT/'dist'/f'stage7_long_content_{state}_{width}.png'
                page.screenshot(path=str(path), full_page=True)
        page.close()
    browser.close()

report={'widths':list(WIDTHS),'states':len(STATES),'observations':len(records),
        'failures':failures,'pageErrors':errors}
(ROOT/'dist'/'stage7_long_content_v0133_report.json').write_text(
    json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(records)==len(WIDTHS)*len(STATES), report
assert not failures, f'{len(failures)} long-content overflows: {failures[:8]}'
assert not errors, errors
print(f'07.04 long content PASS: {len(records)} states × width scenarios; no horizontal overflow, JS errors or lost member labels')
