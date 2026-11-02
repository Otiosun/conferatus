"""Stage 07.10: inspect rendered foreground/background pairs in dynamic preview states.

A bounded Chromium DOM audit of solid-color backgrounds; *not* an accessibility
certification. Gradients, images, and assistive-technology announcements need
separate human verification. Intended to catch future low-contrast text regressions.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
WIDTHS = (320, 390, 740, 1440)
JS = r'''() => {
  function rgb(s) {
    const m = s.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const values = m[1].split(',').map(Number);
    return values.length === 3 ? [...values,1] : values;
  }
  function over(front, back) {
    const opacity = front[3] ?? 1;
    return [0,1,2].map(i => front[i]*opacity + back[i]*(1-opacity)).concat([1]);
  }
  function backdrop(element) {
    let color = [255,255,255,1];
    const chain = [];
    for(let el=element;el && el.nodeType===1;el=el.parentElement) chain.push(el);
    for(const el of chain.reverse()) {
      const computed = getComputedStyle(el), c = rgb(computed.backgroundColor);
      if(c) color=over(c,color);
    }
    return color;
  }
  const luminance = (rgb) => rgb.slice(0,3).map(x => {
    x /= 255;
    return x<=0.04045 ? x/12.92 : ((x+0.055)/1.055)**2.4;
  }).reduce((s,x,i)=>s+x*[0.2126,0.7152,0.0722][i],0);
  function ratio(fg,bg) {
    const a=luminance(fg),b=luminance(bg);
    return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
  }
  const results=[];
  for(const el of document.querySelectorAll('body *')) {
    const style=getComputedStyle(el),box=el.getBoundingClientRect();
    if(style.display==='none'||style.visibility==='hidden'||box.width===0||box.height===0 ||el.closest('svg') ||el.closest('[aria-hidden="true"]')) continue;
    const text=[...el.childNodes].filter(n=>n.nodeType===3 && n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
    if(!text) continue;
    // Rasterized text on gradients/images is not covered by this CSS color model.
    let gradient=false;
    for(let p=el;p;p=p.parentElement) {
      const s=getComputedStyle(p);
      if(s.backgroundImage!=='none') {gradient=true;break;}
    }
    if(gradient) continue;
    const fg=rgb(style.color),bg=backdrop(el);
    if(!fg) continue;
    const font=parseFloat(style.fontSize),bold=parseInt(style.fontWeight,10)>=700;
    const large=font>=24||(font>=18.66&&bold);
    const actual=ratio(over(fg,bg),bg);
    const threshold=large?3:4.5;
    results.push({text:text.slice(0,70),selector:el.tagName.toLowerCase()+'.'+(typeof el.className==='string'?el.className.replace(/\s+/g,'.'):''),font,ratio:+actual.toFixed(3),threshold,pass:actual+0.005>=threshold});
  }
  return results;
}'''

report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  page=browser.new_page(viewport={'width':width,'height':860})
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('about:blank?demo=1')
  page.set_content(HTML)
  scenarios=[('ballot',None),('ballot-menu','.footer-nav'),('ballot-options','[data-action=toggle-demo]'),
   ('members',None),('members-search','[data-action=search]'),('profile/m01',None),
   ('overview',None),('overview-proposals','[data-overview-tab=proposicoes]'),
   ('governance',None),('governance-tools','[data-action=toggle-tools]'),
   ('calendar',None),('calendar-schedule','[data-action=open-schedule]'),
   ('proposals',None),('proposals-invite','[data-action=invite-socii]')]
  for case,open_selector in scenarios:
   route=case.split('-')[0]
   page.evaluate(f'location.hash="#/{route}"')
   page.wait_for_timeout(22)
   if open_selector:
    e=page.locator(open_selector).first
    if e.count():e.click()
   measures=page.evaluate(JS)
   report.append({'width':width,'case':case,'checks':measures})
   if width==390 and case in ('overview','proposals'):
    page.screenshot(path=str(ROOT/f'dist/stage7_contrast_{case}_v0143.png'),full_page=True)
  assert not errors,(width,'JS exceptions',errors)
  page.close()
 browser.close()
failures=[{**{k:row[k] for k in ('width','case')},**check} for row in report for check in row['checks'] if not check['pass']]
all_checks=sum(len(row['checks']) for row in report)
out={'cases':len(report),'measurements':all_checks,'failures':failures,'passed':all_checks-len(failures), 'note':'Solid CSS background contrast only; excludes gradient and image backgrounds'}
(ROOT/'dist/stage7_dynamic_text_contrast_v0143.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(f"Dynamic text contrast: {out['passed']}/{out['measurements']} across {out['cases']} scenarios; failures={len(failures)}")
for f in failures[:12]: print(f)
assert not failures,'Insufficient rendered text contrast'
