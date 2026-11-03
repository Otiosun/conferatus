"""Academy identity boundary: visibly honest, no second login, no implicit power.

Offline preview only; this cannot verify real Academy authentication.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':840})
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank?demo=1')
  page.set_content(HTML)
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="overview"]').click()
  page.locator('.panel-button').click()
  page.locator('[data-action="toggle-tools"]').click()
  panel=page.locator('.demo-tools')
  panel.wait_for(state='visible')
  text=panel.inner_text()
  assert 'Identidade Academy: não conectada' in text,(width,text)
  assert 'perfis abaixo são simulações, não permissões reais' in text,(width,text)
  assert not page.locator('input[type=password]').count(),width
  assert not page.locator('form[action*="login"],form[action*="auth"]').count(),width
  assert not errors,(width,errors)
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),width
  if width==390:page.screenshot(path=str(ROOT/'dist/academy_identity_boundary_390.png'),full_page=True)
  page.close()
 browser.close()
print('ACADEMY IDENTITY BOUNDARY PASS: 4 viewports, no false login/authorization or overflow')
