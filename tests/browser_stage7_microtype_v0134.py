"""Stage 07.04: inspect critical legibility labels in the offline Chromium preview.

10 CSS px is a project readability floor for these small *informational* labels,
not a WCAG AA certification or a standard-specified font-size requirement.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 360, 390, 540, 740, 768, 1024, 1440)
ROUTES = ('ballot', 'members', 'overview', 'proposals')
SELECTORS = ('.footer-demo', '.result-count', '.result-percentage',
             '.profile-summary>.metrics small', '.member-item .metric-cell small',
             '.activity-code')

samples = []
issues = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width': width, 'height': 820})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?stage7=legibility')
        page.set_content(HTML)
        for route in ROUTES:
            page.evaluate('(r) => { location.hash = "#/" + r }', route)
            page.wait_for_timeout(45)
            sample = page.evaluate('''(selectors) => {
                const f=document.querySelector('.app-footer');
                const box=(el)=>{let r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
                const records=selectors.flatMap(selector=>[...document.querySelectorAll(selector)].map(el=>{
                    const r=box(el),s=getComputedStyle(el);
                    return {selector,font:parseFloat(s.fontSize),text:el.textContent.trim().slice(0,60),...r,
                        visible:s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
                })).filter(x=>x.visible);
                return {records, scroll:document.documentElement.scrollWidth, viewport:innerWidth,
                   footer:box(f),logo:box(f.querySelector('img')),label:box(f.querySelector('.footer-demo')),
                   nav:box(f.querySelector('.footer-nav')),home:box(f.querySelector('.footer-home'))};
            }''', SELECTORS)
            for item in sample['records']:
                item['width'] = width
                item['route'] = route
                samples.append(item)
                if item['font'] < 10:
                    issues.append((width, route, item['selector'], item['text'], item['font']))
            if sample['scroll'] > width + 1:
                issues.append((width, route, 'horizontal overflow', sample['scroll']))
            footer = sample['footer']
            note = sample['label']
            logo = sample['logo']
            nav = sample['nav']
            home = sample['home']
            if note['top'] < footer['top'] - 1 or note['bottom'] > footer['bottom'] + 1:
                issues.append((width, route, 'preview disclaimer clipped by footer', note, footer))
            # Text can be directly under nav/logo in horizontal space only if vertical ranges are disjoint.
            for target_name, target in (('official logo', logo), ('menu button', nav)):
                x_overlap = min(note['right'], target['right']) - max(note['left'], target['left'])
                y_overlap = min(note['bottom'], target['bottom']) - max(note['top'], target['top'])
                if x_overlap > 1 and y_overlap > 1:
                    issues.append((width, route, 'disclaimer overlaps '+target_name, round(x_overlap, 1), round(y_overlap, 1)))
            if route == 'ballot' and width in (280, 390, 740):
                page.screenshot(path=str(ROOT / 'dist' / f'stage7_microtype_{width}.png'), full_page=True)
        if errors:
            issues.append((width, 'page errors', errors))
        page.close()
    browser.close()

out = {'sampled': len(samples), 'routes': ROUTES, 'widths': WIDTHS,
       'under10': sum(x['font'] < 10 for x in samples), 'issues': issues}
(ROOT / 'dist' / 'stage7_microtype_v0134_report.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Microtype {len(samples)} samples, {len(issues)} issues, {out["under10"]} under 10 CSS px')
for issue in issues[:16]: print('ISSUE', issue)
assert not issues, 'Microtype legibility regression detected'
