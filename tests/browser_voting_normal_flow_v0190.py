"""Product-facing initial ballot: no laboratory controls or manual choice of mode.
The six-mode technical laboratory remains separately available with ?demo=1.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  page.set_default_timeout(6000)
  errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto('about:blank');page.set_content(HTML)
  expect(page.locator('[data-action=enter-ballot]')).to_have_text('Participar')
  assert page.locator('[data-action=toggle-voting-forms]').count()==0,width
  assert page.locator('#preview-vote-lab:visible').count()==0,width
  page.locator('[data-action=enter-ballot]').click()
  expect(page.locator('#preview-vote-title')).to_contain_text('Revisão do calendário')
  assert page.locator('#preview-vote-method').count()==0,width
  expect(page.locator('.preview-vote-choice')).to_have_count(2)
  expect(page.locator('.preview-vote-choice').first).to_contain_text('Calendário mensal')
  assert page.locator('.preview-vote-summary').count()==0,width
  page.locator('.preview-vote-submit').click()
  expect(page.locator('#preview-vote-error')).to_be_visible()
  page.locator('input[name=selected]').first.check()
  page.locator('.preview-vote-submit').click()
  expect(page.locator('.preview-vote-receipt')).to_contain_text('Calendário mensal')
  page.locator('[data-action=reset-preview-vote]').click()
  assert page.locator('input[name=selected]:checked').count()==0,width
  page.locator('input[name=selected]').nth(1).check()
  page.locator('.preview-vote-submit').click()
  expect(page.locator('.preview-vote-receipt')).to_contain_text('Calendário quinzenal')
  page.locator('[data-action=exit-preview-schedule]').click()
  expect(page.locator('[data-action=enter-ballot]')).to_be_visible()
  assert page.locator('#preview-vote-lab:visible').count()==0,width
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  assert not errors,(width,errors)
  page.close()
  print('PASS natural initial participation',width)
 advanced=browser.new_page(viewport={'width':390,'height':850})
 advanced.goto('about:blank?demo=1');advanced.set_content(HTML)
 expect(advanced.locator('#preview-vote-method')).to_be_visible()
 advanced.locator('#preview-vote-method').select_option('aprovacao')
 expect(advanced.locator('input[name=approved]')).to_have_count(3)
 advanced.close();browser.close()
print('PASS product ballot entry 4 widths and isolated technical selector')
