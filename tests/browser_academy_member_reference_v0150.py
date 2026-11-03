"""Reference-only profile deep links. No Academy session, auth or role inference."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as playwright:
  browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width in (280,390,740,1280):
    page=browser.new_page(viewport={'width':width,'height':840})
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.set_content(HTML)
    page.evaluate("location.hash='#/profile/acdm/DEMO-0002'")
    page.get_by_text('Caio Martins').first.wait_for()
    assert 'Caio Martins' in page.locator('.profile-identity').inner_text(),width
    ref_link=page.locator('.profile-reference-link')
    assert ref_link.count()==1,width
    assert ref_link.get_attribute('href')=='#/profile/acdm/DEMO-0002',width
    assert 'referência' in ref_link.get_attribute('aria-label').lower(),width
    assert ref_link.bounding_box()['height']>=44,(width,ref_link.bounding_box())
    page.evaluate("location.hash='#/profile/acdm/DEMO-UNLISTED'")
    page.get_by_text('Perfil não encontrado').wait_for()
    assert page.locator('.profile-reference-link').count()==0,width
    page.evaluate("location.hash='#/profile/m02'")
    page.get_by_text('Caio Martins').first.wait_for()
    page.locator('.profile-reference-link').click()
    assert page.evaluate('location.hash')=='#/profile/acdm/DEMO-0002',width
    assert page.locator('input[type=password]').count()==0,width
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),width
    assert not errors,(width,errors)
    if width==390:page.screenshot(path=str(ROOT/'dist/academy_reference_profile_390.png'),full_page=True)
    page.close()
  browser.close()
print('ACADEMY MEMBER REFERENCE PASS: 4 viewports, exact synthetic ID lookup, safe unknown, clickable deep link')
