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
// All six new ballot modes run in memory only, behind ?demo=1.
let previewMode: DeliberationMethod = 'binaria';
let previewVoteError = '';
let previewVoteReceipt: PreviewVote | null = null;
let previewVoteMemberId = '';
// Deliberately memory-only; never part of the session archive or legacy ballot totals.
const previewSampleLedger=createPreviewSampleLedger(100);
let previewRequestSequence=0;
let previewRequestId:string|null=null;
function previewSampleScope():string {
 const scheduled=previewSelectedSchedule();
 return scheduled?`schedule:${scheduled.id}`:`fixture:${previewMode}`;
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
function navigate(route: Route, memberId?: string) {
  if(route!=='calendar'){scheduleFormOpen=false;scheduleMethod=null;}
  menuOpen = false;
  demoToolsOpen = false;
  notice = '';
  editError = '';
  lastChange = null;
  const hash = `#/${route}${route==='profile' && memberId?`/${encodeURIComponent(memberId)}`:''}`;
  if (location.hash === hash) {
    render();
    document.querySelector<HTMLElement>('#main-content')?.focus({preventScroll:true});
  } else location.hash = hash;
  window.scrollTo({ top: 0, behavior: 'instant' });
}
function crest() { return '<img src="./assets/crest.png" width="29" height="29" alt="Símbolo da Academy">'; }
function footer() {
  return `${menuOpen ? `<nav id="bottom-navigation" class="bottom-menu" aria-label="Navegação principal"><div class="menu-list">
    <button class="menu-item" data-route="members" ${routeFromHash()==='members'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="7" r="3"/><path d="M3.5 19v-2.2a5.5 5.5 0 0 1 11 0V19M17 8h4M17 12h4M17 16h4"/></svg></span>Membros e Serviços da Cúpula Cíntia</button>
    <button class="menu-item" data-route="overview" ${routeFromHash()==='overview'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h2M12 9h5M7 13h2M12 13h5M7 17h2M12 17h5"/></svg></span>Histórico de Votações e Proposições</button>
    <button class="menu-item" data-route="calendar" ${routeFromHash()==='calendar'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true">▦</span>Agendar e Iniciar Deliberação</button>
    <button class="menu-item" data-route="proposals" ${['proposals','compose','review'].includes(routeFromHash())?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true">✎</span>Elaborar Proposição e Socii</button>
  </div></nav>` : ''}
  <footer class="app-footer">${crest()}<button type="button" class="footer-home" data-route="ballot" aria-label="Voltar à votação">CONFFRATUS</button><small class="footer-demo">DADOS FICTÍCIOS · PRÉVIA</small>
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
  <div class="metric-cell">${m.approved}<small>PR</small></div>
  <div class="metric-cell">${m.officialLetters ?? 0}<small>Ofício</small></div><div class="metric-cell">${m.collaborations}<small>Socii</small></div></div>`;
}
function tabBar(tab: Tab, personalVotingHistory = true) {
  const showSelected=routeFromHash()!=='members';
  return `<div class="tabs" role="group" aria-label="Histórico do membro">
   ${personalVotingHistory ? `<button class="tab" type="button" aria-pressed="${showSelected && tab==='votos'}" data-tab="votos">Histórico de votações</button>` : ''}
   <button class="tab" type="button" aria-pressed="${showSelected && tab==='proposicoes'}" data-tab="proposicoes">Proposições</button>
  </div>`;
}
function memberHeader(m:Member, tab:Tab, displayTabs=true) {
 const identity=routeFromHash()==='members'
  ? `<button type="button" class="profile-name-button" data-member="${m.id}" aria-label="Abrir perfil de ${escapeHTML(m.name)}">${escapeHTML(m.name)}</button>`
  : `<strong>${escapeHTML(m.name)}</strong>`;
 return `<div class="profile-head"><div class="profile-summary"><div class="avatar avatar--large" aria-hidden="true"></div>
   ${metricRow(m)}</div><div class="profile-identity"><div>${identity} <small>${m.role==='diretor'?'Diretoria':isDeliberativeMember(m, sections)?'Membro deliberativo':'Membro da Academy'}</small></div>
   <p>${escapeHTML(m.subtitle)}</p>${routeFromHash()==='profile' && m.acdmId?`<p class="profile-reference"><a class="profile-reference-link" href="#/profile/acdm/${encodeURIComponent(m.acdmId)}" aria-label="Abrir link de referência demonstrativa ACDM ID ${escapeHTML(m.acdmId)}">ACDM ID: ${escapeHTML(m.acdmId)}</a><span> · prévia local</span></p>`:''}</div>${displayTabs?tabBar(tab, hasPersonalVoteHistory(m, sections)):''}</div>`;
}

function previewSelectedSchedule():Deliberation|undefined {
 return schedule.find(item=>item.id===previewScheduleId&&item.status==='programada'&&item.method===previewMode&&
  (previewMode==='binaria'||isValidPreviewChoices(item.choices)));
}
function previewVoteChoices(): readonly {id:string;label:string}[] {
 return previewMode==='binaria'?PREVIEW_BINARY_OPTIONS:(previewSelectedSchedule()?.choices??PREVIEW_LIST_OPTIONS);
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
 const receipt=previewVoteReceipt?.method===previewMode?previewVoteReceipt:null;
 return '<section class="preview-vote-lab" aria-labelledby="preview-vote-title">'+
  '<h2 id="preview-vote-title">Laboratório das seis modalidades</h2>'+ 
  (contextual?'<p class="preview-vote-context"><strong>Deliberação programada:</strong> '+escapeHTML(contextual.title)+
   '<span>Proposição: '+escapeHTML(drafts.find(d=>d.id===contextual.proposalId)?.title??'Indisponível')+'</span></p>':'')+
  '<p class="preview-vote-disclaimer">Apenas em ?demo=1. Alternativas fictícias, sem voto oficial, apuração institucional, login ou envio de informações.</p>'+
  '<label for="preview-vote-method">Modalidade de deliberação</label>'+
  '<select id="preview-vote-method"'+(contextual?' disabled':'')+'>'+DELIBERATION_METHODS.map(mode=>
   '<option value="'+mode.id+'"'+(mode.id===previewMode?' selected':'')+'>'+escapeHTML(mode.label)+'</option>').join('')+'</select>'+
  '<p class="preview-vote-detail">'+escapeHTML(method?.detail??'')+'</p>'+ 
  (contextual?'<button type="button" class="preview-vote-secondary" data-action="exit-preview-schedule">Voltar às alternativas de teste</button>':'')+
  (receipt?'<div class="preview-vote-receipt" role="status"><strong>Voto simulado conferido nesta aba</strong>'+
   '<p>'+previewVoteReceiptText(receipt)+'</p>'+
   '<button type="button" class="preview-vote-secondary" data-action="reset-preview-vote">Registrar outra amostra</button></div>':
   '<form id="preview-vote-form" data-mode="'+previewMode+'" data-preview-member="'+previewVoteMemberId+'" novalidate>'+previewVoteFieldset()+
   (previewVoteError?'<p class="preview-vote-error" role="alert" id="preview-vote-error" tabindex="-1">'+escapeHTML(previewVoteError)+'</p>':'')+
   '<button type="submit" class="preview-vote-submit"'+
    (previewMode==='cumulativa' && !members.some(m=>isDeliberativeMember(m,sections)&&
     isPositiveCumulativeVoteWeight(m.cumulativeVoteWeight))?' disabled':'')+
   '>Conferir voto fictício</button></form>')+
  previewVoteSummary()+
  '</section>';
}

function ballotPage() {
 const ballot=ballots[0]; if(!ballot) return '<p>Nenhuma votação disponível.</p>';
 const demoOptions = ballot.options.map(o => ({...o, votes:o.votes + (canRecordVote(ballot) && demoVoteId===o.id?1:0)}));
 const sum=totalVotes(demoOptions);
 return `<div class="main-pad">${header(undefined,undefined,true)}<div class="results">
 ${demoOptions.map(o=>`<div class="result-row ${demoVoteId===o.id?'result-row--chosen':''}" aria-label="${escapeHTML(o.label)}: ${o.votes} votos, ${demoVoteId?(100*o.votes/sum).toFixed(1):resultPercentage(o.votes,sum)} por cento"><span class="result-label">${escapeHTML(o.label)}${demoVoteId===o.id?'<small class="your-vote">Escolha simulada</small>':''}</span><span class="result-count">${o.votes} Votos</span><span class="result-percentage">${demoVoteId?(100*o.votes/sum).toFixed(1):resultPercentage(o.votes,sum)}%</span></div>`).join('')}
 </div><hr class="hairline"></div><section class="description-panel"><div class="description-heading"><span>Descrição da votação</span><button class="demo-toggle" type="button" data-action="toggle-demo" aria-expanded="${demoExpanded}" ${demoExpanded?'aria-controls="demo-vote-panel"':''}>${demoExpanded?'Fechar':canRecordVote(ballot)?'Participar':'Ver situação'}</button></div>
 <p class="ballot-description">${escapeHTML(ballot.description)}</p><p class="ballot-preview-disclosure" role="note">Resultados fictícios. A escolha é simulada somente nesta aba; nenhum voto é enviado à Academy.</p>${demoExpanded?`<div id="demo-vote-panel" class="demo-ballot"><h2>${escapeHTML(ballot.title)}</h2><p>${canRecordVote(ballot)?'Votação fictícia aberta. Selecione uma opção apenas para simular.':'Esta votação está encerrada. Os resultados permanecem disponíveis para consulta.'}</p>
 ${canRecordVote(ballot)?`<div class="vote-actions">${ballot.options.map(o=>`<button type="button" data-vote="${o.id}" class="vote-button" aria-pressed="${demoVoteId===o.id}">${escapeHTML(o.label)}</button>`).join('')}</div>
 <p class="vote-feedback" role="status">${demoVoteId?'Escolha simulada nesta aba. Nenhum voto foi enviado.':'Selecione uma opção para a simulação.'}</p>
 ${demoVoteId?'<button class="reset-vote" type="button" data-action="reset-vote">Alterar escolha</button>':''}`:''}</div>`:''}</section>${advancedPreview?previewVoteLab():''}`;
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
  ? drafts.map(d=>`<article class="activity activity-proposal session-proposal"><button type="button" data-draft="${escapeHTML(d.id)}" class="session-proposal-link"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${draftStatusLabel(d)} · ${escapeHTML(d.type)}</small><span>${escapeHTML(d.body.slice(0,170))}</span></button>${linkedScheduleButtons(d)}</article>`).join('') : '';
 return `${header(undefined,undefined,false)}${memberHeader(member,activeTab)}<section class="section-body">
 ${local?`<h2 class="session-proposals-heading">Proposições desta sessão</h2>${local}${relevant.length?'<h2 class="session-proposals-heading">Histórico demonstrativo</h2>':''}`:''}
 ${relevant.length?relevant.map(activityItem).join(''):local?'':'<p class="status-line">Nenhum registro encontrado.</p>'}</section>`;
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
  ? `<section class="overview-local-history" aria-label="Proposições desta sessão"><h2 class="session-proposals-heading">Proposições desta sessão</h2><p class="overview-local-disclosure">Registros locais de demonstração. Não alteram os indicadores fictícios acima.</p>${drafts.map(d=>`<article class="workflow-record overview-local-proposal"><button type="button" data-draft="${escapeHTML(d.id)}" class="workflow-record-btn"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${draftStatusLabel(d)} · ${escapeHTML(d.type)}</small><p>${escapeHTML(d.body.slice(0,140))}</p></button>${linkedScheduleButtons(d)}</article>`).join('')}</section>` : '';
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
 <p class="governance-preview-disclosure" role="note">Gerenciamento fictício nesta prévia: editar ou rebaixar altera somente dados locais deste navegador. Nenhum cadastro da Academy é modificado.</p>
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
function savedRecordNotice(){return ignoredSavedRecords?'<p class="workflow-form-error" role="status">Alguns registros incompletos ou repetidos desta prévia local não foram carregados.</p>':'';}
const blankDraft=()=>({title:'',body:''});
let draftForm=blankDraft();
let currentDraftId='';
let finishedProposalReturnTo:'proposals'|'calendar'|'overview'|'profile'='proposals';
let workflowNotice='';
let composeError='';
let scheduleFormOpen=false;
let expandedSchedule='sample-1';
let cancelledHistoryOpen=false;
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
function linkedScheduleButtons(d:Draft) {
 const linked=schedule.filter(item=>item.proposalId===d.id&&item.status==='programada');
 return linked.length?`<div class="session-schedule-links" role="group" aria-label="Programações locais desta proposição">${linked.map(item=>`<button type="button" class="session-schedule-link" data-linked-schedule="${escapeHTML(item.id)}">Programação: ${escapeHTML(item.title)} · ${friendlyStamp(item.start)} (prévia local)</button>`).join('')}</div>`:'';
}
function proposalsPage(){
 const author=members[0];
 const examples=activities.filter(a=>a.type==='proposicao' && a.memberId===author?.id).slice(0,4);
 return `${header(undefined,undefined,false)}<div class="workflow-profile">${author?memberHeader(author,'proposicoes',false):''}<div class="tabs workflow-tabs" role="group" aria-label="Histórico do membro"><button class="tab" type="button" data-route="profile" aria-label="Consultar histórico de votação">Histórico de votações</button><span class="tab" aria-current="page">Proposições e Socii</span></div></div>
  <div class="workflow-layout workflow-proposals-layout">${savedRecordNotice()}${drafts.length?'<h2 class="workflow-record-heading">Proposições desta sessão</h2>':''}${drafts.length?drafts.map(d=>`<article class="workflow-record"><button data-draft="${escapeHTML(d.id)}" class="workflow-record-btn"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${draftStatusLabel(d)} · ${escapeHTML(d.type)}</small><p>${escapeHTML(d.body.slice(0,140))}</p></button>${linkedScheduleButtons(d)}${d.partners.length?`<p class="workflow-partners"><strong>Concluíram ${Number(d.authorComplete)+d.partners.filter(p=>p.complete).length} de ${d.partners.length+1}</strong><span>Autoria: ${d.authorComplete?'concluída':'pendente'} · Socii: ${d.partners.map(p=>`${escapeHTML(members.find(m=>m.id===p.id)?.name??'Membro')} (${p.complete?'concluiu':'pendente'})`).join(', ')}</span></p>`:''}${advancedPreview&&d.partners.some(p=>!p.complete)?d.partners.filter(p=>!p.complete).map(p=>`<button class="workflow-demo-confirm" data-confirm-partner="${escapeHTML(d.id)}:${escapeHTML(p.id)}">Simular conclusão de ${escapeHTML(members.find(m=>m.id===p.id)?.name??'participante')}</button>`).join(''):''}</article>`).join(''):''}
 ${examples.length?'<h2 class="workflow-record-heading">Histórico demonstrativo</h2>':''}${examples.map(activityItem).join('')}
 ${advancedPreview?`<section class="local-archive" aria-label="Cópia de segurança dos registros da prévia"><h2>Cópia local da prévia</h2><p>Exporta apenas proposições, Socii e programações desta aba. O arquivo pode conter o texto que você escreveu. Não inclui login, votos, permissões ou dados da Academy.</p><div class="local-archive-actions"><button type="button" data-action="export-local-archive">Baixar cópia JSON</button><button type="button" data-action="import-local-archive">Restaurar cópia JSON</button><input id="archive-file-input" type="file" accept=".json,application/json" hidden></div>${archiveMessage?`<p class="local-archive-message" role="${archiveIsError?'alert':'status'}">${escapeHTML(archiveMessage)}</p>`:''}</section>`:''}
 </div><div class="workflow-actions"><button type="button" class="workflow-outline" data-action="invite-socii" aria-expanded="${inviteOpen}" ${inviteOpen?'aria-controls="invite-socii-form"':''}>Convidar para Socii</button>${inviteOpen?`<form id="invite-socii-form" class="workflow-inline" aria-label="Adicionar participante Socii (prévia local)"><label>Proposição<select name="draftId" required>${drafts.filter(d=>d.status!=='concluida').map(d=>`<option value="${escapeHTML(d.id)}">${escapeHTML(d.title)}</option>`).join('')}</select></label><label>Participante<select name="memberId" required><option value="" selected disabled>Selecione uma pessoa</option>${selectOptions('',members.slice(1))}</select></label><button class="workflow-primary" ${!drafts.some(d=>d.status!=='concluida')?'disabled':''}>Adicionar participante</button></form>`:''}
 <button type="button" class="workflow-primary" data-action="new-proposal">Redigir proposição</button></div>
 ${workflowNotice?`<p class="workflow-status">${escapeHTML(workflowNotice)}</p>`:''}`;
}
// Show only participants linked to this proposal; a local preview has no valid elapsed time.
function sociiEditorBar(d:Draft|undefined){
 if(!d?.partners.length)return '';
 const names=d.partners.map(p=>members.find(m=>m.id===p.id)?.name).filter((n):n is string=>Boolean(n));
 const participantText=names.length===1?`Você e ${names[0]}`:`Você e ${d.partners.length} participantes`;
 const finished=Number(d.authorComplete)+d.partners.filter(p=>p.complete).length;
 return `<aside class="workflow-socii-editor-bar" aria-label="Socii desta proposição, demonstração local">
 <span class="workflow-socii-avatars" aria-hidden="true"><i></i><i></i></span>
 <div class="workflow-socii-editor-status"><strong>${escapeHTML(participantText)} em Socii</strong><small>Prévia local · Concluíram ${finished} de ${d.partners.length+1}</small></div>
 <span class="workflow-socii-editor-label" aria-hidden="true">Socii</span></aside>`;
}
function composePage(){
 const editing=drafts.find(d=>d.id===currentDraftId);
 return `${sociiEditorBar(editing)}<div class="workflow-editor-head"><span>CONFFRATUS</span><h1>${escapeHTML(draftForm.title||'Título')}</h1></div>
 <form id="compose-proposal-form" class="workflow-editor"><label for="draft-title">Título da proposição</label><input id="draft-title" name="title" maxlength="140" required ${composeError?'aria-invalid="true" aria-describedby="compose-save-error"':''} placeholder="Título" value="${escapeHTML(draftForm.title)}">
 <label for="draft-body">Redação</label><textarea id="draft-body" name="body" required minlength="20" ${composeError?'aria-invalid="true" aria-describedby="compose-save-error"':''} placeholder="Escreva...">${escapeHTML(draftForm.body)}</textarea>
 ${composeError?`<p id="compose-save-error" class="workflow-form-error" role="alert">${escapeHTML(composeError)}</p>`:''}
 <div class="workflow-editor-actions"><button class="workflow-primary" type="submit" name="intent" value="conclude">Concluir redação</button><button class="workflow-outline" type="submit" name="intent" value="save" formnovalidate>Salvar rascunho</button><button class="workflow-outline" type="button" data-route="${finishedProposalReturnTo==='profile'?'profile':'proposals'}">${finishedProposalReturnTo==='profile'?'Voltar ao perfil':'Voltar'}</button></div></form>`;
}
function reviewPage(){
 const d=drafts.find(x=>x.id===currentDraftId);if(!d)return proposalsPage();
 if(d.status==='concluida')return `<div class="workflow-editor-head"><span>CONFFRATUS</span><h1>${escapeHTML(d.title)}</h1></div><div class="workflow-review-body"><p>${escapeHTML(d.body)}</p></div><div class="workflow-review-panel"><div class="workflow-finished"><strong>Proposição concluída</strong><p>Seção: ${escapeHTML(sections.find(s=>s.id===d.sectionId)?.name??'Não definida')} · ${escapeHTML(d.type)}</p>${linkedScheduleButtons(d)}<button type="button" class="workflow-primary" data-route="${finishedProposalReturnTo}">${finishedProposalReturnTo==='calendar'?'Voltar à programação':finishedProposalReturnTo==='overview'?'Voltar ao histórico':finishedProposalReturnTo==='profile'?'Voltar ao perfil':'Voltar às proposições'}</button></div></div>`;
 return `<div class="workflow-editor-head"><span>CONFFRATUS</span><h1>${escapeHTML(d.title)}</h1></div>
 <div class="workflow-review-body"><p>${escapeHTML(d.body)}</p></div>
 <div class="workflow-review-panel"><form id="confirm-proposal-form" class="workflow-form workflow-review-form">
 <div class="workflow-review-sheet"><img class="workflow-review-crest" src="./assets/crest.png" alt="" width="38" height="38"><p>Confira os dados e a redação antes de confirmar a conclusão.</p>
 <label>Seção responsável<select name="sectionId" required>${selectOptions(d.sectionId,sections.filter(s=>s.category==='deliberativa'))}</select></label>
 <label>Tipo de proposição<select name="type" required>${['PDR','PR','Ofício'].map(t=>`<option value="${t}" ${t===d.type?'selected':''}>${t}</option>`).join('')}</select></label>
 </div><div class="workflow-review-buttons"><button type="button" class="workflow-outline" data-route="compose" aria-label="Cancelar confirmação e voltar à redação">Cancelar</button><button class="workflow-primary" type="submit">Confirmar</button></div></form></div>`;
}
// Display only Socii participants already linked to this session's proposal.
function calendarSociiLine(proposalId:string){
 const draft=drafts.find(d=>d.id===proposalId);
 const names=draft?.partners.map(p=>members.find(m=>m.id===p.id)?.name)
  .filter((name):name is string=>Boolean(name))??[];
 return names.length?`<span class="calendar-socii">Socii: ${names.map(escapeHTML).join(', ')}</span>`:'';
}
function calendarPage(){
 const sample:Deliberation[]=[{id:'sample-1',title:'Revisão do calendário de reuniões',sectionId:'integridade',objective:'Organizar o calendário de reuniões institucionais.',start:'2026-11-22T14:00',end:'2026-11-23T14:00',type:'PDR',proposalId:'',status:'programada' as const}];
 const all=[...sample,...schedule.filter(s=>s.status==='programada')]
  .sort((a,b)=>a.start.localeCompare(b.start));
 const visible=selectedCalendarDay?all.filter(item=>item.start.slice(0,10)<=selectedCalendarDay&&item.end.slice(0,10)>=selectedCalendarDay):all;
 // Cancelled entries remain in the session's original schedule array. Keep them
 // separate from active calendar markers, date filters and scheduling controls.
 const cancelled=schedule.filter(item=>item.status==='cancelada');
 const cancelledHistory=cancelled.length?`<section class="calendar-history" aria-label="Histórico de cancelamentos da prévia local">
 <button type="button" class="calendar-history-toggle" data-action="toggle-cancelled-history" aria-expanded="${cancelledHistoryOpen}" ${cancelledHistoryOpen?'aria-controls="cancelled-schedule-history"':''}>Histórico de cancelamentos da prévia (${cancelled.length})</button>
 ${cancelledHistoryOpen?`<div id="cancelled-schedule-history" role="region" aria-label="Programações canceladas da sessão"><p class="calendar-history-note">Registros da sessão, somente para consulta. Cancelamento não é uma deliberação ativa.</p>${cancelled.map(item=>{
   const linked=drafts.find(d=>d.id===item.proposalId);
   return `<article class="calendar-cancelled-record"><h3>${escapeHTML(item.title)}</h3><p><strong>Cancelada</strong> · ${escapeHTML(item.type)}</p><p>Modalidade: ${escapeHTML(DELIBERATION_METHODS.find(m=>m.id===item.method)?.label??'Não informada (registro anterior)')}</p><p>${friendlyStamp(item.start)} até ${friendlyStamp(item.end)}</p><p>Seção: ${escapeHTML(sections.find(section=>section.id===item.sectionId)?.name??'Não disponível')}</p><p>Proposição: ${linked?escapeHTML(linked.title):'Proposição associada indisponível nesta sessão'}</p><p>${escapeHTML(item.objective)}</p></article>`;
  }).join('')}</div>`:''}</section>`:'';
 return `<div class="workflow-layout">${savedRecordNotice()}${calendarGrid(all)}<button class="workflow-open" type="button" data-action="open-schedule" aria-expanded="${scheduleFormOpen}" ${scheduleFormOpen?'aria-controls="schedule-deliberation-form"':''}>${scheduleFormOpen?'Fechar agendamento':'Iniciar uma Votação'}</button>
 <p class="calendar-preview-disclosure" role="note">Esta prévia apenas programa uma deliberação; não inicia uma votação real.</p>
 ${scheduleFormOpen?`<form id="schedule-deliberation-form" class="workflow-form workflow-schedule-form"><h2>Programar deliberação</h2>
 ${!drafts.some(d=>d.status==='concluida')?'<p class="workflow-help">Para agendar, conclua uma proposição primeiro. <button type="button" data-route="proposals">Ir às proposições</button></p>':''}
 <label>Título da deliberação<input name="title" maxlength="140" required placeholder="Título da deliberação"></label>
 <label>Descrição objetiva<textarea name="objective" required minlength="15" rows="3" placeholder="Descrição objetiva"></textarea></label>
 <label>Selecione a proposição<select name="proposalId" required ${!drafts.some(d=>d.status==='concluida')?'disabled':''}><option value="">Selecione</option>${drafts.filter(d=>d.status==='concluida').map(d=>`<option value="${escapeHTML(d.id)}">${escapeHTML(d.title)}</option>`).join('')}</select></label>
 <label>Seção deliberativa<select name="sectionId" required>${selectOptions('integridade',sections.filter(s=>s.category==='deliberativa'))}</select></label>
 <div class="workflow-grid-two"><label>Data e hora de início<input type="datetime-local" name="start" required></label><label>Data e hora de encerramento<input type="datetime-local" name="end" required></label></div>
 <label>Tipo de proposição<select name="type" required><option value="PDR">PDR</option><option value="PR">PR</option><option value="Ofício">Ofício</option></select></label>
  <label>Modalidade de votação<select name="method" id="schedule-method" required><option value="">Selecione a modalidade</option>${DELIBERATION_METHODS.map(mode=>`<option value="${mode.id}">${escapeHTML(mode.label)} — ${escapeHTML(mode.detail)}</option>`).join('')}</select></label>
  ${scheduleMethod&&scheduleMethod!=='binaria'?`<label>Alternativas para esta deliberação<textarea name="choices" rows="5" maxlength="648" placeholder="Uma alternativa por linha, de 2 a 8" required></textarea></label><p class="workflow-help">De 2 a 8 alternativas distintas, uma por linha (até 80 caracteres cada).</p>`:'' }
  <p class="workflow-help">A modalidade descreve como os membros votariam. A prévia não contabiliza votos institucionais.</p>
 <button class="workflow-primary" type="submit" ${!drafts.some(d=>d.status==='concluida')?'disabled':''}>Confirmar programação</button></form>`:''}
 ${cancellationSaveFailed||workflowNotice?`<p class="workflow-status">${escapeHTML(cancellationSaveFailed?cancellationSaveWarning:workflowNotice)}</p>`:''}
 ${cancellationSaveFailed?'<button type="button" class="calendar-save-retry" data-action="retry-cancellation-save">Tentar salvar cancelamento nesta sessão</button>':''}
 <div class="calendar-list"><div class="calendar-list-head"><h2>${selectedCalendarDay?`Programações em ${new Date(`${selectedCalendarDay}T12:00`).toLocaleDateString('pt-BR')}`:'Programações'}</h2>${selectedCalendarDay?'<button type="button" data-action="calendar-all">Ver todas</button>':''}</div>${visible.length===0?'<p class="calendar-empty-message">Nenhuma programação nesta data.</p>':''}${visible.map(item=>`<article class="calendar-item${expandedSchedule===item.id?' calendar-item--expanded':''}"><button type="button" data-schedule="${escapeHTML(item.id)}" aria-expanded="${expandedSchedule===item.id}" ${expandedSchedule===item.id?`aria-controls="schedule-details-${escapeHTML(item.id)}"`: ''}><strong>${escapeHTML(item.title)}</strong><small>${friendlyStamp(item.start)} até ${friendlyStamp(item.end)}</small><span>Seção: ${escapeHTML(sections.find(s=>s.id===item.sectionId)?.name??'')}</span>${calendarSociiLine(item.proposalId)}</button>
 ${expandedSchedule===item.id?`<div id="schedule-details-${escapeHTML(item.id)}" class="calendar-expanded"><div class="calendar-status"><span class="calendar-status-type">${escapeHTML(item.type)}</span><strong>PROPOSIÇÃO EM DELIBERAÇÃO</strong></div><p>${escapeHTML(item.objective)}</p><p>Modalidade: ${escapeHTML(DELIBERATION_METHODS.find(mode=>mode.id===item.method)?.label??'Não informada (registro anterior)')}</p>${item.choices?`<p>Alternativas: ${item.choices.map(option=>escapeHTML(option.label)).join(' · ')}</p>`:''}${advancedPreview&&item.id!=='sample-1'&&item.method&&(item.method==='binaria'||isValidPreviewChoices(item.choices))?`<button type="button" data-preview-schedule="${escapeHTML(item.id)}" class="preview-schedule-open">Simular voto nesta programação</button>`:''}${item.proposalId?(drafts.some(d=>d.id===item.proposalId)?`<button type="button" class="calendar-proposal-link" data-open-schedule-proposal="${escapeHTML(item.proposalId)}">Ver proposição associada</button>`:'<p class="calendar-link-missing" role="status">Proposição vinculada indisponível nesta sessão.</p>'):''}${item.proposalId&&drafts.some(d=>d.id===item.proposalId)&&members[0]?'<button type="button" data-open-proposal-author>Ver perfil da autoria (prévia local)</button>':''}<button type="button" data-cancel-schedule="${escapeHTML(item.id)}" ${item.id==='sample-1'?'disabled title="Exemplo fixo"':''}>Cancelar programação deliberativa</button></div>`:''}</article>`).join('')}</div>${cancelledHistory}</div>`;
}

let lastRenderedHash = location.hash;
function render() {
 if (!root) return;
 // A local edit must not unexpectedly jump the user to the top of a long page.
 const previousScroll = window.scrollY;
 // Preserve local scheduling inputs while browsing days and months.
 const scheduleForm = root.querySelector<HTMLFormElement>('#schedule-deliberation-form');
 const scheduleValues = scheduleForm ? new FormData(scheduleForm) : null;
 // Never use data-member here: it triggers the global profile-navigation click handler.
 // Preserve checked values on ballot validation errors, not across distinct methods.
 const priorVoteForm=root.querySelector<HTMLFormElement>('#preview-vote-form');
 const voteFields=priorVoteForm?.dataset.mode===previewMode&&priorVoteForm?.dataset.previewMember===previewVoteMemberId
  ? Array.from(priorVoteForm.querySelectorAll<HTMLInputElement|HTMLSelectElement>('input,select')).map(field=>({name:field.name,value:field.value,checked:field instanceof HTMLInputElement?field.checked:undefined})) : null;
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
 if (scheduleValues) {
  const nextForm = root.querySelector<HTMLFormElement>('#schedule-deliberation-form');
  if (nextForm) for (const [name, value] of scheduleValues) {
   const field = nextForm.elements.namedItem(name);
   if (field instanceof HTMLInputElement || field instanceof HTMLTextAreaElement || field instanceof HTMLSelectElement) field.value = String(value);
  }
 }
 if(voteFields){
  const fields=root.querySelector<HTMLFormElement>('#preview-vote-form')?.querySelectorAll<HTMLInputElement|HTMLSelectElement>('input,select');
  if(fields?.length===voteFields.length)fields.forEach((field,index)=>{
   const previous=voteFields[index];
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
  menuOpen=false;demoToolsOpen=false;syncRouteState();render();
  if(routeFromHash()==='ballot'&&previewScheduleId){
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
  else if(searchExpanded && routeFromHash()==='members'){
   searchExpanded=false;filter='';render();document.querySelector<HTMLButtonElement>('[data-action=search]')?.focus();
  }
 }
});
document.addEventListener('click',(event)=>{
 const target=event.target;
 if (!(target instanceof Element)) return;
 const skip=target.closest<HTMLAnchorElement>('.skip-link');
 if(skip){event.preventDefault();document.querySelector<HTMLElement>('#main-content')?.focus({preventScroll:true});return;}
 const contextualVote=advancedPreview?target.closest<HTMLElement>('[data-preview-schedule]'):null;
 if(contextualVote?.dataset.previewSchedule){
  const item=schedule.find(s=>s.id===contextualVote.dataset.previewSchedule&&s.status==='programada');
  if(item?.method && (item.method==='binaria'||isValidPreviewChoices(item.choices))){
   previewScheduleId=item.id;previewMode=item.method;previewRequestId=null;previewVoteReceipt=null;previewVoteMemberId='';previewVoteError='';
   navigate('ballot');document.querySelector<HTMLElement>('#preview-vote-title')?.scrollIntoView({block:'center'});
  }return;
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
 if(advancedPreview && actionEl?.dataset.action==='exit-preview-schedule'){
  previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';previewVoteMemberId='';render();
  document.querySelector<HTMLSelectElement>('#preview-vote-method')?.focus({preventScroll:true});return;
 }
 if(advancedPreview && actionEl?.dataset.action==='clear-preview-samples'){
  const scope=previewSampleScope();
  if(!window.confirm('Limpar apenas as amostras desta simulação?'))return;
  previewSampleLedger.clear(scope);
  previewRequestId=null;previewVoteReceipt=null;previewVoteError='';render();
  document.querySelector<HTMLElement>('#preview-vote-form')?.querySelector<HTMLElement>('input,select')?.focus({preventScroll:true});return;
 }
 if(advancedPreview && actionEl?.dataset.action==='reset-preview-vote'){
  previewRequestId=null;previewVoteReceipt=null;previewVoteError='';render();
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
 if(actionEl?.dataset.action==='toggle-demo'){demoExpanded=!demoExpanded;render();return;}
 if(actionEl?.dataset.action==='reset-vote'){
  demoVoteId=null;try{sessionStorage.removeItem('conferatus:demo-vote');}catch{}
  render();document.querySelector<HTMLButtonElement>('[data-vote]')?.focus({preventScroll:true});
  return;
 }
 if (actionEl?.dataset.action==='menu') {menuOpen=!menuOpen; render(); (menuOpen?document.querySelector<HTMLButtonElement>('.menu-item'):document.querySelector<HTMLButtonElement>('.footer-nav'))?.focus(); return;}
 if (routeEl?.classList.contains('footer-home') && Date.now() < suppressFooterHomeClickUntil) {return;}

 if(advancedPreview){const partnerEl=target.closest<HTMLElement>('[data-confirm-partner]');
  if(partnerEl?.dataset.confirmPartner){const [draftId,partnerId]=partnerEl.dataset.confirmPartner.split(':');const d=drafts.find(d=>d.id===draftId);const partner=d?.partners.find(p=>p.id===partnerId);if(d&&partner){partner.complete=true;d.status=draftReady(d)?'concluida':'revisao';
   const saved=saveWorkflows();
   workflowNotice=saved?(d.status==='concluida'?'Todas as partes concluíram. Proposição concluída.':'Participação registrada nesta simulação.'):'Conclusão aplicada somente nesta aba: não foi possível salvar.';
   render();}return;}}
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
 if(actionEl?.dataset.action==='new-proposal'){currentDraftId='';draftForm=blankDraft();workflowNotice='';composeError='';navigate('compose');return;}
 if(actionEl?.dataset.action==='invite-socii'){inviteOpen=!inviteOpen;render();return;}
 if(actionEl?.dataset.action==='open-schedule'){scheduleFormOpen=!scheduleFormOpen;scheduleMethod=null;if(!cancellationSaveFailed)workflowNotice='';render();return;}
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
 if(actionEl?.dataset.action==='calendar-prev'){calendarShift(-1);render();announceCalendarView();return;}
 if(actionEl?.dataset.action==='calendar-next'){calendarShift(1);render();announceCalendarView();return;}
 if(actionEl?.dataset.action==='calendar-today'){const currentDay=new Date();calendarYear=currentDay.getFullYear();calendarMonth=currentDay.getMonth();selectedCalendarDay=isoDay(currentDay);render();announceCalendarView();return;}
 if(actionEl?.dataset.action==='calendar-all'){
  selectedCalendarDay='';render();announceCalendarView();
  const heading=document.querySelector<HTMLElement>('.calendar-list-head h2');
  if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}
  return;
 }
 const dayEl=target.closest<HTMLElement>('[data-calendar-day]');
 if(dayEl?.dataset.calendarDay){selectedCalendarDay=selectedCalendarDay===dayEl.dataset.calendarDay?'':dayEl.dataset.calendarDay;render();announceCalendarView();return;}
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
 if(draftEl?.dataset.draft){const d=drafts.find(x=>x.id===draftEl.dataset.draft);if(d){currentDraftId=d.id;finishedProposalReturnTo=routeFromHash()==='overview'?'overview':routeFromHash()==='profile'?'profile':'proposals';draftForm={title:d.title,body:d.body};composeError='';navigate(d.status==='redacao'?'compose':'review');}return;}
 const scheduleEl=target.closest<HTMLElement>('[data-schedule]');
 if(scheduleEl?.dataset.schedule){expandedSchedule=expandedSchedule===scheduleEl.dataset.schedule?'':scheduleEl.dataset.schedule;render();return;}
 const proposalEl=target.closest<HTMLElement>('[data-open-schedule-proposal]');
 if(proposalEl?.dataset.openScheduleProposal){
  const d=drafts.find(x=>x.id===proposalEl.dataset.openScheduleProposal);
  if(d){currentDraftId=d.id;finishedProposalReturnTo='calendar';draftForm={title:d.title,body:d.body};navigate('review');}
  return;
 }
 const cancelEl=target.closest<HTMLElement>('[data-cancel-schedule]');
 if(cancelEl?.dataset.cancelSchedule){const item=schedule.find(x=>x.id===cancelEl.dataset.cancelSchedule);if(item&&item.status==='programada'){
  item.status='cancelada';
  // A cancelled schedule must not leave a vote sandbox bound to its old alternatives.
  previewSampleLedger.clear(`schedule:${item.id}`);
  if(previewScheduleId===item.id){
   previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;
   previewVoteError='';previewVoteMemberId='';
  }
  const saved=saveWorkflows();cancellationSaveFailed=!saved;
  workflowNotice=saved?'Programação cancelada e salva nesta sessão.':cancellationSaveWarning;
  render();
  const heading=document.querySelector<HTMLElement>('.calendar-list-head h2');
  if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}
 }return;}
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
 previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;
 previewVoteError='';previewVoteMemberId='';
 currentDraftId='';draftForm=blankDraft();inviteOpen=false;expandedSchedule='';
 archiveMessage=`Cópia restaurada nesta sessão: ${drafts.length} proposição(ões) e ${schedule.length} programação(ões).`;
 archiveIsError=false;render();
 document.querySelector<HTMLButtonElement>('[data-action="import-local-archive"]')?.focus({preventScroll:true});
});
document.addEventListener('submit',(event)=>{
 const form=event.target;if(!(form instanceof HTMLFormElement))return;
 const id=form.id;
 if(!['compose-proposal-form','confirm-proposal-form','schedule-deliberation-form','invite-socii-form'].includes(id))return;
 event.preventDefault();
 const submitter=(event as SubmitEvent).submitter;
 const saveOnly=id==='compose-proposal-form' && submitter instanceof HTMLButtonElement && submitter.value==='save';
 if(!saveOnly && !form.reportValidity())return;
 const data=new FormData(form);
 if(id==='compose-proposal-form'){
  const title=String(data.get('title')??'').trim(),body=String(data.get('body')??'').trim();
  if(saveOnly ? (!title && !body) : (title.length<3||body.length<20)){
   if(saveOnly){
    composeError='Escreva um título ou algum texto antes de salvar.';
    render();
    document.querySelector<HTMLInputElement>('#draft-title')?.focus({preventScroll:true});
   }
   return;
  }
  composeError='';
  draftForm={title,body};
  let d=drafts.find(x=>x.id===currentDraftId);
  let confirmationsReset=false;
  if(!d||d.status==='concluida'){
   d={id:nextLocalRecordId('draft',drafts),title,body,sectionId:'integridade',type:'PDR',authorComplete:false,partners:[],status:'redacao'};drafts.unshift(d);currentDraftId=d.id;
  }else{
   // A confirmation of an earlier text cannot approve a changed version.
   if(d.title!==title||d.body!==body){
    confirmationsReset=d.authorComplete||d.partners.some(p=>p.complete);
    d.authorComplete=false;
    d.partners.forEach(p=>{p.complete=false;});
    d.status='redacao';
   }
   d.title=title;d.body=body;
  }
  const stored=saveWorkflows();
  if(saveOnly){
   workflowNotice=stored?'Rascunho salvo nesta sessão.':'Rascunho mantido somente enquanto a página estiver aberta.';
   if(confirmationsReset)workflowNotice+=' O texto mudou; confirmações anteriores foram reiniciadas nesta prévia.';
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
  workflowNotice=(classificationChanged&&d.partners.length?'A seção ou o tipo mudou; as confirmações do Socii foram reiniciadas nesta prévia. ':'')+
   (saved?(d.status==='concluida'?'Proposição concluída.':'Sua parte foi concluída. Aguardando participantes do Socii.'):'Conclusão aplicada somente nesta aba: não foi possível salvar.');
  navigate('proposals');return;
 }
 if(id==='invite-socii-form'){
  const d=drafts.find(x=>x.id===String(data.get('draftId')??'')),memberId=String(data.get('memberId')??'');
  if(d&&memberId&&memberId!==members[0]?.id&&!d.partners.some(p=>p.id===memberId)){
   d.partners.push({id:memberId,complete:false});if(d.authorComplete)d.status='revisao';
   const saved=saveWorkflows();
   workflowNotice=saved?'Participante incluído na simulação. Nenhum convite real foi enviado.':'Participante incluído apenas nesta aba: não foi possível salvar. Nenhum convite real foi enviado.';
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
  schedule.unshift(item);const stored=saveWorkflows();workflowNotice=stored?'Deliberação programada nesta demonstração.':'Programação mantida somente enquanto a página estiver aberta.';scheduleFormOpen=false;scheduleMethod=null;expandedSchedule=item.id;
  const date=new Date(`${start.slice(0,10)}T12:00:00`);calendarYear=date.getFullYear();calendarMonth=date.getMonth();selectedCalendarDay=start.slice(0,10);
  render();
  // The saved schedule is the result of the form which has just disappeared.
  document.querySelector<HTMLButtonElement>(`[data-schedule="${item.id}"]`)?.focus({preventScroll:true});
  return;
 }
});
document.addEventListener('submit',(event)=>{
 const form=event.target;
 if(!(form instanceof HTMLFormElement)||form.id!=='preview-vote-form'||!advancedPreview)return;
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
 const result=validatePreviewVote(previewMode,payload,selectedMember?.cumulativeVoteWeight,previewVoteChoices().map(option=>option.id));
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
 notice=`Cadastro demonstrativo de ${member.name} atualizado.`;
 editingMemberId=null;render();
 document.querySelector<HTMLButtonElement>('[data-action=undo]')?.focus({preventScroll:true});
});
document.addEventListener('input',(event)=>{
 const target=event.target;
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
document.addEventListener('change',(event)=>{
 const target=event.target;
 if(target instanceof HTMLSelectElement && target.id==='schedule-method' && target.closest('#schedule-deliberation-form')){
  scheduleMethod=isDeliberationMethod(target.value)?target.value:null;render();
  document.querySelector<HTMLSelectElement>('#schedule-method')?.focus({preventScroll:true});return;
 }
 if(advancedPreview && target instanceof HTMLSelectElement && target.id==='preview-vote-method'){
  if(isDeliberationMethod(target.value)){
   previewMode=target.value;previewScheduleId=null;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';previewVoteMemberId='';render();
   document.querySelector<HTMLSelectElement>('#preview-vote-method')?.focus({preventScroll:true});
  }return;
 }
 if(advancedPreview && target instanceof HTMLSelectElement && target.id==='preview-vote-member'){
  previewVoteMemberId=target.value;previewRequestId=null;previewVoteReceipt=null;previewVoteError='';render();
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