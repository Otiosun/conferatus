import { activities, ballots } from './data/fixtures.js';
import { FixtureMemberProvider } from './domain/providers.js';
import { escapeHTML, resultPercentage, totalVotes, updateSectionAssignment, demoteToCommonMember, canRecordVote, restoreDemoMembers, searchKey, isDeliberativeMember, hasPersonalVoteHistory } from './domain/rules.js';
import type { Activity, Member } from './domain/types.js';

type Route = 'ballot' | 'members' | 'profile' | 'overview' | 'governance' | 'calendar' | 'proposals' | 'compose' | 'review';
type Tab = 'votos' | 'proposicoes';
const root = document.querySelector<HTMLDivElement>('#root');
if (!root) throw new Error('Root missing');
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
let filter = '';
let searchExpanded = false;
let directoryExpanded = false;
let expandedActivity = '';
let rolePreview: 'diretor' | 'membro' = 'diretor';
let demoToolsOpen = false;
const advancedPreview = new URLSearchParams(location.search).get('demo') === '1';
let lastChange: {memberId: string; acdmId: string | undefined; sectionIds: string[]; role: Member['role']; hadDeliberativeHistory?: boolean} | null = null;
const initialMembers = new Map(members.map(m=>[m.id,{name:m.name,acdmId:m.acdmId,sectionIds:[...m.sectionIds],role:m.role,hadDeliberativeHistory:m.hadDeliberativeHistory}]));
const demoMembersKey = 'conferatus:demo-members-v07';
function resetDemoState() {
  for (const member of members) {
    const original = initialMembers.get(member.id);
    if (original) { member.name=original.name; member.acdmId=original.acdmId; member.sectionIds=[...original.sectionIds];member.role=original.role;member.hadDeliberativeHistory=original.hadDeliberativeHistory; }
  }
  demoVoteId=null; demoExpanded=false; editingMemberId=null; editError=''; lastChange=null;
  rolePreview='diretor'; demoToolsOpen=false; expandedSection=''; expandedActivity='';
  profileTab='votos'; overviewTab='votos'; overviewExpanded=false; searchExpanded=false; directoryExpanded=false; filter='';
  try { sessionStorage.removeItem(demoMembersKey); sessionStorage.removeItem('conferatus:demo-vote'); } catch {}
}

function saveDemoMembers() {
  try {
    sessionStorage.setItem(demoMembersKey, JSON.stringify(members.map(m=>({id:m.id, acdmId:m.acdmId, sectionIds:m.sectionIds,role:m.role,hadDeliberativeHistory:m.hadDeliberativeHistory}))));
  } catch { /* Preview still works with session storage disabled. */ }
}
function rememberChange(m: Member) {
  lastChange={memberId:m.id,acdmId:m.acdmId,sectionIds:[...m.sectionIds],role:m.role,hadDeliberativeHistory:m.hadDeliberativeHistory};
}
try {
  restoreDemoMembers(members, sections.map(s => s.id), JSON.parse(sessionStorage.getItem(demoMembersKey) ?? 'null'));
} catch { /* Ignore damaged or blocked session data. */ }
let demoVoteId: string | null = null;
let demoExpanded = false;
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
  if(route!=='calendar') scheduleFormOpen=false;
  menuOpen = false;
  demoToolsOpen = false;
  notice = '';
  editError = '';
  lastChange = null;
  const hash = `#/${route}${route==='profile' && memberId?`/${encodeURIComponent(memberId)}`:''}`;
  if (location.hash === hash) render(); else location.hash = hash;
  window.scrollTo({ top: 0, behavior: 'instant' });
}
function crest() { return '<img src="./assets/crest.png" width="29" height="29" alt="Símbolo da Academy">'; }
function footer() {
  return `${menuOpen ? `<nav class="bottom-menu" aria-label="Navegação principal"><div class="menu-list">
    <button class="menu-item" data-route="members" ${routeFromHash()==='members'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="7" r="3"/><path d="M3.5 19v-2.2a5.5 5.5 0 0 1 11 0V19M17 8h4M17 12h4M17 16h4"/></svg></span>Membros e Serviços da Cúpula Cíntia</button>
    <button class="menu-item" data-route="overview" ${routeFromHash()==='overview'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h2M12 9h5M7 13h2M12 13h5M7 17h2M12 17h5"/></svg></span>Histórico de Votações e Proposições</button>
    <button class="menu-item" data-route="calendar" ${routeFromHash()==='calendar'?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true">▦</span>Agendar e Iniciar Deliberação</button>
    <button class="menu-item" data-route="proposals" ${['proposals','compose','review'].includes(routeFromHash())?'aria-current="page"':''}><span class="menu-icon" aria-hidden="true">✎</span>Elaborar Proposição e Socii</button>
  </div></nav>` : ''}
  <footer class="app-footer">${crest()}<button type="button" class="footer-home" data-route="ballot" aria-label="Voltar à votação">CONFERATUS</button><small class="footer-demo">DADOS FICTÍCIOS · PRÉVIA</small>
   <button type="button" class="footer-nav" aria-expanded="${menuOpen}" aria-label="${menuOpen?'Fechar':'Abrir'} menu" data-action="menu">${menuOpen?'Fechar ×':'☰ Menu'}</button>
  </footer>`;
}
function header(title?: string, subtitle?: string, tall=false) {
  if (title) return `<header class="page-header">
   ${advancedPreview?`<button type="button" class="panel-button" data-action="toggle-tools" aria-label="Opções de teste" aria-expanded="${demoToolsOpen}"><img src="./assets/painel.png" alt=""></button>`:`<img class="panel-mark" src="./assets/painel.png" alt="">`}
   <h1>${escapeHTML(title)}</h1>${subtitle?`<p>${escapeHTML(subtitle)}</p>`:''}
   ${advancedPreview && demoToolsOpen?`<aside class="demo-tools" aria-label="Ferramentas de demonstração">
     <strong>Opções de visualização</strong><p>Selecione um perfil para visualizar as permissões.</p>
     <label for="role-mode">Visualizar como</label><select id="role-mode" aria-label="Simular perfil"><option value="diretor" ${rolePreview==='diretor'?'selected':''}>Diretor</option><option value="membro" ${rolePreview==='membro'?'selected':''}>Membro comum</option></select>
     ${expandedSection&&rolePreview==='diretor'?`<div class="tools-divider"><label for="add-member">Vincular à seção aberta</label><div class="tools-add"><select id="add-member"><option value="">Selecione um membro…</option>${members.filter(m=>!m.sectionIds.includes(expandedSection)).map(m=>`<option value="${m.id}">${escapeHTML(m.name)}</option>`).join('')}</select><button type="button" class="small-action" data-action="add-member">Vincular</button></div></div>`:''}
     <button type="button" class="reset-tools" data-action="reset-admin">Reiniciar alterações administrativas</button>
   </aside>`:''}
  </header>`;
  const panelShortcut = routeFromHash()==='overview' ? `<button class="panel-button" data-route="governance" aria-label="Abrir gerenciamento deliberativo" title="Gerenciamento deliberativo"><img src="./assets/painel.png" alt=""></button>` : '';
  return `<header class="hero ${tall?'':'hero--flat'}" aria-label="Faixa azul do CONFERATUS">${panelShortcut}</header>`;
}
function metricRow(m: Member) {
  const personalVotes = hasPersonalVoteHistory(m, sections) ? String(m.totalVotes) : '—';
  return `<div class="metrics" aria-label="Indicadores de participação">
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
   <p>${escapeHTML(m.subtitle)}</p></div>${displayTabs?tabBar(tab, hasPersonalVoteHistory(m, sections)):''}</div>`;
}
function ballotPage() {
 const ballot=ballots[0]; if(!ballot) return '<p>Nenhuma votação disponível.</p>';
 const demoOptions = ballot.options.map(o => ({...o, votes:o.votes + (canRecordVote(ballot) && demoVoteId===o.id?1:0)}));
 const sum=totalVotes(demoOptions);
 return `<div class="main-pad">${header(undefined,undefined,true)}<div class="results">
 ${demoOptions.map(o=>`<div class="result-row ${demoVoteId===o.id?'result-row--chosen':''}" aria-label="${escapeHTML(o.label)}: ${o.votes} votos, ${demoVoteId?(100*o.votes/sum).toFixed(1):resultPercentage(o.votes,sum)} por cento"><span class="result-label">${escapeHTML(o.label)}${demoVoteId===o.id?'<small class="your-vote">Sua escolha</small>':''}</span><span class="result-count">${o.votes} Votos</span><span class="result-percentage">${demoVoteId?(100*o.votes/sum).toFixed(1):resultPercentage(o.votes,sum)}%</span></div>`).join('')}
 </div><hr class="hairline"></div><section class="description-panel"><div class="description-heading"><span>Descrição da votação</span><button class="demo-toggle" type="button" data-action="toggle-demo" aria-expanded="${demoExpanded}">${demoExpanded?'Fechar':canRecordVote(ballot)?'Participar':'Ver situação'}</button></div>
 <p class="ballot-description">${escapeHTML(ballot.description)}</p>${demoExpanded?`<div class="demo-ballot"><h2>${escapeHTML(ballot.title)}</h2><p>${canRecordVote(ballot)?'Votação aberta. Selecione uma opção.':'Esta votação está encerrada. Os resultados permanecem disponíveis para consulta.'}</p>
 ${canRecordVote(ballot)?`<div class="vote-actions">${ballot.options.map(o=>`<button type="button" data-vote="${o.id}" class="vote-button" aria-pressed="${demoVoteId===o.id}">${escapeHTML(o.label)}</button>`).join('')}</div>
 <p class="vote-feedback" role="status">${demoVoteId?'Escolha registrada.':'Selecione uma das opções.'}</p>
 ${demoVoteId?'<button class="reset-vote" type="button" data-action="reset-vote">Alterar escolha</button>':''}`:''}</div>`:''}</section>`;
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
 <div class="member-list" aria-label="Diretório de membros">
 <button type="button" class="search-trigger" data-action="search" aria-expanded="${searchExpanded}" aria-label="${searchExpanded?'Fechar busca de membros':'Buscar membros'}">${searchExpanded?'Fechar busca ×':'Buscar ⌕'}</button>
 ${searchExpanded?`<div class="toolbar"><label for="search-members">Buscar membro</label><input id="search-members" type="search" placeholder="Nome ou identificador" value="${escapeHTML(filter)}" autocomplete="off" aria-controls="member-results"><button type="button" class="clear-search" data-action="clear-search" ${filter?'':'hidden'}>Limpar</button></div>`:''}
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
 const directId=location.hash.replace(/^#\/profile\/?/, '').split('/')[0];
 const chosenId=directId || currentMember;
 const member=members.find(m=>m.id===chosenId);
 if(!member) return `${header(undefined,undefined,false)}<section class="missing-profile" role="status"><strong>Perfil não encontrado</strong><p>Não encontramos um membro com esse identificador.</p><button type="button" data-route="members">Voltar aos membros</button></section>`;
 const personalVotingHistory = hasPersonalVoteHistory(member, sections);
 const activeTab: Tab = personalVotingHistory ? profileTab : 'proposicoes';
 const relevant=activities.filter(a=>a.memberId===member.id && a.type===(activeTab==='votos'?'voto':'proposicao'));
 return `${header(undefined,undefined,false)}${memberHeader(member,activeTab)}<section class="section-body">
 ${relevant.length?relevant.map(activityItem).join(''):'<p class="status-line">Nenhum registro encontrado.</p>'}</section>`;
}
function overviewPage() {
 const votes=activities.filter(a=>a.type==='voto');
 const proposals=activities.filter(a=>a.type==='proposicao');
 const accepted=proposals.filter(a=>a.approved).length;
 const relevant=overviewTab==='votos'?votes:proposals;
 const visible=overviewExpanded?relevant:relevant.slice(0,6);
 const remaining=relevant.length-visible.length;
 return `${header(undefined,undefined,false)}<div class="overview-stats" aria-label="Indicadores institucionais">
  <span class="stat-chip">${accepted} Aprovados</span><span class="stat-chip">${proposals.length-accepted} Arquivados</span>
  <span class="stat-figure">${votes.reduce((n,a)=>n+a.votes,0)} Votos</span>
  <span class="stat-figure">${proposals.length} PDR</span><span class="stat-figure">${String(accepted).padStart(2,'0')} PR</span>
  </div><div class="tabs overview-tabs" role="group" aria-label="Histórico institucional"><button class="tab" data-overview-tab="votos" aria-pressed="${overviewTab==='votos'}">Histórico de votações</button><button class="tab" data-overview-tab="proposicoes" aria-pressed="${overviewTab==='proposicoes'}">Proposições</button></div>
  <section class="section-body overview-content">${visible.length?visible.map(activityItem).join(''):'<p class="status-line">Nenhum registro encontrado.</p>'}
   ${remaining>0?`<button class="overview-more" type="button" data-action="show-more-history">Ver mais ${remaining} ${overviewTab==='votos'?'votações':'proposições'}</button>`:''}
  </section>`;
}
function governancePage() {
 const active=sections.find(s=>s.id===expandedSection);
 return `${header('GERENCIAMENTO DELIBERATIVO','Gerencie as seções e deliberados da Cúpula Institucional Academy.')}
 ${rolePreview==='membro'?'<p class="status-line" role="status">O gerenciamento das seções é exclusivo da diretoria.</p>':
 `<div class="governance-list">${sections.map(s=>`${s.category==='comum'?'<h2 class="governance-group-heading">Membros da Academy</h2>':''}<div><button type="button" class="section-toggle" data-section="${s.id}" aria-expanded="${expandedSection===s.id}"><span>${escapeHTML(s.name)}${s.places ? `<small class="section-capacity">${s.places} integrantes previstos</small>` : ''}</span><span class="section-chevron" aria-hidden="true">${expandedSection===s.id?'▾':'▸'}</span></button>
 ${expandedSection===s.id?`<div>${members.filter(m=>m.sectionIds.includes(s.id)).map(m=>`<div class="section-member"><div class="avatar" aria-hidden="true"></div><button class="section-member-name" type="button" data-edit="${m.id}" title="Editar ${escapeHTML(m.name)}">${escapeHTML(m.name)}</button><button class="icon-button icon-button--edit" type="button" data-edit="${m.id}" aria-label="Editar identificador de ${escapeHTML(m.name)}"><img src="./assets/editar.png" alt=""></button>${s.id==='membros'?'':`<button class="icon-button" type="button" data-demote="${m.id}" aria-label="Rebaixar ${escapeHTML(m.name)} para membro comum"><img src="./assets/rebaixamento.png" alt=""></button>`}</div>
 ${editingMemberId===m.id?`<form class="edit-form" id="edit-member-form" novalidate><label for="member-acdm-id">ACDM ID</label><input id="member-acdm-id" name="acdmId" value="${escapeHTML(m.acdmId ?? '')}" placeholder="DEMO-0001" required minlength="3" maxlength="40" pattern="[A-Za-z0-9_-]+" autocomplete="off" ${editError?'aria-invalid="true" aria-describedby="edit-error"':''}><input type="hidden" name="memberId" value="${m.id}"><button type="submit" class="small-action">Salvar</button>${editError?`<p id="edit-error" class="edit-error" role="alert">${escapeHTML(editError)}</p>`:''}</form>`:''}`).join('')}
 ${members.every(m=>!m.sectionIds.includes(s.id))?'<p class="section-empty">Nenhum membro nesta seção.</p>':''}</div>`:''}</div>`).join('')}</div>`}
 ${notice?`<p class="status-line" role="status">${escapeHTML(notice)} ${lastChange?'<button type="button" class="undo-action" data-action="undo">Desfazer</button>':''}</p>`:''}`;
}

// Only the preview data changes here. Authentication and shared records remain external.
type ProposalType = 'PDR' | 'PR' | 'Ofício';
type Draft = {id:string;title:string;body:string;sectionId:string;type:ProposalType;authorComplete:boolean;partners:{id:string;complete:boolean}[];status:'redacao'|'revisao'|'concluida'};
type Deliberation = {id:string;title:string;objective:string;proposalId:string;sectionId:string;start:string;end:string;type:string;status:'programada'|'cancelada'};
const draftKey='conferatus:proposals-v010';
const deliberationKey='conferatus:deliberations-v010';
function readSessionArray<T>(key:string):T[]{
 try {const value=JSON.parse(sessionStorage.getItem(key)??'[]');return Array.isArray(value)?value:[];}catch{return [];}
}
const drafts:Draft[]=readSessionArray<Draft>(draftKey).filter(d=>typeof d?.id==='string'&&typeof d?.title==='string');
const schedule:Deliberation[]=readSessionArray<Deliberation>(deliberationKey).filter(d=>typeof d?.id==='string'&&typeof d?.title==='string');
const blankDraft=()=>({title:'',body:''});
let draftForm=blankDraft();
let currentDraftId='';
let workflowNotice='';
let scheduleFormOpen=false;
let expandedSchedule='sample-1';
let inviteOpen=false;
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
  const current=day===isoDay(today);
  return `<button type="button" class="calendar-day${selected?' calendar-day--selected':''}${current?' calendar-day--today':''}" data-calendar-day="${day}" aria-pressed="${selected}" aria-label="${new Intl.DateTimeFormat('pt-BR',{dateStyle:'full'}).format(new Date(calendarYear,calendarMonth,n+1))}${events?`, ${events} programação${events===1?'':'ões'}`:''}"><span>${n+1}</span>${events?`<i aria-hidden="true" class="calendar-marker"></i>`:''}</button>`;
 });
 return `<div class="calendar-hero"><div class="calendar-toolbar"><h1>CALENDÁRIO</h1><div class="calendar-month-nav"><button type="button" data-action="calendar-prev" aria-label="Mês anterior">‹</button><h2 aria-live="polite">${escapeHTML(monthLabel)}</h2><button type="button" data-action="calendar-next" aria-label="Próximo mês">›</button></div></div><div class="calendar-grid" aria-label="Dias do mês">${['D','S','T','Q','Q','S','S'].map(d=>`<span class="calendar-weekday">${d}</span>`).join('')}${'<span class="calendar-empty"></span>'.repeat(offset)}${days.join('')}</div><div class="calendar-foot"><span><i class="calendar-marker" aria-hidden="true"></i> Dia programado</span><button type="button" data-action="calendar-today">Hoje</button></div></div>`;
}
function saveWorkflows(){
 try{sessionStorage.setItem(draftKey,JSON.stringify(drafts));sessionStorage.setItem(deliberationKey,JSON.stringify(schedule));}catch{}
}
function selectOptions(selected:string,items:{id:string;name:string}[]){return items.map(x=>`<option value="${escapeHTML(x.id)}" ${selected===x.id?'selected':''}>${escapeHTML(x.name)}</option>`).join('');}
function draftReady(d:Draft){return d.authorComplete&&d.partners.every(p=>p.complete);}
function friendlyStamp(date:string){const parsed=new Date(date);return Number.isNaN(parsed.getTime())?'Data não definida':parsed.toLocaleString('pt-BR',{dateStyle:'short',timeStyle:'short'});}
function proposalsPage(){
 const author=members[0];
 const examples=activities.filter(a=>a.type==='proposicao').slice(0,4);
 return `${header(undefined,undefined,false)}<div class="workflow-head"><h1>Proposições e Socii</h1><p>${escapeHTML(author?.name??'Membro')}</p></div>
 <div class="workflow-layout"><div class="workflow-metrics"><span>${author?.totalVotes??0} Votos</span><span>${author?.proposals??0} PDR</span><span>${author?.approved??0} PR</span><span>${author?.officialLetters??0} Ofício</span><span>${author?.collaborations??0} Socii</span></div>
 <div class="tabs workflow-tabs"><button class="tab" data-route="profile" aria-label="Consultar histórico de votação">Histórico de votações</button><button class="tab" aria-pressed="true">Proposições e Socii</button></div>
 ${drafts.length?drafts.map(d=>`<article class="workflow-record"><button data-draft="${escapeHTML(d.id)}" class="workflow-record-btn"><strong>${escapeHTML(d.title||'Rascunho sem título')}</strong><small>${d.status==='concluida'?'Concluída':d.status==='revisao'?'Aguardando Socii':'Em redação'} · ${escapeHTML(d.type)}</small><p>${escapeHTML(d.body.slice(0,140))}</p></button>${d.partners.length?`<p class="workflow-partners">Socii: ${d.partners.map(p=>`${escapeHTML(members.find(m=>m.id===p.id)?.name??'Membro')} (${p.complete?'concluiu':'pendente'})`).join(', ')}</p>`:''}${advancedPreview&&d.partners.some(p=>!p.complete)?d.partners.filter(p=>!p.complete).map(p=>`<button class="workflow-demo-confirm" data-confirm-partner="${escapeHTML(d.id)}:${escapeHTML(p.id)}">Simular conclusão de ${escapeHTML(members.find(m=>m.id===p.id)?.name??'participante')}</button>`).join(''):''}</article>`).join(''):''}
 ${examples.map(a=>`<article class="workflow-record"><strong>${escapeHTML(a.title)}</strong><small>${escapeHTML(a.code)}</small><p>${escapeHTML(a.summary)}</p></article>`).join('')}
 </div><div class="workflow-actions"><button type="button" class="workflow-outline" data-action="invite-socii">Convidar para Socii</button>${inviteOpen?`<form id="invite-socii-form" class="workflow-inline"><label>Proposição<select name="draftId" required>${drafts.filter(d=>d.status!=='concluida').map(d=>`<option value="${escapeHTML(d.id)}">${escapeHTML(d.title)}</option>`).join('')}</select></label><label>Participante<select name="memberId" required>${selectOptions('',members.slice(1))}</select></label><button class="workflow-primary" ${!drafts.some(d=>d.status!=='concluida')?'disabled':''}>Adicionar participante</button></form>`:''}
 <button type="button" class="workflow-primary" data-action="new-proposal">Redigir proposição</button></div>
 ${workflowNotice?`<p role="status" class="workflow-status">${escapeHTML(workflowNotice)}</p>`:''}`;
}
function composePage(){
 return `<div class="workflow-editor-head"><span>CONFERATUS</span><h1>${escapeHTML(draftForm.title||'Título')}</h1></div>
 <form id="compose-proposal-form" class="workflow-editor"><label for="draft-title">Título da proposição</label><input id="draft-title" name="title" maxlength="140" required placeholder="Título" value="${escapeHTML(draftForm.title)}">
 <label for="draft-body">Redação</label><textarea id="draft-body" name="body" required minlength="20" placeholder="Escreva...">${escapeHTML(draftForm.body)}</textarea>
 <div class="workflow-editor-actions"><button class="workflow-primary" type="submit" name="intent" value="conclude">Concluir redação</button><button class="workflow-outline" type="submit" name="intent" value="save" formnovalidate>Salvar rascunho</button><button class="workflow-outline" type="button" data-route="proposals">Voltar</button></div></form>`;
}
function reviewPage(){
 const d=drafts.find(x=>x.id===currentDraftId);if(!d)return proposalsPage();
 if(d.status==='concluida')return `<div class="workflow-editor-head"><span>CONFERATUS</span><h1>${escapeHTML(d.title)}</h1></div><div class="workflow-review-body"><p>${escapeHTML(d.body)}</p></div><div class="workflow-review-panel"><div class="workflow-finished"><strong>Proposição concluída</strong><p>Seção: ${escapeHTML(sections.find(s=>s.id===d.sectionId)?.name??'Não definida')} · ${escapeHTML(d.type)}</p><button type="button" class="workflow-primary" data-route="proposals">Voltar às proposições</button></div></div>`;
 return `<div class="workflow-editor-head"><span>CONFERATUS</span><h1>${escapeHTML(d.title)}</h1></div>
 <div class="workflow-review-body"><p>${escapeHTML(d.body)}</p></div>
 <div class="workflow-review-panel"><form id="confirm-proposal-form" class="workflow-form"><p>Confira os dados e a redação antes de confirmar a conclusão.</p>
 <label>Seção responsável<select name="sectionId" required>${selectOptions(d.sectionId,sections.filter(s=>s.category==='deliberativa'))}</select></label>
 <label>Tipo de proposição<select name="type" required>${['PDR','PR','Ofício'].map(t=>`<option value="${t}" ${t===d.type?'selected':''}>${t}</option>`).join('')}</select></label>
 <div class="workflow-review-buttons"><button type="button" class="workflow-outline" data-route="compose">Voltar</button><button class="workflow-primary" type="submit">Confirmar conclusão</button></div></form></div>`;
}
function calendarPage(){
 const sample=[{id:'sample-1',title:'Revisão do calendário de reuniões',sectionId:'integridade',objective:'Organizar o calendário de reuniões institucionais.',start:'2026-11-22T14:00',end:'2026-11-23T14:00',type:'PDR',proposalId:'',status:'programada' as const}];
 const all=[...sample,...schedule.filter(s=>s.status==='programada')]
  .sort((a,b)=>a.start.localeCompare(b.start));
 const visible=selectedCalendarDay?all.filter(item=>item.start.slice(0,10)<=selectedCalendarDay&&item.end.slice(0,10)>=selectedCalendarDay):all;
 return `<div class="workflow-layout">${calendarGrid(all)}<button class="workflow-open" type="button" data-action="open-schedule" aria-expanded="${scheduleFormOpen}">${scheduleFormOpen?'Fechar agendamento':'Iniciar uma Votação'}</button>
 ${scheduleFormOpen?`<form id="schedule-deliberation-form" class="workflow-form workflow-schedule-form"><h2>Programar deliberação</h2>
 ${!drafts.some(d=>d.status==='concluida')?'<p class="workflow-help">Para agendar, conclua uma proposição primeiro. <button type="button" data-route="proposals">Ir às proposições</button></p>':''}
 <label>Título da deliberação<input name="title" maxlength="140" required placeholder="Título da deliberação"></label>
 <label>Descrição objetiva<textarea name="objective" required minlength="15" rows="3" placeholder="Descrição objetiva"></textarea></label>
 <label>Selecione a proposição<select name="proposalId" required ${!drafts.some(d=>d.status==='concluida')?'disabled':''}><option value="">Selecione</option>${drafts.filter(d=>d.status==='concluida').map(d=>`<option value="${escapeHTML(d.id)}">${escapeHTML(d.title)}</option>`).join('')}</select></label>
 <label>Seção deliberativa<select name="sectionId" required>${selectOptions('integridade',sections.filter(s=>s.category==='deliberativa'))}</select></label>
 <div class="workflow-grid-two"><label>Data e hora de início<input type="datetime-local" name="start" required></label><label>Data e hora de encerramento<input type="datetime-local" name="end" required></label></div>
 <label>Tipo de deliberação<select name="type" required><option value="PDR">PDR</option><option value="PR">PR</option><option value="Ofício">Ofício</option></select></label>
 <button class="workflow-primary" type="submit" ${!drafts.some(d=>d.status==='concluida')?'disabled':''}>Confirmar programação</button></form>`:''}
 ${workflowNotice?`<p role="status" class="workflow-status">${escapeHTML(workflowNotice)}</p>`:''}
 <div class="calendar-list"><div class="calendar-list-head"><h2>${selectedCalendarDay?`Programações em ${new Date(`${selectedCalendarDay}T12:00`).toLocaleDateString('pt-BR')}`:'Programações'}</h2>${selectedCalendarDay?'<button type="button" data-action="calendar-all">Ver todas</button>':''}</div>${visible.length===0?'<p class="calendar-empty-message">Nenhuma programação nesta data.</p>':''}${visible.map(item=>`<article class="calendar-item"><button type="button" data-schedule="${escapeHTML(item.id)}" aria-expanded="${expandedSchedule===item.id}"><strong>${escapeHTML(item.title)}</strong><small>${friendlyStamp(item.start)} até ${friendlyStamp(item.end)}</small><span>Seção: ${escapeHTML(sections.find(s=>s.id===item.sectionId)?.name??'')}</span></button>
 ${expandedSchedule===item.id?`<div class="calendar-expanded"><div class="calendar-status">${escapeHTML(item.type)} <strong>PROPOSIÇÃO EM DELIBERAÇÃO</strong></div><p>${escapeHTML(item.objective)}</p>${item.proposalId?`<button type="button" class="calendar-proposal-link" data-open-schedule-proposal="${escapeHTML(item.proposalId)}">Ver proposição associada</button>`:''}<button type="button" data-cancel-schedule="${escapeHTML(item.id)}" ${item.id==='sample-1'?'disabled title="Exemplo fixo"':''}>Cancelar programação deliberativa</button></div>`:''}</article>`).join('')}</div></div>`;
}

let lastRenderedHash = location.hash;
function render() {
 if (!root) return;
 // A local edit must not unexpectedly jump the user to the top of a long page.
 const previousScroll = window.scrollY;
 const preserveScroll = location.hash === lastRenderedHash;
 lastRenderedHash = location.hash;
 // Keep keyboard focus on the same action after updating the preview DOM.
 const active = document.activeElement;
 const attributes = ['data-vote','data-tab','data-overview-tab','data-section','data-activity','data-action','data-calendar-day'];
 const focusTarget = active instanceof HTMLElement
   ? attributes.map(attr => [attr, active.getAttribute(attr)] as const).find(([,value]) => value!==null)
   : undefined;
 const route=routeFromHash();
 const page=route==='ballot'?ballotPage():route==='members'?memberList():route==='profile'?profilePage():route==='overview'?overviewPage():route==='calendar'?calendarPage():route==='proposals'?proposalsPage():route==='compose'?composePage():route==='review'?reviewPage():governancePage();
 root.innerHTML=`<div class="app-shell" aria-label="CONFERATUS — dados fictícios"><a href="#main-content" class="skip-link">Ir para o conteúdo</a><main id="main-content" tabindex="-1">${page}</main>${footer()}
</div>`;
 if (focusTarget) {
  const [attr,value]=focusTarget;
  [...root.querySelectorAll<HTMLElement>(`[${attr}]`)]
   .find(element=>element.getAttribute(attr)===value)?.focus({preventScroll:true});
 }
 if (preserveScroll) window.scrollTo({top:previousScroll,behavior:'instant'});
}
function syncRouteState() {
 const [route,id] = location.hash.replace(/^#\/?/, '').split('/');
 if(route==='profile' && id && members.some(member=>member.id===id)) currentMember=id;
}
window.addEventListener('hashchange',()=>{menuOpen=false;demoToolsOpen=false;syncRouteState();render();});
// Megalos' interaction: swipe the CONFERATUS name upwards to reveal navigation.
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
  else if(editingMemberId){editingMemberId=null;render();document.querySelector<HTMLButtonElement>('[data-section][aria-expanded=true]')?.focus();}
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
 if(actionEl?.dataset.action==='undo'&&lastChange){
  const member=members.find(m=>m.id===lastChange?.memberId);
  if(member){member.acdmId=lastChange.acdmId;member.sectionIds=[...lastChange.sectionIds];member.role=lastChange.role;member.hadDeliberativeHistory=lastChange.hadDeliberativeHistory;saveDemoMembers();}
  lastChange=null;notice='Alteração desfeita.';render();return;
 }
 if(advancedPreview && actionEl?.dataset.action==='toggle-tools'){demoToolsOpen=!demoToolsOpen;render();document.querySelector<HTMLButtonElement>('[data-action=toggle-tools]')?.focus();return;}
 if(advancedPreview && actionEl?.dataset.action==='reset-admin'){
  for(const member of members){const original=initialMembers.get(member.id);if(original){member.name=original.name;member.acdmId=original.acdmId;member.sectionIds=[...original.sectionIds];member.role=original.role;member.hadDeliberativeHistory=original.hadDeliberativeHistory;}}
  editingMemberId=null;lastChange=null;notice='Alterações restauradas.';rolePreview='diretor';demoToolsOpen=false;try{sessionStorage.removeItem(demoMembersKey);}catch{}render();return;
 }
 if(actionEl?.dataset.action==='show-more-members'){directoryExpanded=true;render();return;}
 if(actionEl?.dataset.action==='show-more-history'){overviewExpanded=true;render();return;}
 if(actionEl?.dataset.action==='search'){searchExpanded=!searchExpanded;if(!searchExpanded)filter='';render();if(searchExpanded)document.querySelector<HTMLInputElement>('#search-members')?.focus();return;}
 if(actionEl?.dataset.action==='clear-search'){filter='';render();document.querySelector<HTMLInputElement>('#search-members')?.focus();return;}
 if(actionEl?.dataset.action==='toggle-demo'){demoExpanded=!demoExpanded;render();return;}
 if(actionEl?.dataset.action==='reset-vote'){demoVoteId=null;try{sessionStorage.removeItem('conferatus:demo-vote');}catch{}render();return;}
 if (actionEl?.dataset.action==='menu') {menuOpen=!menuOpen; render(); (menuOpen?document.querySelector<HTMLButtonElement>('.menu-item'):document.querySelector<HTMLButtonElement>('.footer-nav'))?.focus(); return;}
 if (routeEl?.classList.contains('footer-home') && Date.now() < suppressFooterHomeClickUntil) {return;}

 if(advancedPreview){const partnerEl=target.closest<HTMLElement>('[data-confirm-partner]');
  if(partnerEl?.dataset.confirmPartner){const [draftId,partnerId]=partnerEl.dataset.confirmPartner.split(':');const d=drafts.find(d=>d.id===draftId);const partner=d?.partners.find(p=>p.id===partnerId);if(d&&partner){partner.complete=true;d.status=draftReady(d)?'concluida':'revisao';saveWorkflows();workflowNotice=d.status==='concluida'?'Todas as partes concluíram. Proposição concluída.':'Participação registrada nesta simulação.';render();}return;}}
 if(actionEl?.dataset.action==='new-proposal'){currentDraftId='';draftForm=blankDraft();workflowNotice='';navigate('compose');return;}
 if(actionEl?.dataset.action==='invite-socii'){inviteOpen=!inviteOpen;render();return;}
 if(actionEl?.dataset.action==='open-schedule'){scheduleFormOpen=!scheduleFormOpen;workflowNotice='';render();return;}
 if(actionEl?.dataset.action==='calendar-prev'){calendarShift(-1);render();return;}
 if(actionEl?.dataset.action==='calendar-next'){calendarShift(1);render();return;}
 if(actionEl?.dataset.action==='calendar-today'){calendarYear=today.getFullYear();calendarMonth=today.getMonth();selectedCalendarDay=isoDay(today);render();return;}
 if(actionEl?.dataset.action==='calendar-all'){selectedCalendarDay='';render();return;}
 const dayEl=target.closest<HTMLElement>('[data-calendar-day]');
 if(dayEl?.dataset.calendarDay){selectedCalendarDay=selectedCalendarDay===dayEl.dataset.calendarDay?'':dayEl.dataset.calendarDay;render();return;}
 const draftEl=target.closest<HTMLElement>('[data-draft]');
 if(draftEl?.dataset.draft){const d=drafts.find(x=>x.id===draftEl.dataset.draft);if(d){currentDraftId=d.id;draftForm={title:d.title,body:d.body};navigate(d.status==='redacao'?'compose':'review');}return;}
 const scheduleEl=target.closest<HTMLElement>('[data-schedule]');
 if(scheduleEl?.dataset.schedule){expandedSchedule=expandedSchedule===scheduleEl.dataset.schedule?'':scheduleEl.dataset.schedule;render();return;}
 const proposalEl=target.closest<HTMLElement>('[data-open-schedule-proposal]');
 if(proposalEl?.dataset.openScheduleProposal){
  const d=drafts.find(x=>x.id===proposalEl.dataset.openScheduleProposal);
  if(d){currentDraftId=d.id;draftForm={title:d.title,body:d.body};navigate('review');}
  return;
 }
 const cancelEl=target.closest<HTMLElement>('[data-cancel-schedule]');
 if(cancelEl?.dataset.cancelSchedule){const item=schedule.find(x=>x.id===cancelEl.dataset.cancelSchedule);if(item){item.status='cancelada';saveWorkflows();workflowNotice='Programação cancelada.';render();}return;}
 if (routeEl?.dataset.route) {navigate(routeEl.dataset.route as Route);return;}
 if (memberEl?.dataset.member) {currentMember=memberEl.dataset.member;profileTab='votos';navigate('profile', currentMember);return;}
 if (tabEl) {if (tabEl.dataset.overviewTab){overviewTab=tabEl.dataset.overviewTab as Tab;overviewExpanded=false;expandedActivity='';} else profileTab=tabEl.dataset.tab as Tab; if(routeFromHash()==='members'){currentMember=members[0]?.id??'m01';navigate('profile', currentMember);}else{render();}return;}
 if (sectionEl?.dataset.section) {expandedSection=expandedSection===sectionEl.dataset.section?'':sectionEl.dataset.section;editingMemberId=null;editError='';notice='';lastChange=null;demoToolsOpen=false;render();return;}
 if (editEl?.dataset.edit) {editingMemberId=editingMemberId===editEl.dataset.edit?null:editEl.dataset.edit;editError='';render();if(editingMemberId)document.querySelector<HTMLInputElement>('#member-acdm-id')?.focus();return;}
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
  if(member){rememberChange(member);member.sectionIds=updateSectionAssignment(member,expandedSection,true).member.sectionIds;saveDemoMembers();notice=`${member.name} adicionado à seção.`;demoToolsOpen=false;render();}
 }
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
   workflowNotice='Escreva um título ou algum texto antes de salvar.';
   if(saveOnly)render();
   return;
  }
  draftForm={title,body};
  let d=drafts.find(x=>x.id===currentDraftId);
  if(!d||d.status==='concluida'){
   d={id:`draft-${Date.now().toString(36)}`,title,body,sectionId:'integridade',type:'PDR',authorComplete:false,partners:[],status:'redacao'};drafts.unshift(d);currentDraftId=d.id;
  }else{d.title=title;d.body=body;}
  saveWorkflows();
  if(saveOnly){workflowNotice='Rascunho salvo neste navegador.';navigate('proposals');}
  else navigate('review');
  return;
 }
 if(id==='confirm-proposal-form'){
  const d=drafts.find(x=>x.id===currentDraftId);if(!d)return;
  d.sectionId=String(data.get('sectionId')??'integridade');d.type=String(data.get('type')??'PDR') as ProposalType;
  d.authorComplete=true;d.status=draftReady(d)?'concluida':'revisao';saveWorkflows();workflowNotice=d.status==='concluida'?'Proposição concluída.':'Sua parte foi concluída. Aguardando participantes do Socii.';navigate('proposals');return;
 }
 if(id==='invite-socii-form'){
  const d=drafts.find(x=>x.id===String(data.get('draftId')??'')),memberId=String(data.get('memberId')??'');
  if(d&&memberId&&memberId!==members[0]?.id&&!d.partners.some(p=>p.id===memberId)){
   d.partners.push({id:memberId,complete:false});if(d.authorComplete)d.status='revisao';saveWorkflows();workflowNotice='Participante incluído na simulação. Nenhum convite real foi enviado.';
  }else workflowNotice='Selecione uma pessoa que ainda não esteja no Socii.';
  inviteOpen=false;render();return;
 }
 if(id==='schedule-deliberation-form'){
  const title=String(data.get('title')??'').trim(),objective=String(data.get('objective')??'').trim();
  const start=String(data.get('start')??''),end=String(data.get('end')??'');
  if(!title||!objective||!start||!end||new Date(start).getTime()>=new Date(end).getTime()){
   const message='Confira o título, a descrição e o período: o encerramento deve ser posterior ao início.';
   const old=form.querySelector<HTMLElement>('.workflow-form-error');
   if(old)old.textContent=message;
   else form.insertAdjacentHTML('afterbegin',`<p class="workflow-form-error" role="alert">${message}</p>`);
   return;
  }
  const proposalId=String(data.get('proposalId')??'');
  if(!drafts.some(d=>d.id===proposalId&&d.status==='concluida')){
   const message='Selecione uma proposição concluída.';
   const old=form.querySelector<HTMLElement>('.workflow-form-error');
   if(old)old.textContent=message;
   else form.insertAdjacentHTML('afterbegin',`<p class="workflow-form-error" role="alert">${message}</p>`);
   return;
  }
  const item:Deliberation={id:`sched-${Date.now().toString(36)}`,title,objective,proposalId,sectionId:String(data.get('sectionId')??''),start,end,type:String(data.get('type')??''),status:'programada'};
  schedule.unshift(item);saveWorkflows();workflowNotice='Deliberação programada nesta demonstração.';scheduleFormOpen=false;expandedSchedule=item.id;
  const date=new Date(`${start.slice(0,10)}T12:00:00`);calendarYear=date.getFullYear();calendarMonth=date.getMonth();selectedCalendarDay=start.slice(0,10);
  render();return;
 }
});
document.addEventListener('submit',(event)=>{
 const form=event.target;
 if(!(form instanceof HTMLFormElement)||form.getAttribute('id')!=='edit-member-form') return;
 event.preventDefault();
 const data=new FormData(form), member=members.find(m=>m.id===data.get('memberId'));
 const acdmId=String(data.get('acdmId')??'').trim().toUpperCase();
 if(!member) return;
 if(!/^[A-Z0-9_-]{3,40}$/.test(acdmId)) {
  editError='Use de 3 a 40 caracteres: letras, números, hífen ou sublinhado.';
  notice='';render();
  document.querySelector<HTMLInputElement>('#member-acdm-id')?.focus({preventScroll:true});
  return;
 }
 if(members.some(m=>m.id!==member.id && m.acdmId===acdmId)){
  editError='Este identificador já pertence a outro membro.';notice='';render();
  const field=document.querySelector<HTMLInputElement>('#member-acdm-id');field?.focus({preventScroll:true});field?.select();return;
 }
 editError='';rememberChange(member);member.acdmId=acdmId;saveDemoMembers();
 notice=`Identificador de ${member.name} atualizado.`;
 editingMemberId=null;render();
 document.querySelector<HTMLButtonElement>('[data-action=undo]')?.focus({preventScroll:true});
});
document.addEventListener('input',(event)=>{
 const target=event.target;
 if(target instanceof HTMLInputElement&&target.id==='search-members') {
  filter=target.value;
  updateMemberSearch();
 }
});
document.addEventListener('change',(event)=>{
 const target=event.target;
 if(advancedPreview && target instanceof HTMLSelectElement&&target.id==='role-mode'){rolePreview=target.value==='membro'?'membro':'diretor';render();}
});
syncRouteState();
render();