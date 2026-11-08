"""Cross-engine experiment: explicit guards around noneditable <hr> nodes.

The same TypeScript module intended for a future segmented editor is injected
from dist. This does not enable any button in the Conffratus application.
"""
import json
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE=os.getenv('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
source=Path('dist/domain/rich-block-dom.js').read_text(encoding='utf-8')
source=re.sub(r'(?m)^export\s+', '', source)
source+='\nwindow.installRuleDeletionGuard=installRuleDeletionGuard;'

HTML="""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>html,body{margin:0}#editor{padding:15px;overflow-wrap:anywhere}
p{font:16px/1.5 sans-serif}hr{border:0;border-top:1px solid #888}</style>
</head><body><main><div id="editor" contenteditable="true"
role="textbox" aria-multiline="true">
<p id="first" data-rich-block="paragraph">Antes</p>
<hr data-rich-block="horizontalRule" contenteditable="false">
<p id="second" data-rich-block="paragraph">Depois</p></div></main></body></html>"""

def new_case(browser,width):
    page=browser.new_page(viewport={'width':width,'height':760})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('about:blank?rule-guard=1')
    page.set_content(HTML)
    page.add_script_tag(content=source)
    page.evaluate("""() => {
      const host=document.getElementById('editor');
      window.__detachRuleGuard=installRuleDeletionGuard(host);
      window.__keys=[];
      host.addEventListener('keydown',event=>{
       window.__keys.push({key:event.key,prevented:event.defaultPrevented});
      });
    }""")
    return page,errors

def caret(page,paragraph,end):
    page.evaluate("""([id,end]) => {
      const host=document.getElementById('editor');
      host.focus();
      const text=document.getElementById(id).firstChild;
      const range=document.createRange();
      range.setStart(text,end?text.textContent.length:0);
      range.collapse(true);
      const selection=getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }""",[paragraph,end])

def state(page):
    return page.evaluate("""() => ({
      rules:document.querySelectorAll('#editor hr').length,
      first:document.getElementById('first')?.textContent,
      second:document.getElementById('second')?.textContent,
      focus:document.activeElement?.id,
      prevented:window.__keys,
      overflow:document.documentElement.scrollWidth>innerWidth+1
    })""")

with sync_playwright() as playwright:
    options={'headless':True}
    if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
        options.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    browser=getattr(playwright,ENGINE).launch(**options)
    observations=[]
    for width in (280,390,1280):
        # Backspace directly after the rule must not delete it.
        page,errors=new_case(browser,width)
        caret(page,'second',False)
        page.keyboard.press('Backspace')
        backspace=state(page)
        assert backspace['rules']==1 and backspace['first']=='Antes' and backspace['second']=='Depois',(ENGINE,width,backspace)
        assert any(k['key']=='Backspace' and k['prevented'] for k in backspace['prevented']),(ENGINE,width,backspace)
        assert not errors and not backspace['overflow'],(ENGINE,width,errors)
        page.close()

        # Forward Delete immediately before the rule is also guarded.
        page,errors=new_case(browser,width)
        caret(page,'first',True)
        page.keyboard.press('Delete')
        forward=state(page)
        assert forward['rules']==1 and forward['first']=='Antes' and forward['second']=='Depois',(ENGINE,width,forward)
        assert any(k['key']=='Delete' and k['prevented'] for k in forward['prevented']),(ENGINE,width,forward)
        assert not errors and not forward['overflow'],(ENGINE,width,errors)
        page.close()

        # Ordinary Backspace inside the second paragraph must still work.
        page,errors=new_case(browser,width)
        caret(page,'second',True)
        page.keyboard.press('Backspace')
        ordinary=state(page)
        assert ordinary['rules']==1 and ordinary['second']=='Depoi',(ENGINE,width,ordinary)
        assert ordinary['first']=='Antes' and not ordinary['overflow'] and not errors,(ENGINE,width,ordinary)
        page.close()

        # A cancelable beforeinput with no keydown should be blocked too.
        page,errors=new_case(browser,width)
        caret(page,'second',False)
        canceled=page.evaluate("""() => {
          const host=document.getElementById('editor');
          const event=new InputEvent('beforeinput',{bubbles:true,cancelable:true,inputType:'deleteContentBackward'});
          host.dispatchEvent(event);
          return event.defaultPrevented;
        }""")
        assert canceled,(ENGINE,width,'beforeinput was not canceled')
        assert not errors,(ENGINE,width,errors)
        page.evaluate('window.__detachRuleGuard()')
        observations.append({'width':width,'backspace':backspace,
          'forwardDelete':forward,'ordinaryBackspace':ordinary,
          'cancelableBeforeinputBlocked':canceled})
        page.close()
    browser.close()

Path('dist').mkdir(exist_ok=True)
Path(f'dist/cross_engine_block_guard_{ENGINE}.json').write_text(
 json.dumps({'engine':ENGINE,'status':'pass','widths':[280,390,1280],
 'notProofOf':'uncancelable IME/autocorrect, mobile hardware or integrated editor',
 'observations':observations},indent=2,ensure_ascii=False),encoding='utf-8')
print(f'Structural rule deletion guard {ENGINE}: 3 widths, Backspace/Delete/normal editing PASS')
