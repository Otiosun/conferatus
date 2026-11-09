"""The first cancellation tap must not change an active local schedule.

Use an inline, keyboard-accessible confirmation with a safe way back. Only
fictional local records: no Academy identity, database or actual votes.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as p:
 engine=os.getenv('CONFFRATUS_TEST_ENGINE','chromium')
 browser=(p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
          if engine=='chromium' else getattr(p,engine).launch(headless=True))
 for width in (280,320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  page.set_default_timeout(8000)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
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
  page.locator('#draft-title').fill('Proposta para cancelamento consciente')
  page.locator('#draft-body').fill('Redação fictícia concluída para testar a segurança da programação.')
  page.locator('#compose-proposal-form [value=conclude]').click()
  page.locator('#confirm-proposal-form').wait_for(state='visible')
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('[data-action=new-proposal]').wait_for(state='visible')
  page.evaluate('location.hash="#/calendar"')
  page.locator('[data-action=open-schedule]').wait_for(state='visible')
  page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  form.locator('[name=title]').fill('Programação protegida')
  form.locator('[name=objective]').fill('Verificar reversibilidade de uma operação de cancelamento local.')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=method]').select_option('binaria')
  form.locator('[name=start]').fill('2027-02-12T10:00')
  form.locator('[name=end]').fill('2027-02-12T11:00')
  form.locator('button[type=submit]').click()
  row=page.locator('.calendar-item').filter(has_text='Programação protegida')
  row.wait_for(state='visible')
  if row.locator('[data-cancel-schedule]').count()==0:
   row.locator('[data-schedule]').click()
  trigger=row.locator('[data-cancel-schedule]')
  trigger.wait_for(state='visible')
  assert trigger.get_attribute('aria-expanded')=='false',width
  trigger.click()
  panel=row.locator('.calendar-cancel-confirm')
  panel.wait_for(state='visible')
  assert row.count()==1,(width,'first tap immediately cancelled active schedule')
  assert trigger.get_attribute('aria-expanded')=='true',width
  assert panel.get_attribute('role')=='group',width
  assert panel.evaluate('(el)=>document.activeElement===el'),(width,'confirmation focus missing')
  panel_bounds=panel.bounding_box()
  assert panel_bounds and panel_bounds['y']>=-1 and panel_bounds['y']+panel_bounds['height']<=845,(width,'confirmation not visible after click',panel_bounds)
  assert 'permanecerá no histórico' in panel.inner_text(),width
  assert row.locator('[data-confirm-cancel-schedule]').bounding_box()['height']>=44,width
  page.keyboard.press('Escape')
  assert row.locator('.calendar-cancel-confirm').count()==0,(width,'Escape did not close confirmation')
  assert row.locator('[data-cancel-schedule]').evaluate('(e)=>document.activeElement===e'),(width,'Escape did not restore trigger focus')
  trigger_bounds=row.locator('[data-cancel-schedule]').bounding_box()
  assert trigger_bounds and trigger_bounds['y']>=-1 and trigger_bounds['y']+trigger_bounds['height']<=845,(width,'restored trigger outside viewport',trigger_bounds)
  assert row.count()==1,width
  row.locator('[data-cancel-schedule]').click()
  row.locator('[data-keep-schedule]').click()
  assert row.count()==1,(width,'keep cancelled schedule')
  assert row.locator('.calendar-cancel-confirm').count()==0,width
  assert row.locator('[data-cancel-schedule]').evaluate('(e)=>document.activeElement===e'),width
  row.locator('[data-cancel-schedule]').click()
  page.locator('[data-action=calendar-next]').click()
  assert row.locator('.calendar-cancel-confirm').count()==0,(width,'calendar navigation left a stale cancellation prompt')
  assert row.count()==1,(width,'calendar navigation cancelled unexpectedly')
  row.locator('[data-cancel-schedule]').click()
  row.locator('[data-confirm-cancel-schedule]').click()
  assert row.count()==0,(width,'explicit confirmation failed to cancel')
  history=page.locator('[data-action=toggle-cancelled-history]')
  history.wait_for(state='visible')
  history.click()
  record=page.locator('.calendar-cancelled-record').filter(has_text='Programação protegida')
  record.wait_for(state='visible')
  assert 'Cancelada' in record.inner_text(),width
  # The new schedule selects its own date; clear that filter before checking
  # the unrelated fixed calendar fixture, which belongs to another month.
  show_all=page.locator('[data-action=calendar-all]')
  if show_all.count(): show_all.click()
  assert page.locator('.calendar-item').filter(has_text='Revisão do calendário de reuniões').count()==1,width
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'horizontal overflow')
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('PASS: active -> pending -> Escape/keep -> confirmed cancellation and history, 5 widths, '+engine)
