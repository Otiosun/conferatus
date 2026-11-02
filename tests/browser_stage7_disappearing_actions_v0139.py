"""07.09: focus destination when an activated preview control is removed by rerender.

Keyboard only for activation, in two CSS viewport sizes. No production access.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (390,768):
  page=browser.new_page(viewport={'width':width,'height':830})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1');page.set_content(HTML)
  def record(label,selector):
   expected=page.locator(selector)
   ok=expected.count()>0 and expected.first.evaluate('(el)=>el===document.activeElement')
   results.append({'width':width,'label':label,'passed':ok,'focused':page.evaluate('document.activeElement?.outerHTML?.slice(0,110)')})
  def nav(route):
   page.evaluate('(route)=>location.hash="#/"+route',route)
   page.wait_for_timeout(65)
  page.locator('[data-action=toggle-demo]').click()
  page.locator('[data-vote]').first.click()
  page.locator('[data-action=reset-vote]').focus();page.keyboard.press('Enter')
  record('reset vote focus first available option','[data-vote]')
  nav('members')
  page.locator('[data-action=show-more-members]').focus();page.keyboard.press('Enter')
  record('expanded directory focus new member','.member-item:nth-child(8)')
  nav('overview')
  page.locator('[data-action=show-more-history]').focus();page.keyboard.press('Enter')
  record('expanded history focus first new article','.overview-content .activity:nth-child(7)')
  nav('governance')
  page.locator('[data-action=toggle-tools]').click()
  page.locator('[data-action=reset-admin]').focus();page.keyboard.press('Enter')
  record('reset management focus panel trigger','[data-action=toggle-tools]')
  page.locator('[data-section]').first.click()
  page.locator('[data-action=toggle-tools]').click()
  select=page.locator('#add-member')
  ids=[opt.get_attribute('value') for opt in select.locator('option').all() if opt.get_attribute('value')]
  if ids:
   select.select_option(ids[0]);page.locator('[data-action=add-member]').focus();page.keyboard.press('Enter')
   record('add member focus panel trigger','[data-action=toggle-tools]')
  nav('calendar')
  page.locator('[data-calendar-day]').nth(4).click()
  page.locator('[data-action=calendar-all]').focus();page.keyboard.press('Enter')
  record('show all calendar focus list heading','.calendar-list-head h2')
  results.append({'width':width,'label':'no JS errors','passed':not errors,'focused':'\n'.join(errors)})
  page.close()
 browser.close()
report={'checks':len(results),'passed':sum(x['passed'] for x in results),'failed':[x for x in results if not x['passed']]}
(ROOT/'dist'/'stage7_disappearing_actions_v0139_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'07.09 removed controls focus: {report["passed"]}/{report["checks"]}')
for x in report['failed']:print('FAIL:',x)
assert not report['failed']
