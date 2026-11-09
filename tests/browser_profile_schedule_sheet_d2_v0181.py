"""Opt-in D2 candidate: native profile sheet shares calendar scheduling validation.

Only fictional session data; no Academy accounts or actual votes.
This candidate must NOT replace the default profile-to-calendar route before
Megalos accepts the visual contract.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width in (280,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(8000)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1&d2=sheet')
  page.evaluate("""() => {
   const store=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>store.get(k)??null,
    setItem:(k,v)=>store.set(k,String(v)),
    removeItem:k=>store.delete(k)
   }});
  }""")
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Proposição concluída para folha')
  page.locator('#draft-body').fill('Registro sintético suficientemente longo para completar e agendar a deliberação.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=members]').click()
  page.locator('.profile-name-button').click()
  page.locator('[data-tab=proposicoes]').click()
  btn=page.locator('.session-proposal').filter(has_text='Proposição concluída para folha').locator('[data-schedule-draft]')
  btn.click()
  sheet=page.locator('#profile-schedule-dialog')
  sheet.wait_for(state='visible')
  assert page.evaluate('location.hash').startswith('#/profile'),width
  assert sheet.evaluate('(el)=>el.open&&el.matches(":modal")'),(width,'sheet is not native modal')
  assert page.locator('#schedule-deliberation-form').count()==1,width
  order=sheet.locator('#schedule-deliberation-form select, #schedule-deliberation-form input, #schedule-deliberation-form textarea').evaluate_all('(xs)=>xs.map(el=>el.name)')
  assert order[:5]==['proposalId','sectionId','start','end','type'],(width,'sheet diverged from original field order',order)
  assert 'title' in order and 'objective' in order and 'method' in order,width
  assert sheet.locator('[name=proposalId]').input_value()!='',width
  assert sheet.locator('#profile-schedule-sheet-label').evaluate('(el)=>document.activeElement===el'),width
  assert sheet.evaluate('(el)=>getComputedStyle(el).position')=='fixed',width
  assert sheet.bounding_box()['width']<=width+1,width
  sheet_box=sheet.bounding_box()
  emblem_box=sheet.locator('.profile-schedule-sheet-head img').bounding_box()
  assert emblem_box and abs((emblem_box['x']+emblem_box['width']/2)-(sheet_box['x']+sheet_box['width']/2))<3,(width,'crest not centered over D2 sheet',emblem_box,sheet_box)
  close_box=sheet.locator('[data-dismiss-schedule-sheet]').bounding_box()
  assert close_box and close_box['height']>=44,(width,'explicit close target is too small')
  bounds=sheet.bounding_box()
  # The original sheet begins lower on the profile. Keep the opt-in candidate
  # compact at normal viewport height without hiding required extra inputs.
  assert bounds['y']>= (400 if width<=380 else 455),(width,'D2 sheet hides too much of the profile',bounds)
  assert sheet.evaluate('(e)=>e.scrollHeight>e.clientHeight'),(width,'required extra inputs must remain scrollable')
  assert sheet.locator('[name=proposalId]').bounding_box()['height']>=50,(width,'sheet inputs too small')
  if width==390:
   # Dynamic browser chrome / mobile keyboard can reduce available height.
   # Re-expand usable dialog area instead of leaving a tiny scroll viewport.
   page.set_viewport_size({'width':390,'height':520})
   short=sheet.bounding_box()
   assert short and short['height']>=380 and short['y']>=0,(width,'short-viewport sheet unusable',short)
   page.set_viewport_size({'width':390,'height':850})
  # Tab must stay inside the modal, never reach background buttons.
  for _ in range(12):
   page.keyboard.press('Tab')
   assert sheet.evaluate('(el)=>el.contains(document.activeElement)'),(width,'focus escaped modal')
  page.keyboard.press('Escape')
  assert sheet.count()==0,(width,'pristine Escape failed')
  assert btn.evaluate('(el)=>document.activeElement===el'),(width,'focus not returned')
  btn.click()
  sheet=page.locator('#profile-schedule-dialog');sheet.wait_for(state='visible')
  form=sheet.locator('#schedule-deliberation-form')
  form.locator('[name=title]').fill('Sessão do perfil')
  form.locator('[name=objective]').fill('Validar vínculo e integridade do formulário existente.')
  method_field=form.locator('[name=method]')
  method_field.scroll_into_view_if_needed()
  scroll_before=sheet.evaluate('(el)=>el.scrollTop')
  assert scroll_before>40,(width,'test did not scroll into extra fields',scroll_before)
  method_field.select_option('nominal')
  form.locator('[name=choices]').wait_for(state='visible')
  scroll_after=sheet.evaluate('(el)=>el.scrollTop')
  assert abs(scroll_after-scroll_before)<=4,(width,'method change reset internal reading position',scroll_before,scroll_after)
  assert form.locator('[name=title]').input_value()=='Sessão do perfil',width
  form.locator('[name=choices]').fill('Primeira\nSegunda')
  form.locator('[name=start]').fill('2027-04-13T10:00')
  form.locator('[name=end]').fill('2027-04-13T11:00')
  # A rejected Escape must not discard the entered fields.
  page.once('dialog',lambda dlg:dlg.dismiss())
  page.keyboard.press('Escape')
  assert sheet.is_visible(),(width,'declined Escape discarded sheet')
  assert form.locator('[name=title]').input_value()=='Sessão do perfil',width
  page.once('dialog',lambda dlg:dlg.dismiss())
  sheet.locator('[data-dismiss-schedule-sheet]').click()
  assert sheet.is_visible(),(width,'declined explicit close discarded sheet')
  # Direct hashes and browser history can move between two profile IDs without
  # changing the route name. Refusing the departure must preserve form values.
  page.once('dialog',lambda dlg:dlg.dismiss())
  page.evaluate('location.hash="#/profile/m04"')
  page.wait_for_timeout(80)
  assert page.evaluate('location.hash')=='#/profile/m01',(width,'same-route hash discarded changes')
  assert sheet.is_visible() and form.locator('[name=title]').input_value()=='Sessão do perfil',width
  # Single source of truth: the shared submit handler stores the new item.
  form.locator('button[type=submit]').click()
  sheet.wait_for(state='detached')
  drafts=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
  scheduled=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))')
  assert len(scheduled)==1 and scheduled[0]['proposalId']==drafts[0]['id'],(width,scheduled)
  assert scheduled[0]['method']=='nominal' and len(scheduled[0]['choices'])==2,width
  assert page.locator('.session-proposal .session-schedule-link').count()==1,width
  outcome=page.locator('.profile-schedule-result')
  outcome.wait_for(state='visible')
  assert 'Deliberação programada' in outcome.inner_text(),(width,'missing visible save confirmation')
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'overflow')
  page.close()
 # Default is intentionally unchanged, even in advanced demo mode.
 page=browser.new_page(viewport={'width':390,'height':850})
 page.goto('about:blank?demo=1')
 page.set_content(html)
 assert page.locator('#profile-schedule-dialog').count()==0
 browser.close()
print('PASS: opt-in profile D2 native sheet focus, Escape, validation, save and default isolation; '+engine)
