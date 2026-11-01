"""Unreadable saved JSON and forged completed states do not cause data loss or bypass Socii."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
DRAFT_KEY='conferatus:proposals-v010'
SCHEDULE_KEY='conferatus:deliberations-v010'
RAW_BACKUP_KEY='conferatus:unreadable-session-backup-v0115'
INVALID_BACKUP_KEY='conferatus:invalid-session-backup-v0114'

def boot(browser, width, values):
    page=browser.new_page(viewport={'width':width,'height':844})
    page.set_default_timeout(5000)
    page.goto('about:blank?demo=1')
    page.evaluate('''values=>{const data=new Map(Object.entries(values));Object.defineProperty(window,'sessionStorage',{
      configurable:true,value:{getItem:k=>data.has(k)?data.get(k):null,
      setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k),clear:()=>data.clear()}})}''',values)
    page.set_content(HTML)
    return page

def proposals(page):
    page.locator('.footer-nav').click()
    page.locator('.menu-item[data-route=proposals]').click()

def save_new(page,title):
    page.locator('[data-action=new-proposal]').click()
    page.locator('#draft-title').fill(title)
    page.locator('#draft-body').fill('Rascunho verdadeiro para verificar a persistência e a recuperação de uma sessão local.')
    page.locator('#compose-proposal-form [value=save]').click()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        broken_draft='[{"id":"legacy-unfinished"'  # genuinely broken JSON
        wrong_shape=json.dumps({'legacy':'not an array'},ensure_ascii=False)
        page=boot(browser,width,{DRAFT_KEY:broken_draft,SCHEDULE_KEY:wrong_shape})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        proposals(page)
        assert 'registros incompletos' in page.locator('.workflow-form-error').inner_text().lower(),width
        if width in (390,740):
            page.screenshot(path=f'/mnt/data/conferatus_v0115_unreadable_{width}.png',full_page=True)
        title='Proposta recuperada após falha de JSON'
        save_new(page,title)
        backup=json.loads(page.evaluate('key=>sessionStorage.getItem(key)',RAW_BACKUP_KEY))
        assert backup=={'drafts':broken_draft,'schedule':wrong_shape},(width,backup)
        snapshot={k:page.evaluate('key=>sessionStorage.getItem(key)',k)
                  for k in (DRAFT_KEY,SCHEDULE_KEY,RAW_BACKUP_KEY)}
        assert json.loads(snapshot[DRAFT_KEY])[0]['title']==title,width
        assert json.loads(snapshot[SCHEDULE_KEY])==[],width
        assert not errors,(width,errors)
        page.close()
        # Reconstruct the app in a new document from the exact serialized values:
        # about:blank is storage-restricted in this test runtime, so storage is mocked.
        page=boot(browser,width,snapshot)
        proposals(page)
        page.locator('.workflow-record').filter(has_text=title).wait_for()
        assert page.locator('.workflow-form-error').count()==0,width
        assert json.loads(page.evaluate('key=>sessionStorage.getItem(key)',RAW_BACKUP_KEY))==backup,width
        page.close()

        forged={'id':'false-complete','title':'Falsa conclusão','body':'Rascunho não assinado por todas as partes.',
                'sectionId':'integridade','type':'PDR','authorComplete':False,
                'partners':[{'id':'m02','complete':False}],'status':'concluida'}
        genuine={**forged,'id':'true-complete','title':'Conclusão verificável',
                 'authorComplete':True,'partners':[{'id':'m02','complete':True}]}
        page=boot(browser,width,{DRAFT_KEY:json.dumps([forged,genuine]),SCHEDULE_KEY:'[]'})
        proposals(page)
        page.locator('.workflow-record').filter(has_text='Conclusão verificável').wait_for()
        assert page.locator('.workflow-record').filter(has_text='Falsa conclusão').count()==0,width
        assert page.locator('.workflow-record').filter(has_text='Conclusão verificável').count()==1,width
        save_new(page,'Novo texto mantendo sessão íntegra')
        rejected=json.loads(page.evaluate('key=>sessionStorage.getItem(key)',INVALID_BACKUP_KEY))
        assert [d['id'] for d in rejected['drafts']]==['false-complete'],(width,rejected)
        current=json.loads(page.evaluate('key=>sessionStorage.getItem(key)',DRAFT_KEY))
        assert 'true-complete' in [d['id'] for d in current],width
        assert 'false-complete' not in [d['id'] for d in current],width
        # Only an actual completed record may be scheduled.
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=calendar]').click()
        page.locator('[data-action=open-schedule]').click()
        options=page.locator('select[name=proposalId] option').all_text_contents()
        assert 'Conclusão verificável' in options and 'Falsa conclusão' not in options,(width,options)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        page.close()
    browser.close()
print('Unreadable storage preserved, restored draft retained, forged signoff rejected at 4 widths: OK')
