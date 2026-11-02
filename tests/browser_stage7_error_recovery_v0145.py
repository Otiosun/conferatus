"""07.10: validation errors must be announced, linked and recover when fixed.

A browser-verified local preview contract; does not claim real screen-reader speech.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(320,390,740,1440)
results=[]

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in WIDTHS:
        page=browser.new_page(viewport={'width':width,'height':850})
        page.goto('about:blank?demo=1')
        errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.set_content(HTML)
        # The empty save must not create a record, and both fields are described by the alert.
        page.evaluate('location.hash="#/compose"')
        page.locator('#draft-title').wait_for()
        page.locator('#compose-proposal-form button[value=save]').click()
        alert=page.locator('#compose-save-error')
        assert alert.is_visible(),(width,'blank draft error not visible')
        assert alert.get_attribute('role')=='alert'
        for field in ('draft-title','draft-body'):
            e=page.locator('#'+field)
            assert e.get_attribute('aria-describedby')=='compose-save-error',(width,field,'no error description')
            assert e.get_attribute('aria-invalid')=='true',(width,field,'no invalid state')
        if width==390:
            page.screenshot(path=str(ROOT/'dist/stage7_error_recovery_draft_invalid_390.png'))
        results.append((width,'empty save exposes alert and invalid fields'))
        page.locator('#draft-title').fill('Proposição experimental legível')
        assert page.locator('#compose-save-error').count()==0,(width,'error persists after typing valid title')
        for field in ('draft-title','draft-body'):
            assert page.locator('#'+field).get_attribute('aria-invalid') is None,(width,field,'stale invalid')
            assert page.locator('#'+field).get_attribute('aria-describedby') is None,(width,field,'stale description')
        if width==390:
            page.screenshot(path=str(ROOT/'dist/stage7_error_recovery_draft_corrected_390.png'))
        results.append((width,'error clears when title is supplied'))
        page.locator('#compose-proposal-form button[value=save]').click()
        page.locator('.workflow-status').wait_for()
        assert ('Rascunho salvo' in page.locator('.workflow-status').inner_text() or 'Rascunho mantido' in page.locator('.workflow-status').inner_text()),(width,page.locator('.workflow-status').inner_text())
        results.append((width,'save-only behavior remains intact'))
        # The demo ID validation similarly must clear on correction, without saving early.
        page.evaluate('location.hash="#/governance"')
        page.locator('.section-toggle').first.wait_for()
        page.locator('.section-toggle').first.click()
        page.locator('[data-edit]').first.click()
        field=page.locator('#member-acdm-id')
        field.fill('a')
        page.locator('#edit-member-form button[type=submit]').click()
        assert page.locator('#edit-error').is_visible(),(width,'ID error not visible')
        assert field.get_attribute('aria-invalid')=='true'
        assert field.get_attribute('aria-describedby')=='edit-error'
        if width==390:
            page.screenshot(path=str(ROOT/'dist/stage7_error_recovery_member_invalid_390.png'))
        results.append((width,'invalid member ID exposes error'))
        corrected='DEMO-UNIQUE-987654'
        field.fill(corrected)
        assert page.locator('#edit-error').count()==0,(width,'member ID error persists after correction')
        assert field.get_attribute('aria-invalid') is None,(width,'stale member ID invalid')
        assert field.get_attribute('aria-describedby') is None,(width,'stale member ID description')
        assert not page.locator('[data-action=undo]').count(),(width,'member saved prematurely')
        if width==390:
            page.screenshot(path=str(ROOT/'dist/stage7_error_recovery_member_corrected_390.png'))
        results.append((width,'member ID error clears without saving prematurely'))
        page.locator('#edit-member-form button[type=submit]').click()
        assert page.locator('[data-action=undo]').count(),(width,'corrected member ID did not save')
        results.append((width,'corrected member ID still saves'))
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,'horizontal overflow')
        assert not errors,(width,'Javascript errors',errors)
        if width in (320,390):
            page.screenshot(path=str(ROOT/f'dist/stage7_error_recovery_v0145_{width}.png'))
        page.close()
    browser.close()

(ROOT/'dist/stage7_error_recovery_v0145.json').write_text(json.dumps({'checks':len(results),'results':results},ensure_ascii=False,indent=2))
print(f'Validation recovery: {len(results)}/{len(WIDTHS)*6} PASS')
