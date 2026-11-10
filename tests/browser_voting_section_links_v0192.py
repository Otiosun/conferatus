"""Cross-section, cross-method link integrity for the fictional prototype only.
No Academy roles or binding institutional voting rules are asserted.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
SECTIONS=('diretoria','coordenacao','integridade','representantes')
MODES=('binaria','nominal','ordenada','aprovacao','escalar','cumulativa')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    covered=0
    for section in SECTIONS:
        for method in MODES:
            id_='sched-'+section+'-'+method
            proposal={
                'id':'draft-'+section+'-'+method,
                'title':'Proposta da seção '+section+' / '+method,
                'body':'Proposta de demonstração com dados fictícios.',
                'sectionId':section,'type':'PDR',
                'authorComplete':True,'partners':[],'status':'concluida'
            }
            schedule={
                'id':id_,'title':'Deliberação '+section+' / '+method,
                'objective':'Teste do vínculo local sem dados de integrantes reais.',
                'proposalId':proposal['id'],'sectionId':section,
                'start':'2026-12-21T09:00','end':'2026-12-21T11:00',
                'type':'PDR','status':'programada','method':method
            }
            if method!='binaria':
                schedule['choices']=[{'id':'opt-1','label':'Opção da '+section},
                                     {'id':'opt-2','label':'Alternativa fictícia'}]
            page=browser.new_page(viewport={'width':390,'height':844})
            page.set_default_timeout(5000)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto('about:blank')
            page.evaluate('''([draft,item]) => {
              const store=new Map([
                ['conferatus:proposals-v010',JSON.stringify([draft])],
                ['conferatus:deliberations-v010',JSON.stringify([item])]
              ]);
              Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
                getItem:key=>store.get(key)??null,
                setItem:(key,val)=>store.set(key,String(val)),
                removeItem:key=>store.delete(key)
              }});
            }''',[proposal,schedule])
            page.set_content(HTML)
            page.locator('.footer-nav').click()
            page.locator('.menu-item[data-route=calendar]').click()
            row=page.locator(f'[data-schedule="{id_}"]')
            expect(row).to_be_visible()
            expect(row).to_contain_text('Deliberação '+section+' / '+method)
            row.click()
            details=page.locator(f'#schedule-details-{id_}')
            expect(details).to_be_visible()
            expect(details).to_contain_text('Modalidade:')
            expect(details).to_contain_text('Opção da '+section if method!='binaria' else 'Modalidade:')
            expect(page.locator(f'[data-open-schedule-proposal="{proposal["id"]}"]')).to_be_visible()
            page.locator(f'[data-preview-schedule="{id_}"]').click()
            expect(page.locator('#preview-vote-lab')).to_be_visible()
            expect(page.locator('.preview-vote-detail').first).to_contain_text('Modalidade:')
            expect(page.locator('.preview-vote-context')).to_contain_text(proposal['title'])
            expect(page.locator('.preview-vote-context')).to_contain_text(schedule['title'])
            assert page.locator('.results').count()==0, (section,method)
            if method=='binaria':
                expect(page.locator('#preview-vote-form')).to_contain_text('Sim')
            else:
                expect(page.locator('#preview-vote-form')).to_contain_text('Opção da '+section)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),(section,method)
            assert not errors,(section,method,errors)
            covered+=1
            page.close()
    browser.close()
    print(f'PASS: {covered} fictional section/method/program/proposal links; no unrelated vote results')
