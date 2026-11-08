"""Warn on page unload only while the composer actually has unsaved changes.

Synthetic beforeunload dispatch exercises listener wiring, NOT browser mobile
shutdown behavior or guaranteed recovery; browsers can skip this event.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/'dist/CONFERATUS_demo_offline.html').read_text(encoding='utf-8')
probe="""() => {
  const event=new Event('beforeunload',{cancelable:true});
  window.dispatchEvent(event);
  return event.defaultPrevented;
}"""
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':844})
  page.set_default_timeout(6500)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route=proposals]').click()
  page.locator('[data-action=new-proposal]').click()
  page.locator('#draft-title').wait_for(state='visible')
  assert not page.evaluate(probe),(width,'false prompt for empty composer')
  page.locator('#draft-title').fill('Proposição com alterações não salvas')
  assert page.evaluate(probe),(width,'missing protection for unsaved title')
  page.locator('#draft-body').fill('Redação institucional de teste ainda não salva, suficiente para conclusão posterior.')
  page.locator('.footer-nav').click()
  assert page.evaluate(probe),(width,'footer rerender disabled dirty guard')
  page.keyboard.press('Escape')
  page.locator('#compose-proposal-form [value=save]').click()
  page.locator('[data-action=new-proposal]').wait_for(state='visible')
  assert not page.evaluate(probe),(width,'stale unload guard after saving')
  page.locator('.workflow-record [data-draft]').first.click()
  page.locator('#draft-title').wait_for(state='visible')
  assert not page.evaluate(probe),(width,'unchanged draft flagged dirty')
  page.locator('#draft-title').fill('Proposição alterada depois de salvar')
  assert page.evaluate(probe),(width,'saved draft modification not guarded')
  page.locator('#draft-title').fill('Proposição com alterações não salvas')
  assert not page.evaluate(probe),(width,'reverted value still marked dirty')
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('PASS: conditional unload guard and cleanup for new and edited drafts, four widths')
