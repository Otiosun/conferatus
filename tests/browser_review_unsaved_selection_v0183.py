"""Keep unconfirmed section and proposal type on the SAME review sheet rerender.

Synthetic local data only. This doesn't imply real Academy sign-offs or votes.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as pw:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(pw,engine).launch(headless=True))
 for width in (280,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(8000)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank?demo=1')
  page.evaluate("""() => {
   const store=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),
    removeItem:k=>store.delete(k)
   }});
  }""")
  page.set_content(html)
  def menu(route):
   page.locator('.footer-nav').click()
   page.locator(f'.menu-item[data-route="{route}"]').click()
  def open_new_draft(title):
   menu('proposals')
   page.locator('[data-action=new-proposal]').click()
   page.locator('#draft-title').fill(title)
   page.locator('#draft-body').fill('Texto demonstrativo de proposição para rever seção e tipo, sem efeitos institucionais.')
   page.locator('#compose-proposal-form [value=conclude]').click()
   page.locator('#confirm-proposal-form').wait_for(state='visible')
  open_new_draft('Proposta A')
  form=page.locator('#confirm-proposal-form')
  old_section=form.locator('[name=sectionId]').input_value()
  old_type=form.locator('[name=type]').input_value()
  changed_section=next(v for v in form.locator('[name=sectionId] option').evaluate_all('(xs)=>xs.map(x=>x.value)') if v!=old_section)
  changed_type=next(v for v in form.locator('[name=type] option').evaluate_all('(xs)=>xs.map(x=>x.value)') if v!=old_type)
  form.locator('[name=sectionId]').select_option(changed_section)
  form.locator('[name=type]').select_option(changed_type)
  page.locator('.footer-nav').click()
  assert form.locator('[name=sectionId]').input_value()==changed_section,(engine,width,'section reset by menu open')
  assert form.locator('[name=type]').input_value()==changed_type,(engine,width,'type reset by menu open')
  page.locator('.footer-nav').click()
  assert form.locator('[name=sectionId]').input_value()==changed_section,(engine,width,'section reset by menu close')
  assert form.locator('[name=type]').input_value()==changed_type,(engine,width,'type reset by menu close')
  form.locator('button[type=submit]').click()
  page.locator('.workflow-record').filter(has_text='Proposta A').wait_for(state='visible')
  proposals=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
  assert len(proposals)==1 and proposals[0]['sectionId']==changed_section and proposals[0]['type']==changed_type,(engine,width,proposals)
  # The next draft must start with its own saved/default selections.
  open_new_draft('Proposta B')
  form=page.locator('#confirm-proposal-form')
  assert form.locator('[name=sectionId]').input_value()==old_section,(engine,width,'stale section leaked to second draft')
  assert form.locator('[name=type]').input_value()==old_type,(engine,width,'stale type leaked to second draft')
  assert not errors,(engine,width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(engine,width,'overflow')
  page.close()
 browser.close()
print('PASS: same-proposal review selections retained through rerenders and isolated across drafts; '+engine)
