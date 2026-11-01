"""Socii editor banner is grounded in session participants, never fabricated timing or shared edits."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':844})
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.goto('about:blank?demo=1')
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=proposals]').click()
        page.locator('[data-action=new-proposal]').click()
        assert page.locator('.workflow-socii-editor-bar').count()==0, width
        title='Programa conjunto da Academy'
        body='Esta redação é um rascunho de exemplo construído para verificar o editor e seus participantes.'
        page.locator('#draft-title').fill(title)
        page.locator('#draft-body').fill(body)
        page.get_by_role('button',name='Salvar rascunho').click()
        page.locator('[data-action=invite-socii]').click()
        participant=page.locator('[name=memberId] option').nth(1).inner_text()
        page.locator('[name=memberId]').select_option(index=1)
        page.locator('#invite-socii-form button.workflow-primary').click()
        page.locator('.workflow-record').filter(has_text=title).locator('[data-draft]').click()
        bar=page.locator('.workflow-socii-editor-bar')
        bar.wait_for(state='visible')
        assert participant in bar.inner_text(),(width,participant,bar.inner_text())
        assert 'Prévia local' in bar.inner_text(), width
        assert 'Concluíram 0 de 2' in bar.inner_text(), width
        assert 'hora' not in bar.inner_text().lower(), width
        assert bar.locator('.workflow-socii-avatars i').count()==2, width
        assert page.locator('#draft-title').input_value()==title, width
        assert page.locator('#draft-body').input_value()==body, width
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'), width
        if width in (390,740):
            page.screenshot(path=f'/mnt/data/conferatus_v0112_socii_editor_{width}.png',full_page=True)
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        page.get_by_text('Concluíram 1 de 2').wait_for()
        assert page.get_by_text('Aguardando Socii',exact=False).count()>0, width
        assert page.get_by_text('Concluída',exact=True).count()==0,width
        page.locator('[data-confirm-partner]').click()
        page.get_by_text('Concluíram 2 de 2').wait_for()
        assert not errors,(width,errors)
        page.close()
    browser.close()
print('Socii editor: local participants, honest timing, no change to completion gate (320/390/740/1280): OK')
