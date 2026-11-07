"""Formatting must survive proposal save, reopen and review; markup remains literal."""
from pathlib import Path
from playwright.sync_api import sync_playwright
html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  pg=browser.new_page(viewport={'width':width,'height':840})
  errors=[]
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.goto('about:blank?rich=1')
  pg.evaluate("""() => {
   const m=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>m.get(k)??null,setItem:(k,v)=>m.set(k,String(v)),
    removeItem:k=>m.delete(k),clear:()=>m.clear()
   }});
  }""")
  pg.set_content(html)
  pg.locator('.footer-nav').click()
  pg.locator('.menu-item[data-route=proposals]').click()
  pg.locator('[data-action=new-proposal]').click()
  pg.locator('#draft-title').fill(f'Proposta formatada {width}')
  pg.locator('#draft-body').fill('Texto para aplicar formato e preservar a revisão.')
  pg.locator('[data-action=enable-rich-editor]').click()
  editor=pg.locator('#draft-rich-body')
  assert editor.is_visible(),width
  pg.evaluate("""() => {
   const n=document.querySelector('#draft-rich-body').firstChild;
   const r=document.createRange(),s=getSelection();
   r.setStart(n,0);r.setEnd(n,5);s.removeAllRanges();s.addRange(r);
  }""")
  pg.locator('[data-rich-command=bold]').click()
  assert 'Texto' in editor.locator('strong,b').inner_text(),(width,editor.inner_html())
  before_save=editor.inner_html()
  pg.locator('#compose-proposal-form [value=save]').click()
  saved_draft=pg.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  record=pg.locator('.workflow-record').filter(has_text=f'Proposta formatada {width}')
  record.locator('[data-draft]').click()
  pg.locator('#draft-rich-body').wait_for(state='visible')
  reopened=pg.evaluate("""() => ({path:location.hash,
   editor:document.querySelector('#draft-rich-body')?.innerHTML ?? null,
   body:document.querySelector('#draft-body')?.value ?? null})""")
  assert pg.locator('#draft-rich-body strong,#draft-rich-body b').count()>0,(width,before_save,saved_draft,reopened)
  pg.locator('#compose-proposal-form [value=conclude]').click()
  pg.locator('#confirm-proposal-form').wait_for(state='visible')
  assert pg.locator('.workflow-review-body strong').count()>0,width
  pg.locator('#confirm-proposal-form button[type=submit]').click()
  pg.locator('.workflow-record').filter(has_text=f'Proposta formatada {width}').locator('[data-draft]').click()
  pg.locator('.workflow-finished').wait_for(state='visible')
  assert pg.locator('.workflow-review-body strong').count()>0,width
  pg.evaluate('location.hash="#/proposals"')
  pg.locator('[data-action=new-proposal]').click()
  pg.locator('#draft-title').fill('Texto literal seguro')
  pg.locator('#draft-body').fill('Texto inicial preenchido antes da formatação.')
  pg.locator('[data-action=enable-rich-editor]').click()
  pg.locator('#draft-rich-body').fill('<img src=x onerror=window.__test=1> & <svg onload=window.__test=2></svg>')
  # Format part of the *literal* markup so restoration must use the safe renderer.
  pg.evaluate("""() => {
   const n=document.querySelector('#draft-rich-body').firstChild;
   const r=document.createRange(),s=getSelection();
   r.setStart(n,0);r.setEnd(n,4);s.removeAllRanges();s.addRange(r);
  }""")
  pg.locator('[data-rich-command=bold]').click()
  pg.locator('#compose-proposal-form [value=save]').click()
  pg.locator('.workflow-record').filter(has_text='Texto literal seguro').locator('[data-draft]').click()
  pg.locator('#draft-rich-body').wait_for(state='visible')
  assert pg.locator('#draft-rich-body strong').count()>0,width
  assert pg.locator('#draft-rich-body img,#draft-rich-body svg').count()==0,width
  assert '<img src=x' in pg.locator('#draft-rich-body').inner_text(),width
  assert not errors,(width,errors)
  assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  pg.close()
 browser.close()
print('Proposal rich editor formatting/roundtrips/literal markup 4 widths PASS')
