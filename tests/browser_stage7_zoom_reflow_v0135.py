"""Stage 07.05: CSS reflow for 1280px/400%=320px and 200%=640px,
plus synthetic 200%-text stress across compact and wide viewports.
Includes the Socii review and footer legibility; storage uses a memory substitute.
This is not native browser zoom, real hardware, WCAG certification or Academy.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
VIEWPORTS=(320,640,1280) # CSS viewport equivalents for 1280px at 400%, 200%, 100%
TEXT_VIEWPORTS=(280,320,390,540,640,740,1280)
ROUTES=('ballot','members','overview','governance','calendar','proposals','compose','review')
records=[]; failures=[]; screenshots=[]

def navigate(page,route):
    page.evaluate('(route) => location.hash="#/"+route',route)
    if route=='governance':
        page.locator('.panel-button').first.click()
    elif route=='compose':
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').click()
    elif route=='review':
        # Exercise the review with an actual linked Socii participant, not a
        # blank direct hash; this adds the formerly untested review layout.
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').click()
        page.locator('#draft-title').fill('Revisão de acessibilidade')
        page.locator('#draft-body').fill('Texto demonstrativo para verificar a revisão com Socii em telas estreitas e texto ampliado.')
        page.locator('#compose-proposal-form [value="save"]').click()
        page.locator('[data-action="invite-socii"]').click()
        page.locator('#invite-socii-form [name="memberId"]').select_option(index=1)
        page.locator('#invite-socii-form button.workflow-primary').click()
        record=page.locator('.workflow-record').filter(has_text='Revisão de acessibilidade')
        record.locator('[data-confirm-partner]').click()
        page.locator('.workflow-record').filter(has_text='Revisão de acessibilidade').locator('[data-draft]').click()
        page.locator('#confirm-proposal-form').wait_for(state='visible')

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
      const homeEl=footer.querySelector('.footer-home'), navEl=footer.querySelector('.footer-nav');
      const brandRange=document.createRange();
      brandRange.selectNodeContents(homeEl);
      const brandLines=new Set([...brandRange.getClientRects()]
          .filter(r=>r.width>0).map(r=>Math.round(r.top))).size;
      const f=rect(footer),home=rect(homeEl),
            demo=rect(footer.querySelector('.footer-demo')),nav=rect(navEl),
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
                  brandLines, navClipped:navEl.scrollHeight>navEl.clientHeight+1,
                  h:home, demo, nav, logo, height:f.height},cal,header,
          reviewNote:(()=>{
            const note=document.querySelector('.workflow-review-sheet > p');
            if(!note)return null;
            const rgb=s=>(s.match(/[0-9.]+/g)||[]).slice(0,3).map(Number);
            const luminance=s=>{
              const [r,g,b]=rgb(s).map(n=>{
                const c=n/255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4;
              });
              return .2126*r+.7152*g+.0722*b;
            };
            const fg=luminance(getComputedStyle(note).color);
            const bg=luminance(getComputedStyle(note.parentElement).backgroundColor);
            const labelContrasts=[...note.parentElement.querySelectorAll('label')].map(label=>{
              const labelLight=luminance(getComputedStyle(label).color);
              return (Math.max(labelLight,bg)+.05)/(Math.min(labelLight,bg)+.05);
            });
            return {contrast:(Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05),labelContrasts};
          })(),
          statsLocalOverflow:statRail?statRail.scrollWidth>statRail.clientWidth+1:false};
    }''')
    errors=[]
    if results['scroll']>results['client']+1:errors.append('document overflow')
    if not results['footer']['inside']:errors.append('footer text clipped')
    if results['footer']['collisions']>1:errors.append('footer text overlaps crest/menu')
    if width<=360 and results['footer']['brandLines']!=1:errors.append('footer brand wraps at compact width')
    if results['footer']['navClipped']:errors.append('footer menu label is clipped')
    if route=='review' and (not results['reviewNote'] or results['reviewNote']['contrast']<4.5):
        errors.append('review notice text contrast below 4.5:1')
    if route=='review' and results['reviewNote'] and any(value<4.5 for value in results['reviewNote']['labelContrasts']):
        errors.append('review form label contrast below 4.5:1')
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
            page.goto('about:blank?demo=1')
            # Opaque about:blank denies native sessionStorage. Replace it only
            # for this visual/reflow test; persistence failures have separate tests.
            page.evaluate('''() => {
              const values=new Map();
              Object.defineProperty(window,'sessionStorage',{configurable:true,
                get:()=>({
                  getItem:k=>values.get(String(k))??null,
                  setItem:(k,v)=>values.set(String(k),String(v)),
                  removeItem:k=>values.delete(String(k)),
                  clear:()=>values.clear()
                })});
            }''')
            page.set_content(HTML)
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
print('07.05 zoom/reflow PASS:',len(records),'route-width combinations (24 viewport equivalents + 56 synthetic text-size stresses); month controls functional')
print('NOTE: 640px overview statistics remain in an intentional internal scrolling rail, not document-level overflow.')
