import { activities, ballots } from './data/fixtures.js';
import { FixtureMemberProvider } from './domain/providers.js';
import { UnconnectedAcademyIdentityProvider } from './domain/academy-identity.js';
import { resolveMemberReference } from './domain/member-reference.js';
import { exportWorkflowArchive, parseWorkflowArchive, WORKFLOW_ARCHIVE_MAX_BYTES } from './domain/workflow-archive.js';
import { escapeHTML, resultPercentage, totalVotes, updateSectionAssignment, demoteToCommonMember, canRecordVote, restoreDemoMembers, searchKey, isDeliberativeMember, hasPersonalVoteHistory, DELIBERATION_METHODS, isDeliberationMethod, isPositiveCumulativeVoteWeight, PREVIEW_BINARY_OPTIONS, PREVIEW_LIST_OPTIONS, validatePreviewVote, summarizePreviewVotes } from './domain/rules.js';
import type { PreviewVote } from './domain/rules.js';
import { createPreviewSampleLedger } from './domain/preview-ledger.js';
import { isValidPreviewChoices, isSavedDraft, cleanDraftRecord, cleanScheduleRecord, isRestorableSchedule, uniqueSavedRecords, nextLocalRecordId } from './domain/workflow-records.js';
import type { ProposalType, Draft, PreviewChoice, Deliberation } from './domain/workflow-records.js';
import { renderRichText, DEFAULT_RICH_LAYOUT, isRichLayout, richLayoutStyle, normalizeHttpHref } from './domain/rich-text.js';
import type { RichTextRun, RichBodyLayout } from './domain/rich-text.js';
import { runsFromEditable } from './domain/rich-editor.js';
import type { Activity, Member, DeliberationMethod } from './domain/types.js';

type Route = 'ballot' | 'members' | 'profile' | 'overview' | 'governance' | 'calendar' | 'proposals' | 'compose' | 'review';
type Tab = 'votos' | 'proposicoes';
const root = document.querySelector<HTMLDivElement>('#root');
if (!root) throw new Error('Root missing');
// A polite announcement must survive our screen rerenders. The visible workflow
// notices are kept in place; this separate, persistent region owns speech output.
const workflowAnnouncer = document.createElement('div');
workflowAnnouncer.id = 'app-live-announcer';
workflowAnnouncer.className = 'sr-only';
workflowAnnouncer.setAttribute('role', 'status');
workflowAnnouncer.setAttribute('aria-atomic', 'true');
root.insertAdjacentElement('afterend', workflowAnnouncer);
let announcedWorkflowNotice = '';
const academyIdentity = await new UnconnectedAcademyIdentityProvider().currentIdentity();
const memberProvider = new FixtureMemberProvider();
const [members, sections] = await Promise.all([memberProvider.listMembers(), memberProvider.listSections()]);
let currentMember = members[0]?.id ?? 'm01';
let profileTab: Tab = 'votos';
let overviewTab: Tab = 'votos';
let overviewExpanded = false;
let menuOpen = false;
let suppressFooterHomeClickUntil = 0;
let footerSwipeStart: {x:number;y:number} | null = null;
let expandedSection = '';
let editingMemberId: string | null = null;
let notice = '';
let editError = '';
let editErrorField: 'acdmId' | 'cumulativeVoteWeight' = 'acdmId';
let filter = '';
let searchExpanded = false;
let directoryExpanded = false;
let expandedActivity = '';
let rolePreview: 'diretor' | 'membro' = 'diretor';
let demoToolsOpen = false;
const advancedPreview = new URLSearchParams(location.search).get('demo') === '1';
const profileSheetExperiment=advancedPreview&&new URLSearchParams(location.search).get('d2')==='sheet';
// D3 is a reversible visual candidate, never the default Academy review contract.
const d3SingleExperiment=advancedPreview&&new URLSearchParams(location.search).get('d3')==='single';
let lastChange: {memberId: string; acdmId: string | undefined; sectionIds: string[]; role: Member['role']; hadDeliberativeHistory?: boolean; cumulativeVoteWeight?: number} | null = null;
const initialMembers = new Map(members.map(m=>[m.id,{name:m.name,acdmId:m.acdmId,sectionIds:[...m.sectionIds],role:m.role,hadDeliberativeHistory:m.hadDeliberativeHistory,cumulativeVoteWeight:m.cumulativeVoteWeight}]));
const demoMembersKey = 'conferatus:demo-members-v07';
function saveDemoMembers() {
  try {
    sessionStorage.setItem(demoMembersKey, JSON.stringify(members.map(m=>({id:m.id, acdmId:m.acdmId, sectionIds:m.sectionIds,role:m.role,hadDeliberativeHistory:m.hadDeliberativeHistory,cumulativeVoteWeight:m.cumulativeVoteWeight}))));
  } catch { /* Preview still works with session storage disabled. */ }
}
function rememberChange(m: Member) {
  lastChange={memberId:m.id,acdmId:m.acdmId,sectionIds:[...m.sectionIds],role:m.role,hadDeliberativeHistory:m.hadDeliberativeHistory,cumulativeVoteWeight:m.cumulativeVoteWeight};
}
try {
  restoreDemoMembers(members, sections.map(s => s.id), JSON.parse(sessionStorage.getItem(demoMembersKey) ?? 'null'));
} catch { /* Ignore damaged or blocked session data. */ }
let demoVoteId: string | null = null;
let demoExpanded = false;
let votingFormsOpen = false;
let previewHomeBallot = false;
let previewClosedScheduleNotice = '';
let pendingCalendarReturnId: string | null = null;
// Six modes share one local validation path; only the technical selector belongs to ?demo=1.
let previewMode: DeliberationMethod = 'binaria';
let previewVoteError = '';
let previewVoteReceipt: PreviewVote | null = null;
let previewVoteMemberId = '';
// Keep an unfinished local vote draft when the disclosure is collapsed or the
// user visits another page. Never store it outside this browser tab.
type PreviewVoteDraft = {
 scope: string;
 memberId: string;
 fields: {name: string; value: string; checked?: boolean}[];
};
let previewVoteDraft: PreviewVoteDraft | null = null;
// Deliberately memory-only; never part of the session archive or legacy ballot totals.
const previewSampleLedger=createPreviewSampleLedger(100);
let previewRequestSequence=0;
let previewRequestId:string|null=null;
function previewSampleScope():string {
 const scheduled=previewSelectedSchedule();
 return scheduled?`schedule:${scheduled.id}`:previewHomeBallot?`fixture:home-${ballots[0]?.id??'none'}`:`fixture:${previewMode}`;
}
let previewScheduleId: string | null = null;
let scheduleMethod: DeliberationMethod | null = null;
try {
  const saved = sessionStorage.getItem('conferatus:demo-vote');
  if (ballots[0] && canRecordVote(ballots[0]) && ballots[0].options.some(option => option.id === saved)) demoVoteId = saved;
} catch { /* Preview continues if storage is unavailable. */ }
demoExpanded = demoVoteId!==null;
const demoBallot = ballots[0];

function routeFromHash(): Route {
  const name = location.hash.replace(/^#\/?/, '').split('/')[0];
  switch(name) {
    case 'members': case 'profile': case 'overview': case 'governance': case 'calendar': case 'proposals': case 'compose': case 'review': return name;
    default: return 'ballot';
  }
}
// A rerender or route switch must not silently discard an unfinished proposal.
// Compare against the last saved local record, not against the mutable form cache.
let approvedComposeDeparture=false;
function hasPendingComposeChanges():boolean{
 const form=document.querySelector<HTMLFormElement>('#compose-proposal-form');
 if(!form)return false;
 const title=form.querySelector<HTMLInputElement>('#draft-title')?.value.trim()??'';
 const plainBody=form.querySelector<HTMLTextAreaElement>('#draft-body')?.value??'';
 const body=(richEditorOpen?draftForm.body:plainBody).trim();
 const original=drafts.find(d=>d.id===currentDraftId);
 if(!original)return Boolean(title||body);
 const formatted=richEditorOpen&&hasFormatting(draftForm.bodyRuns)?draftForm.bodyRuns:undefined;
 const layout=richEditorOpen&&isRichLayout(draftForm.bodyLayout)?draftForm.bodyLayout:undefined;
 return original.title!==title||original.body!==body||
  JSON.stringify(original.bodyRuns??[])!==JSON.stringify(formatted??[])||
  JSON.stringify(original.bodyLayout??null)!==JSON.stringify(layout??null);
}
function confirmComposeDeparture():boolean{
 return !hasPendingComposeChanges()||window.confirm('Esta redação tem alterações não salvas. Deseja sair e descartá-las?');
}
// Do not treat unchanged required defaults as a schedule the user has begun.
// Changes to any field, including a modality/section select, count as unfinished work.
function hasPendingScheduleChanges():boolean{
 const form=document.querySelector<HTMLFormElement>('#schedule-deliberation-form');
 if(!form)return false;
 // Hidden options are still unsaved author input until this form closes.
 if(scheduleChoicesDraft.trim()&&!form.elements.namedItem('choices'))return true;
 for(const [name,value] of new FormData(form)){
  if(typeof value!=='string')continue;
  const initial=name==='sectionId'?'integridade':name==='type'?'PDR':name==='proposalId'?(schedulePrefillProposalId??''):'';
  if(value.trim()!==initial)return true;
 }
 return false;
}
function hasPendingD3ReviewChanges():boolean{
 if(!d3SingleExperiment)return false;
 const form=document.querySelector<HTMLFormElement>('#d3-review-dialog #confirm-proposal-form');
 if(!form)return false;
 const draft=drafts.find(d=>d.id===form.dataset.reviewDraft);
 if(!draft)return false;
 return form.querySelector<HTMLSelectElement>('[name="sectionId"]')?.value!==draft.sectionId||
        form.querySelector<HTMLSelectElement>('[name="type"]')?.value!==draft.type;
}
function confirmD3ReviewDeparture():boolean{
 return !hasPendingD3ReviewChanges()||
  window.confirm('A confirmação tem escolhas não salvas. Voltar à redação e descartá-las?');
}
let approvedD3ReviewDeparture=false;
function dismissD3Review(){
 if(!d3SingleExperiment||!document.querySelector<HTMLDialogElement>('#d3-review-dialog')?.open)return;
 if(!confirmD3ReviewDeparture())return;
 approvedD3ReviewDeparture=true;
 navigate('compose');
}
function confirmScheduleDeparture():boolean{
 return !hasPendingScheduleChanges()||
  window.confirm('O agendamento tem informações não salvas. Deseja sair e descartá-las?');
}
let approvedScheduleDeparture=false;
// The route guard protects in-app navigation. A separate, conditional
// beforeunload listener also warns when reloading/closing a dirty composer.
// Browsers (especially mobile) may skip this event: it is not an autosave.
let composerUnloadListenerAttached=false;
function warnBeforeComposerUnload(event: BeforeUnloadEvent) {
 if(!hasPendingComposeChanges()&&!hasPendingScheduleChanges()&&!hasPendingD3ReviewChanges())return;
 event.preventDefault();
 event.returnValue=' ';
}
function refreshComposerUnloadGuard(){
 const pending=hasPendingComposeChanges()||hasPendingScheduleChanges()||hasPendingD3ReviewChanges();
 if(pending&&!composerUnloadListenerAttached){
  window.addEventListener('beforeunload',warnBeforeComposerUnload);
  composerUnloadListenerAttached=true;
 }else if(!pending&&composerUnloadListenerAttached){
  window.removeEventListener('beforeunload',warnBeforeComposerUnload);
  composerUnloadListenerAttached=false;
 }
}
function navigate(route: Route, memberId?: string) {
 if(profileScheduleSheetOpen&&(route!=='profile'||(memberId!==undefined&&memberId!==currentMember))){
  if(!confirmScheduleDeparture())return;
  profileScheduleSheetOpen=false;schedulePrefillProposalId=null;scheduleMethod=null;
 }
 if(routeFromHash()==='compose'&&route!=='compose'){
  if(!confirmComposeDeparture()){
   if(menuOpen){menuOpen=false;render();}
   return;
  }
  approvedComposeDeparture=true;
 }
 if(routeFromHash()==='calendar'&&route!=='calendar'&&hasPendingScheduleChanges()){
  if(!confirmScheduleDeparture()){
   if(menuOpen){menuOpen=false;render();}
   return;
  }
  approvedScheduleDeparture=true;
 }
  if(route!=='calendar'){scheduleFormOpen=false;scheduleMethod=null;pendingScheduleCancellation=null;schedulePrefillProposalId=null;}
  menuOpen = false;
  demoToolsOpen = false;
  notice = '';
  editError = '';
  lastChange = null;
  const hash = `#/${route}${route==='profile' && memberId?`/${encodeURIComponent(memberId)}`:''}`;
  if (location.hash === hash) {
    approvedComposeDeparture=false;
    render();
    document.querySelector<HTMLElement>('#main-content')?.focus({preventScroll:true});
  } else location.hash = hash;
  window.scrollTo({ top: 0, behavior: 'instant' });
}
function crest(inDrawer=false) { return `<img${inDrawer?' class="drawer-crest"':''} src="./assets/crest.png" width="29" height="29" alt="Símbolo da Academy">`; }
function footer() {
  return `<footer class="app-footer">${menuOpen ? `<nav id="bottom-navigation" class="bottom-menu" aria-label="Navegação principal">${crest(true)}<div class="menu-list">
    <button class="menu-item" data-route="members" ${routeFromHash()==='members'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="7" r="3"/><path d="M3.5 19v-2.2a5.5 5.5 0 0 1 11 0V19M17 8h4M17 12h4M17 16h4"/></svg></span>Membros e Serviços da Cúpula Cíntia</button>
    <button class="menu-item" data-route="overview" ${routeFromHash()==='overview'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h2M12 9h5M7 13h2M12 13h5M7 17h2M12 17h5"/></svg></span>Histórico de Votações e Proposições</button>
    <button class="menu-item" data-route="calendar" ${routeFromHash()==='calendar'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true">▦</span>Agendar e Iniciar Deliberação</button>
    <button class="menu-item" data-route="proposals" ${['proposals','compose','review'].includes(routeFromHash())?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true">✎</span>Elaborar Proposição e Socii</button>
  </div></nav>` : ''}${menuOpen?'':crest()}<button type="button" class="footer-home" data-route="ballot" aria-label="Voltar à votação">CONFFRATUS</button><small class="footer-demo">DADOS FICTÍCIOS · PRÉVIA</small>
   <button type="button" class="footer-nav" aria-expanded="${menuOpen}" ${menuOpen?'aria-controls="bottom-navigation"':''} aria-label="${menuOpen?'Fechar':'Abrir'} menu" data-action="menu">${menuOpen?'Fechar ×':'☰ Menu'}</button>
  </footer>`;
}
function header(title?: string, subtitle?: string, tall=false) {
  if (title) return `<header class="page-header">
   ${advancedPreview?`<button type="button" class="panel-button" data-action="toggle-tools" aria-label="Opções de teste" aria-expanded="${demoToolsOpen}" ${demoToolsOpen?'aria-controls="demo-tools-panel"':''}><img src="./assets/painel.png" alt=""></button>`:`<img class="panel-mark" src="./assets/painel.png" alt="">`}
   <h1>${escapeHTML(title)}</h1>${subtitle?`<p>${escapeHTML(subtitle)}</p>`:''}
   ${advancedPreview && demoToolsOpen?`<aside id="demo-tools-panel" class="demo-tools" aria-label="Ferramentas de demonstração">
     <strong>Opções de visualização</strong><p>Identidade Academy: ${academyIdentity.state==='unavailable'?'não conectada':'identificada, sem autorização nesta prévia'}. Os perfis abaixo são simulações, não permissões reais.</p>
     <label for="role-mode">Visualizar como</label><select id="role-mode" aria-label="Simular perfil"><option value="diretor" ${rolePreview==='diretor'?'selected':''}>Diretor</option><option value="membro" ${rolePreview==='membro'?'selected':''}>Membro comum</option></select>
     ${expandedSection&&rolePreview==='diretor'?`<div class="tools-divider"><label for="add-member">Vincular à seção aberta</label><div class="tools-add"><select id="add-member"><option value="">Selecione um membro…</option>${members.filter(m=>!m.sectionIds.includes(expandedSection)).map(m=>`<option value="${m.id}">${escapeHTML(m.name)}</option>`).join('')}</select><button type="button" class="small-action" data-action="add-member">Vincular</button></div><label for="link-cumulative-weight">Proporção cumulativa (opcional)</label><input id="link-cumulative-weight" type="number" min="1" step="1" inputmode="numeric" placeholder="Quantidade de votos"></div>`:''}
     <button type="button" class="reset-tools" data-action="reset-admin">Reiniciar alterações administrativas</button>
   </aside>`:''}
  </header>`;
  const panelShortcut = routeFromHash()==='overview' ? `<button class="panel-button" data-route="governance" aria-label="Abrir gerenciamento deliberativo" title="Gerenciamento deliberativo"><img src="./assets/painel.png" alt=""></button>` : '';
  return `<header class="hero ${tall?'':'hero--flat'}" aria-label="Faixa azul do CONFFRATUS">${panelShortcut}</header>`;
}
function metricRow(m: Member) {
  const personalVotes = hasPersonalVoteHistory(m, sections) ? String(m.totalVotes) : '—';
  return `<div class="metrics" role="group" aria-label="Indicadores de participação">
  <div class="metric-cell">${personalVotes}<small>Votos</small></div>
  <div class="metric-cell">${m.proposals}<small>PDR</small></div>
  <div class="metric-cell">${String(m.approved).padStart(2,'0')}<small>PR</small></div>
  <div class="metric-cell">${m.officialLetters ?? 0}<small>Ofício</small></div><div class="metric-cell">${m.collaborations}<small>Socii</small></div></div>`;
}
function tabBar(tab: Tab, personalVotingHistory = true, hasSociiContext = false) {
  const showSelected=routeFromHash()!=='members';
  return `<div class="tabs" role="group" aria-label="Histórico do membro">
   ${personalVotingHistory ? `<button class="tab" type="button" aria-pressed="${showSelected && tab==='votos'}" data-tab="votos">Histórico de votações</button>` : ''}
   <button class="tab" type="button" aria-pressed="${showSelected && tab==='proposicoes'}" data-tab="proposicoes">${hasSociiContext?'Proposições e Socii':'Proposições'}</button>
  </div>`;
}
function memberHeader(m:Member, tab:Tab, displayTabs=true) {
 const identity=routeFromHash()==='members'
  ? `<button type="button" class="profile-name-button" data-member="${m.id}" aria-label="Abrir perfil de ${escapeHTML(m.name)}">${escapeHTML(m.name)}</button>`
  : `<strong>${escapeHTML(m.name)}</strong>`;
 return `<div class="profile-head"><div class="profile-summary"><div class="avatar avatar--large" aria-hidden="true"></div>
   ${metricRow(m)}</div><div class="profile-identity"><div>${identity} <small>${m.role==='diretor'?'Diretoria':isDeliberativeMember(m, sections)?'Membro deliberativo':'Membro da Academy'}</small></div>
   <p>${escapeHTML(m.subtitle)}</p>${routeFromHash()==='profile' && m.acdmId?`<p class="profile-reference"><a class="profile-reference-link" href="#/profile/acdm/${encodeURIComponent(m.acdmId)}" aria-label="Abrir link de referência demonstrativa ACDM ID ${escapeHTML(m.acdmId)}">ACDM ID: ${escapeHTML(m.acdmId)}</a><span> · prévia local</span></p>`:''}</div>${displayTabs?tabBar(tab, hasPersonalVoteHistory(m, sections), routeFromHash()==='profile'&&m.id===members[0]?.id):''}</div>`;
}

function previewSelectedSchedule():Deliberation|undefined {
 return schedule.find(item=>item.id===previewScheduleId&&item.status==='programada'&&item.method===previewMode&&
  (previewMode==='binaria'||isValidPreviewChoices(item.choices)));
}
function previewVoteChoices(): readonly {id:string;label:string}[] {
 return previewHomeBallot&&previewMode==='nominal'?(ballots[0]?.options.map(o=>({id:o.id,label:o.label}))??[]):previewMode==='binaria'?PREVIEW_BINARY_OPTIONS:(previewSelectedSchedule()?.choices??PREVIEW_LIST_OPTIONS);
}
function previewVoteFieldset():string {
 const options=previewVoteChoices();
 if(previewMode==='binaria'||previewMode==='nominal') {
  return '<fieldset class="preview-vote-fieldset"><legend>Escolha uma alternativa</legend>'+
   options.map(option=>'<label class="preview-vote-choice"><input type="radio" name="selected" value="'+option.id+'"> '+escapeHTML(option.label)+'</label>').join('')+'</fieldset>';
 }
 if(previewMode==='ordenada') {
  return '<fieldset class="preview-vote-fieldset"><legend>Organize as alternativas por preferência</legend>'+
   options.map((_,position)=>'<label>'+String(position+1)+'º lugar'+
    '<select name="rank-'+String(position)+'" required><option value="">Selecione</option>'+
    options.map(option=>'<option value="'+option.id+'">'+escapeHTML(option.label)+'</option>').join('')+
    '</select></label>').join('')+'</fieldset>';
 }
 if(previewMode==='aprovacao') {
  return '<fieldset class="preview-vote-fieldset"><legend>Marque as alternativas aceitáveis</legend>'+
   options.map(option=>'<label class="preview-vote-choice"><input type="checkbox" name="approved" value="'+option.id+'"> '+escapeHTML(option.label)+'</label>').join('')+'</fieldset>';
 }
 if(previewMode==='escalar') {
  return '<fieldset class="preview-vote-fieldset"><legend>De 1 a 10 para cada alternativa</legend>'+
   options.map(option=>'<label>'+escapeHTML(option.label)+
    '<select name="score-'+option.id+'" required><option value="">Selecione uma nota</option>'+
    Array.from({length:10},(_,index)=>'<option value="'+String(index+1)+'">'+String(index+1)+'</option>').join('')+
    '</select></label>').join('')+'</fieldset>';
 }
 if(!advancedPreview){
  return '<fieldset class="preview-vote-fieldset"><legend>Distribua até 5 unidades fictícias</legend>'+
   '<p>Esta cota é apenas um exemplo, não representa regra ou participante da Academy.</p>'+
   options.map(option=>'<label>'+escapeHTML(option.label)+
    '<input type="number" min="0" max="5" step="1" inputmode="numeric" name="alloc-'+option.id+'" value="0" required></label>').join('')+
   '</fieldset>';
 }
 const qualified=members.filter(member=>isDeliberativeMember(member,sections)&&
  isPositiveCumulativeVoteWeight(member.cumulativeVoteWeight));
 const selected=qualified.find(member=>member.id===previewVoteMemberId);
 const weight=selected?.cumulativeVoteWeight;
 const intro='<label for="preview-vote-member">Membro fictício com cota configurada</label>'+
  '<select id="preview-vote-member" name="voteMemberId"><option value="">Selecione um membro</option>'+
  qualified.map(member=>'<option value="'+member.id+'"'+(member.id===previewVoteMemberId?' selected':'')+'>'+
   escapeHTML(member.name)+' — '+String(member.cumulativeVoteWeight)+' votos</option>').join('')+'</select>';
 if(!qualified.length) {
  return '<div class="preview-vote-fieldset">'+intro+
   '<p role="status">Nenhum membro deliberativo fictício tem proporção cumulativa definida. Configure-a em Gerenciamento Deliberativo.</p>'+
   '<button type="button" class="preview-vote-secondary" data-route="governance">Configurar cotas dos membros</button></div>';
 }
 if(!weight) return '<div class="preview-vote-fieldset">'+intro+
  '<p>Escolha um membro para distribuir sua cota de votos fictícia.</p></div>';
 return '<div class="preview-vote-fieldset">'+intro+
  '<fieldset><legend>Distribua até '+String(weight)+' votos entre as alternativas</legend>'+
  options.map(option=>'<label>'+escapeHTML(option.label)+
   '<input type="number" min="0" max="'+String(weight)+'" step="1" inputmode="numeric" name="alloc-'+option.id+'" value="0" required></label>').join('')+
  '</fieldset><p>Uso parcial da cota permitido somente nesta simulação. A regra institucional permanece indefinida.</p></div>';
}
function previewVoteReceiptText(vote:PreviewVote):string {
 const label=(id:string)=>escapeHTML(previewVoteChoices().find(option=>option.id===id)?.label??id);
 if(vote.method==='binaria'||vote.method==='nominal')return 'Escolha: '+label(vote.selected);
 if(vote.method==='ordenada')return vote.ranking.map((id,index)=>String(index+1)+'º '+label(id)).join(' · ');
 if(vote.method==='aprovacao')return 'Aceitas: '+vote.approved.map(label).join(', ');
 if(vote.method==='escalar')return previewVoteChoices().map(option=>label(option.id)+': '+String(vote.scores[option.id])+'/10').join(' · ');
 if(vote.method!=='cumulativa')return '';
 const used=Object.values(vote.allocation).reduce((sum,count)=>sum+count,0);
 return previewVoteChoices().map(option=>label(option.id)+': '+String(vote.allocation[option.id])).join(' · ')+
  ' (distribuídos '+String(used)+' de '+String(vote.weight)+')';
}

function previewVoteSummary():string {
 const scope=previewSampleScope();
 const summary=summarizePreviewVotes(previewMode,previewVoteChoices(),
   previewSampleLedger.votes(scope));
 if(!summary.samples)return '';
 return '<section class="preview-vote-summary" aria-labelledby="preview-vote-summary-title">'+
  '<h3 id="preview-vote-summary-title">Distribuição das amostras nesta aba ('+String(summary.samples)+')</h3>'+
  '<p>Resumo descritivo, não apuração institucional. Nenhuma alternativa é declarada vencedora.</p>'+
  '<p class="preview-vote-unit">'+escapeHTML(summary.unit)+'</p>'+
  '<div class="preview-vote-summary-rows">'+summary.rows.map(row=>
   '<div class="preview-vote-summary-row"><span>'+escapeHTML(row.label)+'</span><strong>'+escapeHTML(row.total)+'</strong>'+
   (row.detail?'<small>'+escapeHTML(row.detail)+'</small>':'')+'</div>').join('')+'</div>'+
  '<button type="button" class="preview-vote-secondary" data-action="clear-preview-samples">Limpar amostras desta simulação</button>'+
  '</section>';
}

function previewVoteLab():string {
 const method=DELIBERATION_METHODS.find(entry=>entry.id===previewMode);
 const contextual=previewSelectedSchedule();
 const homeBallot=previewHomeBallot?ballots[0]:undefined;
 const receipt=previewVoteReceipt?.method===previewMode?previewVoteReceipt:null;
 return '<section id="preview-vote-lab" class="preview-vote-lab" aria-labelledby="preview-vote-title">'+
  (advancedPreview?'<h2 id="preview-vote-title">Laboratório das seis modalidades</h2>':'<h2 id="preview-vote-title">'+escapeHTML(contextual?.title??homeBallot?.title??'Votação')+'</h2>')+ 
  (contextual?'<p class="preview-vote-context"><strong>Deliberação programada:</strong> '+escapeHTML(contextual.title)+
   '<span>Seção: '+escapeHTML(sections.find(s=>s.id===contextual.sectionId)?.name??contextual.sectionId)+'</span>'+(contextual.proposalId?'<span>Proposição: '+escapeHTML(drafts.find(d=>d.id===contextual.proposalId)?.title??'Indisponível')+'</span>':'')+'</p>':homeBallot?'<p class="preview-vote-context">'+escapeHTML(homeBallot.description)+'<span>Seção: '+escapeHTML(homeBallot.section)+'</span></p>':'')+
  (advancedPreview?'<p class="preview-vote-disclaimer">Apenas em ?demo=1. Alternativas fictícias, sem voto oficial, apuração institucional, login ou envio de informações.</p>':'<p class="preview-vote-disclaimer">Prévia com dados fictícios. Sua escolha permanece nesta aba e não é enviada à Academy.</p>')+
  (advancedPreview?'<label for="preview-vote-method">Modalidade de deliberação</label><select id="preview-vote-method"'+(contextual?' disabled':'')+'>'+DELIBERATION_METHODS.map(mode=>'<option value="'+mode.id+'"'+(mode.id===previewMode?' selected':'')+'>'+escapeHTML(mode.label)+'</option>').join('')+'</select>':'<p class="preview-vote-detail">Modalidade: '+escapeHTML(method?.label??'')+'</p>')+
  (advancedPreview?'<p class="preview-vote-detail">'+escapeHTML(method?.detail??'')+'</p>':'')+ 
  ((contextual||homeBallot)?'<button type="button" class="preview-vote-secondary" data-action="exit-preview-schedule">'+(advancedPreview?'Voltar às alternativas de teste':contextual?'Voltar ao calendário':'Voltar às votações')+'</button>':'')+
  (receipt?'<div class="preview-vote-receipt" role="status"><strong>'+(advancedPreview?'Voto simulado conferido nesta aba':'Escolha confirmada nesta prévia')+'</strong>'+
   '<p>'+previewVoteReceiptText(receipt)+'</p>'+
   '<button type="button" class="preview-vote-secondary" data-action="reset-preview-vote">'+(advancedPreview?'Registrar outra amostra':'Alterar escolha')+'</button></div>':
   '<form id="preview-vote-form" data-mode="'+previewMode+'" data-preview-member="'+previewVoteMemberId+'" novalidate>'+previewVoteFieldset()+
   (previewVoteError?'<p class="preview-vote-error" role="alert" id="preview-vote-error" tabindex="-1">'+escapeHTML(previewVoteError)+'</p>':'')+
   '<button type="submit" class="preview-vote-submit"'+
    (previewMode==='cumulativa' && advancedPreview && !members.some(m=>isDeliberativeMember(m,sections)&&
     isPositiveCumulativeVoteWeight(m.cumulativeVoteWeight))?' disabled':'')+
   '>'+(advancedPreview?'Conferir voto fictício':'Confirmar escolha')+'</button></form>')+
  (advancedPreview?previewVoteSummary():'')+
  '</section>';
}

function ballotPage() {
 // An unavailable program retains its title instead of falling through to the home ballot.
 if(!advancedPreview&&previewScheduleId&&!previewSelectedSchedule()){
  const unavailable=schedule.find(item=>item.id===previewScheduleId);
  const cancelled=unavailable?.status==='cancelada';
  votingFormsOpen=false;
  previewVoteReceipt=null;
  previewVoteDraft=null;
  previewRequestId=null;
  previewVoteError='';
  previewVoteMemberId='';
  return `<div class="main-pad">${header(undefined,undefined,false)}</div>
   <section id="preview-vote-lab" class="preview-vote-lab" aria-labelledby="preview-vote-title">
    <h2 id="preview-vote-title">${escapeHTML(unavailable?.title??'Programação indisponível')}</h2>
    <p class="preview-vote-context" role="status"><strong>${cancelled?'Programação cancelada':'Programação indisponível'}</strong><span>${cancelled?'Esta programação foi cancelada. Consulte seu registro no calendário.':'As opções desta programação não estão disponíveis nesta sessão.'}</span></p>
    <p class="preview-vote-disclaimer">Prévia com dados fictícios. Nenhuma escolha é enviada à Academy.</p>
    <button type="button" class="preview-vote-secondary" data-action="exit-preview-schedule">Voltar ao calendário</button>
   </section>`;
 }
 // A scheduled demo must not display unrelated sample results first.
 if(!advancedPreview && votingFormsOpen && (previewSelectedSchedule()||previewHomeBallot)){
  return `<div class="main-pad">${header(undefined,undefined,false)}</div>${previewVoteLab()}`;
 }
 const ballot=ballots[0]; if(!ballot) return '<p>Nenhuma votação disponível.</p>';
 const demoOptions = ballot.options.map(o => ({...o, votes:o.votes + (advancedPreview&&canRecordVote(ballot)&&demoVoteId===o.id?1:0)}));
 const sum=totalVotes(demoOptions);
 return `<div class="main-pad">${header(undefined,undefined,true)}<div class="results">
 ${demoOptions.map(o=>`<div class="result-row ${advancedPreview&&demoVoteId===o.id?'result-row--chosen':''}" aria-label="${escapeHTML(o.label)}: ${o.votes} votos, ${advancedPreview&&demoVoteId?(100*o.votes/sum).toFixed(1):resultPercentage(o.votes,sum)} por cento"><span class="result-label">${escapeHTML(o.label)}${advancedPreview&&demoVoteId===o.id?'<small class="your-vote">Sua escolha</small>':''}</span><span class="result-count">${o.votes} Votos</span><span class="result-percentage">${advancedPreview&&demoVoteId?(100*o.votes/sum).toFixed(1):resultPercentage(o.votes,sum)}%</span></div>`).join('')}
 </div><hr class="hairline"></div><section class="description-panel"><div class="description-heading"><span>Descrição da votação</span><button class="demo-toggle" type="button" data-action="${advancedPreview?'toggle-demo':'enter-ballot'}" aria-expanded="${advancedPreview?demoExpanded:false}" ${advancedPreview&&demoExpanded?'aria-controls="demo-vote-panel"':''} ${!advancedPreview&&!canRecordVote(ballot)?'disabled aria-disabled="true"':''}>${advancedPreview&&demoExpanded?'Fechar':canRecordVote(ballot)?'Participar':advancedPreview?'Ver situação':'Encerrada'}</button></div>
 <p class="ballot-description">${escapeHTML(ballot.description)}</p>${!advancedPreview&&previewClosedScheduleNotice?`<p class="vote-feedback" role="status">${escapeHTML(previewClosedScheduleNotice)}</p>`:''}${advancedPreview&&demoExpanded?`<div id="demo-vote-panel" class="demo-ballot"><h2>${escapeHTML(ballot.title)}</h2><p>${canRecordVote(ballot)?'Selecione uma opção para testar a votação.':'Esta votação está encerrada. Os resultados permanecem disponíveis para consulta.'}</p>
 ${canRecordVote(ballot)?`<div class="vote-actions">${ballot.options.map(o=>`<button type="button" data-vote="${o.id}" class="vote-button" aria-pressed="${demoVoteId===o.id}">${escapeHTML(o.label)}</button>`).join('')}</div>
 <p class="vote-feedback" role="status">${demoVoteId?'Opção selecionada. Você pode alterá-la.':'Selecione uma opção.'}</p>
 ${demoVoteId?'<button class="reset-vote" type="button" data-action="reset-vote">Alterar escolha</button>':''}`:''}</div>`:''}${false?`<div class="voting-preview-entry"><button type="button" data-action="toggle-voting-forms" aria-expanded="${votingFormsOpen}" aria-controls="preview-vote-lab">${votingFormsOpen?'Fechar formulário':'Abrir formulário de votação'}</button><p>Seis modalidades disponíveis para demonstração com dados fictícios.</p></div>`:''}</section>${advancedPreview||votingFormsOpen?previewVoteLab():'<div id="preview-vote-lab" hidden></div>'}`;
}
function matchingMembers() {
 const candidates = searchExpanded && filter.trim() ? members : members.slice(1);
 return candidates.filter(m => searchKey(`${m.name} ${m.acdmId ?? ''}`).includes(searchKey(filter)));
}
function memberResults(visible: Member[]) {
 return visible.length
  ? visible.map(m=>`<button type="button" class="member-item" data-member="${m.id}"><div class="avatar" aria-hidden="true"></div><span class="member-name">${escapeHTML(m.name)}</span>${metricRow(m)}</button>`).join('')
  : '<p class="status-line">Nenhum membro encontrado.</p>';
}
// Update only the directory while typing: preserves caret, mobile keyboard and IME composition.
function updateMemberSearch() {
 const results=document.querySelector<HTMLElement>('#member-results');
 const status=document.querySelector<HTMLElement>('#member-count');
 const clear=document.querySelector<HTMLButtonElement>('[data-action="clear-search"]');
 const visible=matchingMembers();
 if(results) results.innerHTML=memberResults(visible);
 const more=document.querySelector<HTMLButtonElement>('[data-action=show-more-members]');
 if(more) more.hidden=filter.trim().length>0;
 if(status) status.textContent=`${visible.length} ${visible.length===1?'membro encontrado':'membros encontrados'}`;
 if(clear) clear.hidden=filter==='';
}
function memberList() {
 const lead = members[0]; if(!lead) return '';
 const candidates=matchingMembers();
 const visible=(directoryExpanded || (searchExpanded && filter.trim()))?candidates:candidates.slice(0,7);
 return `${header(undefined,undefined,false)}${memberHeader(lead,'votos')}
 <div class="member-list" role="region" aria-label="Diretório de membros">
 <button type="button" class="search-trigger" data-action="search" aria-expanded="${searchExpanded}" ${searchExpanded?'aria-controls="directory-search-tools"':''} aria-label="${searchExpanded?'Fechar busca de membros':'Buscar membros'}">${searchExpanded?'Fechar busca ×':'Buscar ⌕'}</button>
 ${searchExpanded?`<div id="directory-search-tools" class="toolbar"><label for="search-members">Buscar membro</label><input id="search-members" type="search" placeholder="Nome ou identificador" value="${escapeHTML(filter)}" autocomplete="off" aria-controls="member-results"><button type="button" class="clear-search" data-action="clear-search" ${filter?'':'hidden'}>Limpar</button></div>`:''}
 ${searchExpanded?`<p id="member-count" class="sr-only" role="status" aria-live="polite">${visible.length} ${visible.length===1?"membro encontrado":"membros encontrados"}</p>`:""}
 <div id="member-results">${memberResults(visible)}</div>
 ${!directoryExpanded && candidates.length>7?`<button class="member-more" type="button" data-action="show-more-members" ${searchExpanded&&filter.trim()?'hidden':''}>Mostrar mais ${candidates.length-7} membros</button>`:''}
 </div>`;
}
function activityItem(a:Activity) {
 const isVote=a.type==='voto';
 const expanded=expandedActivity===a.id;
 if (!isVote) return `<article class="activity activity-proposal ${expanded?'activity-proposal--expanded':''}">
   <button type="button" class="proposal-trigger" data-activity="${a.id}" aria-expanded="${expanded}" aria-controls="proposal-${a.id}" aria-label="${expanded?'Recolher':'Ver detalhes de'} ${escapeHTML(a.title)}">
     <span class="activity-head"><span class="activity-title">${escapeHTML(a.title)}</span><span class="activity-code">${escapeHTML(a.code)}</span></span>
     <span class="proposal-preview">${escapeHTML(a.summary)}</span>
   </button>
   ${expanded?`<div class="proposal-expansion" id="proposal-${a.id}">
      <div class="proposal-meta-row"><span class="proposal-tag">PDR</span><span class="proposal-outcome"><span class="proposal-flag" aria-hidden="true">⚑</span><span>${a.approved?'Proposição aprovada':'Proposição arquivada'}</span><span class="proposal-score">${a.votes} votos <strong>${a.percentage}%</strong></span></span></div>
      <p>${escapeHTML(a.section)}</p>
   </div>`:`<div id="proposal-${a.id}" hidden></div>`}
  </article>`;
 return `<article class="activity activity-vote"><div class="activity-head"><h2 class="activity-title">${escapeHTML(a.title)}</h2><span class="activity-code">${escapeHTML(a.code)}</span></div>
   <p class="activity-text">${escapeHTML(a.section)}</p><p class="activity-text">${escapeHTML(a.summary)}</p>
   <div class="activity-result"><span class="${a.approved?'':'no'}">⚑ OPÇÃO VOTADA</span><span>${a.votes} votos&nbsp;&nbsp; <strong>${a.percentage}%</strong></span></div></article>`;
}
function profilePage() {
 const referencePath=location.hash.replace(/^#\/profile\/?/, '').split('/');
 // A reference link resolves a PUBLIC DEMONSTRATION PROFILE only. It never
 // authenticates the holder or grants voting/administrative permissions.
 let member: Member | undefined;
 if (referencePath[0] === 'acdm') {
  let reference = '';
  try { reference = decodeURIComponent(referencePath[1] ?? ''); } catch { /* Invalid URL: no member. */ }
  const result = resolveMemberReference(members, reference);
  member = result.state === 'found' ? result.member : undefined;
 } else {
  member = members.find(m=>m.id===(referencePath[0] || currentMember));
 }
 if(!member) return `${header(undefined,undefined,false)}<section class="missing-profile" role="status"><strong>Perfil não encontrado</strong><p>Não encontramos um membro com esse identificador.</p><button type="button" data-route="members">Voltar aos membros</button></section>`;
 const personalVotingHistory = hasPersonalVoteHistory(member, sections);
 const activeTab: Tab = personalVotingHistory ? profileTab : 'proposicoes';
 const relevant=activities.filter(a=>a.memberId===member.id && a.type===(activeTab==='votos'?'voto':'proposicao'));
 const local=member.id===members[0]?.id && activeTab==='proposicoes'
  ? drafts.map(d=>`<article class="activity activity-proposal session-proposal"><button type="button" data-draft="${escapeHTML(d.id)}" class="session-proposal-link"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${draftStatusLabel(d)} · ${escapeHTML(d.type)}</small><span>${escapeHTML(d.body.slice(0,170))}</span></button>${linkedScheduleButtons(d)}${contextualScheduleButton(d)}</article>`).join('') : '';
 return `${header(undefined,undefined,false)}${memberHeader(member,activeTab)}<section class="section-body">
 ${local?`<h2 class="session-proposals-heading">Proposições desta sessão</h2>${local}${relevant.length?'<h2 class="session-proposals-heading">Histórico de exemplo</h2>':''}`:''}
 ${relevant.length?relevant.map(activityItem).join(''):local?'':'<p class="status-line">Nenhum registro encontrado.</p>'}</section>${member.id===members[0]?.id&&activeTab==='proposicoes'?`<div class="workflow-actions profile-workflow-actions" role="group" aria-label="Ações da proposição"><button type="button" class="workflow-outline" data-action="invite-socii-from-profile">Adicionar ao Socii</button><button type="button" class="workflow-primary" data-action="new-proposal">Redigir proposição</button></div>`:''}${profileSheetExperiment&&member.id===members[0]?.id&&workflowNotice?`<p class="profile-schedule-result" role="status">${escapeHTML(workflowNotice)}</p>`:''}${profileSheetExperiment&&profileScheduleSheetOpen&&member.id===members[0]?.id&&activeTab==='proposicoes'?`<dialog id="profile-schedule-dialog" closedby="none" aria-labelledby="profile-schedule-sheet-label"><div class="profile-schedule-sheet-head">${crest()}<h2 id="profile-schedule-sheet-label" tabindex="-1">Programar deliberação</h2><button type="button" class="profile-schedule-sheet-close" data-dismiss-schedule-sheet aria-label="Fechar agendamento">Fechar</button></div>${scheduleFormMarkup(true)}</dialog>`:''}`;
}
function overviewPage() {
 const votes=activities.filter(a=>a.type==='voto');
 const proposals=activities.filter(a=>a.type==='proposicao');
 const accepted=proposals.filter(a=>a.approved).length;
 const relevant=overviewTab==='votos'?votes:proposals;
 const visible=overviewExpanded?relevant:relevant.slice(0,6);
 const remaining=relevant.length-visible.length;
 // New drafts belong to this browser session. They never change fixture totals.
 const localHistory=overviewTab==='proposicoes'&&drafts.length
  ? `<section class="overview-local-history" aria-label="Proposições desta sessão"><h2 class="session-proposals-heading">Proposições desta sessão</h2>${drafts.map(d=>`<article class="workflow-record overview-local-proposal"><button type="button" data-draft="${escapeHTML(d.id)}" class="workflow-record-btn"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${draftStatusLabel(d)} · ${escapeHTML(d.type)}</small><p>${escapeHTML(d.body.slice(0,140))}</p></button>${linkedScheduleButtons(d)}</article>`).join('')}</section>` : '';
 return `${header(undefined,undefined,false)}<div class="overview-stats" role="group" aria-label="Indicadores institucionais">
  <span class="stat-chip">${accepted} Aprovados</span><span class="stat-chip">${proposals.length-accepted} Arquivados</span>
  <span class="stat-figure">${votes.reduce((n,a)=>n+a.votes,0)} Votos</span>
  <span class="stat-figure">${proposals.length} PDR</span><span class="stat-figure">${String(accepted).padStart(2,'0')} PR</span>
  </div><div class="tabs overview-tabs" role="group" aria-label="Histórico institucional"><button class="tab" data-overview-tab="votos" aria-pressed="${overviewTab==='votos'}">Histórico de votações</button><button class="tab" data-overview-tab="proposicoes" aria-pressed="${overviewTab==='proposicoes'}">Proposições</button></div>
  <section class="section-body overview-content">${localHistory}${visible.length?visible.map(activityItem).join(''):localHistory?'':'<p class="status-line">Nenhum registro encontrado.</p>'}
   ${remaining>0?`<button class="overview-more" type="button" data-action="show-more-history">Ver mais ${remaining} ${overviewTab==='votos'?'votações':'proposições'}</button>`:''}
  </section>`;
}
function governancePage() {
 const active=sections.find(s=>s.id===expandedSection);
 return `${header('GERENCIAMENTO DELIBERATIVO','Gerencie as seções e deliberados da Cúpula Institucional Academy.')}
 <p class="governance-preview-disclosure" role="note">Alterações nesta página não afetam cadastros oficiais.</p>
 ${rolePreview==='membro'?'<p class="status-line" role="status">O gerenciamento das seções é exclusivo da diretoria.</p>':
 `<div class="governance-list">${sections.map(s=>`${s.category==='comum'?'<h2 class="governance-group-heading">Membros da Academy</h2>':''}<div><button type="button" class="section-toggle" data-section="${s.id}" aria-expanded="${expandedSection===s.id}" ${expandedSection===s.id?`aria-controls="section-members-${escapeHTML(s.id)}"`: ''}><span>${escapeHTML(s.name)}${s.places ? `<small class="section-capacity">${s.places} integrantes previstos</small>` : ''}</span><span class="section-chevron" aria-hidden="true">${expandedSection===s.id?'▾':'▸'}</span></button>
 ${expandedSection===s.id?`<div id="section-members-${escapeHTML(s.id)}">${members.filter(m=>m.sectionIds.includes(s.id)).map(m=>`<div class="section-member"><div class="avatar" aria-hidden="true"></div><button class="section-member-name" type="button" data-edit="${m.id}" title="Editar ${escapeHTML(m.name)}">${escapeHTML(m.name)}</button><button class="icon-button icon-button--edit" type="button" data-edit="${m.id}" aria-label="Editar identificador de ${escapeHTML(m.name)}"><img src="./assets/editar.png" alt=""></button>${s.id==='membros'?'':`<button class="icon-button" type="button" data-demote="${m.id}" aria-label="Rebaixar ${escapeHTML(m.name)} para membro comum"><img src="./assets/rebaixamento.png" alt=""></button>`}</div>
 ${editingMemberId===m.id?`<form class="edit-form" id="edit-member-form" novalidate><label for="member-acdm-id">ACDM ID</label><input id="member-acdm-id" name="acdmId" value="${escapeHTML(m.acdmId ?? '')}" placeholder="DEMO-0001" required minlength="3" maxlength="40" pattern="[A-Za-z0-9_-]+" autocomplete="off" ${editError&&editErrorField==='acdmId'?'aria-invalid="true" aria-describedby="edit-error"':''}><label for="member-cumulative-weight">Proporção de voto cumulativo (opcional)</label><input id="member-cumulative-weight" name="cumulativeVoteWeight" type="number" min="1" step="1" inputmode="numeric" placeholder="Não definida" value="${m.cumulativeVoteWeight??''}" ${editError&&editErrorField==='cumulativeVoteWeight'?'aria-invalid="true" aria-describedby="edit-error"':''}><input type="hidden" name="memberId" value="${m.id}"><button type="submit" class="small-action">Salvar</button>${editError?`<p id="edit-error" class="edit-error" role="alert">${escapeHTML(editError)}</p>`:''}</form>`:''}`).join('')}
 ${members.every(m=>!m.sectionIds.includes(s.id))?'<p class="section-empty">Nenhum membro nesta seção.</p>':''}</div>`:''}</div>`).join('')}</div>`}
 ${notice?`<p class="status-line" role="status">${escapeHTML(notice)} ${lastChange?'<button type="button" class="undo-action" data-action="undo">Desfazer</button>':''}</p>`:''}`;
}

// Only the preview data changes here. Authentication and shared records remain external.
const draftKey='conferatus:proposals-v010';
const deliberationKey='conferatus:deliberations-v010';
// Keep the original bytes of a legacy entry that cannot be interpreted as an array.
// A later save must never silently destroy an unreadable previous session.
function readSessionRecords(key:string):{records:unknown[];unreadableRaw:string|null}{
 let raw:string|null=null;
 try{
  raw=sessionStorage.getItem(key);
  if(raw===null)return {records:[],unreadableRaw:null};
  const parsed:unknown=JSON.parse(raw);
  return Array.isArray(parsed)?{records:parsed,unreadableRaw:null}:{records:[],unreadableRaw:raw};
 }catch{return {records:[],unreadableRaw:raw};}
}
// The fixture references are stable; membership changes never create new identities.
const workflowValidation = {
 memberIds: new Set(members.map(member => member.id)),
 deliberativeSectionIds: new Set(sections.filter(section => section.category === 'deliberativa').map(section => section.id)),
 authorId: members[0]?.id
};
const isSavedLocalDraft = (value: unknown): value is Draft => isSavedDraft(value, workflowValidation);
const draftRestore=readSessionRecords(draftKey);
const scheduleRestore=readSessionRecords(deliberationKey);
const savedDrafts=draftRestore.records;
const savedSchedule=scheduleRestore.records;
const restoredDrafts=uniqueSavedRecords(savedDrafts,isSavedLocalDraft);
const drafts:Draft[]=restoredDrafts.accepted;
const isRestorableLocalSchedule = (value: unknown, candidateDrafts: readonly Draft[] = drafts): value is Deliberation =>
 isRestorableSchedule(value, candidateDrafts, workflowValidation.deliberativeSectionIds);
const restoredSchedule=uniqueSavedRecords(savedSchedule,isRestorableLocalSchedule);
const schedule:Deliberation[]=restoredSchedule.accepted;
// A failed cancellation is kept in this tab, but must never be presented as saved.
const cancellationSaveWarning='Programação cancelada somente nesta aba: não foi possível salvar. Ao recarregar, a programação poderá reaparecer.';
let cancellationSaveFailed=false;
// Any local draft/Socii/schedule write can fail: never call a change saved
// until both session keys are committed. The pending in-memory state is
// recoverable with a single explicit retry, without changing record IDs.
let workflowSaveFailed=false;
const workflowSaveWarning='Não foi possível salvar as alterações desta sessão. Elas estão apenas nesta aba e podem desaparecer ao recarregar.';
const unreadableRecordsBackup={drafts:draftRestore.unreadableRaw,schedule:scheduleRestore.unreadableRaw};
const ignoredRecordsBackup={drafts:restoredDrafts.rejected,schedule:restoredSchedule.rejected};
const ignoredSavedRecords=ignoredRecordsBackup.drafts.length>0||ignoredRecordsBackup.schedule.length>0||
 draftRestore.unreadableRaw!==null||scheduleRestore.unreadableRaw!==null;
function savedRecordNotice(){return ignoredSavedRecords?'<p class="workflow-form-error" role="status">Alguns registros incompletos ou repetidos não foram carregados.</p>':'';}
const blankDraft=():{title:string;body:string;bodyRuns?:RichTextRun[];bodyLayout?:RichBodyLayout}=>({title:'',body:''});
let draftForm=blankDraft();
let richEditorOpen=false;
let lastRichSelection:Range|null=null;
const hasFormatting=(runs?:readonly RichTextRun[])=>Boolean(runs?.some(
 run=>run.marks.length||run.font||run.size||run.color||run.highlight||run.href
));
function syncRichEditor(){
 const editor=document.querySelector<HTMLElement>('#draft-rich-body');
 const field=document.querySelector<HTMLTextAreaElement>('#draft-body');
 if(!editor||!field)return;
 const runs=runsFromEditable(editor);
 const body=runs.map(run=>run.text).join('');
 field.value=body;
 draftForm.body=body;
 draftForm.bodyRuns=hasFormatting(runs)?runs:undefined;
 if(composeError&&(body.trim()||document.querySelector<HTMLInputElement>('#draft-title')?.value.trim())){
  composeError='';
  document.querySelector('#compose-save-error')?.remove();
  document.querySelector('#draft-title')?.removeAttribute('aria-invalid');
  field.removeAttribute('aria-invalid');
  editor.removeAttribute('aria-invalid');
 }
 refreshComposerUnloadGuard();
}
let currentDraftId='';
let finishedProposalReturnTo:'proposals'|'calendar'|'overview'|'profile'='proposals';
let workflowNotice='';
let composeError='';
let composeErrorField: 'title' | 'body' = 'title';
let scheduleFormOpen=false;
let schedulePrefillProposalId:string|null=null;
// Temporary draft only: not a saved option set and never shared across sessions.
let scheduleChoicesDraft='';
let profileScheduleSheetOpen=false;
// Shared, guarded exit for close button, Escape and native close requests.
function dismissProfileScheduleSheet(){
 if(!profileScheduleSheetOpen||!confirmScheduleDeparture())return;
 const proposalId=schedulePrefillProposalId;
 profileScheduleSheetOpen=false;schedulePrefillProposalId=null;scheduleMethod=null;
 render();
 [...document.querySelectorAll<HTMLButtonElement>('[data-schedule-draft]')]
  .find(btn=>btn.dataset.scheduleDraft===proposalId)?.focus();
}
let expandedSchedule='sample-1';
let cancelledHistoryOpen=false;
let pendingScheduleCancellation:string|null=null;
let inviteOpen=false;
let archiveMessage='';
let archiveIsError=false;
// The calendar is a view over the local demo schedule, never a separate data store.
const today=new Date();
let calendarYear=today.getFullYear();
let calendarMonth=today.getMonth();
let selectedCalendarDay='';
function isoDay(date:Date){return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;}
function calendarShift(delta:number){
 const target=new Date(calendarYear,calendarMonth+delta,1);
 calendarYear=target.getFullYear();calendarMonth=target.getMonth();selectedCalendarDay='';
}
function calendarGrid(items:Deliberation[]){
 const first=new Date(calendarYear,calendarMonth,1);
 const offset=first.getDay();
 const count=new Date(calendarYear,calendarMonth+1,0).getDate();
 const monthLabel=new Intl.DateTimeFormat('pt-BR',{month:'long',year:'numeric'}).format(first);
 const days=Array.from({length:count},(_,n)=>{
  const day=isoDay(new Date(calendarYear,calendarMonth,n+1));
  const events=items.filter(item=>item.start.slice(0,10)<=day&&item.end.slice(0,10)>=day).length;
  const selected=selectedCalendarDay===day;
  const current=day===isoDay(new Date());
  return `<button type="button" class="calendar-day${selected?' calendar-day--selected':''}${current?' calendar-day--today':''}" data-calendar-day="${day}" aria-pressed="${selected}" aria-label="${new Intl.DateTimeFormat('pt-BR',{dateStyle:'full'}).format(new Date(calendarYear,calendarMonth,n+1))}${events?`, ${events} programação${events===1?'':'ões'}`:''}"><span>${n+1}</span>${events?`<i aria-hidden="true" class="calendar-marker"></i>`:''}</button>`;
 });
 return `<div class="calendar-hero"><div class="calendar-toolbar"><h1>CALENDÁRIO</h1><div class="calendar-month-nav"><button type="button" data-action="calendar-prev" aria-label="Mês anterior">‹</button><h2 aria-live="polite">${escapeHTML(monthLabel)}</h2><button type="button" data-action="calendar-next" aria-label="Próximo mês">›</button></div></div><div class="calendar-grid" role="group" aria-label="Dias do mês">${[['D','Domingo'],['S','Segunda-feira'],['T','Terça-feira'],['Q','Quarta-feira'],['Q','Quinta-feira'],['S','Sexta-feira'],['S','Sábado']].map(([short,full])=>`<span class="calendar-weekday"><span aria-hidden="true">${short}</span><span class="sr-only">${full}</span></span>`).join('')}${'<span class="calendar-empty"></span>'.repeat(offset)}${days.join('')}</div><div class="calendar-foot"><span><i class="calendar-marker" aria-hidden="true"></i> Dia programado</span><button type="button" data-action="calendar-today">Hoje</button></div></div>`;
}
function saveWorkflows():boolean{
 try{
  // Preserve rejected entries separately before overwriting the working session state.
  if((unreadableRecordsBackup.drafts!==null||unreadableRecordsBackup.schedule!==null)&&
     !sessionStorage.getItem('conferatus:unreadable-session-backup-v0115'))
   sessionStorage.setItem('conferatus:unreadable-session-backup-v0115',JSON.stringify(unreadableRecordsBackup));
  if(ignoredRecordsBackup.drafts.length||ignoredRecordsBackup.schedule.length){
   // Keep the original legacy backup unchanged, even if a later session has new rejects.
   const legacyKey='conferatus:invalid-session-backup-v0114';
   if(!sessionStorage.getItem(legacyKey))sessionStorage.setItem(legacyKey,JSON.stringify(ignoredRecordsBackup));
   // A separate append-only journal covers later rejections without overwriting older copies.
   const journalKey='conferatus:quarantined-session-backups-v0116';
   const previous=sessionStorage.getItem(journalKey);
   const journal:unknown=previous===null?[]:JSON.parse(previous);
   if(!Array.isArray(journal))throw new Error('Invalid local recovery journal');
   const current=JSON.stringify(ignoredRecordsBackup);
   if(!journal.some(entry=>JSON.stringify(entry)===current))
    sessionStorage.setItem(journalKey,JSON.stringify([...journal,ignoredRecordsBackup]));
  }
  // Both keys represent one local workflow snapshot. If the second write fails,
  // restore the first key rather than leaving a partially committed session.
  const previousDrafts=sessionStorage.getItem(draftKey);
  sessionStorage.setItem(draftKey,JSON.stringify(drafts));
  try{sessionStorage.setItem(deliberationKey,JSON.stringify(schedule));}
  catch(error){
   try{
    if(previousDrafts===null)sessionStorage.removeItem(draftKey);
    else sessionStorage.setItem(draftKey,previousDrafts);
   }catch{/* Best effort only: browser storage can also fail during rollback. */}
   throw error;
  }
  cancellationSaveFailed=false;
  workflowSaveFailed=false;
  return true;
 }catch{
  workflowSaveFailed=true;
  return false;
 }
}
function selectOptions(selected:string,items:{id:string;name:string}[]){return items.map(x=>`<option value="${escapeHTML(x.id)}" ${selected===x.id?'selected':''}>${escapeHTML(x.name)}</option>`).join('');}
function draftReady(d:Draft){return d.authorComplete&&d.partners.every(p=>p.complete);}
function draftStatusLabel(d:Draft){return d.status==='concluida'?'Concluída':d.status==='revisao'?(d.authorComplete?'Aguardando Socii':'Aguardando autoria'):'Em redação';}
function friendlyStamp(date:string){const parsed=new Date(date);return Number.isNaN(parsed.getTime())?'Data não definida':parsed.toLocaleString('pt-BR',{dateStyle:'short',timeStyle:'short'});}
// Session proposals are authored by the preview's lead fixture member, NOT by
// an authenticated Academy account. Show only active, already-linked schedules.
function contextualScheduleButton(d:Draft){
 if(d.status!=='concluida')return '';
 return `<button type="button" class="session-schedule-start" data-schedule-draft="${escapeHTML(d.id)}">Programar deliberação sobre esta proposição</button>`;
}
function linkedScheduleButtons(d:Draft) {
 const linked=schedule.filter(item=>item.proposalId===d.id&&item.status==='programada');
 return linked.length?`<div class="session-schedule-links" role="group" aria-label="Programações locais desta proposição">${linked.map(item=>`<button type="button" class="session-schedule-link" data-linked-schedule="${escapeHTML(item.id)}">Programação: ${escapeHTML(item.title)} · ${friendlyStamp(item.start)}</button>`).join('')}</div>`:'';
}
function proposalsPage(){
 const author=members[0];
 const examples=activities.filter(a=>a.type==='proposicao' && a.memberId===author?.id).slice(0,4);
 return `${header(undefined,undefined,false)}<div class="workflow-profile">${author?memberHeader(author,'proposicoes',false):''}<div class="tabs workflow-tabs" role="group" aria-label="Histórico do membro"><button class="tab" type="button" data-route="profile" aria-label="Consultar histórico de votação">Histórico de votações</button><span class="tab" aria-current="page">Proposições e Socii</span></div></div>
  <div class="workflow-layout workflow-proposals-layout">${savedRecordNotice()}${drafts.length?'<h2 class="workflow-record-heading">Proposições desta sessão</h2>':''}${drafts.some(d=>d.partners.some(p=>!p.complete))?'<p class="workflow-socii-help" role="note">Nesta prévia, as etapas do Socii são locais. Nenhuma outra conta é acessada ou notificada.</p>':''}${drafts.length?drafts.map(d=>`<article class="workflow-record"><button data-draft="${escapeHTML(d.id)}" class="workflow-record-btn"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${draftStatusLabel(d)} · ${escapeHTML(d.type)}</small><p>${escapeHTML(d.body.slice(0,140))}</p></button>${linkedScheduleButtons(d)}${contextualScheduleButton(d)}${d.partners.length?`<p class="workflow-partners"><strong>Concluíram ${Number(d.authorComplete)+d.partners.filter(p=>p.complete).length} de ${d.partners.length+1}</strong><span>Autoria: ${d.authorComplete?'concluída':'pendente'} · Socii: ${d.partners.map(p=>`${escapeHTML(members.find(m=>m.id===p.id)?.name??'Membro')} (${p.complete?'concluiu':'pendente'})`).join(', ')}</span></p>`:''}${d.partners.some(p=>!p.complete)?'<div class="workflow-socii-completion" role="group" aria-label="Etapas fictícias do Socii">'+d.partners.filter(p=>!p.complete).map(p=>`<button type="button" class="workflow-demo-confirm" data-confirm-partner="${escapeHTML(d.id)}:${escapeHTML(p.id)}">Marcar etapa de ${escapeHTML(members.find(m=>m.id===p.id)?.name??'participante')} como concluída</button>`).join('')+'</div>':''}</article>`).join(''):''}
 ${examples.length?'<h2 class="workflow-record-heading">Histórico de exemplo</h2>':''}${examples.map(activityItem).join('')}
 ${advancedPreview?`<section class="local-archive" aria-label="Cópia de segurança dos registros da prévia"><h2>Cópia local da prévia</h2><p>Exporta apenas proposições, Socii e programações desta aba. O arquivo pode conter o texto que você escreveu. Não inclui login, votos, permissões ou dados da Academy.</p><div class="local-archive-actions"><button type="button" data-action="export-local-archive">Baixar cópia JSON</button><button type="button" data-action="import-local-archive">Restaurar cópia JSON</button><input id="archive-file-input" type="file" accept=".json,application/json" hidden></div>${archiveMessage?`<p class="local-archive-message" role="${archiveIsError?'alert':'status'}">${escapeHTML(archiveMessage)}</p>`:''}</section>`:''}
 </div><div class="workflow-actions"><button type="button" class="workflow-outline" data-action="invite-socii" aria-expanded="${inviteOpen}" ${inviteOpen?'aria-controls="invite-socii-form"':''}>Adicionar ao Socii</button>${inviteOpen?`<form id="invite-socii-form" class="workflow-inline" aria-label="Adicionar participante ao Socii">${!drafts.some(d=>d.status!=='concluida')?'<p class="workflow-socii-help" role="status">Para adicionar participantes, primeiro redija e salve uma proposição.</p>':''}<p class="workflow-socii-help">Esta lista representa participantes fictícios. Nenhum convite é enviado à Academy.</p><label>Proposição<select name="draftId" required>${drafts.filter(d=>d.status!=='concluida').length>1?'<option value="" disabled selected>Selecione a proposição</option>':''}${drafts.filter(d=>d.status!=='concluida').map(d=>`<option value="${escapeHTML(d.id)}">${escapeHTML(d.title)}</option>`).join('')}</select></label><label>Participante<select name="memberId" required><option value="" selected disabled>Selecione uma pessoa</option>${selectOptions('',members.slice(1))}</select></label><button class="workflow-primary" ${!drafts.some(d=>d.status!=='concluida')?'disabled':''}>Adicionar participante</button></form>`:''}
 <button type="button" class="workflow-primary" data-action="new-proposal">Redigir proposição</button></div>
 ${workflowNotice?`<p class="workflow-status" role="status">${escapeHTML(workflowNotice)}</p>`:''}`;
}
// Show only participants linked to this proposal; a local preview has no valid elapsed time.
function sociiEditorBar(d:Draft|undefined){
 if(!d?.partners.length)return '';
 const names=d.partners.map(p=>members.find(m=>m.id===p.id)?.name).filter((n):n is string=>Boolean(n));
 const participantText=names.length===1?`Você e ${names[0]}`:`Você e ${d.partners.length} participantes`;
 const finished=Number(d.authorComplete)+d.partners.filter(p=>p.complete).length;
 return `<aside class="workflow-socii-editor-bar" aria-label="Participantes do Socii nesta proposição">
 <span class="workflow-socii-avatars" aria-hidden="true"><i></i><i></i></span>
 <div class="workflow-socii-editor-status"><strong>${escapeHTML(participantText)} em Socii</strong><small>Concluíram ${finished} de ${d.partners.length+1}</small></div>
 <span class="workflow-socii-editor-label" aria-hidden="true">Socii</span></aside>`;
}
function composePage(){
 const layout=draftForm.bodyLayout??DEFAULT_RICH_LAYOUT;
 const alignChoices: [RichBodyLayout['align'],string][]=[
  ['left','Esquerda'],['center','Centro'],['right','Direita'],['justify','Justificado']
 ];
 const indentChoices=[0,16,32] as const;
 const lineChoices=[1.4,1.7,2] as const;
 const editing=drafts.find(d=>d.id===currentDraftId);
 return `${sociiEditorBar(editing)}<div class="workflow-editor-head"><span>CONFFRATUS</span><h1>${escapeHTML(draftForm.title||'Título')}</h1></div>
 <form id="compose-proposal-form" class="workflow-editor" novalidate><label for="draft-title">Título da proposição</label><input id="draft-title" name="title" minlength="3" maxlength="140" required ${composeErrorField==='title'&&composeError?'aria-invalid="true" aria-describedby="compose-save-error"':''} placeholder="Título" value="${escapeHTML(draftForm.title)}">
 <label for="draft-body">Redação</label>${richEditorOpen?`<div class="workflow-rich-toolbar" role="group" aria-label="Formatação da redação">
 <button type="button" data-rich-command="bold" aria-label="Negrito"><strong>B</strong></button>
 <button type="button" data-rich-command="italic" aria-label="Itálico"><em>I</em></button>
 <button type="button" data-rich-command="underline" aria-label="Sublinhado"><u>S</u></button>
 <button type="button" data-rich-command="strike" aria-label="Tachado"><s>T</s></button>
 <button type="button" data-rich-command="subscript" aria-label="Subscrito (x dois)">x<sub>2</sub></button>
 <button type="button" data-rich-command="superscript" aria-label="Sobrescrito (x ao quadrado)">x<sup>2</sup></button></div>
 <div class="workflow-rich-options" role="group" aria-label="Tipografia e cores">
 <label>Fonte<select data-rich-format="font" aria-label="Fonte do texto selecionado"><option value="">Escolha a fonte</option><option value="aptos">Aptos</option><option value="arial">Arial</option><option value="georgia">Georgia</option></select></label>
 <label>Tamanho<select data-rich-format="size" aria-label="Tamanho do texto selecionado"><option value="">Tamanho</option><option value="12">12 px</option><option value="16">16 px</option><option value="18">18 px</option><option value="24">24 px</option><option value="30">30 px</option></select></label>
 <label>Cor do texto<input type="color" data-rich-format="color" value="#242733" aria-label="Cor do texto selecionado"></label>
 <label>Marca-texto<input type="color" data-rich-format="highlight" value="#fff0a5" aria-label="Cor de realce do texto selecionado"></label>
 </div>
 <div class="workflow-rich-links" role="group" aria-label="Links do texto selecionado">
 <label for="draft-link-url">Link do trecho selecionado</label>
 <input id="draft-link-url" type="text" inputmode="url" autocomplete="url" maxlength="2048" placeholder="https://exemplo.com" aria-describedby="draft-link-feedback">
 <div class="workflow-rich-link-actions">
 <button type="button" data-rich-link="apply">Inserir link</button>
 <button type="button" data-rich-link="remove">Remover link</button>
 </div>
 <p id="draft-link-feedback" role="status" aria-live="polite">Selecione um trecho da redação antes de aplicar ou remover um link.</p>
 </div>
 <div class="workflow-rich-layout" role="group" aria-label="Alinhamento e espaçamento da redação inteira">
 <p class="workflow-rich-layout-caption">Redação inteira</p>
 <label>Alinhamento<select data-rich-layout="align" aria-label="Alinhamento da redação">
 ${alignChoices.map(([value,label])=>`<option value="${value}" ${layout.align===value?'selected':''}>${label}</option>`).join('')}
 </select></label>
 <label>Altura de linha<select data-rich-layout="lineHeight" aria-label="Altura de linha da redação">
 ${lineChoices.map(value=>`<option value="${value}" ${layout.lineHeight===value?'selected':''}>${String(value).replace('.',',')}</option>`).join('')}
 </select></label>
 <label>Recuo esquerdo<select data-rich-layout="left" aria-label="Recuo à esquerda">
 ${indentChoices.map(value=>`<option value="${value}" ${layout.left===value?'selected':''}>${value===0?'Sem recuo':value+' px'}</option>`).join('')}
 </select></label>
 <label>Recuo direito<select data-rich-layout="right" aria-label="Recuo à direita">
 ${indentChoices.map(value=>`<option value="${value}" ${layout.right===value?'selected':''}>${value===0?'Sem recuo':value+' px'}</option>`).join('')}
 </select></label>
 </div>
 <div id="draft-rich-body" class="workflow-rich-editor" contenteditable="true" role="textbox" aria-multiline="true" aria-label="Redação" data-placeholder="Escreva..." style="${richLayoutStyle(draftForm.bodyLayout,true)}" ${composeErrorField==='body'&&composeError?'aria-invalid="true" aria-describedby="compose-save-error"':''}>${renderRichText(draftForm.body,draftForm.bodyRuns)}</div>
 <textarea id="draft-body" name="body" hidden>${escapeHTML(draftForm.body)}</textarea>`:`<textarea id="draft-body" name="body" required minlength="20" ${composeErrorField==='body'&&composeError?'aria-invalid="true" aria-describedby="compose-save-error"':''} placeholder="Escreva...">${escapeHTML(draftForm.body)}</textarea>
 <button type="button" class="workflow-enable-rich" data-action="enable-rich-editor">Formatar texto</button>`}
 ${composeError?`<p id="compose-save-error" class="workflow-form-error" role="alert">${escapeHTML(composeError)}</p>`:''}
 <div class="workflow-editor-actions"><button class="workflow-primary" type="submit" name="intent" value="conclude">Concluir redação</button><button class="workflow-outline" type="submit" name="intent" value="save" formnovalidate>Salvar rascunho</button><button class="workflow-outline" type="button" data-route="${finishedProposalReturnTo==='profile'?'profile':'proposals'}">${finishedProposalReturnTo==='profile'?'Voltar ao perfil':'Voltar'}</button></div></form>`;
}
function reviewPage(){
 const d=drafts.find(x=>x.id===currentDraftId);if(!d)return proposalsPage();
 if(d.status==='concluida')return `<div class="workflow-editor-head"><span>CONFFRATUS</span><h1>${escapeHTML(d.title)}</h1></div><div class="workflow-review-body"><p style="${richLayoutStyle(d.bodyLayout)}">${renderRichText(d.body,d.bodyRuns)}</p></div><div class="workflow-review-panel"><div class="workflow-finished"><strong>Proposição concluída</strong><p>Seção: ${escapeHTML(sections.find(s=>s.id===d.sectionId)?.name??'Não definida')} · ${escapeHTML(d.type)}</p>${linkedScheduleButtons(d)}<button type="button" class="workflow-primary" data-route="${finishedProposalReturnTo}">${finishedProposalReturnTo==='calendar'?'Voltar à programação':finishedProposalReturnTo==='overview'?'Voltar ao histórico':finishedProposalReturnTo==='profile'?'Voltar ao perfil':'Voltar às proposições'}</button></div></div>`;
 const d3Start=d3SingleExperiment?'<dialog id="d3-review-dialog" closedby="none" aria-labelledby="d3-review-title">':'';
 const d3End=d3SingleExperiment?'</dialog>':'';
 const d3Close=d3SingleExperiment?'<button type="button" class="d3-review-close" data-dismiss-d3-review aria-label="Voltar à redação sem confirmar">×</button>':'';
 const d3Cancel=d3SingleExperiment?'':'<button type="button" class="workflow-outline" data-route="compose" aria-label="Cancelar confirmação e voltar à redação">Cancelar</button>';
 const confirmedPartner=d.partners.find(p=>p.complete);
 const confirmedName=confirmedPartner?members.find(m=>m.id===confirmedPartner.id)?.name:undefined;
 const reviewMessage=confirmedPartner
  ? `${confirmedName?escapeHTML(confirmedName):'Um participante do Socii'} concluiu sua parte. Confira os dados e a redação antes de confirmar a conclusão.`
  : 'Confira os dados e a redação antes de confirmar a conclusão.';
 return `${sociiEditorBar(d)}<div class="workflow-editor-head"><span>CONFFRATUS</span><h1>${escapeHTML(d.title)}</h1></div>
 <div class="workflow-review-body${d3SingleExperiment?' workflow-review-body--d3':''}"><p style="${richLayoutStyle(d.bodyLayout)}">${renderRichText(d.body,d.bodyRuns)}</p></div>
 <div class="workflow-review-panel workflow-review-panel--pending${d3SingleExperiment?' workflow-review-panel--d3':''}">${d3Start}<form id="confirm-proposal-form" class="workflow-form workflow-review-form" data-review-draft="${escapeHTML(d.id)}">
 <div class="workflow-review-sheet"><img class="workflow-review-crest" src="./assets/crest.png" alt="" width="38" height="38">${d3SingleExperiment?'<h2 id="d3-review-title" class="sr-only">Confirmar proposição</h2>':`<p>${reviewMessage}</p>`}${d3Close}
 <label>Seção responsável<select name="sectionId" required>${selectOptions(d.sectionId,sections.filter(s=>s.category==='deliberativa'))}</select></label>
 <label>Tipo de proposição<select name="type" required>${['PDR','PR','Ofício'].map(t=>`<option value="${t}" ${t===d.type?'selected':''}>${t}</option>`).join('')}</select></label>
 </div><div class="workflow-review-buttons">${d3Cancel}<button class="workflow-primary" type="submit">${d3SingleExperiment?'CONFIRMAR':'Confirmar'}</button></div></form>${d3End}</div>`;
}
// Display only Socii participants already linked to this session's proposal.
function calendarSociiLine(proposalId:string){
 const draft=drafts.find(d=>d.id===proposalId);
 const names=draft?.partners.map(p=>members.find(m=>m.id===p.id)?.name)
  .filter((name):name is string=>Boolean(name))??[];
 return names.length?`<span class="calendar-socii">Socii: ${names.map(escapeHTML).join(', ')}</span>`:'';
}
// Share a single form, validation and persistence path with the D2 prototype.
function scheduleFormMarkup(profileSheet=false){
 const heading=`<form id="schedule-deliberation-form" class="workflow-form workflow-schedule-form"><h2>Programar deliberação</h2>
 ${!drafts.some(d=>d.status==='concluida')?'<p class="workflow-help">Para agendar, conclua uma proposição primeiro. <button type="button" data-route="proposals">Ir às proposições</button></p>':''}
 `;
 const titleField=`<label>Título da deliberação<input name="title" maxlength="140" required placeholder="Título da deliberação"></label>
 `;
 const objectiveField=`<label>Descrição objetiva<textarea name="objective" required minlength="15" rows="3" placeholder="Descrição objetiva"></textarea></label>
 `;
 const proposalField=`<label>Selecione a proposição<select name="proposalId" required ${!drafts.some(d=>d.status==='concluida')?'disabled':''}><option value="" ${schedulePrefillProposalId?'':'selected'}>Selecione</option>${drafts.filter(d=>d.status==='concluida').map(d=>`<option value="${escapeHTML(d.id)}" ${d.id===schedulePrefillProposalId?'selected':''}>${escapeHTML(d.title)}</option>`).join('')}</select></label>
 `;
 const sectionField=`<label>Seção deliberativa<select name="sectionId" required>${selectOptions('integridade',sections.filter(s=>s.category==='deliberativa'))}</select></label>
 `;
 const datesField=`<div class="workflow-grid-two"><label>Data e hora de início<input type="datetime-local" name="start" required></label><label>Data e hora de encerramento<input type="datetime-local" name="end" required></label></div>
 `;
 const typeField=`<label>Tipo de proposição<select name="type" required><option value="PDR">PDR</option><option value="PR">PR</option><option value="Ofício">Ofício</option></select></label>
  `;
 const methodField=`<label>Modalidade de votação<select name="method" id="schedule-method" required><option value="">Selecione a modalidade</option>${DELIBERATION_METHODS.map(mode=>`<option value="${mode.id}">${escapeHTML(mode.label)} — ${escapeHTML(mode.detail)}</option>`).join('')}</select></label>
`;
 const choicesField=`  ${scheduleMethod&&scheduleMethod!=='binaria'?`<label>Alternativas para esta deliberação<textarea name="choices" rows="5" maxlength="648" placeholder="Uma alternativa por linha, de 2 a 8" required></textarea></label><p class="workflow-help">De 2 a 8 alternativas distintas, uma por linha (até 80 caracteres cada).</p>`:'' }
`;
 const helpField=`  <p class="workflow-help">Defina como as opções serão apresentadas aos participantes.</p>
`;
 const footer=` <button class="workflow-primary" type="submit" ${!drafts.some(d=>d.status==='concluida')?'disabled':''}>Confirmar programação</button></form>`;
 const normal=titleField+objectiveField+proposalField+sectionField+datesField+typeField+methodField+choicesField+helpField;
 const supplemental=`<section class="profile-schedule-supplemental" aria-labelledby="profile-sheet-supplemental-title"><h3 id="profile-sheet-supplemental-title">Detalhes da programação</h3>${titleField}${objectiveField}${methodField}${choicesField}${helpField}</section>`;
 const sheet=proposalField+sectionField+datesField+typeField+supplemental;
 return heading+(profileSheet?sheet:normal)+footer;
}
function calendarPage(){
 const sample:Deliberation[]=[{id:'sample-1',title:'Revisão do calendário de reuniões',sectionId:'integridade',objective:'Organizar o calendário de reuniões institucionais.',start:'2026-11-22T14:00',end:'2026-11-23T14:00',type:'PDR',proposalId:'',status:'programada' as const}];
 const all=[...sample,...schedule.filter(s=>s.status==='programada')]
  .sort((a,b)=>a.start.localeCompare(b.start));
 const visible=selectedCalendarDay?all.filter(item=>item.start.slice(0,10)<=selectedCalendarDay&&item.end.slice(0,10)>=selectedCalendarDay):all;
 // Cancelled entries remain in the session's original schedule array. Keep them
 // separate from active calendar markers, date filters and scheduling controls.
 const cancelled=schedule.filter(item=>item.status==='cancelada');
 const cancelledHistory=cancelled.length?`<section class="calendar-history" aria-label="Histórico de cancelamentos">
 <button type="button" class="calendar-history-toggle" data-action="toggle-cancelled-history" aria-expanded="${cancelledHistoryOpen}" ${cancelledHistoryOpen?'aria-controls="cancelled-schedule-history"':''}>Programações canceladas (${cancelled.length})</button>
 ${cancelledHistoryOpen?`<div id="cancelled-schedule-history" role="region" aria-label="Programações canceladas da sessão"><p class="calendar-history-note">Programações canceladas permanecem disponíveis para consulta.</p>${cancelled.map(item=>{
   const linked=drafts.find(d=>d.id===item.proposalId);
   return `<article class="calendar-cancelled-record"><h3>${escapeHTML(item.title)}</h3><p><strong>Cancelada</strong> · ${escapeHTML(item.type)}</p><p>Modalidade: ${escapeHTML(DELIBERATION_METHODS.find(m=>m.id===item.method)?.label??'Não informada (registro anterior)')}</p><p>${friendlyStamp(item.start)} até ${friendlyStamp(item.end)}</p><p>Seção: ${escapeHTML(sections.find(section=>section.id===item.sectionId)?.name??'Não disponível')}</p><p>Proposição: ${linked?escapeHTML(linked.title):'Proposição associada indisponível nesta sessão'}</p><p>${escapeHTML(item.objective)}</p></article>`;
  }).join('')}</div>`:''}</section>`:'';
 return `<div class="workflow-layout">${savedRecordNotice()}${calendarGrid(all)}<button class="workflow-open" type="button" data-action="open-schedule" aria-expanded="${scheduleFormOpen}" ${scheduleFormOpen?'aria-controls="schedule-deliberation-form"':''}>${scheduleFormOpen?'Fechar agendamento':'Iniciar uma Votação'}</button>
 <p class="calendar-preview-disclosure" role="note">Defina a data e a modalidade da deliberação.</p>
 ${scheduleFormOpen?scheduleFormMarkup():''}
 ${cancellationSaveFailed||workflowNotice?`<p class="workflow-status">${escapeHTML(cancellationSaveFailed?cancellationSaveWarning:workflowNotice)}</p>`:''}
 ${cancellationSaveFailed?'<button type="button" class="calendar-save-retry" data-action="retry-cancellation-save">Tentar salvar cancelamento nesta sessão</button>':''}
 <div class="calendar-list"><div class="calendar-list-head"><h2>${selectedCalendarDay?`Programações em ${new Date(`${selectedCalendarDay}T12:00`).toLocaleDateString('pt-BR')}`:'Programações'}</h2>${selectedCalendarDay?'<button type="button" data-action="calendar-all">Ver todas</button>':''}</div>${visible.length===0?'<p class="calendar-empty-message">Nenhuma programação nesta data.</p>':''}${visible.map(item=>`<article class="calendar-item${expandedSchedule===item.id?' calendar-item--expanded':''}"><button type="button" data-schedule="${escapeHTML(item.id)}" aria-expanded="${expandedSchedule===item.id}" ${expandedSchedule===item.id?`aria-controls="schedule-details-${escapeHTML(item.id)}"`: ''}><strong>${escapeHTML(item.title)}</strong><small>${friendlyStamp(item.start)} até ${friendlyStamp(item.end)}</small><span>Seção: ${escapeHTML(sections.find(s=>s.id===item.sectionId)?.name??'')}</span>${calendarSociiLine(item.proposalId)}</button>
 ${expandedSchedule===item.id?`<div id="schedule-details-${escapeHTML(item.id)}" class="calendar-expanded"><div class="calendar-status"><span class="calendar-status-type">${escapeHTML(item.type)}</span><strong>PROPOSIÇÃO EM DELIBERAÇÃO</strong></div><p>${escapeHTML(item.objective)}</p>${item.id==='sample-1'&&!item.method?'':`<p>Modalidade: ${escapeHTML(DELIBERATION_METHODS.find(mode=>mode.id===item.method)?.label??'Não informada (registro anterior)')}</p>`}${item.choices?`<p>Alternativas: ${item.choices.map(option=>escapeHTML(option.label)).join(' · ')}</p>`:''}${item.id!=='sample-1'&&item.method&&(item.method==='binaria'||isValidPreviewChoices(item.choices))?`<button type="button" data-preview-schedule="${escapeHTML(item.id)}" class="preview-schedule-open">Participar nesta votação</button>`:''}${item.proposalId?(drafts.some(d=>d.id===item.proposalId)?`<button type="button" class="calendar-proposal-link" data-open-schedule-proposal="${escapeHTML(item.proposalId)}">Ver proposição associada</button>`:'<p class="calendar-link-missing" role="status">Proposição vinculada indisponível nesta sessão.</p>'):''}${item.proposalId&&drafts.some(d=>d.id===item.proposalId)&&members[0]?'<button type="button" data-open-proposal-author>Ver perfil da autoria</button>':''}<button type="button" data-cancel-schedule="${escapeHTML(item.id)}" aria-expanded="${pendingScheduleCancellation===item.id}" ${pendingScheduleCancellation===item.id?`aria-controls="schedule-cancel-confirm-${escapeHTML(item.id)}"`:''} ${item.id==='sample-1'?'disabled title="Exemplo fixo"':''}>Cancelar programação deliberativa</button>${pendingScheduleCancellation===item.id?`<div id="schedule-cancel-confirm-${escapeHTML(item.id)}" class="calendar-cancel-confirm" role="group" tabindex="-1" aria-label="Confirmar cancelamento de programação"><p>Cancelar a programação “${escapeHTML(item.title)}”? Ela sairá da lista ativa, mas permanecerá no histórico desta sessão.</p><div class="calendar-cancel-confirm-actions"><button type="button" data-keep-schedule="${escapeHTML(item.id)}">Manter programação</button><button type="button" data-confirm-cancel-schedule="${escapeHTML(item.id)}">Confirmar cancelamento</button></div></div>`:''}</div>`:''}</article>`).join('')}</div>${cancelledHistory}</div>`;
}

let lastRenderedHash = location.hash;
function render() {
 if (!root) return;
 // The footer/menu and validation messages rerender the composer; first capture
 // plain input fields so this local UI refresh does not erase unsaved keystrokes.
 const composing=root.querySelector<HTMLFormElement>('#compose-proposal-form');
 if(composing){
  const titleInput=composing.querySelector<HTMLInputElement>('#draft-title');
  const plainBody=composing.querySelector<HTMLTextAreaElement>('#draft-body');
  if(titleInput)draftForm.title=titleInput.value;
  if(!richEditorOpen&&plainBody)draftForm.body=plainBody.value;
 }
 // A local edit must not unexpectedly jump the user to the top of a long page.
 const previousScroll = window.scrollY;
 // The D2 bottom sheet is a separate scroll container; preserve its viewport
 // when a voting method change rebuilds the shared form's extra fields.
 const previousProfileSheetScroll=root.querySelector<HTMLDialogElement>('#profile-schedule-dialog')?.scrollTop;
 // Preserve local scheduling inputs while browsing days and months.
 const scheduleForm = root.querySelector<HTMLFormElement>('#schedule-deliberation-form');
 const scheduleValues = scheduleForm ? new FormData(scheduleForm) : null;
 // Preserve unsaved choices on the SAME proposal's review sheet when local
 // UI controls (such as the footer menu) rerender the page.
 const previousReviewForm=root.querySelector<HTMLFormElement>('#confirm-proposal-form');
 const previousReviewDraft=previousReviewForm?.dataset.reviewDraft;
 const previousReviewSection=previousReviewForm?.querySelector<HTMLSelectElement>('[name="sectionId"]')?.value;
 const previousReviewType=previousReviewForm?.querySelector<HTMLSelectElement>('[name="type"]')?.value;
 const previousChoices=scheduleForm?.querySelector<HTMLTextAreaElement>('[name="choices"]');
 if(previousChoices)scheduleChoicesDraft=previousChoices.value;
 // Never use data-member here: it triggers the global profile-navigation click handler.
 // Preserve checked values on ballot validation errors, not across distinct methods.
 const priorVoteForm=root.querySelector<HTMLFormElement>('#preview-vote-form');
 const voteFields=priorVoteForm?.dataset.mode===previewMode&&priorVoteForm?.dataset.previewMember===previewVoteMemberId
  ? Array.from(priorVoteForm.querySelectorAll<HTMLInputElement|HTMLSelectElement>('input,select')).map(field=>({name:field.name,value:field.value,checked:field instanceof HTMLInputElement?field.checked:undefined})) : null;
 // A new context must never inherit an unfinished choice from another ballot.
 const voteDraftScope=previewSampleScope();
 if(voteFields && !previewVoteReceipt){
  previewVoteDraft={scope:voteDraftScope,memberId:previewVoteMemberId,fields:voteFields};
 }
 const fieldsToRestore=voteFields??(
  previewVoteDraft?.scope===voteDraftScope && previewVoteDraft.memberId===previewVoteMemberId
   ? previewVoteDraft.fields : null
 );
 const preserveScroll = location.hash === lastRenderedHash;
 lastRenderedHash = location.hash;
 // Keep keyboard focus on the same action after updating the preview DOM.
 const active = document.activeElement;
 const attributes = ['data-vote','data-tab','data-overview-tab','data-section','data-edit','data-activity','data-action','data-calendar-day','data-schedule'];
 const focusTarget = active instanceof HTMLElement
   ? attributes.map(attr => [attr, active.getAttribute(attr)] as const).find(([,value]) => value!==null)
   : undefined;
 const route=routeFromHash();
 const page=route==='ballot'?ballotPage():route==='members'?memberList():route==='profile'?profilePage():route==='overview'?overviewPage():route==='calendar'?calendarPage():route==='proposals'?proposalsPage():route==='compose'?composePage():route==='review'?reviewPage():governancePage();
 const saveWarning=workflowSaveFailed && !(cancellationSaveFailed && route==='calendar')
  ? `<section class="workflow-save-warning" role="alert" aria-label="Gravação local pendente"><p>${workflowSaveWarning}</p><button type="button" data-action="retry-workflow-save">Tentar salvar alterações nesta sessão</button></section>`
  : '';
 root.innerHTML=`<div class="app-shell" aria-label="CONFFRATUS — dados fictícios"><a href="#main-content" class="skip-link">Ir para o conteúdo</a><main id="main-content" tabindex="-1">${saveWarning}${page}</main>${footer()}
</div>`;
 // Some legacy visual layouts have no visible heading. Supply one for heading
 // navigation without changing their typography or the Megalos composition.
 const mainContent = root.querySelector<HTMLElement>('#main-content');
 if (mainContent && !mainContent.querySelector('h1')) {
  const heading = document.createElement('h1');
  heading.className = 'sr-only';
  const routeHeadings: Record<Route,string> = {
   ballot:'Votação demonstrativa', members:'Membros', profile:'Perfil do membro',
   overview:'Histórico de votações e proposições', governance:'Gerenciamento deliberativo',
   calendar:'Calendário', proposals:'Proposições e Socii',
   compose:'Redigir proposição', review:'Revisão de proposição'
  };
  heading.textContent = routeHeadings[route];
  mainContent.prepend(heading);
 }
 const d3Dialog=root.querySelector<HTMLDialogElement>('#d3-review-dialog');
 if(d3Dialog&&!d3Dialog.open){
  d3Dialog.showModal();
  d3Dialog.querySelector<HTMLSelectElement>('[name="sectionId"]')?.focus({preventScroll:true});
 }
 const profileDialog=root.querySelector<HTMLDialogElement>('#profile-schedule-dialog');
 if(profileDialog&&!profileDialog.open){
  profileDialog.showModal();
  profileDialog.querySelector<HTMLElement>('#profile-schedule-sheet-label')?.focus({preventScroll:true});
 }
 if (scheduleValues) {
  const nextForm = root.querySelector<HTMLFormElement>('#schedule-deliberation-form');
  if (nextForm) for (const [name, value] of scheduleValues) {
   const field = nextForm.elements.namedItem(name);
   if (field instanceof HTMLInputElement || field instanceof HTMLTextAreaElement || field instanceof HTMLSelectElement) field.value = String(value);
  }
 }
 // A method may hide the choices textarea. Keep its unsaved text on a
 // method round-trip, then discard the cache when the scheduling form closes.
 const currentScheduleForm=root.querySelector<HTMLFormElement>('#schedule-deliberation-form');
 if(currentScheduleForm){
  const choiceField=currentScheduleForm.querySelector<HTMLTextAreaElement>('[name="choices"]');
  if(choiceField&&!scheduleValues?.has('choices'))choiceField.value=scheduleChoicesDraft;
 }else scheduleChoicesDraft='';
 const nextReviewForm=root.querySelector<HTMLFormElement>('#confirm-proposal-form');
 if(previousReviewDraft && nextReviewForm?.dataset.reviewDraft===previousReviewDraft){
  const nextSection=nextReviewForm.querySelector<HTMLSelectElement>('[name="sectionId"]');
  const nextType=nextReviewForm.querySelector<HTMLSelectElement>('[name="type"]');
  if(nextSection && previousReviewSection && [...nextSection.options].some(o=>o.value===previousReviewSection))
   nextSection.value=previousReviewSection;
  if(nextType && previousReviewType && [...nextType.options].some(o=>o.value===previousReviewType))
   nextType.value=previousReviewType;
 }
 if(fieldsToRestore){
  const fields=root.querySelector<HTMLFormElement>('#preview-vote-form')?.querySelectorAll<HTMLInputElement|HTMLSelectElement>('input,select');
  if(fields?.length===fieldsToRestore.length)fields.forEach((field,index)=>{
   const previous=fieldsToRestore[index];
   if(previous&&field.name===previous.name){field.value=previous.value;if(field instanceof HTMLInputElement&&previous.checked!==undefined)field.checked=previous.checked;}
  });
 }
 if (focusTarget) {
  const [attr,value]=focusTarget;
  [...root.querySelectorAll<HTMLElement>(`[${attr}]`)]
   .find(element=>element.getAttribute(attr)===value)?.focus({preventScroll:true});
 }
 // Only changed notices should be announced, not unrelated rerenders.
 if (workflowNotice !== announcedWorkflowNotice) {
  announcedWorkflowNotice = workflowNotice;
  workflowAnnouncer.textContent = workflowNotice;
 }
 if (preserveScroll) window.scrollTo({top:previousScroll,behavior:'instant'});
 if(profileDialog?.open&&previousProfileSheetScroll!==undefined){
  profileDialog.scrollTop=previousProfileSheetScroll;
 }
 refreshComposerUnloadGuard();
}
// Announce calendar filtering and month changes through the existing stable
// status region. Recreating an aria-live element during render() does not
// reliably announce its contents to assistive technologies.
function announceCalendarView() {
 const month=document.querySelector<HTMLElement>('.calendar-month-nav h2')?.textContent?.trim()??'';
 const heading=document.querySelector<HTMLElement>('.calendar-list-head h2')?.textContent?.trim()??'Programações';
 const count=document.querySelectorAll('.calendar-list .calendar-item').length;
 const message=`${month}. ${heading}: ${count} ${count===1?'programação':'programações'} na lista.`;
 announcedWorkflowNotice=message;
 workflowAnnouncer.textContent=message;
}
function syncRouteState() {
 const [route,id] = location.hash.replace(/^#\/?/, '').split('/');
 if(route==='profile' && id && members.some(member=>member.id===id)) currentMember=id;
}
// The route rerenders the entire DOM. Move focus to the destination for keyboard
// and screen-reader users instead of leaving it on the removed navigation button.
window.addEventListener('hashchange',()=>{
 // Browser Back can change the hash without passing through navigate().
 const previousRoute=lastRenderedHash.replace(/^#\/?/,'').split('/')[0];
 const leavingD3=previousRoute==='review'&&routeFromHash()!=='review'&&
  d3SingleExperiment&&Boolean(document.querySelector<HTMLDialogElement>('#d3-review-dialog')?.open);
 if(leavingD3&&!approvedD3ReviewDeparture&&!confirmD3ReviewDeparture()){
  history.replaceState(history.state,'',lastRenderedHash||'#/review');
  return;
 }
 approvedD3ReviewDeparture=false;
 const leavingEditor=previousRoute==='compose'&&routeFromHash()!=='compose';
 if(leavingEditor&&!approvedComposeDeparture&&!confirmComposeDeparture()){
  history.replaceState(history.state,'',lastRenderedHash||'#/compose');
  return;
 }
 approvedComposeDeparture=false;
 if(profileScheduleSheetOpen){
  if(!confirmScheduleDeparture()){
   history.replaceState(history.state,'',lastRenderedHash||'#/profile/m01');return;
  }
  profileScheduleSheetOpen=false;schedulePrefillProposalId=null;scheduleMethod=null;
 }
 const leavingSchedule=previousRoute==='calendar'&&routeFromHash()!=='calendar';
 if(leavingSchedule&&!approvedScheduleDeparture&&!confirmScheduleDeparture()){
  history.replaceState(history.state,'',lastRenderedHash||'#/calendar');
  if(menuOpen){menuOpen=false;render();}
  return;
 }
 approvedScheduleDeparture=false;
 if(routeFromHash()!=='calendar'){
  pendingScheduleCancellation=null;scheduleFormOpen=false;scheduleMethod=null;schedulePrefillProposalId=null;
 }
  menuOpen=false;demoToolsOpen=false;syncRouteState();render();
  if(leavingD3&&routeFromHash()==='compose'){
   // Return to the action that opened the confirmation from the editor.
   document.querySelector<HTMLButtonElement>('#compose-proposal-form [value="conclude"]')?.focus({preventScroll:true});
  }else if(routeFromHash()==='calendar'&&scheduleFormOpen&&schedulePrefillProposalId){
   // Focus the form introduction, not a preselected field in the middle.
   // Tabbing forward must reach title and objective before proposal/section.
   const formHeading=document.querySelector<HTMLElement>('#schedule-deliberation-form h2');
   if(formHeading){
    formHeading.tabIndex=-1;
    formHeading.focus({preventScroll:true});
    formHeading.scrollIntoView({block:'start',inline:'nearest'});
   }
  }else if(routeFromHash()==='calendar'&&pendingCalendarReturnId){
   const id=pendingCalendarReturnId;
   pendingCalendarReturnId=null;
   const source=[...document.querySelectorAll<HTMLButtonElement>('[data-schedule]')]
    .find(button=>button.dataset.schedule===id)
    ?? document.querySelector<HTMLButtonElement>('[data-action=toggle-cancelled-history]');
   (source??document.querySelector<HTMLElement>('#main-content'))?.focus({preventScroll:true});
   source?.scrollIntoView({block:'center',inline:'nearest'});
  }else if(routeFromHash()==='ballot'&&previewScheduleId){
   const title=document.querySelector<HTMLElement>('#preview-vote-title');
   if(title){title.tabIndex=-1;title.focus({preventScroll:true});title.scrollIntoView({block:'start'});}
  }else document.querySelector<HTMLElement>('#main-content')?.focus({preventScroll:true});
});
// Megalos' interaction: swipe the CONFFRATUS name upwards to reveal navigation.
// Keep the existing button as an accessible alternative.
document.addEventListener('touchstart', event => {
 const el = event.target;
 if(!(el instanceof Element) || !el.closest('.footer-home') || event.touches.length !== 1) return;
 const touch = event.touches[0];
 if(!touch) return;
 footerSwipeStart = {x:touch.clientX, y:touch.clientY};
}, {passive:true});
document.addEventListener('touchend', event => {
 if(!footerSwipeStart) return;
 const touch = event.changedTouches[0];
 if(!touch) {footerSwipeStart=null;return;}
 const dx = touch.clientX - footerSwipeStart.x;
 const dy = touch.clientY - footerSwipeStart.y;
 footerSwipeStart = null;
 if(Math.abs(dy)<38 || Math.abs(dy)<Math.abs(dx)*1.3) return;
 suppressFooterHomeClickUntil = Date.now() + 700;
 menuOpen = dy < 0;
 render();
}, {passive:true});
document.addEventListener('touchcancel', () => {footerSwipeStart=null;}, {passive:true});
// Capture Escape before the browser's implicit dialog dismissal. Avoid an
// unguarded close while the user has unconfirmed review choices.
document.addEventListener('keydown', event => {
 if(!d3SingleExperiment)return;
 const dialog=document.querySelector<HTMLDialogElement>('#d3-review-dialog');
 if(!dialog?.open)return;
 if(event.key==='Tab'){
  // Chromium can temporarily focus <body> when Tab wraps in a native
  // dialog. Explicitly wrap between visible descendants, without ever
  // permitting focus on the inert underlying page.
  const controls=[...dialog.querySelectorAll<HTMLElement>(
   'button:not([disabled]),select:not([disabled]),input:not([disabled]),textarea:not([disabled]),a[href],[tabindex]:not([tabindex="-1"])'
  )].filter(el=>el.tabIndex>=0&&el.getClientRects().length>0);
  const index=controls.indexOf(document.activeElement as HTMLElement);
  if(controls.length&&(event.shiftKey?(index<=0):(index===controls.length-1||index<0))){
   event.preventDefault();event.stopPropagation();
   (event.shiftKey?controls[controls.length-1]:controls[0])?.focus({preventScroll:true});
  }
  return;
 }
 if(event.key!=='Escape')return;
 event.preventDefault();event.stopImmediatePropagation();
 dismissD3Review();
},true);
document.addEventListener('keydown', event => {
 if(event.key==='Escape') {
  if(demoToolsOpen){demoToolsOpen=false;render();document.querySelector<HTMLButtonElement>('[data-action=toggle-tools]')?.focus();}
  else if(menuOpen){menuOpen=false;render();document.querySelector<HTMLButtonElement>('.footer-nav')?.focus();}
  else if(editingMemberId){
   const previousId=editingMemberId;
   editingMemberId=null;render();
   const editTrigger=[...document.querySelectorAll<HTMLButtonElement>('[data-edit]')]
    .find(button=>button.dataset.edit===previousId);
   (editTrigger ?? document.querySelector<HTMLButtonElement>('[data-section][aria-expanded=true]'))?.focus();
  }
  else if(pendingScheduleCancellation && routeFromHash()==='calendar'){
   const cancellingId=pendingScheduleCancellation;
   pendingScheduleCancellation=null;render();
   const restored=[...document.querySelectorAll<HTMLButtonElement>('[data-cancel-schedule]')]
    .find(button=>button.dataset.cancelSchedule===cancellingId);
   restored?.focus();
   restored?.scrollIntoView({block:'center',inline:'nearest'});
  }
  else if(searchExpanded && routeFromHash()==='members'){
   searchExpanded=false;filter='';render();document.querySelector<HTMLButtonElement>('[data-action=search]')?.focus();
  }
 }
});
document.addEventListener('click',(event)=>{
 const target=event.target;
 if (!(target instanceof Element)) return;
 const d3Dismiss=target.closest<HTMLElement>('[data-dismiss-d3-review]');
 if(d3Dismiss&&d3SingleExperiment){dismissD3Review();return;}
 const skip=target.closest<HTMLAnchorElement>('.skip-link');
 if(skip){event.preventDefault();document.querySelector<HTMLElement>('#main-content')?.focus({preventScroll:true});return;}
 const contextualVote=target.closest<HTMLElement>('[data-preview-schedule]');
 if(contextualVote?.dataset.previewSchedule){
  const item=schedule.find(s=>s.id===contextualVote.dataset.previewSchedule&&s.status==='programada');
  if(item?.method && (item.method==='binaria'||isValidPreviewChoices(item.choices))){
   previewHomeBallot=false;
   previewClosedScheduleNotice='';
   previewScheduleId=item.id;previewMode=item.method;previewRequestId=null;previewVoteReceipt=null;previewVoteMemberId='';previewVoteError='';previewVoteDraft=null;votingFormsOpen=true;
   navigate('ballot');document.querySelector<HTMLElement>('#preview-vote-title')?.scrollIntoView({block:'center'});
  }return;
 }
 // Links inside the editor remain editable text; never navigate by clicking them.
 const editorLink=target.closest<HTMLAnchorElement>('#draft-rich-body a');
 if(editorLink){event.preventDefault();return;}
 const linkButton=target.closest<HTMLButtonElement>('[data-rich-link]');
 if(linkButton){
  const editor=document.querySelector<HTMLElement>('#draft-rich-body');
  const input=document.querySelector<HTMLInputElement>('#draft-link-url');
  const status=document.querySelector<HTMLElement>('#draft-link-feedback');
  const selected=lastRichSelection;
  const action=linkButton.dataset.richLink;
  const validRange=Boolean(editor&&selected&&!selected.collapsed&&
   editor.contains(selected.startContainer)&&editor.contains(selected.endContainer));
  if(!validRange){
   if(status)status.textContent='Selecione um trecho da redação antes de alterar um link.';
   editor?.focus({preventScroll:true});
   return;
  }
  const href=action==='apply'?normalizeHttpHref(input?.value.trim()):undefined;
  if(action==='apply'&&!href){
   if(status)status.textContent='Informe uma URL completa iniciada por https:// ou http://, sem credenciais.';
   input?.setAttribute('aria-invalid','true');
   input?.focus({preventScroll:true});
   return;
  }
  editor!.focus({preventScroll:true});
  const selection=window.getSelection();
  selection?.removeAllRanges();
  selection?.addRange(selected!.cloneRange());
  const previousBody=draftForm.body;
  const previousRuns=JSON.stringify(draftForm.bodyRuns??[]);
  document.execCommand(action==='remove'?'unlink':'createLink',false,href??'');
  syncRichEditor();
  const metadataChanged=draftForm.body===previousBody&&
   JSON.stringify(draftForm.bodyRuns??[])!==previousRuns;
  const changed=action==='apply'
   ? metadataChanged&&Boolean(draftForm.bodyRuns?.some(run=>run.href===href))
   : metadataChanged;
  if(changed){
   input?.removeAttribute('aria-invalid');
   if(input&&action==='apply')input.value='';
   if(status)status.textContent=action==='apply'?'Link inserido no trecho selecionado.':'Link removido do trecho selecionado.';
  }else if(status)status.textContent='Não foi possível alterar o link dessa seleção.';
  return;
 }
 const richCommand=target.closest<HTMLButtonElement>('[data-rich-command]');
 if(richCommand){
  const editor=document.querySelector<HTMLElement>('#draft-rich-body');
  const command=richCommand.dataset.richCommand;
  if(editor&&['bold','italic','underline','strike','subscript','superscript'].includes(command??'')){
   editor.focus({preventScroll:true});
   if(lastRichSelection&&editor.contains(lastRichSelection.commonAncestorContainer)){
    const selection=window.getSelection();
    selection?.removeAllRanges();selection?.addRange(lastRichSelection);
   }
   document.execCommand(command==='strike'?'strikeThrough':command!,false);
   syncRichEditor();
  }
  return;
 }
 const actionEl=target.closest<HTMLElement>('[data-action]');
 const routeEl=target.closest<HTMLElement>('[data-route]');
 const memberEl=target.closest<HTMLElement>('[data-member]');
 const tabEl=target.closest<HTMLElement>('[data-tab], [data-overview-tab]');
 const sectionEl=target.closest<HTMLElement>('[data-section]');
 const editEl=target.closest<HTMLElement>('[data-edit]');
 const demoteEl=target.closest<HTMLElement>('[data-demote]');
 const activityEl=target.closest<HTMLElement>('[data-activity]');
 const voteEl=target.closest<HTMLElement>('[data-vote]');
 if(voteEl?.dataset.vote && demoBallot && canRecordVote(demoBallot) && demoBallot.options.some(o=>o.id===voteEl.dataset.vote)){demoVoteId=voteEl.dataset.vote;try{sessionStorage.setItem('conferatus:demo-vote',demoVoteId);}catch{}render();return;}
 if((advancedPreview||votingFormsOpen||previewScheduleId!==null) && actionEl?.dataset.action==='exit-preview-schedule'){
  const returnId=!advancedPreview?previewScheduleId:null;
  const source=schedule.find(item=>item.id===returnId);
  previewHomeBallot=false;
  previewClosedScheduleNotice='';
  if(!advancedPreview)votingFormsOpen=false;
  previewVoteDraft=null;previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';previewVoteMemberId='';
  if(returnId){
   pendingCalendarReturnId=returnId;
   expandedSchedule=returnId;
   selectedCalendarDay='';
   if(source){
    const day=new Date(source.start.slice(0,10)+'T12:00:00');
    calendarYear=day.getFullYear();calendarMonth=day.getMonth();
    if(source.status==='cancelada')cancelledHistoryOpen=true;
   }
   navigate('calendar');
   return;
  }
  render();
  document.querySelector<HTMLElement>(advancedPreview?'#preview-vote-method':'[data-action=enter-ballot]')?.focus({preventScroll:true});
  return;
 }
 if((advancedPreview||votingFormsOpen) && actionEl?.dataset.action==='clear-preview-samples'){
  const scope=previewSampleScope();
  if(!window.confirm('Limpar apenas as amostras desta simulação?'))return;
  previewSampleLedger.clear(scope);
  previewVoteDraft=null;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';render();
  document.querySelector<HTMLElement>('#preview-vote-form')?.querySelector<HTMLElement>('input,select')?.focus({preventScroll:true});return;
 }
 if((advancedPreview||votingFormsOpen) && actionEl?.dataset.action==='reset-preview-vote'){
  if(!advancedPreview)previewSampleLedger.clear(previewSampleScope());
  previewVoteDraft=null;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';render();
  const method=document.querySelector<HTMLSelectElement>('#preview-vote-method');
  const firstChoice=document.querySelector<HTMLElement>('#preview-vote-form input:not(:disabled), #preview-vote-form select:not(:disabled)');
  (method&&!method.disabled?method:firstChoice)?.focus({preventScroll:true});
  return;
 }
 if(actionEl?.dataset.action==='undo'&&lastChange){
  const member=members.find(m=>m.id===lastChange?.memberId);
  if(member){member.acdmId=lastChange.acdmId;member.sectionIds=[...lastChange.sectionIds];member.role=lastChange.role;member.hadDeliberativeHistory=lastChange.hadDeliberativeHistory;member.cumulativeVoteWeight=lastChange.cumulativeVoteWeight;saveDemoMembers();}
  const affectedId=lastChange.memberId;
  lastChange=null;notice='Alteração desfeita.';render();
  // Undo removes its own button: return focus to the affected member's editor.
  ([...document.querySelectorAll<HTMLButtonElement>('[data-edit]')].find(el=>el.dataset.edit===affectedId)
   ?? document.querySelector<HTMLButtonElement>('[data-section][aria-expanded=true]'))?.focus({preventScroll:true});
  return;
 }
 if(advancedPreview && actionEl?.dataset.action==='toggle-tools'){demoToolsOpen=!demoToolsOpen;render();document.querySelector<HTMLButtonElement>('[data-action=toggle-tools]')?.focus();return;}
 if(advancedPreview && actionEl?.dataset.action==='reset-admin'){
  for(const member of members){const original=initialMembers.get(member.id);if(original){member.name=original.name;member.acdmId=original.acdmId;member.sectionIds=[...original.sectionIds];member.role=original.role;member.hadDeliberativeHistory=original.hadDeliberativeHistory;member.cumulativeVoteWeight=original.cumulativeVoteWeight;}}
  previewVoteReceipt=null;previewVoteMemberId='';
  editingMemberId=null;lastChange=null;notice='Alterações restauradas.';rolePreview='diretor';demoToolsOpen=false;try{sessionStorage.removeItem(demoMembersKey);}catch{}
  render();document.querySelector<HTMLButtonElement>('[data-action=toggle-tools]')?.focus({preventScroll:true});
  return;
 }
 if(actionEl?.dataset.action==='show-more-members'){
  directoryExpanded=true;render();
  document.querySelectorAll<HTMLButtonElement>('.member-item')[7]?.focus({preventScroll:true});
  return;
 }
 if(actionEl?.dataset.action==='show-more-history'){
  overviewExpanded=true;render();
  // The show-more button disappears; announce the first newly revealed article.
  const firstRevealed=document.querySelectorAll<HTMLElement>('.overview-content .activity')[6];
  if(firstRevealed){firstRevealed.tabIndex=-1;firstRevealed.focus({preventScroll:true});}
  return;
 }
 if(actionEl?.dataset.action==='search'){searchExpanded=!searchExpanded;if(!searchExpanded)filter='';render();if(searchExpanded)document.querySelector<HTMLInputElement>('#search-members')?.focus();return;}
 if(actionEl?.dataset.action==='clear-search'){filter='';render();document.querySelector<HTMLInputElement>('#search-members')?.focus();return;}
 if(actionEl?.dataset.action==='toggle-voting-forms'&&!advancedPreview){
  votingFormsOpen=!votingFormsOpen;
  render();
  const focusTarget=document.querySelector<HTMLElement>(votingFormsOpen?'#preview-vote-method':'[data-action="toggle-voting-forms"]');
  focusTarget?.focus({preventScroll:true});
  if(votingFormsOpen)focusTarget?.scrollIntoView({block:'center'});
  return;
 }
 if(actionEl?.dataset.action==='enter-ballot'&&!advancedPreview&&demoBallot&&canRecordVote(demoBallot)){
  previewHomeBallot=true;previewClosedScheduleNotice='';previewScheduleId=null;previewMode='nominal';
  previewVoteDraft=null;previewVoteReceipt=null;previewVoteError='';previewRequestId=null;
  votingFormsOpen=true;render();
  document.querySelector<HTMLInputElement>('#preview-vote-form input:not(:disabled)')?.focus({preventScroll:true});
  document.querySelector<HTMLElement>('#preview-vote-title')?.scrollIntoView({block:'center'});
  return;
 }
 if(actionEl?.dataset.action==='toggle-demo'){demoExpanded=!demoExpanded;render();return;}
 if(actionEl?.dataset.action==='reset-vote'){
  demoVoteId=null;try{sessionStorage.removeItem('conferatus:demo-vote');}catch{}
  render();document.querySelector<HTMLButtonElement>('[data-vote]')?.focus({preventScroll:true});
  return;
 }
 if (actionEl?.dataset.action==='menu') {menuOpen=!menuOpen; render(); (menuOpen?document.querySelector<HTMLButtonElement>('.menu-item'):document.querySelector<HTMLButtonElement>('.footer-nav'))?.focus(); return;}
 if (routeEl?.classList.contains('footer-home') && Date.now() < suppressFooterHomeClickUntil) {return;}

 {const partnerEl=target.closest<HTMLElement>('[data-confirm-partner]');
  if(partnerEl?.dataset.confirmPartner){const [draftId,partnerId]=partnerEl.dataset.confirmPartner.split(':');const d=drafts.find(d=>d.id===draftId);const partner=d?.partners.find(p=>p.id===partnerId);if(d&&partner){partner.complete=true;d.status=draftReady(d)?'concluida':'revisao';
   const saved=saveWorkflows();
   workflowNotice=saved?(d.status==='concluida'?'Todas as partes concluíram. Proposição concluída.':'Etapa do Socii registrada nesta prévia.'):'Conclusão aplicada somente nesta aba: não foi possível salvar.';
   render();
   // The confirmation button disappears on completion. Keep keyboard focus
   // within this proposal: next pending participant, then scheduling/review.
   const updatedRecord=[...document.querySelectorAll<HTMLElement>('.workflow-record')]
    .find(record=>record.querySelector<HTMLButtonElement>('[data-draft]')?.dataset.draft===draftId);
   const nextAction=updatedRecord?.querySelector<HTMLButtonElement>('[data-confirm-partner]')
    ?? updatedRecord?.querySelector<HTMLButtonElement>('[data-schedule-draft]')
    ?? updatedRecord?.querySelector<HTMLButtonElement>('[data-draft]');
   nextAction?.focus({preventScroll:true});
  }return;}}
 if(advancedPreview && actionEl?.dataset.action==='export-local-archive'){
  try{
   const data=exportWorkflowArchive(drafts.map(cleanDraftRecord),schedule.map(cleanScheduleRecord));
   if(new TextEncoder().encode(data).length>WORKFLOW_ARCHIVE_MAX_BYTES)throw new Error('Archive too large');
   const blob=new Blob([data],{type:'application/json;charset=utf-8'});
   const url=URL.createObjectURL(blob);
   const anchor=document.createElement('a');anchor.href=url;
   anchor.download=`conffratus-previa-${new Date().toISOString().slice(0,10)}.json`;
   document.body.append(anchor);anchor.click();anchor.remove();
   // Revoke on the next user turn, not synchronously during the click.
   window.setTimeout(()=>URL.revokeObjectURL(url),1000);
   archiveMessage='Cópia gerada neste dispositivo. Guarde o arquivo em local seguro.';
   archiveIsError=false;
  }catch{archiveMessage='Não foi possível gerar a cópia nesta sessão.';archiveIsError=true;}
  render();return;
 }
 if(advancedPreview && actionEl?.dataset.action==='import-local-archive'){
  document.querySelector<HTMLInputElement>('#archive-file-input')?.click();return;
 }
 if(actionEl?.dataset.action==='enable-rich-editor'){
  const title=document.querySelector<HTMLInputElement>('#draft-title');
  const body=document.querySelector<HTMLTextAreaElement>('#draft-body');
  draftForm={title:title?.value??draftForm.title,body:body?.value??draftForm.body,bodyRuns:draftForm.bodyRuns,bodyLayout:draftForm.bodyLayout};
  richEditorOpen=true;lastRichSelection=null;render();
  document.querySelector<HTMLElement>('#draft-rich-body')?.focus({preventScroll:true});
  return;
 }
 if(actionEl?.dataset.action==='invite-socii-from-profile'){inviteOpen=true;navigate('proposals');return;}
 if(actionEl?.dataset.action==='new-proposal'){finishedProposalReturnTo=routeFromHash()==='profile'?'profile':'proposals';currentDraftId='';draftForm=blankDraft();richEditorOpen=false;lastRichSelection=null;workflowNotice='';composeError='';navigate('compose');return;}
 if(actionEl?.dataset.action==='invite-socii'){inviteOpen=!inviteOpen;render();return;}
 const fromProposal=target.closest<HTMLElement>('[data-schedule-draft]');
 if(fromProposal?.dataset.scheduleDraft){
  const proposal=drafts.find(d=>d.id===fromProposal.dataset.scheduleDraft&&d.status==='concluida');
  if(!proposal)return;
  schedulePrefillProposalId=proposal.id;
  if(profileSheetExperiment&&routeFromHash()==='profile'){
   profileScheduleSheetOpen=true;scheduleMethod=null;workflowNotice='';render();return;
  }
  scheduleFormOpen=true;
  scheduleMethod=null;
  selectedCalendarDay='';
  pendingScheduleCancellation=null;
  navigate('calendar');
  return;
 }
 const dismissSheet=target.closest<HTMLElement>('[data-dismiss-schedule-sheet]');
 if(dismissSheet&&profileScheduleSheetOpen){dismissProfileScheduleSheet();return;}
 if(actionEl?.dataset.action==='open-schedule'){
  if(scheduleFormOpen&&!confirmScheduleDeparture())return;
  schedulePrefillProposalId=null;
  pendingScheduleCancellation=null;
  scheduleFormOpen=!scheduleFormOpen;
  scheduleMethod=null;
  if(!cancellationSaveFailed)workflowNotice='';
  render();return;
 }
 if(actionEl?.dataset.action==='toggle-cancelled-history'){cancelledHistoryOpen=!cancelledHistoryOpen;render();return;}
 if(actionEl?.dataset.action==='retry-workflow-save' && workflowSaveFailed){
  const saved=saveWorkflows();
  workflowNotice=saved?'Alterações salvas nesta sessão.':workflowSaveWarning;
  render();
  (saved?document.querySelector<HTMLElement>('#main-content'):document.querySelector<HTMLButtonElement>('[data-action="retry-workflow-save"]'))?.focus({preventScroll:true});
  return;
 }
 if(actionEl?.dataset.action==='retry-cancellation-save' && cancellationSaveFailed){
  const saved=saveWorkflows();
  workflowNotice=saved?'Cancelamento salvo nesta sessão.':cancellationSaveWarning;
  render();
  (saved?document.querySelector<HTMLElement>('[data-action=toggle-cancelled-history]'):document.querySelector<HTMLElement>('[data-action=retry-cancellation-save]'))?.focus({preventScroll:true});
  return;
 }
 if(actionEl?.dataset.action==='calendar-prev'){pendingScheduleCancellation=null;calendarShift(-1);render();announceCalendarView();return;}
 if(actionEl?.dataset.action==='calendar-next'){pendingScheduleCancellation=null;calendarShift(1);render();announceCalendarView();return;}
 if(actionEl?.dataset.action==='calendar-today'){pendingScheduleCancellation=null;const currentDay=new Date();calendarYear=currentDay.getFullYear();calendarMonth=currentDay.getMonth();selectedCalendarDay=isoDay(currentDay);render();announceCalendarView();return;}
 if(actionEl?.dataset.action==='calendar-all'){
  pendingScheduleCancellation=null;selectedCalendarDay='';render();announceCalendarView();
  const heading=document.querySelector<HTMLElement>('.calendar-list-head h2');
  if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}
  return;
 }
 const dayEl=target.closest<HTMLElement>('[data-calendar-day]');
 if(dayEl?.dataset.calendarDay){pendingScheduleCancellation=null;selectedCalendarDay=selectedCalendarDay===dayEl.dataset.calendarDay?'':dayEl.dataset.calendarDay;render();announceCalendarView();return;}
 const linkedScheduleEl=target.closest<HTMLElement>('[data-linked-schedule]');
 if(linkedScheduleEl?.dataset.linkedSchedule){
  const linked=schedule.find(item=>item.id===linkedScheduleEl.dataset.linkedSchedule&&item.status==='programada'&&drafts.some(d=>d.id===item.proposalId));
  if(linked){
   const day=new Date(`${linked.start.slice(0,10)}T12:00:00`);
   calendarYear=day.getFullYear();calendarMonth=day.getMonth();
   selectedCalendarDay=linked.start.slice(0,10);expandedSchedule=linked.id;
   navigate('calendar');
  }
  return;
 }
 if(target.closest('[data-open-proposal-author]')){
  const author=members[0];
  if(author){currentMember=author.id;profileTab='proposicoes';navigate('profile',author.id);}
  return;
 }
 const draftEl=target.closest<HTMLElement>('[data-draft]');
 if(draftEl?.dataset.draft){const d=drafts.find(x=>x.id===draftEl.dataset.draft);if(d){currentDraftId=d.id;finishedProposalReturnTo=routeFromHash()==='overview'?'overview':routeFromHash()==='profile'?'profile':'proposals';draftForm={title:d.title,body:d.body,bodyRuns:d.bodyRuns,bodyLayout:d.bodyLayout};richEditorOpen=hasFormatting(d.bodyRuns)||Boolean(d.bodyLayout);lastRichSelection=null;composeError='';navigate(d.status==='redacao'?'compose':'review');}return;}
 const scheduleEl=target.closest<HTMLElement>('[data-schedule]');
 if(scheduleEl?.dataset.schedule){pendingScheduleCancellation=null;expandedSchedule=expandedSchedule===scheduleEl.dataset.schedule?'':scheduleEl.dataset.schedule;render();return;}
 const proposalEl=target.closest<HTMLElement>('[data-open-schedule-proposal]');
 if(proposalEl?.dataset.openScheduleProposal){
  const d=drafts.find(x=>x.id===proposalEl.dataset.openScheduleProposal);
  if(d){currentDraftId=d.id;finishedProposalReturnTo='calendar';draftForm={title:d.title,body:d.body,bodyRuns:d.bodyRuns,bodyLayout:d.bodyLayout};navigate('review');}
  return;
 }
 const cancelEl=target.closest<HTMLElement>('[data-cancel-schedule]');
 if(cancelEl?.dataset.cancelSchedule){
  const item=schedule.find(x=>x.id===cancelEl.dataset.cancelSchedule&&x.status==='programada');
  if(item){
   pendingScheduleCancellation=pendingScheduleCancellation===item.id?null:item.id;
   render();
   const focusTarget=pendingScheduleCancellation
    ? document.querySelector<HTMLElement>('.calendar-cancel-confirm')
    : [...document.querySelectorAll<HTMLButtonElement>('[data-cancel-schedule]')].find(button=>button.dataset.cancelSchedule===item.id);
   focusTarget?.focus();
   focusTarget?.scrollIntoView({block:'center',inline:'nearest'});
  }
  return;
 }
 const keepScheduleEl=target.closest<HTMLElement>('[data-keep-schedule]');
 if(keepScheduleEl?.dataset.keepSchedule){
  const keptId=keepScheduleEl.dataset.keepSchedule;
  pendingScheduleCancellation=null;render();
  const restored=[...document.querySelectorAll<HTMLButtonElement>('[data-cancel-schedule]')]
   .find(button=>button.dataset.cancelSchedule===keptId);
  restored?.focus();
  restored?.scrollIntoView({block:'center',inline:'nearest'});
  return;
 }
 const confirmScheduleEl=target.closest<HTMLElement>('[data-confirm-cancel-schedule]');
 if(confirmScheduleEl?.dataset.confirmCancelSchedule){
  const item=schedule.find(x=>x.id===confirmScheduleEl.dataset.confirmCancelSchedule&&x.status==='programada');
  if(item && pendingScheduleCancellation===item.id){
   pendingScheduleCancellation=null;
   item.status='cancelada';
   // A cancelled schedule must not leave a vote sandbox bound to its old alternatives.
   previewSampleLedger.clear(`schedule:${item.id}`);
   previewVoteDraft=null;
   if(previewScheduleId===item.id){
    // Retain context for the cancelled-state page on a later return.
    votingFormsOpen=false;
    previewClosedScheduleNotice='Esta programação foi cancelada. A votação não está mais disponível.';previewRequestId=null;previewVoteReceipt=null;
    previewVoteError='';previewVoteMemberId='';
   }
   const saved=saveWorkflows();cancellationSaveFailed=!saved;
   workflowNotice=saved?'Programação cancelada e salva nesta sessão.':cancellationSaveWarning;
   render();
   const heading=document.querySelector<HTMLElement>('.calendar-list-head h2');
   if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}
  }
  return;
 }
 if (routeEl?.dataset.route) {
  if (routeEl.dataset.route==='profile') {
   const returningToAuthor = finishedProposalReturnTo==='profile' &&
    ['compose','review'].includes(routeFromHash());
   profileTab=returningToAuthor?'proposicoes':'votos';
   navigate('profile',members[0]?.id);
  } else navigate(routeEl.dataset.route as Route);
  return;
 }
 if (memberEl?.dataset.member) {currentMember=memberEl.dataset.member;profileTab='votos';navigate('profile', currentMember);return;}
 if (tabEl) {if (tabEl.dataset.overviewTab){overviewTab=tabEl.dataset.overviewTab as Tab;overviewExpanded=false;expandedActivity='';} else profileTab=tabEl.dataset.tab as Tab; if(routeFromHash()==='members'){currentMember=members[0]?.id??'m01';navigate('profile', currentMember);}else{render();}return;}
 if (sectionEl?.dataset.section) {expandedSection=expandedSection===sectionEl.dataset.section?'':sectionEl.dataset.section;editingMemberId=null;editError='';notice='';lastChange=null;demoToolsOpen=false;render();return;}
 if (editEl?.dataset.edit) {editingMemberId=editingMemberId===editEl.dataset.edit?null:editEl.dataset.edit;editError='';editErrorField='acdmId';render();if(editingMemberId)document.querySelector<HTMLInputElement>('#member-acdm-id')?.focus();return;}
 if (demoteEl?.dataset.demote) {
  const m=members.find(x=>x.id===demoteEl.dataset.demote);
  if (m&&expandedSection && expandedSection!=='membros' && m.sectionIds.includes(expandedSection)) {
   rememberChange(m);
   const result=demoteToCommonMember(m);
   m.sectionIds=result.member.sectionIds;
   m.role=result.member.role;
   m.hadDeliberativeHistory=result.member.hadDeliberativeHistory;
   saveDemoMembers();
   notice=`${m.name} passou a membro comum. O histórico foi preservado.`;
   editingMemberId=null;editError='';render();
   document.querySelector<HTMLButtonElement>('[data-action=undo]')?.focus({preventScroll:true});
  }
  return;
 }
 if (activityEl?.dataset.activity) {expandedActivity=expandedActivity===activityEl.dataset.activity?'':activityEl.dataset.activity;render();return;}
 if(advancedPreview && actionEl?.dataset.action==='add-member'&&expandedSection) {
  const select=document.querySelector<HTMLSelectElement>('#add-member');
  const member=members.find(m=>m.id===select?.value);
  if(member){
   const rawWeight=document.querySelector<HTMLInputElement>('#link-cumulative-weight')?.value.trim()??'';
   const newWeight=rawWeight===''?undefined:Number(rawWeight);
   if(rawWeight!==''&&!isPositiveCumulativeVoteWeight(newWeight)){
    notice='A proporção cumulativa deve ser uma quantidade inteira positiva.';render();return;
   }
   rememberChange(member);member.sectionIds=updateSectionAssignment(member,expandedSection,true).member.sectionIds;
   if(newWeight!==undefined)member.cumulativeVoteWeight=newWeight;
   saveDemoMembers();notice=`${member.name} adicionado à seção.`;demoToolsOpen=false;render();
   document.querySelector<HTMLButtonElement>('[data-action=toggle-tools]')?.focus({preventScroll:true});
  }
 }
});

// Associate custom scheduling errors with their field as well as announcing them.
function showScheduleFormError(form: HTMLFormElement,message:string,fieldName:string) {
 const old=form.querySelector<HTMLElement>('#schedule-form-error');
 if(old)old.textContent=message;
 else form.insertAdjacentHTML('afterbegin',`<p id="schedule-form-error" class="workflow-form-error" role="alert">${escapeHTML(message)}</p>`);
 const field=form.elements.namedItem(fieldName);
 if(field instanceof HTMLInputElement || field instanceof HTMLSelectElement || field instanceof HTMLTextAreaElement){
  field.setAttribute('aria-invalid','true');
  field.setAttribute('aria-describedby','schedule-form-error');
  field.focus({preventScroll:true});
 }
}
// Restoring a downloaded archive is explicit, validated and all-or-nothing
// for the two session workflow keys. It does not import demo votes or members.
document.addEventListener('change',async event=>{
 const field=event.target;
 if(field instanceof HTMLElement && field.closest('#schedule-deliberation-form'))refreshComposerUnloadGuard();
 if(field instanceof HTMLElement && field.closest('#d3-review-dialog'))refreshComposerUnloadGuard();
 if(!advancedPreview || !(field instanceof HTMLInputElement) || field.id!=='archive-file-input')return;
 const file=field.files?.[0];if(!file)return;
 const report=(text:string,error=true)=>{
  archiveMessage=text;archiveIsError=error;render();
  document.querySelector<HTMLButtonElement>('[data-action="import-local-archive"]')?.focus({preventScroll:true});
 };
 if(file.size>WORKFLOW_ARCHIVE_MAX_BYTES){report('O arquivo excede o limite de 2 MB.');return;}
 let text:string;
 try{text=await file.text();}catch{report('Não foi possível ler o arquivo selecionado.');return;}
 const parsed=parseWorkflowArchive(text);
 if(!parsed.ok){report(parsed.error);return;}
 const items=uniqueSavedRecords(parsed.archive.drafts,isSavedLocalDraft);
 const validatedDrafts=items.accepted.map(cleanDraftRecord);
 const appointments=uniqueSavedRecords(parsed.archive.schedule,(value):value is Deliberation=>isRestorableLocalSchedule(value,validatedDrafts));
 if(items.rejected.length||appointments.rejected.length){
  report('A cópia contém registros inválidos ou IDs repetidos. Nada foi substituído.');return;
 }
 if(workflowSaveFailed||cancellationSaveFailed){
  report('Há alterações ainda não salvas nesta aba. Salve-as antes de restaurar outra cópia.');return;
 }
 if(!window.confirm(`Restaurar ${items.accepted.length} proposição(ões) e ${appointments.accepted.length} programação(ões)? Isso substituirá os registros locais atuais. Guarde uma cópia deles antes de continuar.`))return;
 const previousDrafts=[...drafts],previousSchedule=[...schedule];
 drafts.splice(0,drafts.length,...validatedDrafts);
 schedule.splice(0,schedule.length,...appointments.accepted.map(cleanScheduleRecord));
 if(!saveWorkflows()){
  drafts.splice(0,drafts.length,...previousDrafts);
  schedule.splice(0,schedule.length,...previousSchedule);
  workflowSaveFailed=false;
  report('Não foi possível salvar a cópia restaurada. Os registros anteriores permanecem nesta aba.');
  return;
 }
 // Imported workflows replace the old sandbox contexts. Never reuse stale receipts or samples.
 previewSampleLedger.clearAll();
 previewVoteDraft=null;previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;
 previewVoteError='';previewVoteMemberId='';
 currentDraftId='';draftForm=blankDraft();richEditorOpen=false;lastRichSelection=null;inviteOpen=false;expandedSchedule='';
 archiveMessage=`Cópia restaurada nesta sessão: ${drafts.length} proposição(ões) e ${schedule.length} programação(ões).`;
 archiveIsError=false;render();
 document.querySelector<HTMLButtonElement>('[data-action="import-local-archive"]')?.focus({preventScroll:true});
});
// Some Chromium versions may finish a native Escape close despite a nested
// window.confirm in 'cancel'. Intercept the key request before its default action.
// closedby=none also blocks implicit close requests in browsers that support it.
document.addEventListener('keydown',event=>{
 if(event.key!=='Escape'||!profileScheduleSheetOpen)return;
 const dialog=document.querySelector<HTMLDialogElement>('#profile-schedule-dialog');
 if(!dialog?.open)return;
 event.preventDefault();
 event.stopPropagation();
 dismissProfileScheduleSheet();
},true);
document.addEventListener('cancel',event=>{
 const dialog=event.target;
 if(!(dialog instanceof HTMLDialogElement))return;
 if(dialog.id==='d3-review-dialog'&&d3SingleExperiment){
  event.preventDefault();dismissD3Review();return;
 }
 if(dialog.id!=='profile-schedule-dialog')return;
 event.preventDefault();
 dismissProfileScheduleSheet();
},true);
document.addEventListener('submit',(event)=>{
 const form=event.target;if(!(form instanceof HTMLFormElement))return;
 const id=form.id;
 if(!['compose-proposal-form','confirm-proposal-form','schedule-deliberation-form','invite-socii-form'].includes(id))return;
 event.preventDefault();
 const submitter=(event as SubmitEvent).submitter;
 const saveOnly=id==='compose-proposal-form' && submitter instanceof HTMLButtonElement && submitter.value==='save';
 if(id==='compose-proposal-form'&&richEditorOpen)syncRichEditor();
 if(!saveOnly && id!=='compose-proposal-form' && !form.reportValidity())return;
 const data=new FormData(form);
 if(id==='compose-proposal-form'){
  const title=String(data.get('title')??'').trim(),body=String(data.get('body')??'').trim();
  const bodyRuns=richEditorOpen&&hasFormatting(draftForm.bodyRuns)?draftForm.bodyRuns:undefined;
  const bodyLayout=richEditorOpen&&isRichLayout(draftForm.bodyLayout)?draftForm.bodyLayout:undefined;
  // A short trimmed title previously failed silently. Validate both editor
  // modes consistently, while still allowing incomplete drafts to be saved.
  const titleInvalid=!saveOnly&&title.length<3;
  const bodyInvalid=!saveOnly&&body.length<20;
  if((saveOnly&&!title&&!body)||titleInvalid||bodyInvalid){
   composeError=saveOnly?'Escreva um título ou algum texto antes de salvar.'
    :titleInvalid?'Informe um título com pelo menos 3 caracteres.'
    :'Escreva pelo menos 20 caracteres na redação.';
   composeErrorField=bodyInvalid&&!titleInvalid?'body':'title';
   draftForm={title,body,bodyRuns,bodyLayout};
   render();
   const selector=composeErrorField==='title'?'#draft-title'
    :richEditorOpen?'#draft-rich-body':'#draft-body';
   document.querySelector<HTMLElement>(selector)?.focus({preventScroll:true});
   return;
  }
  composeError='';
  draftForm={title,body,bodyRuns,bodyLayout};
  let d=drafts.find(x=>x.id===currentDraftId);
  let confirmationsReset=false;
  if(!d||d.status==='concluida'){
   d={id:nextLocalRecordId('draft',drafts),title,body,...(bodyRuns?{bodyRuns}:{}),...(bodyLayout?{bodyLayout}:{}),sectionId:'integridade',type:'PDR',authorComplete:false,partners:[],status:'redacao'};drafts.unshift(d);currentDraftId=d.id;
  }else{
   // A confirmation of an earlier text cannot approve a changed version.
   if(d.title!==title||d.body!==body||JSON.stringify(d.bodyRuns??[])!==JSON.stringify(bodyRuns??[])||JSON.stringify(d.bodyLayout??null)!==JSON.stringify(bodyLayout??null)){
    confirmationsReset=d.authorComplete||d.partners.some(p=>p.complete);
    d.authorComplete=false;
    d.partners.forEach(p=>{p.complete=false;});
    d.status='redacao';
   }
   d.title=title;d.body=body;
   if(bodyRuns)d.bodyRuns=bodyRuns;
   else delete d.bodyRuns;
   if(bodyLayout)d.bodyLayout=bodyLayout;
   else delete d.bodyLayout;
  }
  const stored=saveWorkflows();
  if(saveOnly){
   workflowNotice=stored?'Rascunho salvo. Disponível somente nesta aba do navegador.':'Rascunho mantido somente enquanto a página estiver aberta.';
   if(confirmationsReset)workflowNotice+=' O texto mudou; as confirmações anteriores foram reiniciadas.';
   navigate('proposals');
  }
  else navigate('review');
  return;
 }
 if(id==='confirm-proposal-form'){
  const d=drafts.find(x=>x.id===currentDraftId);if(!d)return;
  const sectionId=String(data.get('sectionId')??'integridade');
  const proposalType=String(data.get('type')??'PDR') as ProposalType;
  const classificationChanged=d.sectionId!==sectionId||d.type!==proposalType;
  // A Socii signoff cannot approve a different section or type of proposal.
  if(classificationChanged)d.partners.forEach(p=>{p.complete=false;});
  d.sectionId=sectionId;d.type=proposalType;
  d.authorComplete=true;d.status=draftReady(d)?'concluida':'revisao';
  const saved=saveWorkflows();
  workflowNotice=(classificationChanged&&d.partners.length?'A seção ou o tipo mudou; as confirmações do Socii foram reiniciadas. ':'')+
   (saved?(d.status==='concluida'?'Proposição concluída.':'Sua parte foi concluída. Aguardando participantes do Socii.'):'Conclusão aplicada somente nesta aba: não foi possível salvar.');
  navigate('proposals');return;
 }
 if(id==='invite-socii-form'){
  const d=drafts.find(x=>x.id===String(data.get('draftId')??'')),memberId=String(data.get('memberId')??'');
  if(d&&memberId&&memberId!==members[0]?.id&&!d.partners.some(p=>p.id===memberId)){
   d.partners.push({id:memberId,complete:false});if(d.authorComplete)d.status='revisao';
   const saved=saveWorkflows();
   workflowNotice=saved?'Participante adicionado ao Socii. Nenhum convite foi enviado.':'Participante adicionado, mas não foi possível salvar. Nenhum convite foi enviado.';
  }else workflowNotice='Selecione uma pessoa que ainda não esteja no Socii.';
  inviteOpen=false;render();
  // The submitter disappears when the invitation form closes. Restore a
  // meaningful keyboard destination without introducing a visual control.
  document.querySelector<HTMLButtonElement>('[data-action=invite-socii]')?.focus({preventScroll:true});
  return;
 }
 if(id==='schedule-deliberation-form'){
  const title=String(data.get('title')??'').trim(),objective=String(data.get('objective')??'').trim();
  const start=String(data.get('start')??''),end=String(data.get('end')??'');
  if(!title||!objective||!start||!end||new Date(start).getTime()>=new Date(end).getTime()){
   showScheduleFormError(form,'Confira o título, a descrição e o período: o encerramento deve ser posterior ao início.','end');
   return;
  }
  const proposalId=String(data.get('proposalId')??'');
  if(!drafts.some(d=>d.id===proposalId&&d.status==='concluida')){
   showScheduleFormError(form,'Selecione uma proposição concluída.','proposalId');
   return;
  }
  const method=data.get('method');
   if(!isDeliberationMethod(method)){
    showScheduleFormError(form,'Selecione uma das seis modalidades de votação.','method');return;
   }
   const labels=method==='binaria'?[]:String(data.get('choices')??'').split(/\r?\n/).map(label=>label.trim()).filter(Boolean);
   const choices:PreviewChoice[]=labels.map((label,index)=>({id:`opt-${index+1}`,label}));
   if(method!=='binaria'&&!isValidPreviewChoices(choices)){
    showScheduleFormError(form,'Informe de 2 a 8 alternativas distintas, com até 80 caracteres por linha.','choices');return;
   }
   const item:Deliberation={id:nextLocalRecordId('sched',schedule),title,objective,proposalId,sectionId:String(data.get('sectionId')??''),start,end,type:String(data.get('type')??''),method,...(method!=='binaria'?{choices}:{}),status:'programada'};
  const fromProfileSheet=profileScheduleSheetOpen;
  profileScheduleSheetOpen=false;
  schedule.unshift(item);const stored=saveWorkflows();workflowNotice=stored?'Deliberação programada.':'Programação mantida somente enquanto a página estiver aberta.';scheduleFormOpen=false;scheduleMethod=null;schedulePrefillProposalId=null;expandedSchedule=item.id;
  const date=new Date(`${start.slice(0,10)}T12:00:00`);calendarYear=date.getFullYear();calendarMonth=date.getMonth();selectedCalendarDay=start.slice(0,10);
  render();
  // The saved schedule is the result of the form which has just disappeared.
  if(fromProfileSheet){
   [...document.querySelectorAll<HTMLButtonElement>('[data-schedule-draft]')]
    .find(btn=>btn.dataset.scheduleDraft===item.proposalId)?.focus({preventScroll:true});
  }else document.querySelector<HTMLButtonElement>(`[data-schedule="${item.id}"]`)?.focus({preventScroll:true});
  return;
 }
});
document.addEventListener('submit',(event)=>{
 const form=event.target;
 if(!(form instanceof HTMLFormElement)||form.id!=='preview-vote-form'||!(advancedPreview||votingFormsOpen))return;
 event.preventDefault();
 const data=new FormData(form);
 const integer=(value:FormDataEntryValue|null):number=>typeof value==='string'&&/^(0|[1-9][0-9]*)$/.test(value)?Number(value):NaN;
 let payload:unknown;
 if(previewMode==='binaria'||previewMode==='nominal')payload={selected:data.get('selected')};
 else if(previewMode==='ordenada')payload={ranking:previewVoteChoices().map((_,index)=>data.get('rank-'+String(index)))};
 else if(previewMode==='aprovacao')payload={approved:data.getAll('approved')};
 else if(previewMode==='escalar')payload={scores:Object.fromEntries(previewVoteChoices().map(option=>[option.id,integer(data.get('score-'+option.id))]))};
 else payload={allocation:Object.fromEntries(previewVoteChoices().map(option=>[option.id,integer(data.get('alloc-'+option.id))]))};
 const selectedMember=members.find(member=>member.id===previewVoteMemberId&&isDeliberativeMember(member,sections));
 const result=validatePreviewVote(previewMode,payload,(advancedPreview?selectedMember?.cumulativeVoteWeight:5),previewVoteChoices().map(option=>option.id));
 if(!result.ok){previewVoteError=result.error;render();document.querySelector<HTMLElement>('#preview-vote-error')?.focus({preventScroll:true});return;}
 const scope=previewSampleScope();
 if(previewRequestId===null)previewRequestId='sample-'+String(++previewRequestSequence);
 const submitted=previewSampleLedger.submit({
  scope,requestId:previewRequestId,method:previewMode,
  options:previewVoteChoices(),vote:result.vote
 });
 if(!submitted.ok){
  previewVoteError=submitted.message;render();
  document.querySelector<HTMLElement>('#preview-vote-error')?.focus({preventScroll:true});return;
 }
 previewVoteError='';previewVoteReceipt=result.vote;render();
 const receipt=document.querySelector<HTMLElement>('.preview-vote-receipt');
 if(receipt){receipt.tabIndex=-1;receipt.focus({preventScroll:true});}
});
document.addEventListener('submit',(event)=>{
 const form=event.target;
 if(!(form instanceof HTMLFormElement)||form.getAttribute('id')!=='edit-member-form') return;
 event.preventDefault();
 const data=new FormData(form), member=members.find(m=>m.id===data.get('memberId'));
 const acdmId=String(data.get('acdmId')??'').trim().toUpperCase();
 if(!member) return;
 if(!/^[A-Z0-9_-]{3,40}$/.test(acdmId)) {
  editErrorField='acdmId';editError='Use de 3 a 40 caracteres: letras, números, hífen ou sublinhado.';
  notice='';render();
  document.querySelector<HTMLInputElement>('#member-acdm-id')?.focus({preventScroll:true});
  return;
 }
 if(members.some(m=>m.id!==member.id && m.acdmId===acdmId)){
  editErrorField='acdmId';editError='Este identificador já pertence a outro membro.';notice='';render();
  const field=document.querySelector<HTMLInputElement>('#member-acdm-id');field?.focus({preventScroll:true});field?.select();return;
 }
 const weightText=String(data.get('cumulativeVoteWeight')??'').trim();
 const voteWeight=weightText===''?undefined:Number(weightText);
 if(weightText!==''&&!isPositiveCumulativeVoteWeight(voteWeight)){
  editErrorField='cumulativeVoteWeight';editError='Informe uma quantidade inteira e positiva de votos, ou deixe o campo vazio.';
  notice='';render();document.querySelector<HTMLInputElement>('#member-cumulative-weight')?.focus({preventScroll:true});return;
 }
 editError='';rememberChange(member);member.acdmId=acdmId;member.cumulativeVoteWeight=voteWeight;saveDemoMembers();
 notice=`Dados de ${member.name} atualizados.`;
 editingMemberId=null;render();
 document.querySelector<HTMLButtonElement>('[data-action=undo]')?.focus({preventScroll:true});
});
document.addEventListener('input',(event)=>{
 const target=event.target;
 if(target instanceof HTMLElement&&target.id==='draft-rich-body')syncRichEditor();
 if(target instanceof HTMLElement && target.closest('#compose-proposal-form'))refreshComposerUnloadGuard();
 if(target instanceof HTMLElement && target.closest('#schedule-deliberation-form'))refreshComposerUnloadGuard();
 // An empty draft save is invalid only while *both* fields are blank. Do not
 // leave a stale error attached after the user supplies either field.
 if((target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement) &&
    target.closest('#compose-proposal-form') && composeError){
  const form=target.form;
  const title=form?.elements.namedItem('title');
  const body=form?.elements.namedItem('body');
  if(title instanceof HTMLInputElement && body instanceof HTMLTextAreaElement && (title.value.trim() || body.value.trim())){
   composeError='';
   form?.querySelector('#compose-save-error')?.remove();
   title.removeAttribute('aria-invalid');title.removeAttribute('aria-describedby');
   body.removeAttribute('aria-invalid');body.removeAttribute('aria-describedby');
  }
 }
 // The demonstration member ID is validated on save. A corrected value
 // should stop being reported as invalid without applying changes early.
 if(target instanceof HTMLInputElement && target.id==='member-acdm-id' && editError){
  const id=target.value.trim().toUpperCase();
  const memberId=(target.form?.elements.namedItem('memberId') as HTMLInputElement | null)?.value;
  if(/^[A-Z0-9_-]{3,40}$/.test(id) && !members.some(m=>m.id!==memberId && m.acdmId===id)){
   editError='';
   target.removeAttribute('aria-invalid');target.removeAttribute('aria-describedby');
   target.form?.querySelector('#edit-error')?.remove();
  }
 }
 if(target instanceof HTMLInputElement && target.closest('#schedule-deliberation-form') && (target.name==='start'||target.name==='end')){
  const form=target.form;
  const start=form?.elements.namedItem('start'),end=form?.elements.namedItem('end');
  if(start instanceof HTMLInputElement && end instanceof HTMLInputElement && end.getAttribute('aria-invalid')==='true' && start.value && end.value && new Date(start.value).getTime()<new Date(end.value).getTime()){
   end.removeAttribute('aria-invalid');end.removeAttribute('aria-describedby');
   form?.querySelector('#schedule-form-error')?.remove();
  }
 }

 if(target instanceof HTMLInputElement&&target.id==='search-members') {
  filter=target.value;
  updateMemberSearch();
 }
});
document.addEventListener('keydown',(event)=>{
 const target=event.target;
 if(target instanceof HTMLInputElement&&target.id==='draft-link-url'&&event.key==='Enter'){
  event.preventDefault();
  document.querySelector<HTMLButtonElement>('[data-rich-link="apply"]')?.click();
 }
});
/** Capture selection synchronously before the URL input steals focus.
 * Firefox/WebKit and Chromium differ in when selectionchange is delivered. */
function rememberRichSelection(){
 const editor=document.querySelector<HTMLElement>('#draft-rich-body');
 const selection=window.getSelection();
 if(editor&&selection?.rangeCount&&selection.anchorNode&&selection.focusNode&&
    editor.contains(selection.anchorNode)&&editor.contains(selection.focusNode)){
  lastRichSelection=selection.isCollapsed?null:selection.getRangeAt(0).cloneRange();
 }
}
document.addEventListener('selectionchange',rememberRichSelection);
document.addEventListener('focusout',(event)=>{
 const target=event.target;
 if(target instanceof HTMLElement&&target.id==='draft-rich-body')
  rememberRichSelection();
});
document.addEventListener('pointerdown',(event)=>{
 const target=event.target;
 if(target instanceof Element&&target.closest('.workflow-rich-links,.workflow-rich-toolbar,.workflow-rich-options'))
  rememberRichSelection();
});
document.addEventListener('paste',event=>{
 const target=event.target;
 if(!(target instanceof HTMLElement)||target.id!=='draft-rich-body')return;
 const plain=event.clipboardData?.getData('text/plain');
 if(plain===undefined)return;
 event.preventDefault();
 document.execCommand('insertText',false,plain);
 syncRichEditor();
});
document.addEventListener('change',(event)=>{
 const target=event.target;
 if(target instanceof HTMLSelectElement && target.dataset.richLayout &&
    target.closest('#compose-proposal-form')){
  const key=target.dataset.richLayout;
  if(['align','left','right','lineHeight'].includes(key)){
   const current=draftForm.bodyLayout??DEFAULT_RICH_LAYOUT;
   const next={...current,[key]:key==='align'?target.value:Number(target.value)};
   if(isRichLayout(next)){
    draftForm.bodyLayout=JSON.stringify(next)===JSON.stringify(DEFAULT_RICH_LAYOUT)?undefined:next;
    const editor=document.querySelector<HTMLElement>('#draft-rich-body');
    if(editor)editor.style.cssText=richLayoutStyle(next,true);
   }
  }
  return;
 }
 const format=target instanceof HTMLElement ? target.dataset.richFormat : undefined;
 if(format&&target instanceof HTMLElement&&target.closest('#compose-proposal-form')){
  const family:Record<string,string>={aptos:'Aptos',arial:'Arial',georgia:'Georgia'};
  const sizes:Record<string,string>={'12':'2','16':'3','18':'4','24':'5','30':'6'};
  const selected=target instanceof HTMLSelectElement?target.value:'';
  const fontChoice=family[selected],sizeChoice=sizes[selected];
  let command='',value='';
  if(format==='font'&&target instanceof HTMLSelectElement&&fontChoice){
   command='fontName';value=fontChoice;
  }else if(format==='size'&&target instanceof HTMLSelectElement&&sizeChoice){
   command='fontSize';value=sizeChoice;
  }else if((format==='color'||format==='highlight')&&target instanceof HTMLInputElement&&
           /^#[0-9a-fA-F]{6}$/.test(target.value)){
   command=format==='color'?'foreColor':'hiliteColor';value=target.value;
  }
  if(command){
   const editor=document.querySelector<HTMLElement>('#draft-rich-body');
   if(editor){
    editor.focus({preventScroll:true});
    if(lastRichSelection&&editor.contains(lastRichSelection.commonAncestorContainer)){
     const selection=window.getSelection();
     selection?.removeAllRanges();selection?.addRange(lastRichSelection);
    }
    document.execCommand(command,false,value);
    syncRichEditor();
   }
  }
  if(target instanceof HTMLSelectElement)target.value='';
  return;
 }
 if(target instanceof HTMLSelectElement && target.id==='schedule-method' && target.closest('#schedule-deliberation-form')){
  scheduleMethod=isDeliberationMethod(target.value)?target.value:null;render();
  document.querySelector<HTMLSelectElement>('#schedule-method')?.focus({preventScroll:true});return;
 }
 if((advancedPreview||votingFormsOpen) && target instanceof HTMLSelectElement && target.id==='preview-vote-method'){
  if(isDeliberationMethod(target.value)){
   previewVoteDraft=null;previewMode=target.value;previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';previewVoteMemberId='';render();
   document.querySelector<HTMLSelectElement>('#preview-vote-method')?.focus({preventScroll:true});
  }return;
 }
 if((advancedPreview||votingFormsOpen) && target instanceof HTMLSelectElement && target.id==='preview-vote-member'){
  previewVoteDraft=null;previewVoteMemberId=target.value;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';render();
  document.querySelector<HTMLSelectElement>('#preview-vote-member')?.focus({preventScroll:true});return;
 }
 if(target instanceof HTMLSelectElement && target.name==='proposalId' && target.closest('#schedule-deliberation-form') && target.getAttribute('aria-invalid')==='true'){
  if(drafts.some(d=>d.id===target.value && d.status==='concluida')){
   target.removeAttribute('aria-invalid');target.removeAttribute('aria-describedby');
   target.form?.querySelector('#schedule-form-error')?.remove();
  }
 }

 if(advancedPreview && target instanceof HTMLSelectElement&&target.id==='role-mode'){
  rolePreview=target.value==='membro'?'membro':'diretor';render();
  document.querySelector<HTMLSelectElement>('#role-mode')?.focus({preventScroll:true});
 }
});
syncRouteState();
render();