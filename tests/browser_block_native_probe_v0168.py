"""Measure native caret/Enter/Backspace/undo behavior around an <hr> leaf.

This is NOT an app feature. Native behavior is recorded as evidence, not
mistaken for a production-safe block editor or simulated mobile IME.
"""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE = os.getenv('CONFFRATUS_TEST_ENGINE', 'chromium').lower()
assert ENGINE in ('chromium', 'firefox', 'webkit')

HTML = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>html,body{margin:0}#editor{padding:20px;overflow-wrap:anywhere}
p{font:16px/1.5 sans-serif}hr{border:0;border-top:1px solid #888}</style>
</head><body><main><div id="editor" role="textbox" aria-multiline="true"
contenteditable="true"><p id="first">Antes</p><hr contenteditable="false">
<p id="second">Depois</p></div></main><script>
(() => {
window.__events = [];
const editor=document.getElementById('editor');
for(const type of ['beforeinput','input','compositionstart','compositionend']){
 editor.addEventListener(type,event=>{
  window.__events.push({
   type, inputType:event.inputType||'',
   cancelable:event.cancelable,
   targetRanges:typeof event.getTargetRanges==='function'
    ?event.getTargetRanges().length:null
  });
 });
}
})();
</script></body></html>"""

def fresh(page):
    page.set_content(HTML)
    page.evaluate("""() => {
      document.getElementById('editor').focus();
    }""")

def cursor(page, element, at_end):
    page.evaluate("""({element,atEnd}) => {
      const p=document.getElementById(element);
      if(!p||!p.firstChild)throw Error('Missing text node');
      const node=p.firstChild;
      const range=document.createRange();
      range.setStart(node,atEnd?node.textContent.length:0);
      range.collapse(true);
      const selection=getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      document.getElementById('editor').focus();
    }""",{'element':element,'atEnd':at_end})

def snapshot(page):
    return page.evaluate("""() => ({
      originalWords:['Antes','Depois'].every(t=>document.getElementById('editor').textContent.includes(t)),
      hrCount:document.querySelectorAll('#editor hr').length,
      paragraphCount:document.querySelectorAll('#editor p').length,
      text:document.getElementById('editor').textContent,
      beforeinput:window.__events.filter(x=>x.type==='beforeinput'),
      inputs:window.__events.filter(x=>x.type==='input'),
      viewport:innerWidth,
      overflow:document.documentElement.scrollWidth>innerWidth+1
    })""")

with sync_playwright() as playwright:
    options={'headless':True}
    if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
        options.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    browser=getattr(playwright,ENGINE).launch(**options)
    cases=[]
    for width in (280,390,1280):
        page=browser.new_page(viewport={'width':width,'height':800})
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto('about:blank?block-probe=1')

        fresh(page)
        cursor(page,'first',True)
        page.keyboard.press('Enter')
        enter=snapshot(page)

        fresh(page)
        cursor(page,'second',False)
        page.keyboard.press('Backspace')
        backspace=snapshot(page)

        fresh(page)
        cursor(page,'first',True)
        page.keyboard.insert_text('X')
        typed=snapshot(page)
        page.keyboard.press('ControlOrMeta+z')
        undo=snapshot(page)

        assert enter['originalWords'] and backspace['originalWords'],(ENGINE,width,enter,backspace)
        assert typed['originalWords'] and undo['originalWords'],(ENGINE,width,typed,undo)
        assert not enter['overflow'] and not backspace['overflow'],(ENGINE,width)
        assert not errors,(ENGINE,width,errors)
        cases.append({
          'width':width,'enter':enter,'backspace':backspace,
          'typed':typed,'undo':undo,'jsErrors':errors
        })
        page.close()
    browser.close()

Path('dist').mkdir(exist_ok=True)
Path(f'dist/cross_engine_block_native_probe_{ENGINE}.json').write_text(
    json.dumps({
      'engine':ENGINE,
      'description':'diagnostic native contenteditable around a noneditable horizontal rule',
      'notProofOf':'IME/clipboard/mobile hardware or safe production editing',
      'observations':cases
    },indent=2,ensure_ascii=False),encoding='utf-8'
)
print(f'Block-native probe {ENGINE}: {len(cases)} widths recorded; no JS errors or overflow')
