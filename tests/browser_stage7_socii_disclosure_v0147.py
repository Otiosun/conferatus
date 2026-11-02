"""CONFFRATUS 07.10: Socii invitation disclosure accessibility and keyboard flow.

Chromium offline demo, not a real invitation or a screen-reader speech test.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(280,320,360,390,540,740,768,1024,1440)
results=[]

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in WIDTHS:
        page=browser.new_page(viewport={'width':width,'height':850})
        errors=[]
        page.on('pageerror',lambda exc:errors.append(str(exc)))
        page.goto('about:blank')
        page.set_content(HTML)
        page.evaluate('location.hash="#/proposals"')
        trigger=page.locator('[data-action="invite-socii"]')
        trigger.wait_for()
        assert trigger.get_attribute('aria-expanded')=='false',(width,'closed state not conveyed')
        assert page.locator('#invite-socii-form').count()==0
        results.append({'width':width,'case':'initial state closed'})

        trigger.focus()
        page.keyboard.press('Enter')
        form=page.locator('#invite-socii-form')
        assert form.count()==1,(width,'form not shown')
        assert trigger.get_attribute('aria-expanded')=='true',(width,'open state not conveyed')
        assert trigger.get_attribute('aria-controls')=='invite-socii-form',(width,'no relationship to revealed panel')
        assert form.get_attribute('aria-label')=='Adicionar participante Socii (prévia local)',(width,'form without accessible name')
        assert trigger.evaluate('(x)=>x===document.activeElement'),(width,'keyboard focus lost on open')
        assert form.locator('select').count()==2
        results.append({'width':width,'case':'expanded state and accessible form'})
        if width in (320,390):
            page.screenshot(path=str(ROOT/f'dist/stage7_socii_v0147_open_{width}.png'),full_page=True)

        page.keyboard.press('Enter')
        assert page.locator('#invite-socii-form').count()==0,(width,'form did not close')
        assert trigger.get_attribute('aria-expanded')=='false',(width,'close state not conveyed')
        assert trigger.evaluate('(x)=>x===document.activeElement'),(width,'keyboard focus lost on close')
        results.append({'width':width,'case':'closed with keyboard'})

        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Proposta de inclusão na prévia')
        page.locator('#draft-body').fill('Redação de teste local com texto suficiente para registrar um rascunho de demonstração.')
        page.locator('button[value="save"]').click()
        page.wait_for_function('location.hash==="#/proposals"')
        trigger=page.locator('[data-action="invite-socii"]')
        trigger.click()
        form=page.locator('#invite-socii-form')
        assert form.count()==1
        assert form.locator('select[name="draftId"] option').count()>=1
        member=form.locator('select[name="memberId"]')
        valid=member.locator('option:not([disabled])').first.get_attribute('value')
        assert valid
        member.select_option(valid)
        form.locator('button[type="submit"], button:not([type])').click()
        assert form.count()==0,(width,'form not closed after addition')
        assert trigger.get_attribute('aria-expanded')=='false',(width,'trigger no longer has closed state')
        assert 'Participante incluído' in page.locator('.workflow-status').inner_text(),(width,'visible status missing')
        assert 'Participante incluído' in page.locator('#app-live-announcer').inner_text(),(width,'announcement missing')
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'horizontal overflow')
        assert not errors,(width,'JavaScript errors',errors)
        results.append({'width':width,'case':'draft invitation demo and status'})
        if width in (320,390):
            page.screenshot(path=str(ROOT/f'dist/stage7_socii_v0147_{width}.png'),full_page=True)
        page.close()
    browser.close()

(ROOT/'dist/stage7_socii_disclosure_v0147.json').write_text(json.dumps({'count':len(results),'widths':WIDTHS,'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Socii disclosure keyboard/ARIA: {len(results)}/{len(WIDTHS)*4} PASS')
