"""Changing a proposal's review classification must not inherit a Socii signoff."""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'dist/CONFERATUS_demo_offline.html').read_text()


def open_proposals(page):
    page.locator('.footer-nav').click()
    page.locator('.menu-item[data-route=proposals]').click()


def prepare_partner_review(page, title):
    open_proposals(page)
    page.locator('[data-action=new-proposal]').click()
    page.locator('#draft-title').fill(title)
    page.locator('#draft-body').fill('Documento fictício para verificação da classificação e da confirmação individual do Socii.')
    page.locator('#compose-proposal-form [value=save]').click()
    page.locator('[data-action=invite-socii]').click()
    page.locator('#invite-socii-form [name=memberId]').select_option(index=1)
    page.locator('#invite-socii-form button.workflow-primary').click()
    record=page.locator('.workflow-record').filter(has_text=title)
    record.locator('[data-confirm-partner]').click()
    record=page.locator('.workflow-record').filter(has_text=title)
    assert 'concluíram 1 de 2' in record.inner_text().casefold(),record.inner_text()
    assert 'aguardando autoria' in record.inner_text().casefold(),record.inner_text()
    record.locator('[data-draft]').click()
    page.locator('#confirm-proposal-form').wait_for(state='visible')
    bar=page.locator('.workflow-socii-editor-bar')
    assert bar.count()==1 and bar.is_visible(),title
    assert bar.get_attribute('aria-label')=='Socii desta proposição, demonstração local',title
    assert 'Concluíram 1 de 2' in bar.inner_text(),(title,bar.inner_text())
    assert 'hora' not in bar.inner_text().casefold(),title
    assert 'confirmou sua participação nesta prévia local' in page.locator('.workflow-review-sheet > p').inner_text(),title
    if title=='Classificação unchanged 390':
        page.screenshot(path=str(Path(__file__).resolve().parents[1]/'dist/socii_review_390.png'),full_page=True)


with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':844})
        page.set_default_timeout(5000)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.goto('about:blank?demo=1')
        page.set_content(html)
        for change in ('section','type','both','unchanged'):
            title=f'Classificação {change} {width}'
            prepare_partner_review(page,title)
            section=page.locator('#confirm-proposal-form [name=sectionId]')
            section_options=section.locator('option').evaluate_all('(nodes)=>nodes.map(x=>x.value)')
            assert len(section_options)>1,(width,section_options)
            assert section.input_value()=='integridade',width
            if change in ('section','both'):
                section.select_option(next(value for value in section_options if value!='integridade'))
            if change in ('type','both'):
                page.locator('#confirm-proposal-form [name=type]').select_option('PR')
            page.locator('#confirm-proposal-form button[type=submit]').click()
            record=page.locator('.workflow-record').filter(has_text=title)
            if change=='unchanged':
                assert 'concluíram 2 de 2' in record.inner_text().casefold(),(width,record.inner_text())
                assert 'concluída' in record.inner_text().casefold(),width
            else:
                assert 'concluíram 1 de 2' in record.inner_text().casefold(),f'{width} {change}: metadata inherited Socii approval: {record.inner_text()}'
                assert 'aguardando socii' in record.inner_text().casefold(),(width,record.inner_text())
                assert 'socii: ' in record.inner_text().casefold() and '(pendente)' in record.inner_text().casefold(),width
                assert record.locator('[data-confirm-partner]').count()==1,width
                assert 'confirmações do Socii foram reiniciadas' in page.locator('.workflow-status').inner_text(),width
                if change=='both' and width in (390,740):
                    page.screenshot(path=f'/mnt/data/conferatus_v0119_socii_classification_{width}.png',full_page=True)
                # Only a fresh partner confirmation approves this version.
                record.locator('[data-confirm-partner]').click()
                record=page.locator('.workflow-record').filter(has_text=title)
                assert 'concluíram 2 de 2' in record.inner_text().casefold(),width
                assert 'concluída' in record.inner_text().casefold(),width
        # Proposals without partners should not show a fictitious Socii group.
        open_proposals(page)
        page.locator('[data-action=new-proposal]').click()
        page.locator('#draft-title').fill(f'Sem Socii {width}')
        page.locator('#draft-body').fill('Redação fictícia individual, sem outros participantes vinculados a esta proposição.')
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('#confirm-proposal-form').wait_for(state='visible')
        assert page.locator('.workflow-socii-editor-bar').count()==0,width
        assert page.locator('.workflow-review-sheet > p').inner_text()=='Confira os dados e a redação antes de confirmar a conclusão.',width
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        page.close()
    browser.close()
print('Socii reapproval after section/type change; unchanged metadata stays approved: OK')
