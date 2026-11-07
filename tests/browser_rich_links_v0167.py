"""User-selected secure hyperlinks: validation, persistence, safe rendering and removal."""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE=os.environ.get('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
BODY='Uma referência externa & texto <img src=x onerror=window.bad=1> para análise do conteúdo.'
HREF='https://example.com/material?tema=texto&modo=leitura'

def select_phrase(page,phrase):
 page.evaluate("""phrase => {
  const editor=document.querySelector('#draft-rich-body');
  const text=editor.textContent??'';
  const begin=text.indexOf(phrase);
  if(begin<0)throw Error('Selection phrase missing');
  let offset=0,startNode=null,start=0,endNode=null,end=0;
  const walker=document.createTreeWalker(editor,NodeFilter.SHOW_TEXT);
  for(let n=walker.nextNode();n;n=walker.nextNode()){
   const length=n.textContent?.length??0;
   if(!startNode&&begin>=offset&&begin<offset+length){
    startNode=n;start=begin-offset;
   }
   if(startNode&&begin+phrase.length<=offset+length){
    endNode=n;end=begin+phrase.length-offset;break;
   }
   offset+=length;
  }
  if(!startNode||!endNode)throw Error('Cannot select phrase across text');
  const range=document.createRange(),selection=getSelection();
  range.setStart(startNode,start);range.setEnd(endNode,end);
  selection.removeAllRanges();selection.addRange(range);
 }""",phrase)

def start_draft(page,title,body):
 page.locator('.footer-nav').click()
 page.locator('.menu-item[data-route=proposals]').click()
 page.locator('[data-action=new-proposal]').click()
 page.locator('#draft-title').fill(title)
 page.locator('#draft-body').fill(body)
 page.locator('[data-action=enable-rich-editor]').click()
 page.locator('#draft-rich-body').wait_for(state='visible')

with sync_playwright() as p:
 opts={'headless':True}
 if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
  opts.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 browser=getattr(p,ENGINE).launch(**opts)
 for width in (280,320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?richlinks=1')
  page.evaluate("""() => {
   const store=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),
    removeItem:k=>store.delete(k),clear:()=>store.clear()
   }});
  }""")
  page.set_content(HTML)
  title=f'Links seguros {width}'
  start_draft(page,title,BODY)
  feedback=page.locator('#draft-link-feedback')
  # No selected text must not create a link.
  page.locator('#draft-link-url').fill(HREF)
  page.locator('[data-rich-link=apply]').click()
  assert 'Selecione um trecho' in feedback.inner_text(),(ENGINE,width,feedback.inner_text())
  assert page.locator('#draft-rich-body a').count()==0,(ENGINE,width)
  select_phrase(page,'referência externa')
  # javascript/data/credential URLs cannot ever produce active anchors.
  for hostile in ('javascript:alert(1)','data:text/html,bad','https://user:pass@example.com'):
   page.locator('#draft-link-url').fill(hostile)
   page.locator('[data-rich-link=apply]').click()
   assert page.locator('#draft-link-url').get_attribute('aria-invalid')=='true',(ENGINE,width,hostile)
   assert page.locator('#draft-rich-body a').count()==0,(ENGINE,width,hostile)
  page.locator('#draft-link-url').fill(HREF)
  page.locator('[data-rich-link=apply]').click()
  anchor=page.locator('#draft-rich-body a')
  assert anchor.count()==1,(ENGINE,width,page.locator('#draft-rich-body').inner_html())
  assert anchor.inner_text()=='referência externa',(ENGINE,width,anchor.inner_text())
  assert anchor.get_attribute('href')==HREF,(ENGINE,width,anchor.get_attribute('href'))
  assert feedback.inner_text()=='Link inserido no trecho selecionado.',(ENGINE,width,feedback.inner_text())
  # Editing link text never navigates to the external site.
  previous=page.url
  anchor.click()
  assert page.url==previous,(ENGINE,width,page.url)
  assert page.locator('#draft-rich-body').inner_text()==BODY,(ENGINE,width)
  page.locator('#compose-proposal-form [value=save]').click()
  saved=page.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  assert len(saved)==1 and saved[0]['body']==BODY,(ENGINE,width,saved)
  assert any(r.get('href')==HREF for r in saved[0].get('bodyRuns',[])),(ENGINE,width,saved)
  page.locator('.workflow-record').filter(has_text=title).locator('[data-draft]').click()
  page.locator('#draft-rich-body').wait_for(state='visible')
  assert page.locator('#draft-rich-body a').get_attribute('href')==HREF,(ENGINE,width)
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  review=page.locator('.workflow-review-body')
  link=review.locator('a')
  assert link.count()==1,(ENGINE,width,review.inner_html())
  assert link.get_attribute('href')==HREF,(ENGINE,width)
  assert link.get_attribute('target')=='_blank',(ENGINE,width)
  assert {'noopener','noreferrer'}.issubset(set(link.get_attribute('rel').split())),(ENGINE,width)
  assert review.locator('img,script,svg').count()==0,(ENGINE,width,review.inner_html())
  assert review.inner_text().strip()==BODY,(ENGINE,width,review.inner_text())
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-record').filter(has_text=title).locator('[data-draft]').click()
  page.locator('.workflow-finished').wait_for(state='visible')
  assert page.locator('.workflow-review-body a').count()==1,(ENGINE,width)
  # A separate draft verifies that removal actually eliminates persisted link metadata.
  page.evaluate('location.hash="#/proposals"')
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill(f'Remover links {width}')
  page.locator('#draft-body').fill('Este parágrafo é suficiente para testar a remoção de referências seguras.')
  page.locator('[data-action=enable-rich-editor]').click()
  page.locator('#draft-rich-body').wait_for(state='visible')
  select_phrase(page,'referências')
  page.locator('#draft-link-url').fill(HREF)
  page.locator('#draft-link-url').press('Enter')
  assert page.locator('#compose-proposal-form').count()==1,(ENGINE,width,'Enter unexpectedly submitted the proposal')
  assert page.locator('#draft-rich-body a').count()==1,(ENGINE,width)
  select_phrase(page,'referências')
  page.locator('[data-rich-link=remove]').click()
  assert page.locator('#draft-rich-body a').count()==0,(ENGINE,width,page.locator('#draft-rich-body').inner_html())
  page.locator('#compose-proposal-form [value=save]').click()
  records=page.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  draft=next(r for r in records if r['title']==f'Remover links {width}')
  assert all(not r.get('href') for r in draft.get('bodyRuns',[])),(ENGINE,width,draft)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(ENGINE,width)
  assert not errors,(ENGINE,width,errors)
  page.close()
 browser.close()
Path('dist',f'cross_engine_rich_links_{ENGINE}.json').write_text(json.dumps({
 'engine':ENGINE,'widths':[280,320,390,740,1280],'status':'pass'
},indent=2),encoding='utf-8')
print(f'Safe rich links {ENGINE}: five widths, apply/remove/save/reopen/review PASS')
