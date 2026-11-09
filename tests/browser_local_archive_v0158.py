"""Explicit backup/restore of fictional local workflows only. No Academy integration."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'dist/CONFFRATUS_demo_offline.html').read_text(encoding='utf-8')
KEY_D='conferatus:proposals-v010'
KEY_S='conferatus:deliberations-v010'
INITIAL={'id':'draft-existing','title':'Proposta atual de demonstração',
         'body':'Texto atual da proposta fictícia que não deve ser perdido durante uma restauração falha.',
         'sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
NEW={'id':'draft-imported','title':'Proposta importada de demonstração',
     'body':'Texto do arquivo exportado que deve sobreviver à restauração e ao recarregamento.',
     'sectionId':'integridade','type':'PDR','authorComplete':True,'partners':[],'status':'concluida'}
CANCEL={'id':'sched-imported','title':'Evento cancelado preservado',
        'objective':'Histórico fictício importado sem reativação indevida.',
        'proposalId':'draft-imported','sectionId':'integridade',
        'start':'2026-12-21T09:00','end':'2026-12-21T11:00','type':'PDR','status':'cancelada'}
ACTIVE={**CANCEL,'id':'sched-active','title':'Evento ativo importado','status':'programada'}

def archive(drafts,schedule,version=1):
 return json.dumps({'format':'conffratus-local-workflows','version':version,
                    'exportedAt':'2026-11-03T01:02:03.000Z', 'drafts':drafts,'schedule':schedule})

def menu(page):
 page.locator('.footer-nav').click()
 page.locator('.menu-item[data-route="proposals"]').click()
 page.locator('[data-action="export-local-archive"]').wait_for(state='visible')

def upload(page,text,expected_message=None,decision=None):
 # file.text() is asynchronous: the previous status may still be visible
 # after set_input_files returns. Wait for this input to be replaced by render().
 previous_input=page.locator('#archive-file-input').element_handle()
 def select_file():
  page.locator('#archive-file-input').set_input_files({
   'name':'copia.json','mimeType':'application/json','buffer':text.encode('utf-8')})
 if decision is None:
  select_file()
 else:
  with page.expect_event('dialog') as confirmation:
   page.once('dialog',lambda dialog:dialog.accept() if decision=='accept' else dialog.dismiss())
   select_file()
  assert 'Restaurar' in confirmation.value.message
 if decision=='dismiss':
  assert previous_input.evaluate('(input)=>input.isConnected'), 'Cancel must leave form intact'
  return
 page.wait_for_function('(input)=>!input.isConnected',arg=previous_input)
 if expected_message:
  expect(page.locator('.local-archive-message')).to_contain_text(expected_message)

def message(page):
 page.locator('.local-archive-message').wait_for(state='visible')
 return page.locator('.local-archive-message').inner_text()

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in (280,320,390,740,1280):
  page=browser.new_page(viewport={'width':width,'height':880},accept_downloads=True)
  page.set_default_timeout(7000)
  errors=[]
  page.on('pageerror',lambda error: errors.append(str(error)))
  page.goto('about:blank?demo=1')
  page.evaluate('''([draftKey,schedKey,draft])=>{
    const state=new Map([[draftKey,JSON.stringify([draft])],[schedKey,'[]']]);
    let fail=0;
    Object.defineProperty(window,'sessionStorage',{configurable:true,value:{
     getItem:k=>state.get(k)??null,
     setItem:(k,v)=>{if(k===schedKey&&fail-->0)throw Error('Synthetic quota');state.set(k,v)},
     removeItem:k=>state.delete(k)
    }});
    window.__blockSave=()=>{fail=1};
   }''',[KEY_D,KEY_S,{**INITIAL,'token':'secret-never-export'}])
  page.set_content(HTML)
  menu(page)
  assert page.locator('.local-archive').count()==1, width
  assert page.locator('[data-action="export-local-archive"]').bounding_box()['height']>=44,width
  with page.expect_download() as transfer:
   page.locator('[data-action="export-local-archive"]').click()
  exported=json.loads(Path(transfer.value.path()).read_text(encoding='utf-8'))
  assert set(exported)=={'format','version','exportedAt','drafts','schedule'},width
  assert exported['drafts']==[INITIAL],width
  assert 'secret-never-export' not in json.dumps(exported),width
  assert exported['schedule']==[],width
  assert 'Academy' not in json.dumps(exported),width
  assert 'Guarde' in message(page),width

  # Invalid JSON, unknown archive version and duplicate IDs are never imported.
  for content,expected in (
   ('{not json}','não contém JSON válido'),
   (archive([NEW],[],version=88),'versão de exportação compatível'),
   (archive([NEW,NEW],[]),'IDs repetidos'),
   (archive([NEW],[{**ACTIVE,'proposalId':'not-there','sectionId':'unknown-section'}]),'IDs repetidos'),
  ):
   upload(page,content,expected_message=expected)
   assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')[0]['id']=='draft-existing',width

  # User can refuse the replacement without changing anything.
  upload(page,archive([NEW],[CANCEL,ACTIVE]),decision='dismiss')
  assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')[0]['id']=='draft-existing',width

  # A failed second key write must roll back both in memory and in storage.
  page.evaluate('window.__blockSave()')
  upload(page,archive([NEW],[CANCEL,ACTIVE]),expected_message='registros anteriores',decision='accept')
  assert 'registros anteriores' in message(page).lower(),(width,message(page))
  assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')[0]['id']=='draft-existing',width
  assert page.locator('.workflow-record').filter(has_text='Proposta atual de demonstração').count()==1,width

  # Create a fictitious sample before restoring; a new archive must invalidate it.
  page.locator('.footer-home').click()
  page.locator('#preview-vote-method').select_option('nominal')
  page.locator('#preview-vote-form [name=selected][value=a]').check()
  page.locator('.preview-vote-submit').click()
  assert 'amostras nesta aba (1)' in page.locator('.preview-vote-summary').inner_text(),width
  menu(page)
  upload(page,archive([{**NEW,'authToken':'should-never-import'}],[{**CANCEL,'secret':'should-never-import'},ACTIVE]),expected_message='restaurada',decision='accept')
  assert 'should-never-import' not in page.evaluate('sessionStorage.getItem("conferatus:proposals-v010")'),width
  assert 'should-never-import' not in page.evaluate('sessionStorage.getItem("conferatus:deliberations-v010")'),width
  assert 'restaurada' in message(page).lower(),(width,message(page))
  assert page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:proposals-v010"))')[0]['id']=='draft-imported',width
  assert sorted(x['status'] for x in page.evaluate('JSON.parse(sessionStorage.getItem("conferatus:deliberations-v010"))'))==['cancelada','programada'],width
  page.locator('.footer-home').click()
  assert page.locator('.preview-vote-summary').count()==0,(width,'restored archive retained stale vote samples')
  if width==390:
   page.screenshot(path=str(ROOT/'dist/local_workflow_archive_controls_390.png'),full_page=True)
  page.set_content(HTML)
  menu(page)
  assert page.locator('.workflow-record').filter(has_text='Proposta importada de demonstração').count()==1,width
  page.locator('.footer-nav').click()
  page.locator('.menu-item[data-route="calendar"]').click()
  page.locator('[data-action="toggle-cancelled-history"]').wait_for(state='visible')
  page.locator('[data-action="toggle-cancelled-history"]').click()
  assert page.locator('.calendar-cancelled-record').filter(has_text='Evento cancelado preservado').count()==1,width
  assert page.locator('.calendar-item').filter(has_text='Evento ativo importado').count()==1,width
  assert page.locator('.calendar-item').filter(has_text='Evento cancelado preservado').count()==0,width
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),width
  assert not errors,(width,errors)
  if width==390:
   page.screenshot(path=str(ROOT/'dist/local_workflow_archive_390.png'),full_page=True)
  page.close()

 # The real visual reference is not changed when demo tools are disabled.
 normal=browser.new_page()
 normal.goto('about:blank')
 normal.set_content(HTML)
 normal.locator('.footer-nav').click();normal.locator('[data-route="proposals"]').click()
 normal.locator('.workflow-proposals-layout').wait_for()
 assert normal.locator('.local-archive').count()==0
 browser.close()
print('Workflow export/restore: PASS 5 widths, explicit confirmation, invalid/duplicate rejection, rollback, active/cancelled isolation, no normal UI change')
