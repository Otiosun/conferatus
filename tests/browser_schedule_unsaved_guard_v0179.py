"""Protect entered scheduling data from closing, route changes and reload.

Local fictional workflows only. beforeunload is not guaranteed on mobile.
Checks that blank schedules are not needlessly guarded; discarding is explicit.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
unload_probe="""() => {
 const event=new Event('beforeunload',{cancelable:true});
 window.dispatchEvent(event);
 return event.defaultPrevented;
}"""

with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(7500)
  errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto('about:blank?demo=1')
  # Offline opaque origin needs a deterministic local storage stand-in.
  page.evaluate("""() => {
   const data=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>data.get(k)??null,
    setItem:(k,v)=>data.set(k,String(v)),
    removeItem:k=>data.delete(k)
   }});
  }""")
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Proposta para agendamento seguro')
  page.locator('#draft-body').fill('A redação de teste é concluída para avaliar uma programação deliberativa local.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=calendar]').click()
  toggle=page.locator('[data-action=open-schedule]')
  toggle.wait_for(state='visible')
  toggle.click()
  form=page.locator('#schedule-deliberation-form')
  assert not page.evaluate(unload_probe),(width,'blank form erroneously guarded')
  toggle.click()
  assert form.count()==0,(width,'blank form cannot close')
  toggle.click()
  form=page.locator('#schedule-deliberation-form')
  form.locator('[name=title]').fill('Deliberação em preenchimento')
  form.locator('[name=objective]').fill('O formulário em edição precisa conservar os valores.')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=method]').select_option('nominal')
  choices=form.locator('[name=choices]')
  choices.wait_for(state='visible')
  choices.fill('Primeira alternativa\nSegunda alternativa')
  form.locator('[name=start]').fill('2027-02-12T09:00')
  form.locator('[name=end]').fill('2027-02-12T11:00')
  assert page.evaluate(unload_probe),(width,'dirty schedule not protected on unload')
  seen=[]
  page.once('dialog',lambda dlg:(seen.append(dlg.message),dlg.dismiss()))
  toggle.click()
  assert seen and 'agendamento' in seen[0].lower(),(width,'closing did not warn',seen)
  assert form.is_visible(),(width,'closing despite rejected discard')
  assert form.locator('[name=title]').input_value()=='Deliberação em preenchimento',width
  assert choices.input_value()=='Primeira alternativa\nSegunda alternativa',width
  page.locator('.footer-nav').click()
  page.once('dialog',lambda dlg:dlg.dismiss())
  page.locator('.menu-item[data-route=members]').click()
  assert page.evaluate('location.hash')=='#/calendar',(width,'menu lost unsaved form')
  assert form.locator('[name=title]').input_value()=='Deliberação em preenchimento',width
  assert page.locator('.bottom-menu').count()==0,(width,'menu blocks form after decline')
  # Direct history changes bypass navigate(); the hash listener must protect them.
  page.once('dialog',lambda dlg:dlg.dismiss())
  page.go_back(wait_until='commit',timeout=5000)
  page.wait_for_timeout(80)
  assert page.evaluate('location.hash')=='#/calendar',(width,'Back lost unsaved form')
  assert form.locator('[name=objective]').input_value().startswith('O formulário'),width
  # An explicit accepted departure discards only the unfinished schedule.
  page.once('dialog',lambda dlg:dlg.accept())
  toggle.click()
  assert form.count()==0,(width,'accepted discard kept schedule form open')
  assert not page.evaluate(unload_probe),(width,'unload listener not removed after discard')
  toggle.click()
  form=page.locator('#schedule-deliberation-form')
  assert form.locator('[name=title]').input_value()=='',(width,'discarded form was retained')
  # A valid submission must not prompt and must create exactly one local event.
  form.locator('[name=title]').fill('Programação validada')
  form.locator('[name=objective]').fill('Agenda criada depois do descarte consciente do formulário anterior.')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=method]').select_option('nominal')
  form.locator('[name=choices]').fill('Alternativa A\nAlternativa B')
  form.locator('[name=start]').fill('2027-02-13T09:00')
  form.locator('[name=end]').fill('2027-02-13T11:00')
  form.locator('button[type=submit]').click()
  item=page.locator('.calendar-item').filter(has_text='Programação validada')
  item.wait_for(state='visible')
  assert item.count()==1,width
  assert not page.evaluate(unload_probe),(width,'unload guard survived successful submission')
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('PASS: scheduling form close/menu/Back/unload discard guards, 4 widths, '+engine)
