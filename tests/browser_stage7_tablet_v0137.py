"""Stage 07.07 tablet audit of the static CONFFRATUS preview.

This tests 8 portrait/landscape viewports across 8 routes plus live rotation
of open menu, calendar, search, review and governance states. Chromium offline
only. A bounded 740px reading column is intentional unless approved otherwise.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
SIZES=((600,960),(640,900),(740,1024),(768,1024),(820,1180),(900,600),(1024,768),(1024,1366))
ROUTES=('ballot','members','overview','governance','calendar','proposals','compose','profile')
ROTATIONS=(((600,960),(960,600)),((768,1024),(1024,768)),((820,1180),(1180,820)))
records=[];issues=[];functions=[];screens=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in SIZES:
  page=browser.new_page(viewport={'width':width,'height':height},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank?demo=1');page.set_content(HTML)
  for route in ROUTES:
   if route=='profile':
    page.evaluate('location.hash="#/members"');page.locator('.member-item').first.click()
   elif route=='compose':
    page.evaluate('location.hash="#/proposals"');page.locator('[data-action="new-proposal"]').click()
   else:
    page.evaluate('(r)=>location.hash="#/"+r',route)
    if route=='governance':page.locator('.panel-button').click()
   m=page.evaluate('''()=>{
     const rect=(s)=>{const el=document.querySelector(s);if(!el)return null;const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};};
     const shell=rect('.app-shell'),nav=rect('.footer-nav'),foot=rect('.app-footer'),crest=rect('.app-footer > img'),home=rect('.footer-home');
     const stats=document.querySelector('.overview-stats');
     const tabs=document.querySelector('.tabs');
     const inside=(a,b)=>a.x>=b.x-1&&a.x+a.w<=b.x+b.w+1;
     const intersect=(a,b)=>Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y));
     const controls=[...document.querySelectorAll('button,a,select,input,textarea')].filter(el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return !el.disabled&&s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0;});
     return {innerWidth,documentWidth:document.documentElement.scrollWidth,shell,nav,foot,crest,home,
       controls:controls.length,menuInside:inside(nav,foot),labelLogoCollision:intersect(home,crest),labelMenuCollision:intersect(home,nav),
       stats:stats?{client:stats.clientWidth,scroll:stats.scrollWidth}:null,
       tabs:tabs?{client:tabs.clientWidth,scroll:tabs.scrollWidth}:null,
       badgeLoaded:document.querySelector('.app-footer>img').naturalWidth>0};
   }''')
   records.append({'viewport':[width,height],'route':route,**m})
   if m['documentWidth']>width+1:issues.append([width,height,route,'document overflow',m['documentWidth']])
   if not 599<=m['shell']['w']<=741 or m['shell']['w']>width+1:issues.append([width,height,route,'unexpected shell width',m['shell']])
   if not m['badgeLoaded'] or not m['menuInside']:issues.append([width,height,route,'crest or menu broken'])
   if m['labelLogoCollision']>1 or m['labelMenuCollision']>1:issues.append([width,height,route,'footer collision'])
   if m['tabs'] and m['tabs']['scroll']>m['tabs']['client']+1:issues.append([width,height,route,'tabs locally clipped'])
   if width in (600,768,1024) and route in ('overview','members','calendar','compose'):
    name=f'tablet_v0137_{route}_{width}.png'
    page.screenshot(path=str(ROOT/'dist'/name),full_page=True)
    screens.append(name)
  assert not errors, (width,height,'javascript',errors)
  # Exercise native menu navigation, search/filter/clear and tab in each size.
  page.locator('.footer-nav').click()
  assert page.locator('.menu-item').count()==4
  page.locator('.menu-item[data-route="members"]').click()
  page.locator('.search-trigger').click()
  page.locator('#search-members').fill('bruno')
  assert page.locator('.member-item').count()==1,(width,'search result')
  page.locator('[data-action="clear-search"]').click()
  assert page.locator('.member-item').count()>1,(width,'search clear')
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="overview"]').click()
  page.locator('[data-overview-tab="proposicoes"]').click()
  assert page.locator('[data-overview-tab="proposicoes"]').get_attribute('aria-pressed')=='true'
  functions.append([width,height,'menu,filter,clear,tab'])
  page.close()
 for before,after in ROTATIONS:
  page=browser.new_page(viewport={'width':before[0],'height':before[1]})
  errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  page.goto('about:blank?demo=1');page.set_content(HTML)
  page.evaluate('location.hash="#/calendar"')
  page.locator('[data-action="calendar-next"]').click()
  month=page.locator('.calendar-month-nav h2').inner_text()
  page.set_viewport_size({'width':after[0],'height':after[1]})
  assert page.locator('.calendar-month-nav h2').inner_text()==month,('month lost on rotation',before,after)
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),('overflow after rotation',before,after)
  page.locator('[data-action="calendar-prev"]').click()
  assert page.locator('.calendar-month-nav h2').inner_text()!=month,('previous month after rotation broken',before,after)
  # Open menu after rotation, navigation must still be reachable.
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="proposals"]').click()
  page.locator('[data-action="new-proposal"]').click()
  page.locator('#draft-title').fill('Rascunho de rotação')
  page.locator('#draft-body').fill('Texto demonstrativo que deve permanecer no editor.')
  page.set_viewport_size({'width':before[0],'height':before[1]})
  assert page.locator('#draft-title').input_value()=='Rascunho de rotação',('draft lost on rotation',before,after)
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),('draft overflow',before,after)
  assert not errs,('javascript errors during rotate',errs)
  functions.append([before,after,'calendar,menu,draft preserve state'])
  page.close()
 browser.close()
report={'sizes':SIZES,'routes':ROUTES,'rotations':ROTATIONS,'cases':len(records),'functions':functions,'screenshots':screens,
 'issues':issues,'limitations':'Chromium CSS viewport/resize, not OS hardware orientation; no formal Megalos approval'}
(ROOT/'dist'/'stage7_tablet_v0137_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(records)==len(SIZES)*len(ROUTES)
assert not issues, f'{len(issues)} issues: {issues[:8]}'
print(f'07.07 TABLETS PASS: {len(records)} layouts, {len(functions)} functional sequences and 3 simulated rotations, no overflow/collision/JS errors')
