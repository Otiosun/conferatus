"""Stage 07.10, batch 1: WCAG text-contrast sampling and basic semantics.

Offline Chromium only. This intentionally audits a fixed, reproducible set of
foreground/background pairs; it is NOT a full WCAG or screen-reader audit.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
ROUTES=('ballot','members','profile/m01','overview','governance','calendar','proposals','compose')
WIDTHS=(320,740,1440)
COLORS='''selector => {
  const el=document.querySelector(selector);
  if(!el) return null;
  function rgba(v){const m=v.match(/rgba?\\(([^)]+)\\)/);if(!m)return [0,0,0,0];const a=m[1].split(/[, ]+/).filter(Boolean).map(Number);return [a[0],a[1],a[2],a.length>3?a[3]:1];}
  function blend(top,base){const a=top[3];return [0,1,2].map(i=>a*top[i]+(1-a)*base[i]).concat([1]);}
  let stack=[];for(let n=el;n;n=n.parentElement)stack.push(n);
  let bg=[255,255,255,1];for(let i=stack.length-1;i>=0;i--)bg=blend(rgba(getComputedStyle(stack[i]).backgroundColor),bg);
  const s=getComputedStyle(el),fg=rgba(s.color);
  function linear(v){v/=255;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4);}
  function lum(c){return .2126*linear(c[0])+.7152*linear(c[1])+.0722*linear(c[2]);}
  const a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  return {selector,contrast:Math.round(ratio*100)/100,foreground:s.color,background:bg.slice(0,3).map(Math.round),text:el.innerText.slice(0,35)};
}'''
records=[]
failures=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in WIDTHS:
        page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto('about:blank?demo=1');page.set_content(HTML)
        for route in ROUTES:
            page.evaluate('(route)=>{location.hash="#/"+route}',route)
            page.wait_for_function('(route)=>location.hash==="#/"+route',arg=route)
            page.wait_for_timeout(15)
            names=page.locator('#main-content h1').all_inner_texts()
            heading={'ballot':'Votação demonstrativa','members':'Membros','profile/m01':'Perfil','overview':'Histórico','governance':'GERENCIAMENTO','calendar':'CALENDÁRIO','proposals':'Proposições','compose':'Título'}[route]
            ok=len(names)==1 and heading.casefold() in names[0].casefold()
            records.append({'width':width,'route':route,'case':'page heading','passed':ok,'headings':names})
            if not ok:failures.append(records[-1])
            unlabeled=page.evaluate('''() => [...document.querySelectorAll('button,input,textarea,select')].filter(e=>!e.disabled&&getComputedStyle(e).display!=='none'&&e.getClientRects().length).filter(e=>!(e.getAttribute('aria-label')||(e.labels&&e.labels.length)||(e.innerText||'').trim())).map(e=>e.outerHTML.slice(0,90))''')
            ok=not unlabeled
            records.append({'width':width,'route':route,'case':'named controls','passed':ok,'issues':unlabeled})
            if not ok:failures.append(records[-1])
            selectors=['.footer-demo']
            if route=='ballot':selectors+=['.result-count']
            if route=='overview':selectors+=['.activity-result .no','.stat-chip.secondary']
            if route=='overview':
                page.locator('.footer-nav').click()
                selectors+=['.menu-item']
            for selector in selectors:
                value=page.evaluate(COLORS,selector)
                if value is None:continue
                ok=value['contrast']>=4.5
                data={'width':width,'route':route,'case':'text contrast','passed':ok,**value}
                records.append(data)
                if not ok: failures.append(data)
            if route=='overview':
                menu=page.locator('.menu-item').first
                menu.hover(force=True)
                value=page.evaluate(COLORS,'.menu-item:hover')
                if value:
                    item={'width':width,'route':route,'case':'hover text contrast','passed':value['contrast']>=4.5,**value}
                    records.append(item)
                    if not item['passed']:failures.append(item)
                page.locator('.footer-nav').click()
            if page.evaluate('document.documentElement.scrollWidth>innerWidth+1'):
                failures.append({'width':width,'route':route,'case':'overflow'})
        # Reduced motion preferences are native to CSS; verify the actual duration.
        page.locator('.footer-nav').hover(force=True)
        seconds=page.locator('.footer-nav').evaluate('el=>getComputedStyle(el).transitionDuration')
        reduced=all(float(v.strip().removesuffix('s'))<=.001 for v in seconds.split(','))
        records.append({'width':width,'case':'reduced motion transitions','passed':reduced,'duration':seconds})
        if not reduced:failures.append(records[-1])
        if errors:failures.append({'width':width,'case':'JS errors','errors':errors})
        page.close()
    browser.close()
report={'checks':len(records),'failed':len(failures),'failures':failures,'results':records}
(ROOT/'dist/stage7_contrast_semantics_v0140.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'contrast/semantics: {len(records)-len(failures)}/{len(records)} passed, {len(failures)} failures')
for failure in failures[:35]:print(failure)
assert not failures, 'Contrast or heading/label accessibility regression'
