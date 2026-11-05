"""Menu gesture regression from 05/11/2026 Android recording.

Previously opening the menu changed document height by ~231 CSS px,
pushing the footer below the screen. Uses simulated storage because
about:blank is an opaque origin; this is not a real-device test.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
SIZES=((280,600),(320,568),(360,760),(390,760),(540,760),(740,700),(1280,900),(360,360))
results=[]
METRICS="""() => {
  const rect=selector=>{
    const element=document.querySelector(selector);
    if(!element)return null;
    const box=element.getBoundingClientRect();
    return {top:box.top,bottom:box.bottom,height:box.height};
  };
  return {scrollY:scrollY,docHeight:document.documentElement.scrollHeight,
    clientHeight:innerHeight,
    overflow:document.documentElement.scrollWidth>innerWidth+1,
    menu:rect('.bottom-menu'),footer:rect('.app-footer')};
}"""

with sync_playwright() as playwright:
    browser=playwright.chromium.launch(
        headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width,height in SIZES:
        page=browser.new_page(viewport={'width':width,'height':height},
                              is_mobile=width<740,has_touch=True)
        page.set_default_timeout(7000)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.goto('about:blank')
        page.evaluate("""() => {
          const state=new Map();
          Object.defineProperty(window,'sessionStorage',{configurable:true,get:()=>({
            getItem:k=>state.get(String(k))??null,
            setItem:(k,v)=>state.set(String(k),String(v)),
            removeItem:k=>state.delete(String(k)),
            clear:()=>state.clear()
          })});
        }""")
        page.set_content(HTML)
        page.locator('.footer-nav').wait_for()
        page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)')
        before=page.evaluate(METRICS)
        page.evaluate("""() => {
          const brand=document.querySelector('.footer-home');
          const touch=y=>new Touch({identifier:1,target:brand,
              clientX:innerWidth/2,clientY:y});
          brand.dispatchEvent(new TouchEvent('touchstart',
              {bubbles:true,touches:[touch(innerHeight-40)]}));
          brand.dispatchEvent(new TouchEvent('touchend',
              {bubbles:true,touches:[],changedTouches:[
                  touch(innerHeight-105)]}));
        }""")
        after=page.evaluate(METRICS)
        assert after['menu'],(width,height,'swipe did not open')
        assert page.locator('footer.app-footer > nav.bottom-menu').count()==1
        assert after['docHeight']==before['docHeight'],(width,height,'page height changed')
        assert abs(after['scrollY']-before['scrollY'])<=1,(width,height,'scroll jumped')
        assert abs(after['menu']['bottom']-after['footer']['top'])<=1.5,(
            width,height,'drawer not anchored')
        assert after['menu']['top']>=-1,(width,height,'drawer outside screen')
        assert not after['overflow'],(width,height,'horizontal overflow')
        assert page.locator('.footer-nav').get_attribute('aria-expanded')=='true'
        center=page.evaluate("""() => {
          const r=selector=>{
            const el=document.querySelector(selector);
            if(!el)return null;
            const b=el.getBoundingClientRect();
            return {cx:b.left+b.width/2,top:b.top};
          };
          return {logo:r('.drawer-crest'),title:r('.footer-home'),
            items:[...document.querySelectorAll('.bottom-menu .menu-item')]
              .map(el=>{const b=el.getBoundingClientRect();return b.left+b.width/2;})};
        }""")
        assert center['logo'] and abs(center['logo']['cx']-width/2)<=1,(width,'crest off axis')
        assert abs(center['title']['cx']-width/2)<=1,(width,'brand off axis')
        assert all(abs(cx-width/2)<=1 for cx in center['items']),(width,'item off axis')
        assert center['logo']['top']>=-1,(width,'crest clipped')
        if (width,height) in ((320,568),(390,760)):
            page.screenshot(path=str(ROOT/'dist'/f'footer_drawer_{width}.png'))
        page.locator('.footer-nav').click()
        assert page.locator('.bottom-menu').count()==0
        closed=page.locator('footer.app-footer > img').bounding_box()
        assert closed and abs(closed['x']+closed['width']/2-width/2)<=1,(width,'closed crest off axis')
        page.locator('.footer-nav').focus()
        page.keyboard.press('Enter')
        assert page.locator('.menu-item').first.evaluate(
            '(el)=>document.activeElement===el'),(width,'menu keyboard focus')
        page.keyboard.press('Escape')
        assert page.locator('.bottom-menu').count()==0
        assert page.locator('.footer-nav').evaluate(
            '(el)=>document.activeElement===el'),(width,'focus not restored')
        page.locator('.footer-nav').click()
        page.locator('.menu-item[data-route="members"]').click()
        assert '#/members' in page.url,(width,'route failed')
        assert not errors,(width,errors)
        results.append({'width':width,'height':height,'pass':True})
        page.close()
    browser.close()
(ROOT/'dist'/'footer_drawer_regression.json').write_text(
    json.dumps({'results':results,'limitations':'offline simulated storage; no real devices'},
               indent=2),encoding='utf-8')
print(f'FOOTER_DRAWER PASS: {len(results)}/{len(SIZES)} mobile gesture/layout journeys')
