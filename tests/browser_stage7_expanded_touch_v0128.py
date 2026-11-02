"""Stage 07.03 / second batch: measurable, working touch controls in expanded states.

Tests a comfort target of 44px where space permits. Calendar cells on very
narrow screens retain seven columns, so check WCAG AA's 24px minimum width and
44px height, not the AAA enhanced width. This is not WCAG certification.
"""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright

HTML = (Path(__file__).resolve().parents[1] / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 360, 390, 540, 740, 768, 1024, 1440)
EXPECT_FIXED = os.getenv('STAGE7_FIXED', '1') == '1'
measurements = []
failures = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width': width, 'height': 844}, has_touch=True, is_mobile=True)
        page.set_default_timeout(7000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('about:blank?demo=1')
        page.set_content(HTML)

        def measure(name, locator, min_width=44, min_height=44):
            rect = locator.first.bounding_box()
            assert rect, (width, name, 'missing rect')
            record = {'width':width, 'control':name, 'width_px':round(rect['width'],2), 'height_px':round(rect['height'],2)}
            measurements.append(record)
            if rect['width'] < min_width-0.5 or rect['height'] < min_height-0.5:
                failures.append({**record,'min_width':min_width,'min_height':min_height})
            return rect

        def navigate(route):
            page.locator('.footer-nav').click()
            page.locator(f'.menu-item[data-route="{route}"]').click()

        page.locator('.demo-toggle').tap()
        ballot_option = page.locator('.vote-button').first
        measure('demo vote option', ballot_option)
        ballot_option.tap()
        reset = page.locator('.reset-vote')
        measure('change demo vote', reset)
        reset.tap()
        assert not page.locator('.reset-vote').count()

        navigate('members')
        measure('directory history tab', page.locator('.profile-head .tab').first)
        page.locator('.profile-head .tab').last.tap()
        assert '#/profile/' in page.url
        page.wait_for_function('document.querySelector(".profile-head .tab:last-child")?.getAttribute("aria-pressed")==="true"')
        navigate('overview')
        measure('institutional history tab', page.locator('.overview-tabs .tab').first)
        page.locator('[data-overview-tab=proposicoes]').tap()
        assert page.locator('[data-overview-tab=proposicoes]').get_attribute('aria-pressed') == 'true'

        navigate('calendar')
        days = page.locator('.calendar-day')
        measure('calendar day', days.first, min_width=24)
        prev = page.locator('[data-action=calendar-prev]')
        next_month = page.locator('[data-action=calendar-next]')
        measure('previous month', prev)
        measure('next month', next_month)
        measure('today', page.locator('[data-action=calendar-today]'))
        month_heading = page.locator('.calendar-month-nav h2').bounding_box()
        assert month_heading and month_heading['height'] <= 23, (width, 'month heading wrapped on narrow screen', month_heading)
        label = page.locator('.calendar-month-nav h2').inner_text()
        next_month.tap()
        assert page.locator('.calendar-month-nav h2').inner_text() != label
        prev.tap()
        assert page.locator('.calendar-month-nav h2').inner_text() == label
        page.locator('[data-calendar-day="2026-11-22"]').tap()
        assert page.locator('[data-calendar-day="2026-11-22"]').get_attribute('aria-pressed') == 'true'
        show_all = page.locator('[data-action=calendar-all]')
        measure('show all calendar dates', show_all)
        show_all.tap()
        assert not page.locator('[data-action=calendar-all]').count()
        page.locator('[data-action=open-schedule]').tap()
        helper = page.locator('.workflow-schedule-form .workflow-help button')
        if helper.count():
            measure('go to proposals helper', helper)
            helper.tap()
            assert '#/proposals' in page.url
        else:
            navigate('proposals')

        page.locator('[data-action=new-proposal]').tap()
        page.locator('#draft-title').wait_for(state='visible')
        editor_action = page.locator('.workflow-editor-actions button')
        assert editor_action.count() >= 2
        measure('editor conclude', page.locator('[value=conclude]'))
        page.locator('#draft-title').fill('Auditoria dos controles de toque')
        page.locator('#draft-body').fill('Verificação da prévia institucional, sem enviar informações reais.')
        page.locator('[value=conclude]').tap()
        measure('review confirmation', page.locator('#confirm-proposal-form button[type=submit]'))
        page.locator('#confirm-proposal-form [aria-label="Cancelar confirmação e voltar à redação"]').tap()
        page.locator('#draft-body').wait_for(state='visible')

        navigate('overview')
        page.locator('.panel-button').tap()
        page.locator('.section-toggle').first.wait_for(state='visible')
        if page.locator('.section-toggle').count():
            measure('governance section toggle', page.locator('.section-toggle').last)
            page.locator('.section-toggle').first.tap()
            edit = page.locator('.section-member .icon-button--edit').first
            if edit.count():
                measure('edit member icon', edit)
                edit.tap()
                assert page.locator('#edit-member-form').count() == 1
                measure('save member edit', page.locator('#edit-member-form button[type=submit]'))
                # Do not submit the simulated change; only verify the control.

        overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth+1')
        assert not overflow, (width, 'document overflow')
        assert not errors, (width, errors)
        if width in (320, 390):
            # Screenshot of expanded governance (with the editor open) after tests.
            suffix = 'after' if EXPECT_FIXED else 'before'
            page.screenshot(path=f'/mnt/data/conffratus_source/stage7_0703_{suffix}_governance_{width}.png', full_page=True)
        page.close()
    browser.close()

path = Path('/mnt/data/conffratus_source/stage7_0703_' + ('after' if EXPECT_FIXED else 'before') + '_second_batch_measurements.json')
path.write_text(json.dumps({'measurements':measurements,'failures':failures},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(measurements)} controls checked across {len(WIDTHS)} widths; under comfort threshold: {len(failures)}')
for f in failures[:25]:
    print('UNDERSIZED:',f)
assert not failures, f'{len(failures)} targets smaller than the stated comfort dimensions'
print('Stage 07.03 second batch: touch actions, route states, dimensions, reflow, JS: PASS')
