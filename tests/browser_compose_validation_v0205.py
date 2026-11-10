"""Proposal UX: short titles are explained; partial drafts remain resumable in-session."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
DRAFT_KEY='conferatus:proposals-v010'
SCHEDULE_KEY='conferatus:deliberations-v010'

def boot(browser,width,seed=None):
 p=browser.new_page(viewport={'width':width,'height':850})
 p.set_default_timeout(6000)
 p.goto('about:blank')
 p.evaluate("""entries=>{
  const store=new Map(Object.entries(entries));
  Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
   getItem:k=>store.get(k)??null,
   setItem:(k,v)=>store.set(k,String(v)),
   removeItem:k=>store.delete(k)
  }});
 }""",seed or {})
 p.set_content(HTML)
 p.evaluate("location.hash='#/proposals'")
 return p

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=boot(browser,width)
  errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.locator('[data-action=new-proposal]').click()
  p.locator('#draft-title').fill('  A  ')
  original='Uma redação suficientemente longa para testar a revisão da proposição.'
  p.locator('#draft-body').fill(original)
  p.locator('#compose-proposal-form button[value=conclude]').click()
  expect(p.locator('#compose-save-error')).to_contain_text('título com pelo menos 3 caracteres')
  expect(p.locator('#draft-title')).to_be_focused()
  expect(p.locator('#draft-body')).to_have_value(original)
  assert p.locator('#draft-title').get_attribute('aria-invalid')=='true',width
  assert p.locator('#draft-body').get_attribute('aria-invalid') is None,width

  p.locator('#draft-title').fill('Proposição retomável')
  p.locator('#draft-body').fill('Texto curto')
  p.locator('#compose-proposal-form button[value=conclude]').click()
  expect(p.locator('#compose-save-error')).to_contain_text('20 caracteres')
  expect(p.locator('#draft-body')).to_be_focused()
  assert p.locator('#draft-title').get_attribute('aria-invalid') is None,width
  assert p.locator('#draft-body').get_attribute('aria-invalid')=='true',width

  p.locator('#compose-proposal-form button[value=save]').click()
  expect(p.locator('.workflow-status')).to_contain_text('somente nesta aba do navegador')
  saved=p.evaluate("JSON.parse(sessionStorage.getItem('conferatus:proposals-v010'))")
  assert len(saved)==1 and saved[0]['title']=='Proposição retomável',width
  assert saved[0]['body']=='Texto curto' and saved[0]['status']=='redacao',width
  snapshot={key:p.evaluate('key=>sessionStorage.getItem(key)',key) for key in (DRAFT_KEY,SCHEDULE_KEY)}
  p.close()

  resumed=boot(browser,width,snapshot)
  resumed.on('pageerror',lambda e:errors.append(str(e)))
  record=resumed.locator('.workflow-record').filter(has_text='Proposição retomável')
  expect(record).to_be_visible()
  record.locator('[data-draft]').click()
  expect(resumed.locator('#draft-title')).to_have_value('Proposição retomável')
  expect(resumed.locator('#draft-body')).to_have_value('Texto curto')
  resumed.locator('#draft-body').fill(original)
  resumed.locator('#compose-proposal-form button[value=conclude]').click()
  expect(resumed.locator('#confirm-proposal-form')).to_be_visible()
  expect(resumed.locator('.workflow-review-body')).to_contain_text('Uma redação suficientemente longa')
  assert not errors,(width,errors)
  assert resumed.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS short-title feedback and partial-draft resume',width)
  resumed.close()
 browser.close()
