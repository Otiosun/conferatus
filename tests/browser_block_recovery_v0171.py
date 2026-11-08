"""Synthetic post-input restoration contract across three engines.

This laboratory does not simulate physical IME behavior, and the current app
does not import the experimental controller.
"""
import json
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE=os.environ.get('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
source=Path('dist/domain/rich-block-dom.js').read_text(encoding='utf-8')
source=re.sub(r'(?m)^export\s+', '', source)
source += '\nwindow.installBlockStructureRecovery=installBlockStructureRecovery;'
source += '\nwindow.matchesExpectedBlockStructure=matchesExpectedBlockStructure;'

HTML="""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body><div id="editor" contenteditable="true" aria-label="Laboratório de blocos">
<p id="first" data-rich-block="paragraph">Antes</p>
<hr data-rich-block="horizontalRule" contenteditable="false">
<p id="second" data-rich-block="paragraph">Depois</p>
</div></body></html>"""

def setup(browser,width,recovery=True):
 page=browser.new_page(viewport={'width':width,'height':760})
 errors=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 page.goto('about:blank?postinput-test=1')
 page.set_content(HTML)
 page.add_script_tag(content=source)
 page.evaluate("""recovery => {
  const host=document.getElementById('editor');
  const expected=['paragraph','horizontalRule','paragraph'];
  window.__reports=[];
  window.__repairs=0;
  const restoreTrustedSnapshot=()=>{
   window.__repairs++;
   const paragraph=(id,word)=>{
    const p=document.createElement('p');
    p.id=id;p.dataset.richBlock='paragraph';p.textContent=word;return p;
   };
   const rule=document.createElement('hr');
   rule.dataset.richBlock='horizontalRule';
   rule.setAttribute('contenteditable','false');
   host.replaceChildren(paragraph('first','Antes'),rule,paragraph('second','Depois'));
  };
  window.__blockMonitor=installBlockStructureRecovery(
    host,expected,recovery?restoreTrustedSnapshot:()=>{},
    success=>window.__reports.push(success)
  );
 }""",recovery)
 return page,errors

def structural_state(page):
 return page.evaluate("""() => {
  const host=document.getElementById('editor');
  const verified=window.__blockMonitor.verify();
  return {
   valid:window.matchesExpectedBlockStructure(host,['paragraph','horizontalRule','paragraph']),
   rules:host.querySelectorAll('hr').length,
   first:document.getElementById('first')?.textContent??null,
   second:document.getElementById('second')?.textContent??null,
   repairs:window.__repairs,
   reports:[...window.__reports],
   verified,
   overflow:document.documentElement.scrollWidth>innerWidth+1
  };
 }""")

def simulate(page,mode):
 return page.evaluate("""mode=>{
  const host=document.getElementById('editor');
  const input=()=>host.dispatchEvent(new InputEvent('input',{
   bubbles:true,inputType:'deleteContentBackward'
  }));
  if(mode==='ordinary'){
    document.getElementById('second').textContent='Depois!';
    input();return null;
  }
  if(mode==='missing-rule'){
    const before=new InputEvent('beforeinput',{
      bubbles:true,cancelable:false,inputType:'deleteContentBackward'
    });
    host.dispatchEvent(before);
    host.querySelector('hr').remove();
    input();
    return {beforeinputCanceled:before.defaultPrevented};
  }
  if(mode==='nested-rule'){
    document.getElementById('second').appendChild(document.createElement('hr'));
    input();return null;
  }
  throw Error('Unknown mode');
 }""",mode)

with sync_playwright() as playwright:
 opts={'headless':True}
 if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
  opts.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 browser=getattr(playwright,ENGINE).launch(**opts)
 observations=[]
 for width in (280,390,1280):
  for mode in ('ordinary','missing-rule','nested-rule','restore-fails'):
   page,errors=setup(browser,width,mode!='restore-fails')
   data=simulate(page,'missing-rule' if mode=='restore-fails' else mode)
   state=structural_state(page)
   if mode=='ordinary':
    assert state['valid'] and state['second']=='Depois!',(ENGINE,width,state)
    assert state['repairs']==0 and state['reports']==[],(ENGINE,width,state)
   elif mode in ('missing-rule','nested-rule'):
    assert state['valid'] and state['rules']==1,(ENGINE,width,mode,state)
    assert state['first']=='Antes' and state['second']=='Depois',(ENGINE,width,state)
    assert state['repairs']==1 and state['reports']==[True],(ENGINE,width,state)
    if mode=='missing-rule':
     assert data['beforeinputCanceled'] is False,(ENGINE,width,data)
   else:
    assert not state['valid'] and not state['verified'],(ENGINE,width,state)
    assert state['reports']==[False,False],(ENGINE,width,state)
   assert not state['overflow'] and not errors,(ENGINE,width,mode,errors)
   observations.append({'width':width,'case':mode,'state':state,'errors':errors})
   page.evaluate('window.__blockMonitor.dispose()')
   page.close()
 browser.close()
Path('dist').mkdir(exist_ok=True)
Path(f'dist/cross_engine_block_recovery_{ENGINE}.json').write_text(json.dumps({
 'engine':ENGINE,'status':'pass','observations':observations,
 'notProofOf':'real IME, undo history, clipboard, production Draft or mobile hardware'
},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Post-input structure recovery {ENGINE}: 12 cases, controlled restore/fail-closed PASS')
