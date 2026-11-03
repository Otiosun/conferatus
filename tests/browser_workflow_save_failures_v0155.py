"""Unsaved local workflow changes need truthful feedback and a retry path.

Synthetic preview-only sessionStorage errors. No Academy services or institutional state.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT = {'id':'synthetic-draft-155', 'title':'Proposição fictícia de segurança da sessão',
         'body':'Texto fictício suficientemente longo para validar o fluxo completo de edição de propostas.',
         'sectionId':'integridade','type':'PDR','authorComplete':False,
         'partners':[], 'status':'redacao'}


def launch(browser, width, draft):
    page=browser.new_page(viewport={'width':width,'height':860})
    page.set_default_timeout(6000)
    page.goto('about:blank?demo=1')
    page.evaluate('''draft => {
      const store = new Map([['conferatus:proposals-v010', JSON.stringify([draft])],
                             ['conferatus:deliberations-v010', '[]']]);
      let failures = 0;
      Object.defineProperty(window, 'sessionStorage', {configurable:true, value:{
        getItem:k=>store.get(k) ?? null,
        setItem:(k,v)=>{if(k==='conferatus:deliberations-v010' && failures-- > 0)
                          throw Error('Synthetic session quota failure'); store.set(k,v)},
        removeItem:k=>store.delete(k)
      }});
      window.__failSaves = n => {failures=n};
    }''', draft)
    page.set_content(HTML)
    return page


def menu(page, route):
    page.locator('.footer-nav').click()
    page.locator(f'.menu-item[data-route="{route}"]').click()


def banner(page, width, case):
    alert=page.locator('.workflow-save-warning')
    alert.wait_for(state='visible', timeout=5000)
    assert alert.count()==1, (width, case, 'missing unsaved workflow warning')
    assert 'não foi possível salvar' in alert.inner_text().lower(), (width, case, alert.inner_text())
    btn=alert.locator('[data-action="retry-workflow-save"]')
    assert btn.count()==1, (width, case, 'no retry control')
    assert btn.bounding_box()['height']>=44, (width,case,'touch target too small')
    return btn


def retry(page,width,case):
    control=banner(page,width,case)
    page.evaluate('window.__failSaves(1)')
    control.click()
    assert banner(page,width,case).count()==1, (width,case,'retry disappeared while storage still blocked')
    page.locator('[data-action="retry-workflow-save"]').click()
    page.locator('.workflow-save-warning').wait_for(state='hidden', timeout=5000)
    assert page.locator('.workflow-save-warning').count()==0, (width,case,'saved state still claims failure')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    count=0
    for width in (280,390,740,1280):
        for case in ('author','invite','partner','schedule'):
            fixture={**DRAFT}
            if case=='partner':
                fixture.update(authorComplete=True,status='revisao',partners=[{'id':'m02','complete':False}])
            elif case=='schedule':
                fixture.update(authorComplete=True,status='concluida')
            page=launch(browser,width,fixture)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            if case=='schedule':
                menu(page,'calendar')
                page.locator('[data-action="open-schedule"]').click()
                form=page.locator('#schedule-deliberation-form')
                form.locator('[name="title"]').fill('Programação fictícia não salva')
                form.locator('[name="objective"]').fill('Descrição fictícia para testar recuperação de gravação de agenda.')
                form.locator('[name="proposalId"]').select_option(index=1)
                form.locator('[name="start"]').fill('2026-12-21T09:00')
                form.locator('[name="end"]').fill('2026-12-21T11:00')
                page.evaluate('window.__failSaves(1)')
                form.locator('button[type="submit"]').click()
            else:
                menu(page,'proposals')
                if case=='invite':
                    page.locator('[data-action="invite-socii"]').click()
                    form=page.locator('#invite-socii-form')
                    form.locator('[name="memberId"]').select_option(index=1)
                    page.evaluate('window.__failSaves(1)')
                    form.locator('button.workflow-primary').click()
                elif case=='partner':
                    page.evaluate('window.__failSaves(1)')
                    page.locator('[data-confirm-partner]').click()
                else:
                    page.locator('[data-draft]').first.click()
                    page.locator('#compose-proposal-form button[value="conclude"]').click()
                    page.evaluate('window.__failSaves(1)')
                    page.locator('#confirm-proposal-form button[type="submit"]').click()
            # A visible completion in memory must not masquerade as persisted after reload.
            saved=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))[0]')
            if case=='author': assert not saved['authorComplete'],(width,case,'mock did not fail')
            if case=='invite': assert not saved['partners'],(width,case,'mock did not fail')
            if case=='partner': assert not saved['partners'][0]['complete'],(width,case,'mock did not fail')
            if case=='schedule': assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010")).length')==0
            if width==390 and case=='author':page.screenshot(path=str(ROOT/'dist/workflow_save_failed_v0155_390.png'),full_page=True)
            retry(page,width,case)
            # Confirm the subsequent snapshot, not merely the in-memory UI.
            saved=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))[0]')
            if case=='author':assert saved['authorComplete'],(width,case)
            if case=='invite':assert len(saved['partners'])==1,(width,case)
            if case=='partner':assert saved['partners'][0]['complete'],(width,case)
            if case=='schedule':assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010")).length')==1
            if width==390 and case=='author':page.screenshot(path=str(ROOT/'dist/workflow_save_recovered_v0155_390.png'),full_page=True)
            page.set_content(HTML)
            persisted=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))[0]')
            if case=='author':assert persisted['authorComplete']
            if case=='partner':assert persisted['partners'][0]['complete']
            if case=='invite':assert len(persisted['partners'])==1
            if case=='schedule':assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010")).length')==1
            assert not errors,(width,case,errors)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(width,case,'horizontal overflow')
            count+=1
            page.close()
    browser.close()
print(f'Workflow save-failure recovery: {count}/16 PASS (4 operations × 4 widths)')
