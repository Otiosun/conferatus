"""Stage 07.10: inline form errors are linked to the relevant input fields.

Only the offline demonstration is exercised; no real scheduling or accounts.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
rows=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,740,1440):
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1');page.set_content(HTML)
  page.evaluate('location.hash="#/proposals"');page.wait_for_timeout(40)
  page.locator('[data-action=new-proposal]').click()
  page.locator('#compose-proposal-form [value=save]').click()
  alert=page.locator('#compose-save-error')
  assert alert.is_visible(),(width,'blank draft alert missing')
  assert alert.get_attribute('role')=='alert'
  for selector in ('#draft-title','#draft-body'):
   field=page.locator(selector)
   idref=(field.get_attribute('aria-describedby') or '').split()
   assert 'compose-save-error' in idref,(width,selector,'form error is not related to input')
   rows.append({'width':width,'case':'draft blank message relation','field':selector})
  page.locator('#draft-title').fill('Programação acessível')
  page.locator('#draft-body').fill('Exemplo de texto suficientemente longo para testar o agendamento acessível.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.evaluate('location.hash="#/calendar"');page.wait_for_timeout(40)
  page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  form.locator('[name=title]').fill('Evento demonstrativo')
  form.locator('[name=objective]').fill('Proposta demonstrativa de agendamento')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=method]').select_option('binaria')
  form.locator('[name=start]').fill('2026-11-24T16:00')
  form.locator('[name=end]').fill('2026-11-24T14:00')
  form.locator('button[type=submit]').click()
  alert=form.locator('[role=alert]')
  assert alert.is_visible(),(width,'invalid date alert missing')
  error_id=alert.get_attribute('id')
  end=form.locator('[name=end]')
  assert error_id and error_id in (end.get_attribute('aria-describedby') or '').split(),(width,'date error not linked to end')
  assert end.get_attribute('aria-invalid')=='true',(width,'end should be marked invalid')
  assert end.evaluate('(el)=>document.activeElement===el'),(width,'focus not returned to invalid date')
  rows.append({'width':width,'case':'invalid schedule dates linked and focused'})
  end.fill('2026-11-25T14:00')
  assert end.get_attribute('aria-invalid') is None,(width,'corrected end remains marked invalid')
  assert not alert.is_visible(),(width,'error remains after date corrected')
  rows.append({'width':width,'case':'date error cleared after correction'})
  assert not errors,(width,'JS errors',errors)
  page.close()
 browser.close()
(ROOT/'dist/stage7_error_fields_v0141.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Form error linking: '+str(len(rows))+' checks passed')
