"""Stage 07.10: focus return after successful forms remove their submitters.

Exercises only the offline fixture preview. Not an institutional Socii invitation,
server-backed scheduling, or a real screen-reader speech test.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (280, 320, 390, 540, 740, 1024, 1440)
results = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width': width, 'height': 850}, device_scale_factor=1)
        js_errors = []
        page.on('pageerror', lambda error: js_errors.append(str(error)))
        page.goto('about:blank')
        page.set_content(HTML)
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action=new-proposal]').click()
        page.locator('#draft-title').fill('Proposição de acesso por teclado')
        page.locator('#draft-body').fill('Conteúdo suficiente para testar o formulário de participantes Socii sem convite real.')
        page.locator('button[value="save"]').click()
        invite = page.locator('[data-action=invite-socii]')
        invite.click()
        form = page.locator('#invite-socii-form')
        member = form.locator('[name=memberId]')
        member.select_option(index=1)
        form.get_by_role('button', name='Adicionar participante').focus()
        page.keyboard.press('Enter')
        assert page.locator('#invite-socii-form').count() == 0, (width, 'Socii form did not close')
        assert page.locator('.workflow-status').inner_text().startswith('Participante incluído'), (width, 'Socii success missing')
        assert invite.evaluate('(el) => document.activeElement === el'), (width, 'keyboard focus lost after Socii submission')
        assert invite.get_attribute('aria-expanded') == 'false', (width, 'Socii disclosure not closed')
        results.append({'width': width, 'case': 'Socii success returns focus to invitation trigger'})

        page.locator('[data-action=new-proposal]').click()
        page.locator('#draft-title').fill('Proposição concluída para agendamento')
        page.locator('#draft-body').fill('Redação válida para concluir uma proposição e programar uma deliberação demonstrativa.')
        page.get_by_role('button', name='Concluir redação').click()
        page.locator('#confirm-proposal-form button[type=submit]').click()
        page.evaluate('location.hash="#/calendar"')
        page.locator('[data-action=open-schedule]').click()
        schedule_form = page.locator('#schedule-deliberation-form')
        schedule_form.locator('[name=title]').fill('Agendamento com foco acessível')
        schedule_form.locator('[name=objective]').fill('Descrição suficiente para criar uma programação de demonstração e revisar o foco.')
        schedule_form.locator('[name=proposalId]').select_option(index=1)
        schedule_form.locator('[name=method]').select_option('ordenada')
        schedule_form.locator('[name=start]').fill('2026-12-12T09:00')
        schedule_form.locator('[name=end]').fill('2026-12-12T12:00')
        schedule_form.get_by_role('button', name='Confirmar programação').focus()
        page.keyboard.press('Enter')
        assert page.locator('#schedule-deliberation-form').count() == 0, (width, 'schedule form did not close')
        assert 'programa' in page.locator('.workflow-status').inner_text().lower(), (width, 'schedule status missing')
        schedule_trigger = page.locator('.calendar-list button[data-schedule]:not([disabled])').first
        assert schedule_trigger.count() == 1, (width, 'new schedule not listed')
        assert schedule_trigger.evaluate('(el) => document.activeElement === el'), (width, 'keyboard focus lost after schedule created')
        results.append({'width': width, 'case': 'scheduling success returns focus to newly created item'})

        cancel = page.locator('.calendar-list button[data-cancel-schedule]:not([disabled])').first
        assert cancel.count() == 1, (width, 'cancel control not revealed')
        cancel.focus()
        page.keyboard.press('Enter')
        assert page.locator('.calendar-list button[data-cancel-schedule]:not([disabled])').count() == 0, (width, 'canceled entry remained active')
        heading = page.locator('.calendar-list-head h2')
        assert heading.evaluate('(el) => document.activeElement === el'), (width, 'keyboard focus lost after canceling schedule')
        assert 'cancelada' in page.locator('#app-live-announcer').inner_text().lower(), (width, 'cancellation status missing')
        results.append({'width': width, 'case': 'cancel schedule returns focus to calendar list heading'})

        # Undo also removes its own action button. The affected member stays
        # visible in the opened governance section, so it is the next target.
        page.evaluate('location.hash="#/governance"')
        page.locator('[data-section]').first.click()
        edit = page.locator('button[data-edit]').first
        member_id = edit.get_attribute('data-edit')
        edit.click()
        edit_form = page.locator('#edit-member-form')
        edit_form.locator('[name=acdmId]').fill('STAGE7-UNDO-0148')
        edit_form.locator('button[type=submit]').click()
        undo = page.locator('[data-action=undo]')
        assert undo.count() == 1, (width, 'undo action unavailable')
        undo.focus()
        page.keyboard.press('Enter')
        assert page.locator('[data-action=undo]').count() == 0, (width, 'undo control not removed')
        restored = page.locator(f'button[data-edit="{member_id}"]').first
        assert restored.evaluate('(el) => document.activeElement === el'), (width, 'keyboard focus lost after undo')
        results.append({'width': width, 'case': 'undo returns focus to the affected member'})
        assert not js_errors, (width, js_errors)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (width, 'horizontal overflow')
        if width in (320, 390):
            page.screenshot(path=str(ROOT / f'dist/stage7_disappearing_forms_v0148_{width}.png'), full_page=True)
        page.close()
    browser.close()

(ROOT / 'dist/stage7_disappearing_forms_v0148_report.json').write_text(
    json.dumps({'checks': len(results), 'widths': WIDTHS, 'results': results,
                'limits': 'Chromium offline focus only; no screen reader/hardware verification'},
               ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Stage 07.10 keyboard focus after disappearing forms: {len(results)}/{len(WIDTHS)*4} PASS')
