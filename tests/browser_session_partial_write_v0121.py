"""A failed second sessionStorage write must not partially persist an edited draft."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
base={'id':'stable-draft','title':'Redação original','body':'Este texto anterior permanece armazenado até ambas as operações locais serem bem-sucedidas.', 'sectionId':'integridade','type':'PDR','authorComplete':False,'partners':[],'status':'redacao'}

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (320,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':844})
        page.set_default_timeout(6500)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('about:blank?demo=1')
        page.evaluate('''original=>{
            const values=new Map([['conferatus:proposals-v010',original]]);
            let failScheduleOnce=true;
            Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
              getItem:k=>values.has(k)?values.get(k):null,
              setItem(k,v){if(k==='conferatus:deliberations-v010'&&failScheduleOnce){failScheduleOnce=false;throw new Error('Simulated session quota failure')}values.set(k,v)},
              removeItem:k=>values.delete(k)
            }});
        }''',json.dumps([base]))
        page.set_content(html)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route=proposals]').click()
        page.locator('[data-draft="stable-draft"]').click()
        page.locator('#draft-title').fill('Redação nova não confirmada em armazenamento')
        page.locator('#compose-proposal-form [value=save]').click()
        assert 'somente enquanto a página estiver aberta' in page.locator('.workflow-status').inner_text(),width
        if width in (390,740):
            page.screenshot(path=f'/mnt/data/conferatus_v0121_storage_recovery_{width}.png',full_page=True)
        stored=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
        assert stored==[base],f'{width}: partial session write changed stored draft even though operation failed: {stored}'
        page.locator('[data-draft="stable-draft"]').click()
        page.locator('#compose-proposal-form [value=save]').click()
        assert 'Rascunho salvo nesta sessão' in page.locator('.workflow-status').inner_text(),width
        stored=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
        assert stored[0]['title']=='Redação nova não confirmada em armazenamento',width
        assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')==[],width
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        page.close()

        # The first-ever save must remove the newly created key if its paired write fails.
        fresh=browser.new_page(viewport={'width':width,'height':844})
        fresh.goto('about:blank?demo=1')
        fresh.evaluate('''()=>{
          const values=new Map();let failed=false;
          Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
            getItem:k=>values.has(k)?values.get(k):null,
            setItem(k,v){if(k==='conferatus:deliberations-v010'&&!failed){failed=true;throw new Error('Simulated failed second key')}values.set(k,v)},
            removeItem:k=>values.delete(k)
          }});
        }''')
        fresh.set_content(html)
        fresh.locator('.footer-nav').click()
        fresh.locator('.menu-item[data-route=proposals]').click()
        fresh.locator('[data-action=new-proposal]').click()
        fresh.locator('#draft-title').fill('Rascunho novo no primeiro salvamento')
        fresh.locator('#draft-body').fill('Texto demonstrativo em que uma nova gravação deve ser totalmente revertida.')
        fresh.locator('#compose-proposal-form [value=save]').click()
        assert 'somente enquanto a página estiver aberta' in fresh.locator('.workflow-status').inner_text(),width
        assert fresh.evaluate('sessionStorage.getItem("conferatus:proposals-v010")') is None,width
        assert fresh.evaluate('sessionStorage.getItem("conferatus:deliberations-v010")') is None,width
        fresh.close()
    browser.close()
print('Partial session rollback covers existing and new drafts in four widths: OK')
