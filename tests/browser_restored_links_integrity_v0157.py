"""Restored local proposal/Socii/schedule references must be real, not ghost approvals.

The fixture is synthetic; sessionStorage is local and is not an Academy account.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
valid = {
    'id': 'valid-draft', 'title': 'Proposição de integridade',
    'body': 'Texto suficientemente longo para comprovar uma proposição fictícia íntegra.',
    'sectionId': 'integridade', 'type': 'PDR', 'authorComplete': True,
    'partners': [{'id': 'm02', 'complete': True}], 'status': 'concluida',
}
partial = {**valid, 'id': 'partial-draft', 'title': '', 'body': 'Um rascunho ainda incompleto',
           'sectionId': 'antiga-secao', 'authorComplete': False, 'partners': [], 'status': 'redacao'}
restored_drafts = [
    valid,
    partial,
    {**valid, 'id': 'ghost-socii', 'partners': [{'id': 'm99999', 'complete': True}]},
    {**valid, 'id': 'ghost-section', 'sectionId': 'secao-fantasma'},
    {**valid, 'id': 'ghost-review', 'sectionId': 'secao-fantasma', 'authorComplete': False,
     'partners': [], 'status': 'revisao'},
]
base_schedule = {
    'id': 'valid-schedule', 'title': 'Agenda de teste',
    'objective': 'Agenda fictícia preservada após validação de vínculos.',
    'proposalId': 'valid-draft', 'sectionId': 'integridade',
    'start': '2026-12-14T10:00', 'end': '2026-12-14T11:00',
    'type': 'PDR', 'status': 'programada',
}
restored_schedules = [
    base_schedule,
    {**base_schedule, 'id': 'ghost-schedule-section', 'sectionId': 'secao-fantasma'},
    {**base_schedule, 'id': 'unapproved-schedule', 'proposalId': 'partial-draft'},
    # A historical cancelled entry can keep missing references without becoming active.
    {**base_schedule, 'id': 'old-cancelled', 'sectionId': 'secao-fantasma', 'status': 'cancelada'},
    # Existing behavior preserves a missing proposal link with an explicit unavailable label.
    {**base_schedule, 'id': 'unavailable-link', 'proposalId': 'missing-original'},
]


def navigate(page, route):
    page.locator('.footer-nav').click()
    page.locator(f'.menu-item[data-route="{route}"]').click()
    # Hash navigation renders asynchronously; assert the destination is ready.
    destination = '.calendar-list' if route == 'calendar' else '.workflow-proposals-layout'
    page.locator(destination).wait_for(state='attached')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (280, 390, 740, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 860})
        page.set_default_timeout(7000)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('about:blank?demo=1')
        page.evaluate('''data => {
          const store = new Map([
            ['conferatus:proposals-v010', JSON.stringify(data.drafts)],
            ['conferatus:deliberations-v010', JSON.stringify(data.schedule)]
          ]);
          Object.defineProperty(window, 'sessionStorage', { configurable: true, value: {
            getItem: k => store.get(k) ?? null,
            setItem: (k,v) => store.set(k, String(v)),
            removeItem: k => store.delete(k)
          }});
        }''', {'drafts': restored_drafts, 'schedule': restored_schedules})
        page.set_content(HTML)
        navigate(page, 'proposals')
        visible_drafts = set(page.locator('.workflow-record [data-draft]').evaluate_all(
            '(nodes) => nodes.map(x => x.dataset.draft)'))
        assert visible_drafts == {'valid-draft','partial-draft'}, (width, 'unknown member/section was accepted', visible_drafts)
        navigate(page, 'calendar')
        current_schedules = set(page.locator('.calendar-item [data-schedule]').evaluate_all(
            '(nodes) => nodes.map(x => x.dataset.schedule)'))
        assert {'valid-schedule','unavailable-link'} <= current_schedules, (width, 'valid/legacy active entries lost', current_schedules)
        assert not {'ghost-schedule-section','unapproved-schedule','old-cancelled'} & current_schedules, (width, 'invalid active entry shown', current_schedules)
        assert page.locator('[data-action=toggle-cancelled-history]').count() == 1, (width, 'historical cancellation lost')
        page.locator('[data-action=toggle-cancelled-history]').click()
        assert page.locator('.calendar-cancelled-record').filter(has_text='Agenda de teste').count() == 1, width
        # Store the accepted snapshot; rejected original bytes must first be kept in a recovery backup.
        page.locator('[data-action=open-schedule]').click()
        form = page.locator('#schedule-deliberation-form')
        options = form.locator('[name=proposalId] option').evaluate_all('(nodes)=>nodes.map(x=>x.value)')
        assert options == ['', 'valid-draft'], (width, 'unapproved draft became schedulable', options)
        form.locator('[name=title]').fill('Nova programação local')
        form.locator('[name=objective]').fill('Uma descrição suficientemente longa para conferir a recuperação.')
        form.locator('[name=proposalId]').select_option('valid-draft')
        form.locator('[name=method]').select_option('cumulativa')
        form.locator('[name=start]').fill('2026-12-21T09:00')
        form.locator('[name=end]').fill('2026-12-21T10:00')
        form.locator('button[type=submit]').click()
        rejected = page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:invalid-session-backup-v0114"))')
        assert {x['id'] for x in rejected['drafts']} == {'ghost-socii','ghost-section','ghost-review'}, (width, 'draft quarantine', rejected)
        assert {x['id'] for x in rejected['schedule']} == {'ghost-schedule-section','unapproved-schedule'}, (width, 'schedule quarantine', rejected)
        saved = page.evaluate('''() => ({
          drafts: JSON.parse(sessionStorage.getItem('conferatus:proposals-v010')),
          schedules: JSON.parse(sessionStorage.getItem('conferatus:deliberations-v010'))
        })''')
        assert {x['id'] for x in saved['drafts']} == {'valid-draft','partial-draft'}, (width, 'saved draft set')
        assert {'valid-schedule','unavailable-link','old-cancelled'} <= {x['id'] for x in saved['schedules']}, (width,'saved schedule set')
        assert not errors, (width, errors)
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'), (width, 'overflow')
        if width == 390:
            page.screenshot(path=str(ROOT/'dist/restored_links_integrity_v0157_390.png'), full_page=True)
        page.close()
    browser.close()
print('Restore referential integrity: 4/4 widths PASS, ghost signatures/active events quarantined, historical links retained')
