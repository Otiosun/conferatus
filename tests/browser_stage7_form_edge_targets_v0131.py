"""Stage 07.03, batch 4: menu/management targets and invalid form states.

Run STAGE7_FIXED=0 to document undersized controls before CSS changes.
Tests the standalone demo only: no accounts, institutional integrations or remote data.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import os

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(280,320,360,390,540,740,768,1024,1440)
FIXED=os.environ.get('STAGE7_FIXED','1')=='1'
measurements=[]
defects=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  page=browser.new_page(viewport={'width':width,'height':780},has_touch=True,is_mobile=True)
  page.set_default_timeout(7500)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank?stage7=1');page.set_content(HTML)
  def measure(label,locator):
   locator.evaluate('e=>e.scrollIntoView({block:"center",inline:"nearest"})')
   rect=locator.bounding_box()
   assert rect,(width,label,'missing rectangle')
   hit=locator.evaluate('''e=>{let r=e.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;
     const top=document.elementFromPoint(x,y);return top===e||e.contains(top)}''')
   result={'width':width,'name':label,'w':round(rect['width'],2),'h':round(rect['height'],2),'center_hit':hit}
   measurements.append(result)
   if result['w']<43.5 or result['h']<43.5 or not hit:defects.append(result)
  def open_menu():
   menu=page.locator('.footer-nav');menu.wait_for(state='visible');measure('footer-menu-toggle',menu);menu.tap()
  def nav(route):
   open_menu();page.locator(f'.menu-item[data-route="{route}"]').tap()
  open_menu()
  for route in ('members','overview','calendar','proposals'):
   measure(f'menu-item-{route}',page.locator(f'.menu-item[data-route="{route}"]'))
  page.locator('.menu-item[data-route="overview"]').tap()
  measure('overview-management-shortcut',page.locator('.panel-button'))
  page.locator('.panel-button').tap()
  assert '#/governance' in page.url,(width,'shortcut did not navigate')
  page.locator('.section-toggle').first.tap()
  page.locator('.icon-button--edit').first.tap()
  edit=page.locator('#edit-member-form')
  assert edit.is_visible(),(width,'edit form missing')
  edit.locator('input[name="acdmId"]').fill('!')
  edit.locator('button[type="submit"]').tap()
  err=page.locator('#edit-error')
  assert err.is_visible(),(width,'edit error missing')
  assert page.locator('#member-acdm-id').get_attribute('aria-invalid')=='true',(width,'invalid input not identified')
  assert page.locator('#member-acdm-id').evaluate('e=>document.activeElement===e'),(width,'focus not restored after edit error')
  nav('proposals')
  page.locator('[data-action="new-proposal"]').tap()
  page.locator('#compose-proposal-form [value="save"]').tap()
  assert 'Escreva um título' in page.locator('#compose-proposal-form [role="alert"]').inner_text(),(width,'blank save error not announced inline')
  assert page.locator('#compose-proposal-form').is_visible(),(width,'editor lost after blank save')
  page.locator('#draft-title').fill('Conferência visual do formulário')
  page.locator('#draft-body').fill('Texto demonstrativo extenso para verificar estados de erro e revisão no frontend.')
  page.locator('#compose-proposal-form [value="conclude"]').tap()
  page.locator('#confirm-proposal-form button[type="submit"]').tap()
  assert '#/proposals' in page.url,(width,'review did not return to proposals')
  page.locator('[data-action="new-proposal"]').wait_for(state='visible')
  nav('calendar')
  page.locator('[data-action="open-schedule"]').tap()
  form=page.locator('#schedule-deliberation-form')
  assert form.is_visible(),(width,'schedule form missing')
  form.locator('[name="title"]').fill('Teste de evento demonstrativo')
  form.locator('[name="objective"]').fill('Conferência dos estados visuais do formulário')
  form.locator('[name="proposalId"]').select_option(index=1)
  form.locator('[name="start"]').fill('2026-11-24T16:00')
  form.locator('[name="end"]').fill('2026-11-24T14:00')
  form.locator('button[type="submit"]').tap()
  alert=form.locator('[role="alert"]')
  assert alert.is_visible(),(width,'invalid period error did not display')
  assert 'posterior ao início' in alert.inner_text(),(width,'invalid period message')
  assert form.locator('[name="title"]').input_value()=='Teste de evento demonstrativo',(width,'form lost data on error')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,'horizontal overflow')
  if width in (320,740):
   page.screenshot(path=str(ROOT/f'dist/stage7_forms_error_{width}.png'),full_page=True)
  assert not errors,(width,errors)
  page.close()
 browser.close()

output=ROOT/'dist'/'stage7_form_edge_target_measurements.json'
output.write_text(json.dumps({'measurements':measurements,'defects':defects},ensure_ascii=False,indent=2),encoding='utf-8')
print('Stage 07.03 forms/edge menu:',len(measurements),'measurements,',len(defects),'undersized or non-hittable targets')
for defect in defects[:25]:print('BEFORE_DEFECT',defect)
if FIXED: assert not defects,f'{len(defects)} controls smaller than 44px or occluded'
print('All tested flows functional: invalid member ID, blank draft, schedule invalid period; no JS errors or overflow')
