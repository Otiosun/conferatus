"""Regression: content changed after signoff must not inherit approvals for an older version."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':844})
        page.goto('about:blank?demo=1')
        page.set_content(html)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.locator('.footer-nav').click()
        page.locator('[data-route=proposals]').first.click()
        page.locator('[data-action=new-proposal]').click()
        title='Protocolo de revisão conjunta'
        old_body='Primeira versão do texto para revisão do Socii, assinada antes de uma mudança relevante.'
        new_body='Segunda versão com conteúdo deliberativo substancialmente ALTERADO, exigindo uma nova confirmação.'
        page.locator('#draft-title').fill(title)
        page.locator('#draft-body').fill(old_body)
        page.locator('[value=save]').click()
        page.locator('[data-action=invite-socii]').click()
        page.locator('[name=memberId]').select_option(index=1)
        page.locator('#invite-socii-form button.workflow-primary').click()
        record=page.locator('.workflow-record').filter(has_text=title)
        assert 'concluíram 0 de 2' in record.inner_text().casefold(),(width,record.inner_text())
        record.locator('[data-draft]').click()
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        record=page.locator('.workflow-record').filter(has_text=title)
        assert 'concluíram 1 de 2' in record.inner_text().casefold(),width
        # A no-op save must not invalidate approvals for the same version.
        record.locator('[data-draft]').click()
        page.locator('#confirm-proposal-form [data-route=compose]').click()
        assert page.locator('#draft-body').input_value()==old_body,width
        page.locator('#compose-proposal-form [value=save]').click()
        record=page.locator('.workflow-record').filter(has_text=title)
        assert 'concluíram 1 de 2' in record.inner_text().casefold(),width
        record.locator('[data-draft]').click()
        page.locator('#confirm-proposal-form [data-route=compose]').click()
        page.locator('#draft-body').fill(new_body)
        page.locator('#compose-proposal-form [value=save]').click()
        record=page.locator('.workflow-record').filter(has_text=title)
        assert 'concluíram 0 de 2' in record.inner_text().casefold(),f'{width}: earlier version approvals wrongly retained: {record.inner_text()}'
        assert 'autoria: pendente' in record.inner_text().casefold(),width
        # A partner approval alone cannot conclude the newly edited version.
        record.locator('[data-confirm-partner]').click()
        record=page.locator('.workflow-record').filter(has_text=title)
        assert 'concluíram 1 de 2' in record.inner_text().casefold(),width
        assert 'aguardando autoria' in record.inner_text().casefold(),width
        assert 'autoria: pendente' in record.inner_text().casefold(),width
        # Re-review must re-sign current version and then conclude.
        record.locator('[data-draft]').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        record=page.locator('.workflow-record').filter(has_text=title)
        assert 'concluíram 2 de 2' in record.inner_text().casefold(),width
        assert 'concluída' in record.inner_text().casefold(),width
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),width
        page.close()
    browser.close()
print('Reapproval after editing: OK (320,390,740,1280)')
