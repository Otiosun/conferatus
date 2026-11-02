"""Stage 07.10: persistent nonvisual status region for preview workflow results.

Verifies DOM/ARIA and user flows, not actual screen-reader speech output.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(320,390,740,1440)
checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror', lambda e: errors.append(str(e)))
  page.goto('about:blank?demo=1');page.set_content(HTML)
  announcer=page.locator('#app-live-announcer')
  assert announcer.count()==1,(width,'persistent live status missing')
  assert announcer.get_attribute('role')=='status',(width,'missing polite live role')
  assert announcer.get_attribute('aria-atomic')=='true',(width,'atomic announcement missing')
  assert announcer.inner_text()=='',(width,'announcement must start empty')
  # The announcer must be outside the DOM subtree replaced by render().
  ref=page.evaluate('window.__savedAnnouncer=document.getElementById("app-live-announcer"); __savedAnnouncer.isConnected')
  assert ref,width
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  assert page.evaluate('window.__savedAnnouncer === document.getElementById("app-live-announcer")'),(width,'live region recreated on navigation')
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').fill('Proposição acessível')
  page.locator('#draft-body').fill('Texto da prévia de acessibilidade para anúncio consistente.')
  page.get_by_role('button',name='Salvar rascunho').click()
  page.locator('.workflow-status').wait_for()
  text=page.locator('.workflow-status').inner_text()
  assert 'rascunho' in text.lower(),(width,text)
  assert announcer.inner_text()==text,(width,'screen-reader region lacks new visible message')
  assert announcer.aria_snapshot() == '- status: '+text,(width,'AX tree status does not match visible message')
  assert page.evaluate('window.__savedAnnouncer === document.getElementById("app-live-announcer")'),(width,'live region replaced after status')
  assert page.locator('.workflow-status').get_attribute('role') is None,(width,'duplicate polite status')
  checks.append({'width':width,'case':'draft saved and persistent announcer', 'message':text})
  # New editing flow must not replay a stale success announcement.
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').wait_for()
  page.wait_for_function('document.getElementById("app-live-announcer").textContent === ""')
  assert announcer.inner_text()=='',(width,'stale status remained in live region')
  page.locator('#draft-title').fill('Proposição para agendamento')
  page.locator('#draft-body').fill('Conteúdo extenso para a confirmação e programação local demonstrativa.')
  page.get_by_role('button',name='Concluir redação').click()
  page.locator('#confirm-proposal-form button[type=submit]').click()
  page.locator('.workflow-status').wait_for()
  text=page.locator('.workflow-status').inner_text()
  assert announcer.inner_text()==text,(width,'confirmed proposal not announced')
  assert announcer.aria_snapshot() == '- status: '+text,(width,'AX status of confirmation missing')
  checks.append({'width':width,'case':'proposal concluded', 'message':text})
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=calendar]').click()
  page.locator('[data-action=open-schedule]').click()
  form=page.locator('#schedule-deliberation-form')
  form.locator('[name=title]').fill('Programação anunciada')
  form.locator('[name=objective]').fill('Descrição válida para verificar a conclusão do agendamento.')
  form.locator('[name=proposalId]').select_option(index=1)
  form.locator('[name=start]').fill('2026-12-12T09:00')
  form.locator('[name=end]').fill('2026-12-12T12:00')
  form.locator('button[type=submit]').click()
  page.locator('.workflow-status').wait_for()
  text=page.locator('.workflow-status').inner_text()
  assert announcer.inner_text()==text,(width,'schedule result not announced')
  assert announcer.aria_snapshot() == '- status: '+text,(width,'AX status of calendar notice missing')
  checks.append({'width':width,'case':'schedule created', 'message':text})
  assert page.evaluate('window.__savedAnnouncer === document.getElementById("app-live-announcer")'),(width,'announcer replaced on schedule')
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'overflow')
  page.close()
 browser.close()
report={'checks':len(checks),'results':checks,'scope':'Chromium DOM/ARIA only, no screen reader tested'}
(ROOT/'dist/stage7_live_announcer_v0144.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'Persistent live announcement: {len(checks)}/{len(WIDTHS)*3} flows passed')
