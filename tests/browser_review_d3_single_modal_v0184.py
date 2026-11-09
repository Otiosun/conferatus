"""D3 reference variant is an opt-in native modal, not Academy policy.

The existing confirmation submit handler must remain the sole data-changing path.
Checks focus, refusal to discard, history navigation, and unchanged default.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width in (280,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(9000)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1&d3=single')
  page.evaluate("""() => {
   const store=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>store.get(k)??null,
    setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)
   }});
  }""")
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('D3 confirmação experimental')
  page.locator('#draft-body').fill('Conteúdo demonstrativo para validar a confirmação sem efeitos institucionais.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  modal=page.locator('#d3-review-dialog')
  modal.wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/review',(engine,width,'review route')
  assert modal.evaluate('(d)=>d.open&&d.matches(":modal")'),(engine,width,'not a native modal')
  assert modal.locator('#confirm-proposal-form').count()==1,(engine,width,'shared form not reused')
  assert modal.locator('.workflow-review-buttons button').count()==1,(engine,width,'expected one primary action')
  assert modal.locator('.workflow-review-buttons button').inner_text().strip()=='CONFIRMAR',(engine,width,'wrong primary text')
  assert modal.locator('[data-dismiss-d3-review]').count()==1,(engine,width,'missing accessible way out')
  assert modal.locator('[data-dismiss-d3-review]').get_attribute('aria-label'),(engine,width,'close has no accessible label')
  assert modal.locator('[data-dismiss-d3-review]').bounding_box()['height']>=44,(engine,width,'close too small')
  assert modal.locator('[name=sectionId]').evaluate('(el)=>document.activeElement===el'),(engine,width,'initial focus')
  assert 'blur' in page.locator('.workflow-review-body--d3').evaluate('(el)=>getComputedStyle(el).filter'),(engine,width,'document not blurred')
  assert page.locator('.workflow-editor-head').evaluate('(el)=>getComputedStyle(el).filter')=='none',(engine,width,'title should remain sharp')
  assert modal.bounding_box()['x']>=-1 and modal.bounding_box()['width']<=width+1,(engine,width,'modal width')
  for key in ['Tab']*10+['Shift+Tab']*5:
   page.keyboard.press(key)
   assert modal.evaluate('(el)=>el.contains(document.activeElement)'),(engine,width,'focus escaped modal')
  # Unedited exit is allowed; the same proposal remains available to revise.
  page.keyboard.press('Escape')
  page.locator('#compose-proposal-form').wait_for(state='visible')
  assert page.locator('#compose-proposal-form [value=conclude]').evaluate('(el)=>document.activeElement===el'),(engine,width,'focus did not return to editor action')
  assert page.locator('#draft-title').input_value()=='D3 confirmação experimental',(engine,width,'return lost proposal')
  page.locator('#compose-proposal-form [value=conclude]').click()
  modal.wait_for(state='visible')
  form=modal.locator('#confirm-proposal-form')
  old_section=form.locator('[name=sectionId]').input_value()
  old_type=form.locator('[name=type]').input_value()
  section=next(s for s in form.locator('[name=sectionId] option').evaluate_all('(xs)=>xs.map(x=>x.value)') if s!=old_section)
  typ=next(t for t in form.locator('[name=type] option').evaluate_all('(xs)=>xs.map(x=>x.value)') if t!=old_type)
  form.locator('[name=sectionId]').select_option(section)
  form.locator('[name=type]').select_option(typ)
  # A modal must keep the unconfirmed data when a same-route rerender occurs.
  page.evaluate("window.dispatchEvent(new HashChangeEvent('hashchange'))")
  modal=page.locator('#d3-review-dialog');modal.wait_for(state='visible')
  form=modal.locator('#confirm-proposal-form')
  assert form.locator('[name=sectionId]').input_value()==section,(engine,width,'section lost on rerender')
  assert form.locator('[name=type]').input_value()==typ,(engine,width,'type lost on rerender')
  page.once('dialog',lambda d:d.dismiss())
  page.keyboard.press('Escape')
  assert modal.is_visible() and page.evaluate('location.hash')=='#/review',(engine,width,'declined Escape discarded values')
  page.once('dialog',lambda d:d.dismiss())
  modal.locator('[data-dismiss-d3-review]').click()
  assert modal.is_visible(),(engine,width,'declined close discarded values')
  page.once('dialog',lambda d:d.dismiss())
  page.evaluate("location.hash='#/proposals'")
  page.wait_for_timeout(90)
  assert modal.is_visible() and page.evaluate('location.hash')=='#/review',(engine,width,'declined history navigation discarded values')
  assert form.locator('[name=sectionId]').input_value()==section,(engine,width,'choices not preserved')
  form.locator('button[type=submit]').click()
  page.locator('#d3-review-dialog').wait_for(state='detached')
  drafts=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
  assert len(drafts)==1 and drafts[0]['sectionId']==section and drafts[0]['type']==typ,(engine,width,'submit changed contract')
  assert not errors,(engine,width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(engine,width,'horizontal overflow')
  page.close()
 # No flag or no demo: original two visible review actions and no modal.
 for suffix in ('?demo=1','?d3=single'):
  page=browser.new_page(viewport={'width':390,'height':850})
  page.goto('about:blank'+suffix)
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Normal sem D3')
  page.locator('#draft-body').fill('Corpo demonstrativo suficiente para a revisão padrão da proposição.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  # Hash routing is asynchronous: assert the standard review AFTER it renders.
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  assert page.locator('#d3-review-dialog').count()==0,(engine,suffix,'D3 leaked to standard')
  assert page.locator('#confirm-proposal-form .workflow-review-buttons button').count()==2,(engine,suffix,'standard actions changed')
  page.close()
 browser.close()
print('PASS: opt-in D3 dialog, guarded exits, focus, save and default isolation; '+engine)
