"""Document-level alignment, independent indents and line-height roundtrip."""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE=os.environ.get('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
BODY='Texto de teste para alinhamento e espaçamento independente.\nSegunda linha preservada integralmente.'

with sync_playwright() as p:
 options={'headless':True}
 if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
  options.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 browser=getattr(p,ENGINE).launch(**options)
 for width in (280,320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank?rich-layout=1')
  page.evaluate("""() => {
   const data=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,String(v)),
    removeItem:k=>data.delete(k),clear:()=>data.clear()
   }});
  }""")
  page.set_content(HTML)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill(f'Alinhamento e recuos {width}')
  page.locator('#draft-body').fill(BODY)
  page.locator('[data-action=enable-rich-editor]').click()
  editor=page.locator('#draft-rich-body')
  editor.wait_for(state='visible')
  page.evaluate("""() => {
   const n=document.querySelector('#draft-rich-body').firstChild;
   const selection=getSelection(),range=document.createRange();
   range.setStart(n,0);range.setEnd(n,5);
   selection.removeAllRanges();selection.addRange(range);
  }""")
  page.locator('[data-rich-command=bold]').click()
  assert editor.locator('strong,b').count()>0,width
  page.locator('[data-rich-layout=align]').select_option('justify')
  page.locator('[data-rich-layout=left]').select_option('16')
  page.locator('[data-rich-layout=right]').select_option('32')
  page.locator('[data-rich-layout=lineHeight]').select_option('2')
  layout=editor.evaluate("""e => {
   const s=getComputedStyle(e);
   return {align:s.textAlign,left:s.paddingLeft,right:s.paddingRight,height:s.lineHeight,text:e.textContent};
  }""")
  assert layout['align']=='justify',(width,layout)
  assert layout['left']=='23px' and layout['right']=='39px',(width,layout)
  assert layout['height']=='28px',(width,layout)
  assert layout['text']==BODY,(width,layout)
  page.locator('#compose-proposal-form [value=save]').click()
  saved=page.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  assert len(saved)==1,width
  assert saved[0]['bodyLayout']=={'align':'justify','left':16,'right':32,'lineHeight':2},(width,saved)
  assert saved[0]['body']==BODY,(width,saved)
  assert any('bold' in run['marks'] for run in saved[0].get('bodyRuns',[])),(width,saved)
  page.locator('.workflow-record').filter(has_text=f'Alinhamento e recuos {width}').locator('[data-draft]').click()
  editor.wait_for(state='visible')
  assert editor.evaluate("e=>getComputedStyle(e).paddingRight")=='39px',width
  assert editor.locator('strong,b').count()>0,width
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  paragraph=page.locator('.workflow-review-body p')
  rendered=paragraph.evaluate("""e => {
   const s=getComputedStyle(e);
   return {align:s.textAlign,left:s.paddingLeft,right:s.paddingRight,height:e.style.lineHeight,text:e.textContent};
  }""")
  assert rendered=={'align':'justify','left':'16px','right':'32px','height':'2','text':BODY},(width,rendered)
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-record').filter(has_text=f'Alinhamento e recuos {width}').locator('[data-draft]').click()
  page.locator('.workflow-finished').wait_for(state='visible')
  assert page.locator('.workflow-review-body p').evaluate("e=>getComputedStyle(e).textAlign")=='justify',width
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
Path('dist',f'cross_engine_rich_layout_{ENGINE}.json').write_text(
 json.dumps({'engine':ENGINE,'widths':[280,320,390,740,1280],'status':'pass'},indent=2),encoding='utf-8')
print(f'Rich layout {ENGINE}: 5 widths; alignment, indents, line height and save/review PASS')
