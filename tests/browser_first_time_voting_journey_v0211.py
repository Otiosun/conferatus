"""CP169: first-time user creates a demonstration and knows where to find it."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (320,390,740,1280):
  p=browser.new_page(viewport={'width':width,'height':850})
  p.set_default_timeout(6500)
  errors=[];p.on('pageerror',lambda error:errors.append(str(error)))
  p.goto('about:blank')
  p.evaluate("""()=>{
   const items=new Map();
   Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
    getItem:k=>items.get(k)??null,setItem:(k,v)=>items.set(k,String(v)),
    removeItem:k=>items.delete(k)}});
  }""")
  p.set_content(HTML)
  expect(p.locator('.home-results-context')).to_contain_text('Resultados de exemplo')
  baseline=p.locator('.results').inner_text()
  # Megalos explicitly requested an Ofícios quantity beside Votos/PDR/PR in overview.
  p.locator('.footer-nav').click()
  p.locator('.menu-item[data-route=overview]').click()
  figures=p.locator('.overview-stats .stat-figure').all_inner_texts()
  assert len(figures)==4,(width,figures)
  assert figures[-1]=='23 Ofícios',(width,figures)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  p.locator('.footer-home').click()
  expect(p.locator('.home-create-path')).to_contain_text('primeiro redija')
  # The main shortcut must immediately expose the editor, not a button below the fold.
  p.locator('.home-create-links [data-action=new-proposal]').click()
  expect(p.locator('#compose-proposal-form')).to_be_visible()
  expect(p.locator('#draft-title')).to_be_empty()
  p.locator('.footer-home').click()
  expect(p.locator('.home-create-path')).to_be_visible()
  p.locator('.home-create-links [data-route=calendar]').click()
  expect(p.locator('.calendar-journey-guidance')).to_contain_text('Socii é opcional')
  expect(p.locator('.calendar-item').filter(has_text='Revisão do calendário de reuniões')).to_contain_text('Exemplo de programação')
  expect(p.locator('[data-action=open-schedule]')).to_contain_text('Programar votação')
  p.locator('[data-action=open-schedule]').click()
  expect(p.locator('#schedule-deliberation-form button[type=submit]')).to_be_disabled()
  expect(p.locator('.workflow-form-intro')).to_contain_text('não bloqueiam automaticamente')
  p.locator('#schedule-deliberation-form [data-route=proposals]').click()
  expect(p.locator('.workflow-start-guidance')).to_contain_text('Primeiro passo')
  p.locator('[data-action=new-proposal]').click()
  p.locator('#draft-title').fill('Proposição para votação própria')
  p.locator('#draft-body').fill('Documento fictício com uma decisão a ser discutida no calendário.')
  p.locator('#compose-proposal-form [value=conclude]').click()
  expect(p.locator('#confirm-proposal-form')).to_be_visible()
  p.locator('#confirm-proposal-form button[type=submit]').click()
  record=p.locator('.workflow-record').filter(has_text='Proposição para votação própria')
  expect(record).to_contain_text('Concluída')
  record.locator('[data-schedule-draft]').click()
  form=p.locator('#schedule-deliberation-form')
  expect(form).to_be_visible()
  selected=form.locator('[name=proposalId]')
  assert selected.input_value().startswith('draft-'),width
  expect(selected.locator('option:checked')).to_contain_text('Proposição para votação própria')
  form.locator('[name=title]').fill('Consulta sobre proposta')
  form.locator('[name=objective]').fill('Consulta fictícia relativa à proposição concluída.')
  form.locator('[name=method]').select_option('nominal')
  form.locator('[name=choices]').fill('Opção A\nOpção B')
  form.locator('[name=start]').fill('2026-12-22T10:00')
  form.locator('[name=end]').fill('2026-12-22T11:00')
  form.locator('button[type=submit]').click()
  expect(p.locator('.workflow-status')).to_contain_text('Abra a programação abaixo')
  row=p.locator('.calendar-item').filter(has_text='Consulta sobre proposta')
  expect(row).to_be_visible()
  if row.locator('[data-preview-schedule]').count()==0:
   row.locator('[data-schedule]').click()
  expect(row.locator('.calendar-vote-guidance')).to_contain_text('comprovante')
  expect(row.locator('.calendar-vote-guidance')).to_contain_text('resultados de exemplo')
  row.locator('[data-preview-schedule]').click()
  expect(p.locator('#preview-vote-title')).to_contain_text('Consulta sobre proposta')
  expect(p.locator('[name=selected]')).to_have_count(2)
  p.locator('[name=selected]').first.check()
  p.locator('.preview-vote-submit').click()
  expect(p.locator('.preview-vote-receipt')).to_contain_text('Opção A')
  p.locator('[data-action=exit-preview-schedule]').click()
  expect(row.locator('[data-schedule]')).to_be_focused()
  p.locator('.footer-home').click()
  expect(p.locator('.results')).to_be_visible()
  assert p.locator('.results').inner_text()==baseline,width
  assert not errors,(width,errors)
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  print('PASS first-time user create/participate/return',width)
  p.close()
 browser.close()
