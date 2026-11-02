"""Stage 07.05: reflow at 1280px/400%=320 CSS px, 200%=640 CSS px;
plus an explicitly synthetic 200% TEXT-ONLY enlargement stress test.

This is Chromium offline, not native browser chrome zoom, Firefox text zoom,
WebKit, OS font scaling or hardware certification. Never imply otherwise.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
VIEWPORTS=(320,640,1280) # CSS viewport equivalents for 1280px at 400%, 200%, 100%
TEXT_VIEWPORTS=(280,320,390,540,640,740,1280)
ROUTES=('ballot','members','overview','governance','calendar','proposals','compose')
records=[]; failures=[]; screenshots=[]

def navigate(page,route):
    page.evaluate('(route) => location.hash="#/"+route',route)
    if route=='governance':
        page.locator('.panel-button').first.click()
    elif route=='compose':
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').click()

def scale_text(page):
    # Intentionally style only text-bearing DOM nodes; persistent nodes are
    # flagged so navigation doesn't compound the font-size multiplier.
    page.evaluate('''() => { for(const el of document.querySelectorAll('body *')) {
      if(el.dataset.stage7Text200 || ![...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim())) continue;
      const size=parseFloat(getComputedStyle(el).fontSize);
      if(size>0 && size<100){el.style.setProperty('font-size',size*2+'px','important');el.dataset.stage7Text200='1';}
    }}''')

def measure(page,mode,width,route):
    results=page.evaluate('''() => {
      const rect=el=>{const b=el.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,height:b.height}};
      const footer=document.querySelector('.app-footer');
      const within=(a,b)=>a.left>=b.left-1&&a.right<=b.right+1&&a.top>=b.top-1&&a.bottom<=b.bottom+1;
      const intersection=(a,b)=>Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left))*Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
      const f=rect(footer),home=rect(footer.querySelector('.footer-home')),
            demo=rect(footer.querySelector('.footer-demo')),nav=rect(footer.querySelector('.footer-nav')),
            logo=rect(footer.querySelector('img'));
      let cal=null, header=null;
      const month=document.querySelector('.calendar-month-nav');
      if(month){const nodes=month.querySelectorAll('button,h2');const [prev,title,next]=[...nodes].map(rect);
         cal={prev,title,next,overlap:intersection(prev,title)+intersection(title,next),inside:within(title,rect(month))};}
      const heading=document.querySelector('.page-header h1');
      if(heading){const r=rect(heading), panel=document.querySelector('.page-header .panel-button');header={title:r,overlap:panel?intersection(r,rect(panel)):0};}
      const statRail=document.querySelector('.overview-stats');
      return {client:innerWidth,scroll:document.documentElement.scrollWidth,
          footer:{inside:within(home,f)&&within(demo,f),collisions:intersection(home,nav)+intersection(demo,nav)+intersection(home,logo)+intersection(demo,logo),
                  h:home, demo, nav, logo, height:f.height},cal,header,
          statsLocalOverflow:statRail?statRail.scrollWidth>statRail.clientWidth+1:false};
    }''')
    errors=[]
    if results['scroll']>results['client']+1:errors.append('document overflow')
    if not results['footer']['inside']:errors.append('footer text clipped')
    if results['footer']['collisions']>1:errors.append('footer text overlaps crest/menu')
    if results['cal'] and (results['cal']['overlap']>1 or not results['cal']['inside']):errors.append('calendar month/nav collision')
    if results['header'] and results['header']['overlap']>1:errors.append('header title overlaps settings button')
    if errors:failures.append({'mode':mode,'width':width,'route':route,'errors':errors,'metrics':results})
    records.append({'mode':mode,'width':width,'route':route,'metrics':results})

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for mode,widths in (('viewport-equivalent-zoom',VIEWPORTS),('synthetic-text-200',TEXT_VIEWPORTS)):
        for width in widths:
            page=browser.new_page(viewport={'width':width,'height':780})
            page_errors=[]
            page.on('pageerror',lambda e:page_errors.append(str(e)))
            page.goto('about:blank?demo=1');page.set_content(HTML)
            for route in ROUTES:
                navigate(page,route)
                if mode=='synthetic-text-200':scale_text(page)
                measure(page,mode,width,route)
                if mode=='synthetic-text-200' and width==320 and route in ('ballot','governance','calendar'):
                    name=f'zoom_text200_{route}_{width}.png'
                    page.screenshot(path=str(ROOT/'dist'/name),full_page=True)
                    screenshots.append(name)
                if mode=='viewport-equivalent-zoom' and width==320 and route in ('ballot','calendar'):
                    name=f'zoom_reflow_{route}_{width}.png'
                    page.screenshot(path=str(ROOT/'dist'/name),full_page=True)
                    screenshots.append(name)
            # Prove key controls work at CSS viewport equivalent of 400%.
            page.evaluate('location.hash="#/calendar"')
            if mode=='synthetic-text-200':scale_text(page)
            before=page.locator('.calendar-month-nav h2').inner_text()
            page.locator('[data-action="calendar-next"]').click()
            after=page.locator('.calendar-month-nav h2').inner_text()
            assert before!=after,(width,mode,'month navigation failed')
            assert not page_errors,(width,mode,'javascript errors',page_errors)
            page.close()
    browser.close()
report={'cases':len(records),'routes':ROUTES,'viewportWidths':VIEWPORTS,'textOnlyWidths':TEXT_VIEWPORTS,
        'failures':failures,'text-only-is-synthetic':True,'screenshots':screenshots,
        'intentionalStatsRailAt640':sum(1 for x in records if x['width']==640 and x['route']=='overview' and x['metrics']['statsLocalOverflow'])}
(ROOT/'dist'/'stage7_zoom_reflow_v0135_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
assert len(records)==len(ROUTES)*(len(VIEWPORTS)+len(TEXT_VIEWPORTS)),('incomplete scenario matrix',len(records))
assert not failures,f'{len(failures)} zoom/reflow failures: {failures[:5]}'
print('07.05 zoom/reflow PASS:',len(records),'route-width combinations (21 viewport equivalents + 49 synthetic text-size stresses); month controls functional')
print('NOTE: 640px overview statistics remain in an intentional internal scrolling rail, not document-level overflow.')
