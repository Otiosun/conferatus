"""Richer typography survives save, reopening and completed proposal review."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
import json
ENGINE=os.environ.get('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
 options={'headless':True}
 if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
  options.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 browser=getattr(p,ENGINE).launch(**options)
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?rich-typography=1')
  page.evaluate("""() => {
   const store=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),
    removeItem:k=>store.delete(k),clear:()=>store.clear()
   }});
  }""")
  page.set_content(HTML)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill(f'Fontes e cores {width}')
  page.locator('#draft-body').fill('Texto personalizado de exemplo com conteúdo suficiente.')
  page.locator('[data-action=enable-rich-editor]').click()
  editor=page.locator('#draft-rich-body')
  editor.wait_for(state='visible')
  page.evaluate("""() => {
   const node=document.querySelector('#draft-rich-body').firstChild;
   const sel=getSelection(),r=document.createRange();
   r.setStart(node,0);r.setEnd(node,5);
   sel.removeAllRanges();sel.addRange(r);
  }""")
  page.locator('[data-rich-format=font]').select_option('aptos')
  page.locator('[data-rich-format=size]').select_option('24')
  page.locator('[data-rich-format=color]').fill('#123abc')
  page.locator('[data-rich-format=highlight]').fill('#ffef99')
  page.locator('#compose-proposal-form [value=save]').click()
  saved=page.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  runs=saved[0].get('bodyRuns',[])
  assert any(run.get('font')=='aptos' and run.get('size')==24 and
             run.get('color')=='#123abc' and run.get('highlight')=='#ffef99'
             for run in runs),(width,runs)
  page.locator('.workflow-record').filter(has_text=f'Fontes e cores {width}').locator('[data-draft]').click()
  editor.wait_for(state='visible')
  assert editor.locator('span[style*="font-size:24px"]').count()>0,width
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  assert page.locator('.workflow-review-body span[style*="background-color:#ffef99"]').count()>0,width
  assert page.locator('.workflow-review-body').inner_text().strip()=='Texto personalizado de exemplo com conteúdo suficiente.',width
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-record').filter(has_text=f'Fontes e cores {width}').locator('[data-draft]').click()
  page.locator('.workflow-finished').wait_for(state='visible')
  assert page.locator('.workflow-review-body span[style*="font-size:24px"]').count()>0,width
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
Path('dist',f'cross_engine_rich_typography_{ENGINE}.json').write_text(json.dumps({'engine':ENGINE,'widths':[320,390,740,1280],'status':'pass'},indent=2),encoding='utf-8')
print(f'Rich typography {ENGINE}: 4 widths, font/size/color/highlight PASS')
