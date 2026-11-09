"""Never lose draft voting alternatives when a scheduling mode hides their field.

The same validated form is used in calendar and in the opt-in profile sheet.
Only fictional local records; no Academy voting service or real storage.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for as_sheet in (False,True):
  for width in (280,390,740):
   page=browser.new_page(viewport={'width':width,'height':850})
   page.set_default_timeout(8000)
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('about:blank?demo=1'+('&d2=sheet' if as_sheet else ''))
   page.evaluate("""() => {
    const cache=new Map();
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
     getItem:k=>cache.get(k)??null,setItem:(k,v)=>cache.set(k,String(v)),
     removeItem:k=>cache.delete(k)
    }});
   }""")
   page.set_content(html)
   page.locator('.footer-nav').click()
   page.locator('.menu-item[data-route=proposals]').click()
   page.locator('[data-action=new-proposal]').click()
   page.locator('#draft-title').fill('Proposição para testar alternativas')
   page.locator('#draft-body').fill('Texto sintético de proposição concluída para validar opções de votação.')
   page.locator('#compose-proposal-form [value=conclude]').click()
   page.locator('#confirm-proposal-form button[type=submit]').click()
   if as_sheet:
    page.locator('.footer-nav').click()
    page.locator('.menu-item[data-route=members]').click()
    page.locator('.profile-name-button').click()
    page.locator('[data-tab=proposicoes]').click()
   shortcut=page.locator('.session-proposal [data-schedule-draft]' if as_sheet else '.workflow-record [data-schedule-draft]').first
   shortcut.click()
   form=page.locator('#schedule-deliberation-form')
   form.wait_for(state='visible')
   if as_sheet:
    assert page.locator('#profile-schedule-dialog').is_visible()
   else:
    assert page.evaluate('location.hash')=='#/calendar'
   form.locator('[name=method]').select_option('nominal')
   choices=form.locator('[name=choices]')
   choices.fill('Primeira alternativa\nSegunda alternativa\nTerceira alternativa')
   form.locator('[name=method]').select_option('binaria')
   assert form.locator('[name=choices]').count()==0,(engine,as_sheet,width,'binary must hide choices')
   form.locator('[name=method]').select_option('nominal')
   assert form.locator('[name=choices]').input_value()=='Primeira alternativa\nSegunda alternativa\nTerceira alternativa',(engine,as_sheet,width,'lost temporary choices')
   # Switching away again should still guard disposal of the hidden text.
   form.locator('[name=method]').select_option('binaria')
   page.once('dialog',lambda dialog:dialog.dismiss())
   if as_sheet:
    page.keyboard.press('Escape')
    assert page.locator('#profile-schedule-dialog').is_visible(),(engine,width,'declined discard dismissed sheet')
   else:
    page.locator('[data-action=open-schedule]').click()
    assert form.is_visible(),(engine,width,'declined discard closed calendar form')
   page.once('dialog',lambda dialog:dialog.accept())
   if as_sheet: page.keyboard.press('Escape')
   else: page.locator('[data-action=open-schedule]').click()
   assert form.count()==0,(engine,as_sheet,width,'accepted close did not close')
   # The choices cache is edit-session-only, never shared with another form.
   if as_sheet:
    page.locator('.session-proposal [data-schedule-draft]').first.click()
   else:
    page.locator('[data-action=open-schedule]').click()
   form=page.locator('#schedule-deliberation-form')
   form.wait_for(state='visible')
   form.locator('[name=method]').select_option('nominal')
   assert form.locator('[name=choices]').input_value()=='',(engine,as_sheet,width,'draft leaked into new schedule')
   assert not errors,(engine,as_sheet,width,errors)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(engine,as_sheet,width,'overflow')
   page.close()
 browser.close()
print('PASS: choices survive temporary method changes and reset only on close; '+engine)
