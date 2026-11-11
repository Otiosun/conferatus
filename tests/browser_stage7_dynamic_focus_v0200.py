"""Dynamic focus continuity across fictional interactive routes.
Covers keyboard-triggered replacement of controls and negative cancellation.
Chromium desktop viewports only; does not certify screen-reader/WCAG AA.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML=(Path(__file__).resolve().parents[1]/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS=(280,320,390,740,1280)
DRAFT={'id':'draft-focus-01','title':'Proposta de foco','body':'Uma proposta inteiramente fictícia.',
       'sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
SCHEDULE={'id':'schedule-focus-01','title':'Programação de foco','objective':'Teste de foco acessível.',
          'proposalId':'draft-focus-01','sectionId':'integridade','start':'2026-12-21T09:00',
          'end':'2026-12-21T11:00','type':'PDR','status':'programada','method':'nominal',
          'choices':[{'id':'opt-1','label':'Alternativa A'},{'id':'opt-2','label':'Alternativa B'}]}

def focus_then_enter(page, selector, expected):
    el=page.locator(selector).first
    expect(el).to_be_visible()
    el.focus()
    el.press('Enter')
    assert page.evaluate('(s)=>document.activeElement.matches(s)',expected), (
        page.viewport_size,selector,expected,
        page.evaluate('document.activeElement.outerHTML.slice(0,220)'))

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    checks=0
    for width in WIDTHS:
        def scene(route, records=False):
            page=browser.new_page(viewport={'width':width,'height':850})
            page.set_default_timeout(5000)
            page.goto('about:blank')
            if records:
                page.evaluate('''([draft,schedule])=>{
                 const store=new Map([
                  ['conferatus:proposals-v010',JSON.stringify([draft])],
                  ['conferatus:deliberations-v010',JSON.stringify([schedule])]
                 ]);
                 Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
                   getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v)),
                   removeItem:k=>store.delete(k)
                 }});
                }''',[DRAFT,SCHEDULE])
            page.set_content(HTML)
            page.evaluate('(route)=>{location.hash="#/"+route}',route)
            return page
        page=scene('ballot')
        focus_then_enter(page,'[data-action=enter-ballot]','input[name=selected]');checks+=1
        # An empty attempt must focus the inline validation message.
        focus_then_enter(page,'.preview-vote-submit','#preview-vote-error');checks+=1
        page.locator('input[name=selected]').first.check()
        focus_then_enter(page,'.preview-vote-submit','.preview-vote-receipt');checks+=1
        focus_then_enter(page,'[data-action=reset-preview-vote]','input[name=selected]');checks+=1
        focus_then_enter(page,'[data-action=exit-preview-schedule]','[data-action=enter-ballot]');checks+=1
        page.close()
        page=scene('overview')
        focus_then_enter(page,'[data-overview-tab=proposicoes]','[data-overview-tab=proposicoes]');checks+=1
        page.close()
        page=scene('calendar')
        for selector,expected in (
         ('[data-schedule]','[data-schedule]'),
         ('[data-action=calendar-next]','[data-action=calendar-next]'),
         ('[data-calendar-day]','[data-calendar-day]')
        ):
            focus_then_enter(page,selector,expected);checks+=1
        page.close()
        page=scene('members')
        focus_then_enter(page,'[data-action=search]','#search-members');checks+=1
        page.locator('#search-members').fill('Bruno')
        focus_then_enter(page,'[data-action=clear-search]','#search-members');checks+=1
        page.close()
        page=scene('governance')
        focus_then_enter(page,'[data-section=coordenacao]','[data-section=coordenacao]');checks+=1
        focus_then_enter(page,'[data-edit]','#member-acdm-id');checks+=1
        page.keyboard.press('Escape')
        assert page.evaluate('document.activeElement.hasAttribute("data-edit")'),width
        checks+=1
        page.close()
        # A scheduled record disappears after cancellation; its focus must move
        # into the confirmation and then back to a surviving location.
        page=scene('calendar',records=True)
        page.locator('[data-schedule="schedule-focus-01"]').click()
        focus_then_enter(page,'[data-cancel-schedule="schedule-focus-01"]','.calendar-cancel-confirm');checks+=1
        focus_then_enter(page,'[data-keep-schedule="schedule-focus-01"]','[data-cancel-schedule="schedule-focus-01"]');checks+=1
        focus_then_enter(page,'[data-cancel-schedule="schedule-focus-01"]','.calendar-cancel-confirm');checks+=1
        focus_then_enter(page,'[data-confirm-cancel-schedule="schedule-focus-01"]','[data-action=toggle-cancelled-history]');checks+=1
        expect(page.locator('[data-action=toggle-cancelled-history]')).to_be_visible()
        focus_then_enter(page,'[data-action=toggle-cancelled-history]','[data-action=toggle-cancelled-history]');checks+=1
        expect(page.locator('.calendar-cancelled-record')).to_contain_text('Programação de foco')
        page.close()
        print('PASS dynamic keyboard focus after 19 actions:',width)
    browser.close()
    assert checks==len(WIDTHS)*19,checks
print('PASS',checks,'focus transitions (Chromium, five viewport widths)')
