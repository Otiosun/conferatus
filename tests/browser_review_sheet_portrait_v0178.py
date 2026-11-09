"""Megalos' review sheet remains reachable while a long document is readable.

Only the existing two-button state is tested. The separate blurred single-button
reference is NOT implemented without a contract. All records stay fictional.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
cases=((280,844),(320,844),(390,844),(540,844),(390,560),(740,844))
with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width,height in cases:
  page=browser.new_page(viewport={'width':width,'height':height})
  page.set_default_timeout(7000)
  errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto('about:blank')
  page.evaluate("""() => {
    const values=new Map();
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
     getItem:k=>values.get(k)??null,
     setItem:(k,v)=>values.set(k,String(v)),
     removeItem:k=>values.delete(k)
    }});
  }""")
  page.set_content(html)
  page.evaluate('location.hash="#/proposals"')
  page.locator('[data-action=new-proposal]').wait_for(state='visible')
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Documento de revisão extensa')
  body='Texto completo para revisar o documento antes de confirmar a conclusão. '*90
  page.locator('#draft-body').fill(body)
  page.locator('#compose-proposal-form [value=conclude]').click()
  form=page.locator('#confirm-proposal-form')
  form.wait_for(state='visible')
  panel=page.locator('.workflow-review-panel--pending')
  assert panel.count()==1,(width,'pending panel not distinct from finished state')
  box=panel.bounding_box()
  assert box is not None,(width,'panel hidden')
  sticky=(width<=600 and height>=680)
  if sticky:
   assert panel.evaluate('(el)=>getComputedStyle(el).position')=='sticky',width
   assert abs(box['y']+box['height']-height)<3,(width,'panel not reachable at viewport bottom',box)
   assert box['y']>=60,(width,'panel consumes entire visible reading area',box)
   cancel=form.get_by_role('button',name='Cancelar confirmação e voltar à redação')
   confirm=form.get_by_role('button',name='Confirmar',exact=True)
   for button in (cancel,confirm):
    b=button.bounding_box()
    assert b and b['y']>=0 and b['y']+b['height']<=height+2,(width,'button outside viewport',b)
    assert b['height']>=44,(width,'target too small',b)
   page.evaluate('window.scrollTo(0,400)')
   page.wait_for_timeout(60)
   assert page.evaluate('scrollY')>=100,(width,'unable to read long proposal by scrolling')
   after=panel.bounding_box()
   assert abs(after['y']+after['height']-height)<3,(width,'sheet no longer reachable while reading',after)
  else:
   assert panel.evaluate('(el)=>getComputedStyle(el).position')!='sticky',(width,height)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'horizontal overflow')
  form.get_by_role('button',name='Cancelar confirmação e voltar à redação').click()
  page.locator('#draft-title').wait_for(state='visible')
  assert page.locator('#draft-body').input_value()==body,(width,'cancel lost the document')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-record').filter(has_text='Documento de revisão extensa').wait_for(state='visible')
  assert not errors,(width,height,errors)
  page.close()
 browser.close()
print('PASS: portrait review sheet geometry, scroll, cancel/confirm, no overflow, '+engine)
