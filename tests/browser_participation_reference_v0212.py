"""CP174: Megalos-confirmed participation rate remains separate from option results.
The dots illustrate the original visual; they do not count people or imply official data.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':850})
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank')
  page.set_content(HTML)
  assert page.locator('.ballot-participation').count()==1,width
  expect(page.locator('.ballot-participation-top')).to_contain_text('Grupo Votante')
  expect(page.locator('.ballot-participation-value')).to_have_text('76%')
  expect(page.locator('.ballot-participation-caption')).to_have_text('Taxa de participação')
  assert page.locator('.ballot-participation .sr-only').inner_text().find('não estão disponíveis')>=0,width
  # All decorative dots are inaccessible and their count never encodes voter totals.
  assert page.locator('.ballot-participation svg[aria-hidden=true] circle').count()>60,width
  expect(page.locator('.results .result-row')).to_have_count(2)
  assert page.locator('.ballot-result-fill').count()==2,width
  assert page.locator('.ballot-result-fill').first.get_attribute('style')=='width:80%',width
  assert page.locator('.ballot-result-fill').nth(1).get_attribute('style')=='width:20%',width
  assert page.locator('.result-percentage').all_inner_texts()==['80%','20%'],width
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  expect(page.locator('[data-action=enter-ballot]')).to_have_text('Participar')
  page.locator('[data-action=enter-ballot]').click()
  expect(page.locator('#preview-vote-title')).to_contain_text('Revisão do calendário')
  assert page.locator('.ballot-participation').count()==0,width
  page.locator('[name=selected]').first.check()
  page.locator('.preview-vote-submit').click()
  expect(page.locator('.preview-vote-receipt')).to_contain_text('Calendário mensal')
  page.locator('[data-action=exit-preview-schedule]').click()
  expect(page.locator('.ballot-participation-value')).to_have_text('76%')
  assert not errors,(width,errors)
  page.close()
 advanced=browser.new_page(viewport={'width':390,'height':850})
 advanced.goto('about:blank?demo=1')
 advanced.set_content(HTML)
 assert advanced.locator('.ballot-participation').count()==0
 assert advanced.locator('.results .result-row').count()==2
 advanced.close()
 browser.close()
print('CP174 participation/reference layout PASS: 5 widths; choice counts, participation and forms kept separate')
