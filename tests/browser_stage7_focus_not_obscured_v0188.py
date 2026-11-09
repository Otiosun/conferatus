"""WCAG 2.2 2.4.11 (partial): visible keyboard focus in a short viewport.

Checks focus exposure against author-created overlays, not actual assistive
technology or a complete WCAG conformance audit. Uses a synthetic preview.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect, TimeoutError as PlaywrightTimeout

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
VIEWPORTS = ((320, 256), (390, 320), (740, 360))
ROUTES = ('ballot', 'members', 'calendar', 'compose')
SAMPLES = []

FOCUS_PROBE = """() => {
    const el = document.activeElement;
    if (!el || el === document.body) return null;
    const rect = el.getBoundingClientRect();
    const left = Math.max(0, rect.left), right = Math.min(innerWidth, rect.right);
    const top = Math.max(0, rect.top), bottom = Math.min(innerHeight, rect.bottom);
    const visibleRect = right > left + 1 && bottom > top + 1;
    let hits = 0;
    if (visibleRect) {
        for (const fx of [.2,.5,.8]) for (const fy of [.2,.5,.8]) {
            const at = document.elementFromPoint(left + (right-left)*fx, top + (bottom-top)*fy);
            if (at && (el === at || el.contains(at))) hits++;
        }
    }
    return {
        tag: el.tagName, text: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0,60),
        className: typeof el.className === 'string' ? el.className : '',
        focusVisible: el.matches(':focus-visible'), top:rect.top,bottom:rect.bottom,
        visibleRect, visibleSamples:hits, scrollY, width:innerWidth, height:innerHeight
    };
}"""

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width,height in VIEWPORTS:
        for route in ROUTES:
            page = browser.new_page(viewport={'width':width,'height':height}, reduced_motion='reduce')
            page.set_default_timeout(6000)
            errors=[]
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto('about:blank?demo=1#/' + route)
            page.set_content(HTML)
            expect(page.locator('#main-content')).to_be_visible()
            assert page.evaluate('location.hash') == '#/'+route
            # Start a real keyboard traversal; do not focus nodes from JS.
            for step in range(1,18):
                page.keyboard.press('Tab')
                # Retry only while a focus transition/scroll is settling. Never
                # accept a permanently obscured component or use a fixed sleep.
                try:
                    page.wait_for_function(
                        f'() => {{ const state = ({FOCUS_PROBE})(); return !state || state.visibleSamples > 0; }}',
                        timeout=1500
                    )
                except PlaywrightTimeout:
                    result = page.evaluate(FOCUS_PROBE)
                    page.screenshot(path=str(ROOT/'dist/focus_failure_v0188.png'))
                    raise AssertionError((width,height,route,step,result))
                result = page.evaluate(FOCUS_PROBE)
                if not result:
                    continue  # At the end of a tab cycle the browser may focus body.
                assert result['visibleRect'] and result['visibleSamples'] > 0, (width,height,route,step,result)
                SAMPLES.append({'viewport':[width,height], 'route':route, 'tab':step,
                                'tag':result['tag'], 'visibleSamples':result['visibleSamples']})
            assert not errors,(width,height,route,errors)
            page.close()
    browser.close()

(ROOT/'dist/focus_not_obscured_v0188.json').write_text(json.dumps(SAMPLES,indent=2),encoding='utf-8')
print(f'FOCUS NOT OBSCURED sample PASS: {len(SAMPLES)} keyboard-focus samples across '
      f'{len(VIEWPORTS)*len(ROUTES)} route/viewports, without total occlusion; '
      'no screen reader, physical IME or full WCAG audit.')
