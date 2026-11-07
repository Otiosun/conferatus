"""Subscript/superscript roundtrip in four viewports and all browser engines."""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE=os.environ.get('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
BODY='Na fórmula H2O, a unidade m2 representa uma medida de área neste documento.'

def select_character(page, needle, shift):
 page.evaluate("""([needle,shift]) => {
  const editor=document.querySelector('#draft-rich-body');
  const value=editor.textContent??'';
  const at=value.indexOf(needle);
  if(at<0)throw Error('Needle missing from editor');
  const index=at+shift;
  let offset=0,found=false;
  const walker=document.createTreeWalker(editor,NodeFilter.SHOW_TEXT);
  for(let n=walker.nextNode();n;n=walker.nextNode()){
   const len=n.textContent?.length??0;
   if(index<offset+len){
    const sel=getSelection(),range=document.createRange();
    range.setStart(n,index-offset);
    range.setEnd(n,index-offset+1);
    sel.removeAllRanges();sel.addRange(range);
    found=true;break;
   }
   offset+=len;
  }
  if(!found)throw Error('Character not found in a text node');
 }""",[needle,shift])

with sync_playwright() as p:
 opts={'headless':True}
 if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
  opts.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 browser=getattr(p,ENGINE).launch(**opts)
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto('about:blank?indices=1')
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
  page.locator('#draft-title').fill(f'Notação científica {width}')
  page.locator('#draft-body').fill(BODY)
  page.locator('[data-action=enable-rich-editor]').click()
  editor=page.locator('#draft-rich-body')
  editor.wait_for(state='visible')
  select_character(page,'H2O',1)
  page.locator('[data-rich-command=subscript]').click()
  assert editor.locator('sub').count()>0,(ENGINE,width,editor.inner_html())
  select_character(page,'m2',1)
  page.locator('[data-rich-command=superscript]').click()
  assert editor.locator('sup').count()>0,(ENGINE,width,editor.inner_html())
  assert editor.text_content()==BODY,(ENGINE,width,editor.text_content())
  page.locator('#compose-proposal-form [value=save]').click()
  saved=page.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  assert len(saved)==1,(ENGINE,width)
  assert saved[0]['body']==BODY,(ENGINE,width,saved)
  runs=saved[0].get('bodyRuns',[])
  assert any('subscript' in r['marks'] for r in runs),(ENGINE,width,runs)
  assert any('superscript' in r['marks'] for r in runs),(ENGINE,width,runs)
  assert all(not ('subscript' in r['marks'] and 'superscript' in r['marks']) for r in runs),(ENGINE,width,runs)
  page.locator('.workflow-record').filter(has_text=f'Notação científica {width}').locator('[data-draft]').click()
  editor.wait_for(state='visible')
  assert editor.locator('sub').count()>0 and editor.locator('sup').count()>0,(ENGINE,width)
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  review=page.locator('.workflow-review-body')
  assert review.locator('sub').count()>0 and review.locator('sup').count()>0,(ENGINE,width,review.inner_html())
  assert review.inner_text().strip()==BODY,(ENGINE,width,review.inner_text())
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-record').filter(has_text=f'Notação científica {width}').locator('[data-draft]').click()
  page.locator('.workflow-finished').wait_for(state='visible')
  assert page.locator('.workflow-review-body sub').count()>0 and page.locator('.workflow-review-body sup').count()>0,(ENGINE,width)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(ENGINE,width)
  assert not errors,(ENGINE,width,errors)
  page.close()
 browser.close()
Path('dist',f'cross_engine_rich_indices_{ENGINE}.json').write_text(json.dumps({
 'engine':ENGINE,'widths':[320,390,740,1280],'status':'pass'
},indent=2),encoding='utf-8')
print(f'Inline subscripts/superscripts {ENGINE}: 4 widths, save/reopen/review PASS')
