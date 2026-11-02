"""CONFFRATUS 07.10 — calendar weekday names and filter announcements.

Run against the offline Chromium preview. This is a DOM/accessibility-tree
regression, not a claim of testing NVDA/TalkBack/VoiceOver speech output.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = [280, 320, 390, 740, 1024, 1440]
WEEKDAYS = ('Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado')
report=[]

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in WIDTHS:
        page = browser.new_page(viewport={'width':width,'height':850})
        errors=[]
        page.on('pageerror',lambda exc: errors.append(str(exc)))
        page.goto('about:blank')
        page.set_content(HTML)
        page.evaluate('location.hash="#/calendar"')
        page.locator('.calendar-day').first.wait_for()

        grid=page.locator('.calendar-grid')
        assert grid.get_attribute('role')=='group', (width,'calendar days are not named as a group')
        assert grid.get_attribute('aria-label')=='Dias do mês'
        tree=grid.aria_snapshot()
        for day in WEEKDAYS:
            assert day in tree, (width,'weekday missing full accessible name',day,tree[:200])
        assert page.locator('.calendar-weekday [aria-hidden=true]').all_inner_texts()==list('DSTQQSS'),(width,'weekday appearance changed')
        assert page.locator('#app-live-announcer').count()==1

        first=page.locator('.calendar-day').first
        label=first.get_attribute('aria-label')
        first.click()
        status=page.locator('#app-live-announcer').inner_text()
        assert 'Programações em' in status and 'programaç' in status,(width,'filtered result not announced',status)
        assert page.locator('.calendar-day[aria-pressed=true]').count()==1,(width,'date not selected')
        assert page.evaluate("document.activeElement?.hasAttribute('data-calendar-day')"),(width,'date focus lost')
        report.append({'width':width,'step':'filter date','status':status})
        first=page.locator('.calendar-day').first
        first.click()
        status=page.locator('#app-live-announcer').inner_text()
        assert 'Programações' in status and 'programaç' in status,(width,'clear result not announced',status)
        assert page.locator('.calendar-day[aria-pressed=true]').count()==0
        report.append({'width':width,'step':'clear date','status':status})

        next_month=page.locator('[data-action=calendar-next]')
        next_month.click()
        month=page.locator('.calendar-month-nav h2').inner_text()
        status=page.locator('#app-live-announcer').inner_text()
        assert month.casefold() in status.casefold(),(width,'month change not announced',month,status)
        assert page.evaluate("document.activeElement?.getAttribute('data-action')==='calendar-next'"),(width,'month navigation lost focus')
        report.append({'width':width,'step':'next month','status':status})
        page.locator('[data-action=calendar-prev]').click()
        month=page.locator('.calendar-month-nav h2').inner_text()
        assert month.casefold() in page.locator('#app-live-announcer').inner_text().casefold(),(width,'previous month not announced')
        report.append({'width':width,'step':'previous month','status':month})
        page.locator('[data-action=calendar-today]').click()
        assert page.locator('.calendar-day[aria-pressed=true]').count()==1,(width,'Today did not select date')
        assert 'Programações em' in page.locator('#app-live-announcer').inner_text(),(width,'Today result not announced')
        report.append({'width':width,'step':'today','status':page.locator('#app-live-announcer').inner_text()})
        page.locator('[data-action=calendar-all]').click()
        assert 'Programações' in page.locator('#app-live-announcer').inner_text(),(width,'all-programmes result not announced')
        report.append({'width':width,'step':'all','status':page.locator('#app-live-announcer').inner_text()})
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+1'), (width,'horizontal overflow')
        assert not errors,(width,'JavaScript errors',errors)
        if width in (320,390,740):
            page.screenshot(path=str(ROOT/f'dist/stage7_calendar_semantics_v0146_{width}.png'),full_page=True)
        page.close()
    browser.close()

(ROOT/'dist/stage7_calendar_semantics_v0146.json').write_text(json.dumps({'observations':len(report),'widths':WIDTHS,'results':report},ensure_ascii=False,indent=2))
print(f'Calendar ARIA weekday + live updates: {len(report)}/{len(WIDTHS)*6} passed across {len(WIDTHS)} widths')
