"""07.04: extreme titles/bodies and untrusted literal markup survive the workflow.

No inserted HTML/event handler may execute in list, editor or review.
Uses memory-only sessionStorage to avoid opaque-origin false failures; not a real storage/persistence test, nor a security audit of the Academy.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280,320,360,390,540,740,768,1024,1440)
TITLE = ('PROPOSTAINSTITUCIONALSEMSEPARADORES' * 5)[:140]
BODY = (('Relato institucional demonstrativo completo. ' * 10) +
        ('TERMOSEMQUEBRA' * 70) + '\n' + ('texto com espaços. ' * 30))
assert len(TITLE)==140
measurements=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  pg=browser.new_page(viewport={'width':width,'height':810})
  errors=[]
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.goto('about:blank?stage7=1')
  # An opaque about:blank origin blocks browser storage. For this rendering
  # test only, use session storage in memory. Persistence failures are
  # covered separately; do not mistake the mock for a real browser origin.
  pg.evaluate("""() => {
    const items=new Map();
    Object.defineProperty(window,'sessionStorage',{configurable:true,get:()=>({
      getItem:k=>items.get(String(k))??null,
      setItem:(k,v)=>items.set(String(k),String(v)),
      removeItem:k=>items.delete(String(k)),clear:()=>items.clear()
    })});
  }""")
  pg.set_content(HTML)
  pg.locator('.footer-nav').click()
  pg.locator('.menu-item[data-route="proposals"]').click()
  pg.locator('[data-action="new-proposal"]').click()
  title=pg.locator('#draft-title')
  title.fill(TITLE)
  pg.locator('#draft-body').fill(BODY)
  assert title.input_value()==TITLE,(width,'title truncated')
  pg.locator('#compose-proposal-form button[value="conclude"]').click()
  pg.locator('#confirm-proposal-form').wait_for()
  assert pg.locator('.workflow-editor-head h1').inner_text()==TITLE,(width,'review title lost')
  assert pg.locator('.workflow-review-body').inner_text().strip()==BODY.strip(),(width,'review body lost')
  assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'review overflow')
  if width in (280,390,740):
   pg.screenshot(path=str(ROOT/'dist'/f'stage7_long_draft_review_{width}.png'),full_page=True)
  pg.locator('#confirm-proposal-form button[type="submit"]').click()
  pg.locator('.workflow-status').filter(has_text='Proposição concluída.').wait_for()
  listing=pg.locator('.workflow-record').filter(has_text=TITLE)
  assert listing.count()==1,(width,'draft missing in records')
  assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'record overflow')
  listing.locator('[data-draft]').click()
  assert pg.locator('.workflow-editor-head h1').inner_text()==TITLE,(width,'final record title lost')
  assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'final record overflow')
  assert not errors,(width,errors)
  # Untrusted title and body must remain literal text through all three views.
  # This deliberately harmless marker is only set if HTML events execute.
  pg.evaluate('location.hash="#/proposals"')
  pg.locator('[data-action="new-proposal"]').click()
  probe='window.__conffratusInjectionProbe'
  hostile='<img src=x onerror="'+probe+'=1"> & <svg onload="'+probe+'=2"></svg>'
  pg.evaluate('window.__conffratusInjectionProbe=0')
  pg.locator('#draft-title').fill(hostile)
  pg.locator('#draft-body').fill(hostile)
  pg.locator('#compose-proposal-form [value="save"]').click()
  hostile_record=pg.locator('.workflow-record').filter(has_text=probe)
  hostile_record.first.wait_for(state='visible')
  assert hostile_record.count()==1,(width,'escaped draft not listed')
  assert '<img src=x' in hostile_record.inner_text(),(width,'literal markup missing from record')
  assert pg.evaluate('window.__conffratusInjectionProbe')==0,(width,'HTML event executed in record')
  assert hostile_record.locator('img[src="x"],svg[onload]').count()==0,(width,'markup interpreted in record')
  hostile_record.locator('[data-draft]').click()
  assert pg.evaluate('window.__conffratusInjectionProbe')==0,(width,'HTML event executed in editor')
  pg.locator('#compose-proposal-form [value="conclude"]').click()
  pg.locator('#confirm-proposal-form').wait_for(state='visible')
  assert '<img src=x' in pg.locator('.workflow-review-body').inner_text(),width
  assert pg.locator('.workflow-review-body img[src="x"], .workflow-review-body svg[onload]').count()==0,width
  assert pg.evaluate('window.__conffratusInjectionProbe')==0,(width,'HTML event executed in review')
  assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'markup review overflow')
  assert not errors,(width,errors)
  measurements.append({'width':width,'review':True,'records':True,'complete':True,'literalMarkupSafe':True})
  pg.close()
 browser.close()
(ROOT/'dist'/'stage7_long_draft_v0133_report.json').write_text(json.dumps(measurements,indent=2),encoding='utf-8')
print(f'07.04 long draft PASS: {len(measurements)} widths, extreme text preserved, no executable markup injected into proposal workflow')
