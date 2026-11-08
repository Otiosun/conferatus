"""Prevent silent loss of an unsaved proposal on rerenders and navigation.

Runs only against generated fictional offline HTML. Does not assert real storage,
authentication, permissions or institutional voting.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  page.set_default_timeout(6000)
  errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto('about:blank')
  page.set_content(html)
  def new_unsaved():
   page.evaluate('location.hash="#/proposals"')
   page.locator('[data-action=new-proposal]').wait_for(state='visible')
   page.locator('[data-action=new-proposal]').click()
   page.locator('#draft-title').fill('Rascunho importante')
   page.locator('#draft-body').fill('Uma redação longa suficientemente completa e ainda não salva.')
  new_unsaved()
  page.once('dialog',lambda dialog:dialog.dismiss())
  page.locator('.workflow-editor-actions [data-route=proposals]').click()
  assert page.evaluate('location.hash')=='#/compose',width
  assert page.locator('#draft-title').input_value()=='Rascunho importante',width
  # Opening the footer must never reset an unsubmitted title or text.
  page.locator('.footer-nav').click()
  assert page.locator('#draft-title').input_value()=='Rascunho importante',width
  assert page.locator('#draft-body').input_value().startswith('Uma redação longa'),width
  page.once('dialog',lambda dialog:dialog.dismiss())
  page.locator('.menu-item[data-route=members]').click()
  assert page.evaluate('location.hash')=='#/compose',width
  assert page.locator('.bottom-menu').count()==0,(width,'menu blocked editor after cancelled exit')
  assert page.locator('#draft-title').input_value()=='Rascunho importante',width
  # Back is a direct hash transition: it bypasses navigate().
  page.once('dialog',lambda dialog:dialog.dismiss())
  page.go_back(wait_until='commit',timeout=5000)
  page.wait_for_timeout(100)
  assert page.evaluate('location.hash')=='#/compose',width
  assert page.locator('#draft-title').input_value()=='Rascunho importante',width
  page.once('dialog',lambda dialog:dialog.accept())
  page.locator('.workflow-editor-actions [data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/proposals',width
  # An explicit save persists normally; no false discard confirmation.
  new_unsaved()
  unexpected=[]
  page.on('dialog',lambda dialog:(unexpected.append(dialog.message),dialog.dismiss()))
  page.locator('.workflow-editor-actions [value=save]').click()
  page.locator('[data-action=new-proposal]').wait_for(state='visible')
  assert page.evaluate('location.hash')=='#/proposals',width
  assert not unexpected,(width,unexpected)
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  page.close()
 browser.close()
print('Compose unsaved-exit guard: 4 widths, footer rerender, route/menu/Back declines, discard and save OK')
