"""Stage 07.03: keyboard skip link, search field and advanced controls.

STAGE7_FIXED=0 records the failing baseline before the scoped CSS change.
This targets the offline preview only: all data are fictional and session-local.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, os

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(280,320,360,390,540,740,768,1024,1440)
FIXED=os.environ.get('STAGE7_FIXED','1')=='1'
measurements=[]
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  page=browser.new_page(viewport={'width':width,'height':820},has_touch=True,is_mobile=True)
  page.set_default_timeout(7000)
  page.on('pageerror',lambda err:errors.append({'width':width,'error':str(err)}))
  page.goto('about:blank?demo=1')
  page.set_content(HTML)
  def measure(name,loc):
   loc.wait_for(state='visible')
   loc.evaluate('e => e.scrollIntoView({block:"center",inline:"nearest"})')
   rect=loc.bounding_box()
   hit=loc.evaluate('''e => {let b=e.getBoundingClientRect(); let n=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2);return n===e||e.contains(n)}''')
   item={'width':width,'target':name,'height':round(rect['height'],2),'width_px':round(rect['width'],2),'center_hit':hit}
   measurements.append(item)
   return item

  # A skip link is only visible on focus, so test its actual focused rectangle.
  skip=page.locator('.skip-link')
  skip.focus()
  measure('skip-link-focused',skip)
  skip.press('Enter')
  assert page.locator('#main-content').evaluate('e=>document.activeElement===e'),(width,'skip link did not move focus')

  # Open the genuine advanced-panel state and link an actual fixture member.
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="overview"]').click()
  page.locator('.hero [data-route="governance"]').click()
  page.locator('.section-toggle').first.click()
  page.locator('.panel-button').click()
  panel=page.locator('.demo-tools')
  assert panel.is_visible(),(width,'advanced tools not expanded')
  measure('demo-role-select',panel.locator('#role-mode'))
  measure('demo-add-member-select',panel.locator('#add-member'))
  measure('demo-link-member-button',panel.locator('[data-action="add-member"]'))
  if width in (280,390,740) and FIXED:
   page.screenshot(path=str(ROOT/f'dist/stage7_advanced_panel_{width}.png'),full_page=True)
  panel.locator('#add-member').select_option(index=1)
  panel.locator('[data-action="add-member"]').click()
  assert not page.locator('.demo-tools').count(),(width,'linking did not close panel')
  assert 'adicionado à seção' in page.locator('.status-line').inner_text(),(width,'linking did not update preview')

  # The member search is interactive and should preserve the typed filter.
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="members"]').click()
  page.locator('.search-trigger').click()
  search=page.locator('#search-members')
  measure('member-search-input',search)
  search.fill('Helena')
  assert page.locator('.member-item').count()==1,(width,'search results changed unexpectedly')
  page.locator('[data-action="clear-search"]').click()
  assert page.locator('.member-item').count()>1,(width,'clear search failed')

  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,'horizontal overflow')
  if width in (280,390,740) and FIXED:
   page.screenshot(path=str(ROOT/f'dist/stage7_advanced_search_{width}.png'),full_page=True)
  page.close()
 browser.close()

problems=[m for m in measurements if m['height']<43.5 or not m['center_hit']]
(ROOT/'dist/stage7_advanced_controls_v0132_measurements.json').write_text(json.dumps({'targets':measurements,'undersized_or_occluded':problems,'pageerrors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Stage 07.03: {len(measurements)} target measurements, {len(problems)} undersized/occluded, {len(errors)} JS errors')
if not FIXED:
 for issue in problems[:12]:print('BEFORE',json.dumps(issue,ensure_ascii=False))
else:
 assert not problems,problems
assert not errors,errors
print('ADVANCED_CONTROLS PASS: functional linking, search filtering/clear, keyboard skip-link, no horizontal overflow')
