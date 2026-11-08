"""Cross-engine native grapheme boundary evidence (not mobile keyboard QA)."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE=os.environ.get('CONFFRATUS_TEST_ENGINE','chromium').lower()
assert ENGINE in ('chromium','firefox','webkit')
SAMPLES=[
 ('combining','e\u0301x',[0,2,3]),
 ('emoji-zwj','👩🏽‍💻x',[0,7,8]),
 ('flag','🇧🇷!',[0,4,5]),
 ('stacked-accents','a\u0308\u0301z',[0,3,4])
]
with sync_playwright() as p:
 options={'headless':True}
 if ENGINE=='chromium' and Path('/usr/bin/chromium').exists():
  options.update(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 browser=getattr(p,ENGINE).launch(**options)
 result=[]
 for width in (280,390,1280):
  page=browser.new_page(viewport={'width':width,'height':700})
  errors=[]
  page.on('pageerror',lambda e: errors.append(str(e)))
  page.goto('about:blank?grapheme-lab=1')
  actual=page.evaluate("""samples=>samples.map(([label,text])=>{
    if(typeof Intl.Segmenter!=='function') throw Error('Intl.Segmenter unavailable');
    const parts=[...new Intl.Segmenter('pt-BR',{granularity:'grapheme'}).segment(text)];
    return {label,text,positions:[...parts.map(p=>p.index),text.length],
     parts:parts.map(p=>p.segment)};
   })""",[[label,text] for label,text,_ in SAMPLES])
  for item,(label,text,expected) in zip(actual,SAMPLES):
   assert item['label']==label
   assert item['positions']==expected,(ENGINE,width,label,item['positions'],expected)
  assert not errors,(ENGINE,width,errors)
  result.append({'width':width,'cases':actual,'errors':errors})
  page.close()
 browser.close()
Path('dist').mkdir(exist_ok=True)
Path(f'dist/cross_engine_block_grapheme_{ENGINE}.json').write_text(json.dumps({
 'engine':ENGINE,'status':'pass','observations':result,
 'notProofOf':'hardware IME, document persistence or integrated editor'
},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Grapheme boundary probe {ENGINE}: 4 sequences x 3 widths PASS')
