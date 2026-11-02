"""Stage 07: the user's official Academy badge replaces the placeholder in the real footer/menu.

Offline preview validation; no authenticated data, external services or production dependencies.
"""
from pathlib import Path
from hashlib import sha256
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT/'public/assets/crest.png'
OFFLINE = ROOT/'dist/CONFFRATUS_demo_offline.html'
# Pin the image accepted by the owner; don't regress to the tiny pixel-art placeholder.
EXPECTED_SHA = 'b856a8f9be1a8c9e7033ec7039e419e0f9ed665fa9061671f2a615bb24cc1f03'
image = ASSET.read_bytes()
assert sha256(image).hexdigest() == EXPECTED_SHA, 'Official Academy image unexpectedly replaced'
assert len(image) > 4_000, 'Official badge reduced to placeholder/icon'
html = OFFLINE.read_text(encoding='utf-8')
assert 'data:image/png;base64,' in html
assert '<title>CONFFRATUS</title>' in html

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,320,360,390,540,740,768,1024,1440):
  page=browser.new_page(viewport={'width':width,'height':860},device_scale_factor=1)
  page.goto('about:blank')
  errors=[]
  page.on('pageerror', lambda error: errors.append(str(error)))
  page.set_content(html)
  for route in ('ballot','members'):
   if route=='members':
    page.locator('.footer-nav').click()
    page.locator('.menu-item[data-route=members]').click()
   page.locator('.footer-nav').click()
   image_el=page.locator('.app-footer > img')
   assert image_el.count()==1,(width,route,'official crest missing')
   assert image_el.get_attribute('alt') == 'Símbolo da Academy'
   assert image_el.evaluate('(el) => el.complete && el.naturalWidth===256 && el.naturalHeight===216'),(width,route,'crest failed to load')
   metrics=page.evaluate('''() => {
     const r=(selector)=>{const el=document.querySelector(selector);const b=el.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height}};
     return {logo:r('.app-footer > img'),last:r('.menu-item:last-child'),home:r('.footer-home'),menu:r('.footer-nav'),overflow:document.documentElement.scrollWidth>innerWidth+1};
   }''')
   logo, last, home, menu=metrics['logo'],metrics['last'],metrics['home'],metrics['menu']
   assert logo['w']>=40 and logo['h']>=40,(width,route,'official badge too small',logo)
   assert logo['y']>=last['y']+last['h']-1,(width,route,'logo overlaps menu item',metrics)
   assert logo['x']+logo['w']<=home['x']+1,(width,route,'logo overlaps CONFFRATUS home label',metrics)
   assert logo['x']+logo['w']<=menu['x']+1,(width,route,'logo overlaps menu trigger',metrics)
   assert not metrics['overflow'],(width,route,'horizontal overflow')
   if route=='ballot' and width in (280,390,740):
    page.screenshot(path=str(ROOT/f'dist/academy_crest_verified_{width}.png'),full_page=True)
   page.locator('.footer-nav').click()
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('Academy official crest: PASS across 9 widths × 2 routes, official badge embedded and no menu collisions')
