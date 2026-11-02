"""Stage 07.04: metric labels must not collide with neighboring columns.

The layout uses five metrics at normal widths and two columns on small phones.
This is a Chromium regression test, not an assistive-technology audit.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
issues=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in (280,320,360,390,540,740,768,1024,1440):
        page=browser.new_page(viewport={'width':width,'height':820})
        page.goto('about:blank?stage7=metrics')
        page.set_content(HTML)
        page.evaluate('()=>location.hash="#/members"')
        page.wait_for_timeout(40)
        result=page.evaluate('''() => {
          const check=row=>{
            let cells=[...row.querySelectorAll('.metric-cell')];
            let overlaps=[];
            for(let i=0;i<cells.length-1;i++) {
              let a=cells[i].getBoundingClientRect(), b=cells[i+1].getBoundingClientRect();
              if(Math.max(a.top,b.top)<Math.min(a.bottom,b.bottom)-1 && a.right>b.left+1)
                overlaps.push([i, +(a.right-b.left).toFixed(2)]);
            }
            let outside=[];
            for(let c of cells){let cr=c.getBoundingClientRect(),rr=row.getBoundingClientRect();
              if(cr.right>rr.right+1||cr.left<rr.left-1)outside.push([cr.left,cr.right,rr.left,rr.right]);}
            return {overlaps,outside};
          };
          return {profiles:[...document.querySelectorAll('.profile-summary>.metrics')].map(check),
            members:[...document.querySelectorAll('.member-item .metrics')].slice(0,8).map(check),
            horizontal:document.documentElement.scrollWidth>innerWidth+1};
        }''')
        if result['horizontal']:
            issues.append([width,'page_overflow'])
        for kind,rows in (('profiles',result['profiles']),('members',result['members'])):
            for index,row in enumerate(rows):
                if row['overlaps'] or row['outside']:
                    issues.append([width,kind,index,row])
        if width in (280,390,740):
            page.screenshot(path=str(ROOT/'dist'/f'stage7_microtype_members_{width}.png'),full_page=True)
        page.close()
    browser.close()
print('Stage 07.04 metric columns: nine widths, overlap/escape issues:',len(issues))
for issue in issues[:5]: print('ISSUE',json.dumps(issue,ensure_ascii=False))
assert not issues
