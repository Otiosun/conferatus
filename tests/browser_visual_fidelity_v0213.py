"""Reference image fidelity regression: visual geometry, not just JavaScript state.
The exact votes/labels are still independent examples awaiting Megalos' approval.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,320,390,540,740):
  page=browser.new_page(viewport={'width':width,'height':844})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('about:blank')
  page.set_content(HTML)
  assert page.locator('.ballot-participation-dots ellipse').count()==76,width
  assert page.locator('.ballot-participation-scene svg').get_attribute('viewBox')=='0 0 710 363',width
  expect(page.locator('.ballot-participation-value')).to_have_text('76%')
  expect(page.locator('.ballot-participation-caption')).to_have_text('Taxa de participação')
  expect(page.locator('.home-results-context')).to_have_text('Resultados de exemplo · percentuais por alternativa')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  if width==390:
   layout=page.evaluate("""() => {
    const box=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,height:r.height}};
    return {header:box('.ballot-participation-top'),figure:box('.ballot-participation'),
     firstCard:box('.ballot-page .result-row'),description:box('.description-panel'),footer:box('.app-footer')};
   }""")
   assert 24<=layout['header']['height']<=31,layout
   assert 215<=layout['figure']['height']<=237,layout
   assert 225<=layout['firstCard']['top']<=247,layout
   assert 40<=layout['firstCard']['height']<=50,layout
   assert 330<=layout['description']['top']<=370,layout
   assert 785<=layout['footer']['top']<=830,layout
  page.evaluate("location.hash='#/overview'")
  page.locator('.overview-stats').wait_for(state='visible')
  metrics=page.locator('.overview-stats > *').evaluate_all("""es=>es.map(e=>{
    const r=e.getBoundingClientRect();return {text:e.textContent.trim(),left:r.left,right:r.right};
  })""")
  assert len(metrics)==6,(width,metrics)
  assert metrics[-1]['text'].endswith('Ofícios'),(width,metrics)
  assert all(m['left']>=-1 and m['right']<=width+1 for m in metrics),(width,metrics)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  assert not errors,(width,errors)
  page.close()
 browser.close()
print('Reference geometry and all six indicators visible across five viewport widths')
