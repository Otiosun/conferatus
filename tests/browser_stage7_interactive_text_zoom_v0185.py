"""Stage 07.05: interactive reflow with 200% synthetic text and compact widths.

Covers the full local compose/review path, not only static route overflow.
Does NOT certify native 400% browser zoom, screen readers, or physical devices.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(280,320,390,740)
ROUTES=('ballot','members','overview','calendar','proposals','history')

def enlarge_text(page):
 page.evaluate("""() => {
  for(const el of document.querySelectorAll('body *')){
   if(el.dataset.stage7Text200 || ![...el.childNodes].some(n=>n.nodeType===3 && n.textContent.trim()))continue;
   const size=parseFloat(getComputedStyle(el).fontSize);
   if(size>0 && size<100){el.style.setProperty('font-size',(2*size)+'px','important');el.dataset.stage7Text200='1';}
  }
 }""")

def measure(page,width,engine,mode,route):
 metrics=page.evaluate("""() => {
  const e=document.documentElement,footer=document.querySelector('.app-footer'),menu=document.querySelector('.footer-nav');
  const f=footer.getBoundingClientRect(),m=menu.getBoundingClientRect();
  return {viewport:innerWidth,documentWidth:e.scrollWidth,
   footerLeft:f.left,footerRight:f.right,menuLeft:m.left,menuRight:m.right,
   menuHeight:m.height};
 }""")
 assert metrics['documentWidth']<=width+1,(engine,mode,width,route,'horizontal overflow',metrics)
 assert metrics['menuLeft']>=metrics['footerLeft']-1 and metrics['menuRight']<=metrics['footerRight']+1,(engine,mode,width,route,'menu clipped',metrics)

with sync_playwright() as pw:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(pw,engine).launch(headless=True))
 cases=0
 for width in WIDTHS:
  for mode in ('default','synthetic-text-200'):
   page=browser.new_page(viewport={'width':width,'height':720})
   page.set_default_timeout(9000)
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('about:blank?demo=1')
   page.evaluate("""() => {
    const values=new Map();
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
     getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,String(v)),
     removeItem:k=>values.delete(k)
    }});
   }""")
   page.set_content(HTML)
   if mode!='default':enlarge_text(page)
   for route in ROUTES:
    page.evaluate('(r)=>{location.hash="#/"+r}',route)
    # Wait for a route-specific element, not just the hash update.
    target={'ballot':'.app-footer','members':'.member-item',
            'overview':'.overview-stats','calendar':'.calendar-month-nav',
            'proposals':'[data-action=new-proposal]',
            'history':'.history-tabs'}[route]
    page.locator(target).first.wait_for(state='visible')
    if mode!='default':enlarge_text(page)
    measure(page,width,engine,mode,route)
    cases+=1
   page.evaluate('location.hash="#/proposals"')
   page.locator('[data-action=new-proposal]').click()
   page.locator('#draft-title').fill('Reflow de teste')
   page.locator('#draft-body').fill('Proposição fictícia criada para verificar o formulário e a confirmação com texto ampliado.')
   if mode!='default':enlarge_text(page)
   measure(page,width,engine,mode,'compose')
   cases+=1
   page.locator('.footer-nav').click()
   assert page.locator('#draft-title').input_value()=='Reflow de teste',(engine,mode,width,'draft lost')
   page.locator('.footer-nav').click()
   page.locator('#compose-proposal-form [value=conclude]').click()
   page.locator('#confirm-proposal-form').wait_for(state='visible')
   if mode!='default':enlarge_text(page)
   measure(page,width,engine,mode,'review')
   cases+=1
   review=page.locator('#confirm-proposal-form')
   page.locator('.footer-nav').click()
   assert review.is_visible(),(engine,mode,width,'review hidden on menu open')
   page.locator('.footer-nav').click()
   review.locator('button[type=submit]').click()
   page.locator('.workflow-record').filter(has_text='Reflow de teste').wait_for(state='visible')
   assert not errors,(engine,mode,width,'javascript exceptions',errors)
   page.close()
 browser.close()
assert cases==len(WIDTHS)*2*8,(engine,cases,'incomplete matrix')
print('PASS: 64 compact and synthetic 200% text interactive reflow cases; '+engine)
