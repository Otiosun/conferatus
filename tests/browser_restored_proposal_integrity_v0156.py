"""Reject impossible completed proposal/session signoffs without discarding valid drafts.

Exercises local, synthetic sessionStorage records; no institutional data or Academy account.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
BASE={'id':'valid-concluded','title':'Proposição válida','body':'Texto completo e válido para comprovar o fluxo de restauração da proposição.',
      'sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[{'id':'m02','complete':True}],'status':'concluida'}
records=[BASE,
  {**BASE,'id':'valid-review','title':'Revisão válida','authorComplete':False,'partners':[{'id':'m02','complete':False}],'status':'revisao'},
  {**BASE,'id':'invalid-short-title','title':'X','partners':[]},
  {**BASE,'id':'invalid-short-body','title':'Texto inválido','body':'curto','partners':[]},
  {**BASE,'id':'invalid-review-short-body','title':'Revisão sem corpo','body':'insuficiente','authorComplete':False,'partners':[],'status':'revisao'},
  {**BASE,'id':'invalid-author-as-socii','title':'Autoria duplicada em Socii','partners':[{'id':'m01','complete':True}]},
  {**BASE,'id':'invalid-author-partial','title':'Rascunho com autoria duplicada','authorComplete':False,'status':'redacao','partners':[{'id':'m01','complete':False}]},
  {**BASE,'id':'valid-incomplete-draft','title':'', 'body':'texto parcial', 'authorComplete':False,'partners':[],'status':'redacao'}]
INVALID_IDS={'invalid-short-title','invalid-short-body','invalid-review-short-body','invalid-author-as-socii','invalid-author-partial'}


def menu(page,route):
    page.locator('.footer-nav').click()
    page.locator(f'.menu-item[data-route="{route}"]').click()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (280,390,740,1280):
        page=browser.new_page(viewport={'width':width,'height':860})
        page.set_default_timeout(7000)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('about:blank?demo=1')
        page.evaluate('''records=>{
          const store=new Map([['conferatus:proposals-v010',JSON.stringify(records)],['conferatus:deliberations-v010','[]']]);
          Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
            getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)
          }});
        }''',records)
        page.set_content(HTML)
        menu(page,'proposals')
        restored=set(page.locator('.workflow-record [data-draft]').evaluate_all('(nodes)=>nodes.map(el=>el.dataset.draft)'))
        assert restored=={'valid-concluded','valid-review','valid-incomplete-draft'},(width,'impossible completed records loaded',restored)
        assert page.locator('.workflow-form-error').filter(has_text='registros incompletos').count()==1,(width,'quarantine warning missing')
        menu(page,'calendar')
        page.locator('[data-action="open-schedule"]').click()
        select=page.locator('#schedule-deliberation-form [name="proposalId"]')
        options=select.locator('option').evaluate_all('(nodes)=>nodes.map(x=>x.value)')
        assert options==['','valid-concluded'],(width,'corrupt record became schedulable',options)
        page.locator('#schedule-deliberation-form [name="title"]').fill('Agenda válida local')
        page.locator('#schedule-deliberation-form [name="objective"]').fill('Programação demonstrativa para testar se o registro rejeitado fica preservado.')
        select.select_option('valid-concluded')
        page.locator('#schedule-deliberation-form [name="method"]').select_option('escalar')
        page.locator('#schedule-deliberation-form [name=choices]').fill('Trabalho remoto\nTrabalho presencial')
        page.locator('#schedule-deliberation-form [name="start"]').fill('2026-12-12T09:00')
        page.locator('#schedule-deliberation-form [name="end"]').fill('2026-12-12T10:00')
        page.locator('#schedule-deliberation-form button[type="submit"]').click()
        backup=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:invalid-session-backup-v0114"))')
        assert {d['id'] for d in backup['drafts']}==INVALID_IDS,(width,'rejected records not preserved in backup',backup)
        saved=page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')
        assert {d['id'] for d in saved}=={'valid-concluded','valid-review','valid-incomplete-draft'},(width,saved)
        assert not errors,(width,errors)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'horizontal overflow')
        if width==390: page.screenshot(path=str(ROOT/'dist/restored_proposal_integrity_v0156_390.png'),full_page=True)
        page.close()
    browser.close()
print('Restored proposal integrity: 4/4 widths PASS; invalid completion quarantined, partial drafts preserved')
