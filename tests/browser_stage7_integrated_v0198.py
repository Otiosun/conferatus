"""Focused stage-07 functional audit on the compiled fictional prototype.
Uses equivalent compact CSS viewports, synthetic doubled text and reduced viewport
heights; does not claim native browser zoom, mobile OS keyboard or WCAG certification.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
ROUTES=('ballot','members','profile/m01','overview','governance','calendar','proposals')
CASES=[];ERRORS=[]

def measure(page,width,tag):
    data=page.evaluate('''() => {
      let interactive=[...document.querySelectorAll('button,input,textarea,select,a[href]')].filter(el=>el.getClientRects().length && getComputedStyle(el).visibility!=='hidden');
      const missing=interactive.filter(el=> !(
       (el.getAttribute('aria-label')||'').trim() || (el.getAttribute('aria-labelledby')||'').trim() ||
       (el.labels&&el.labels.length) || (el.textContent||'').trim() || (el.getAttribute('title')||'').trim()
      )).map(el=>el.outerHTML.slice(0,140));
      return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
              missing,buttons:interactive.length,headings:document.querySelectorAll('#main-content h1').length};
    }''')
    row={'name':tag,'target':width,**data};CASES.append(row)
    if data['scrollWidth']>width+1 or data['missing'] or data['headings']!=1: ERRORS.append(row)

def double_text(page):
    page.evaluate('''() => {
      for(const el of document.querySelectorAll('body *')){
        if(el.dataset.stage7Text200 || ![...el.childNodes].some(n=>n.nodeType===3 && n.textContent.trim()))continue;
        const px=parseFloat(getComputedStyle(el).fontSize);
        if(px>0 && px<100){el.style.setProperty('font-size',(px*2)+'px','important');el.dataset.stage7Text200='1';}
      }
    }''')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width,mode in ((320,'equivalent400'),(640,'equivalent200'),(280,'compact'),(320,'text200'),(390,'text200'),(740,'text200')):
        page=browser.new_page(viewport={'width':width,'height':760},reduced_motion='reduce')
        page.set_default_timeout(5000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('about:blank');page.set_content(HTML)
        for route in ROUTES:
            page.evaluate('(r)=>location.hash="#/"+r',route)
            page.wait_for_timeout(15)
            if mode=='text200':double_text(page)
            measure(page,width,mode+'-'+route)
        # Real interaction with locally enlarged text (not only screenshots).
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action=new-proposal]').click()
        page.locator('#draft-title').fill('Proposição de teste de reflow')
        page.locator('#draft-body').fill('Redação sintética que será revista e confirmada com texto ampliado.')
        if mode=='text200':double_text(page)
        measure(page,width,mode+'-compose')
        page.locator('#compose-proposal-form [value=conclude]').click()
        page.locator('#confirm-proposal-form').wait_for(state='visible')
        if mode=='text200':double_text(page)
        measure(page,width,mode+'-review')
        page.locator('#confirm-proposal-form button[type=submit]').click()
        expect(page.locator('.workflow-record')).to_be_visible()
        if errors:ERRORS.append({'name':mode,'JS errors':errors})
        page.close()
    # Simulated short keyboard and landscape interaction: not a real native IME.
    for w,h in ((280,320),(320,280),(390,430),(568,320),(740,360)):
        page=browser.new_page(viewport={'width':w,'height':h},is_mobile=True,has_touch=True)
        page.set_default_timeout(5500)
        page.goto('about:blank');page.set_content(HTML)
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="members"]').click()
        page.locator('.search-trigger').click()
        search=page.locator('#search-members');search.click()
        search.fill('Bruno')
        page.set_viewport_size({'width':w,'height':max(205,h-130)})
        search.scroll_into_view_if_needed()
        m=page.evaluate('''() => {
          const r=document.activeElement.getBoundingClientRect();
          return {focus:document.activeElement.id,top:r.top,bottom:r.bottom,height:innerHeight,
           overflow:document.documentElement.scrollWidth-innerWidth};
        }''')
        CASES.append({'name':f'virtual-keyboard-height-{w}x{h}',**m})
        if m['focus']!='search-members' or m['top']<-2 or m['bottom']>m['height']+2 or m['overflow']>1:ERRORS.append(CASES[-1])
        page.close()
    browser.close()

(ROOT/'dist'/'stage07_integrated_v0198.json').write_text(json.dumps({'checks':len(CASES),'failures':ERRORS,'results':CASES},indent=2,ensure_ascii=False))
print('07.05/07.06/07.10 scoped Chromium cases',len(CASES),'errors',len(ERRORS))
for e in ERRORS[:20]:print('FAIL',e)
assert not ERRORS, 'Stage-07 integrated synthetic checks failed'
