"""Small Firefox/WebKit/Chromium preview smoke, synthetic data only.

The in-memory sessionStorage substitutes for the blocked about:blank origin:
this is a navigation/rendering test, not persistence, native mobile, real HTTP
or Academy authentication.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import os

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "dist/CONFFRATUS_demo_offline.html").read_text(encoding="utf-8")
ENGINE = os.environ.get("CONFFRATUS_TEST_ENGINE", "chromium").lower()
assert ENGINE in ("chromium", "firefox", "webkit")
SIZES = ((320, 844), (740, 900), (1280, 800))
results = []
with sync_playwright() as playwright:
    opts = {"headless": True}
    if ENGINE == "chromium" and Path("/usr/bin/chromium").exists():
        opts.update(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    browser = getattr(playwright, ENGINE).launch(**opts)
    for width, height in SIZES:
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page.set_default_timeout(7000)
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.goto("about:blank?demo=1")
        page.evaluate("""() => {
          const state = new Map();
          Object.defineProperty(window, 'sessionStorage', {configurable:true,get:()=>({
            getItem:k=>state.get(String(k))??null,
            setItem:(k,v)=>state.set(String(k),String(v)),
            removeItem:k=>state.delete(String(k)),clear:()=>state.clear()
          })});
        }""")
        page.set_content(HTML, wait_until="domcontentloaded")
        assert page.locator("#main-content").count()==1, (ENGINE,width,"main missing")
        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"), (ENGINE,width,"initial overflow")
        page.locator(".footer-nav").click()
        page.locator('.menu-item[data-route="members"]').click()
        page.locator(".member-item").first.click()
        assert "#/profile/" in page.url and page.locator(".profile-head").is_visible(), (ENGINE,width,"profile")
        page.evaluate('location.hash="#/proposals"')
        page.locator('[data-action="new-proposal"]').click()
        title = f"Cross-engine {ENGINE} {width}"
        page.locator("#draft-title").fill(title)
        page.locator("#draft-body").fill("Proposição fictícia de teste sem envio de votos à Academy.")
        page.locator('#compose-proposal-form [value="save"]').click()
        page.locator('[data-action="invite-socii"]').click()
        page.locator('#invite-socii-form [name="memberId"]').select_option(index=1)
        page.locator("#invite-socii-form button.workflow-primary").click()
        page.locator(".workflow-record").filter(has_text=title).locator("[data-confirm-partner]").click()
        page.locator(".workflow-record").filter(has_text=title).locator("[data-draft]").click()
        page.locator("#confirm-proposal-form").wait_for(state="visible")
        bar = page.locator(".workflow-socii-editor-bar")
        assert bar.is_visible() and "Concluíram 1 de 2" in bar.inner_text(), (ENGINE,width,"review Socii bar")
        assert "confirmou sua participação nesta prévia local" in page.locator(".workflow-review-sheet > p").inner_text(), (ENGINE,width,"review notice")
        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"), (ENGINE,width,"review overflow")
        if width in (320,740):
            page.screenshot(path=str(ROOT / "dist" / f"cross_engine_{ENGINE}_{width}_review.png"),full_page=True)
        page.locator('#confirm-proposal-form button[type="submit"]').click()
        record = page.locator(".workflow-record").filter(has_text=title)
        assert "concluíram 2 de 2" in record.inner_text().casefold(), (ENGINE,width,"author confirmation")
        page.evaluate('location.hash="#/calendar"')
        before = page.locator(".calendar-month-nav h2").inner_text()
        page.locator('[data-action="calendar-next"]').click()
        assert page.locator(".calendar-month-nav h2").inner_text()!=before, (ENGINE,width,"calendar month")
        page.locator('[data-action="open-schedule"]').click()
        assert page.locator("#schedule-deliberation-form").is_visible(), (ENGINE,width,"schedule form")
        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"), (ENGINE,width,"calendar overflow")
        assert not errors, (ENGINE,width,"javascript errors",errors)
        results.append({"engine":ENGINE,"width":width,"height":height,"pass":True})
        page.close()
    browser.close()
(ROOT / "dist" / f"cross_engine_{ENGINE}_report.json").write_text(
    json.dumps({"results":results,"scope":"synthetic Chromium/Firefox/WebKit UI only; memory-only storage"},
               ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Cross-engine preview {ENGINE}: {len(results)}/{len(SIZES)} journeys PASS")
