"""07.04: user-entered maximum title and long body survive editor/review/records.

Offline demo only, no Academy credentials or external resources.
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
  pg.get_by_text('Proposição concluída.').wait_for()
  listing=pg.locator('.workflow-record').filter(has_text=TITLE)
  assert listing.count()==1,(width,'draft missing in records')
  assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'record overflow')
  listing.locator('[data-draft]').click()
  assert pg.locator('.workflow-editor-head h1').inner_text()==TITLE,(width,'final record title lost')
  assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),(width,'final record overflow')
  assert not errors,(width,errors)
  measurements.append({'width':width,'review':True,'records':True,'complete':True})
  pg.close()
 browser.close()
(ROOT/'dist'/'stage7_long_draft_v0133_report.json').write_text(json.dumps(measurements,indent=2),encoding='utf-8')
print(f'07.04 long draft PASS: {len(measurements)} widths, 140-character title and {len(BODY)}-character body preserved in review, list and final record')
