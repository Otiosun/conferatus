import assert from 'node:assert/strict';
import test from 'node:test';
import { totalVotes, resultPercentage, updateSectionAssignment, demoteToCommonMember, canRecordVote, escapeHTML, restoreDemoMembers, searchKey, isDeliberativeMember, hasPersonalVoteHistory, DELIBERATION_METHODS, isDeliberationMethod, isPositiveCumulativeVoteWeight, PREVIEW_BINARY_OPTIONS, PREVIEW_LIST_OPTIONS, validatePreviewVote } from '../dist/domain/rules.js';
import { members as fixtures } from '../dist/data/fixtures.js';

test('count results from options and never hard-code them', () => {
 assert.equal(totalVotes([{id:'a',label:'A',votes:80},{id:'b',label:'B',votes:20}]),100);
 assert.equal(resultPercentage(80,100),80);
 assert.equal(resultPercentage(2,3),67);
 assert.equal(resultPercentage(0,0),0);
});
test('removing role association preserves original profile and historical counters', () => {
 const before={...fixtures[0],sectionIds:[...fixtures[0].sectionIds]};
 const {member:after,change}=updateSectionAssignment(before,'coordenacao',false);
 assert.deepEqual(before.sectionIds,['coordenacao']);
 assert.deepEqual(after.sectionIds,[]);
 assert.equal(after.totalVotes,before.totalVotes);
 assert.equal(after.proposals,before.proposals);
 assert.equal(change.kind,'desvinculo');
});
test('adding an existing section is idempotent',()=>{
 const member=fixtures[0];
 const {member:after}=updateSectionAssignment(member,'coordenacao',true);
 assert.equal(after.sectionIds.filter(x=>x==='coordenacao').length,1);
});
test('escape untrusted display strings',()=>{
 assert.equal(escapeHTML('<img src=x onerror="x">'),'&lt;img src=x onerror=&quot;x&quot;&gt;');
});

test('lookup ignores accents and accepts demo identifiers', () => {
 assert.equal(searchKey('João'), searchKey('joao'));
 assert.equal(searchKey('  DEMO-0002  '), 'demo-0002');
});
test('reloading damaged demo data never imports unknown sections, unknown members or duplicate IDs', () => {
 const data=fixtures.slice(0,2).map(m=>({...m, sectionIds:[...m.sectionIds]}));
 restoreDemoMembers(data, ['coordenacao'], [
  {id:data[0].id, acdmId:'DEMO-NEW', sectionIds:['coordenacao','unexpected','coordenacao']},
  {id:data[1].id, acdmId:'DEMO-NEW', sectionIds:['unexpected']},
  {id:'fake', acdmId:'DEMO-NEW'}
 ]);
 assert.equal(data[0].acdmId,'DEMO-NEW');
 assert.equal(data[1].acdmId,'DEMO-0002');
 assert.deepEqual(data[0].sectionIds,['coordenacao']);
 assert.deepEqual(data[1].sectionIds,[]);
});


test('demotion moves a leader into common members without deleting activity or metrics', () => {
 const prior = {...fixtures[0], sectionIds:[...fixtures[0].sectionIds]};
 const {member,change} = demoteToCommonMember(prior);
 assert.equal(prior.role, 'diretor');
 assert.equal(member.role, 'membro');
 assert.deepEqual(member.sectionIds, ['membros']);
 assert.equal(change.kind, 'rebaixamento');
 assert.equal(change.previousRole, 'diretor');
 assert.deepEqual(change.previousSectionIds, ['coordenacao']);
 assert.equal(member.totalVotes,prior.totalVotes);
 assert.equal(member.proposals,prior.proposals);
 const activities = [{id:'old-vote', memberId:prior.id}];
 assert.deepEqual(activities.filter(a=>a.memberId===member.id),activities);
});
test('a finished ballot never accepts a new simulated vote', () => {
 assert.equal(canRecordVote({id:'x',title:'Exemplo',section:'Academy',status:'encerrada',description:'',options:[]}),false);
 assert.equal(canRecordVote({id:'y',title:'Exemplo',section:'Academy',status:'aberta',description:'',options:[]}),true);
});
test('fixture uses only invented identities and the 16-record demonstration structure', async () => {
 assert.equal(fixtures.length,16);
 assert.ok(fixtures.every(m=>m.acdmId?.startsWith('DEMO-') && /^m\d{2}$/.test(m.id)));
 assert.equal(new Set(fixtures.map(m=>m.acdmId)).size,16);
 assert.ok(fixtures.every(m=>m.sectionIds.length>0));
});

test('browser-restored valid member role persists without adding new identities', () => {
 const m={...fixtures[0],role:'diretor',sectionIds:['coordenacao']};
 restoreDemoMembers([m],['membros','coordenacao'], [{id:m.id,role:'membro',sectionIds:['membros']}]);
 assert.equal(m.role,'membro');
 assert.deepEqual(m.sectionIds,['membros']);
});

test('demo history gives every member distinct proposals with meaningful context', async () => {
 const {activities,sections} = await import('../dist/data/fixtures.js');
 const sectionNames = new Set(sections.map(s=>`Seção: ${s.name}`));
 const ids = new Set(activities.map(a=>a.id));
 assert.equal(ids.size,activities.length,'activity IDs must be unique');
 for (const member of fixtures) {
  const memberActivities = activities.filter(a=>a.memberId===member.id);
  const proposals = memberActivities.filter(a=>a.type==='proposicao');
  assert.ok(proposals.length>=2,`${member.id} needs at least two example proposals`);
  assert.equal(new Set(proposals.map(a=>a.title)).size,proposals.length,`${member.id} has repeated proposal titles`);
  assert.ok(memberActivities.every(a=>a.summary.length>=32 && a.title.length>10));
 }
 assert.ok(activities.filter(a=>a.id.startsWith('sample-')).every(a=>sectionNames.has(a.section)));
});

test('demo proposals do not rely on one repeated placeholder for all members', async () => {
 const {activities}=await import('../dist/data/fixtures.js');
 const proposals=activities.filter(a=>a.type==='proposicao');
 assert.ok(new Set(proposals.map(a=>a.title)).size>=proposals.length-1);
 assert.ok(new Set(proposals.map(a=>a.summary)).size>=proposals.length-1);
});

test('CINSTIA consists of four deliberative sections and a separate Academy roster', async () => {
 const {sections}=await import('../dist/data/fixtures.js');
 const deliberative=sections.filter(s=>s.category==='deliberativa');
 assert.deepEqual(deliberative.map(s=>s.name),['Diretoria','Coordenação','Conselho de Integridade','Representantes Devos']);
 assert.deepEqual(deliberative.map(s=>s.places),[4,8,12,24]);
 assert.equal(sections.filter(s=>s.category==='comum').length,1);
});

test('personal voting eligibility depends on deliberative section membership, not director role', async () => {
 const {sections}=await import('../dist/data/fixtures.js');
 const common={...fixtures[0],role:'diretor',sectionIds:['membros']};
 const deliberative={...fixtures[0],role:'membro',sectionIds:['coordenacao']};
 assert.equal(isDeliberativeMember(common,sections),false);
 assert.equal(isDeliberativeMember(deliberative,sections),true);
 assert.equal(isDeliberativeMember({...deliberative,sectionIds:[]},sections),false);
});

test('demoted deliberative retains voting history, ordinary member has none', async () => {
 const {sections,activities}=await import('../dist/data/fixtures.js');
 const source={...fixtures[0],sectionIds:[...fixtures[0].sectionIds]};
 const demoted=demoteToCommonMember(source).member;
 assert.equal(isDeliberativeMember(demoted,sections),false);
 assert.equal(hasPersonalVoteHistory(demoted,sections),true);
 assert.equal(hasPersonalVoteHistory(fixtures[11],sections),false);
 assert.equal(activities.some(a=>a.memberId==='m12' && a.type==='voto'),false);
});
test('restoring demoted status preserves prior deliberative voting history', async () => {
 const {sections}=await import('../dist/data/fixtures.js');
 const member={...fixtures[0],sectionIds:['coordenacao']};
 const after=demoteToCommonMember(member).member;
 const copy={...member,sectionIds:[...member.sectionIds]};
 restoreDemoMembers([copy],sections.map(s=>s.id),[{id:after.id,sectionIds:after.sectionIds,role:after.role,hadDeliberativeHistory:after.hadDeliberativeHistory}]);
 assert.equal(copy.role,'membro');
 assert.equal(hasPersonalVoteHistory(copy,sections),true);
});

test('Megalos defined six distinct voting modalities independent of proposal types', () => {
 const ids=DELIBERATION_METHODS.map(mode=>mode.id);
 assert.deepEqual(ids,['binaria','nominal','ordenada','aprovacao','escalar','cumulativa']);
 assert.ok(DELIBERATION_METHODS.every(mode=>mode.label.length>3 && mode.detail.length>10));
 assert.ok(ids.every(isDeliberationMethod));
 assert.equal(isDeliberationMethod('PDR'),false);
 assert.equal(isDeliberationMethod('unlisted'),false);
 assert.equal(isDeliberationMethod({id:'binaria'}),false);
});

test('cumulative weight is an optional explicit positive integer, never a default', () => {
 for(const value of [1,4,100,Number.MAX_SAFE_INTEGER]) assert.equal(isPositiveCumulativeVoteWeight(value),true);
 for(const value of [0,-1,1.5,NaN,Infinity,'4',null,undefined,Number.MAX_SAFE_INTEGER+1]) assert.equal(isPositiveCumulativeVoteWeight(value),false);
 const m={...fixtures[0],sectionIds:[...fixtures[0].sectionIds]};
 assert.equal(m.cumulativeVoteWeight,undefined);
 restoreDemoMembers([m],['coordenacao'],[{id:m.id,cumulativeVoteWeight:4}]);
 assert.equal(m.cumulativeVoteWeight,4);
 restoreDemoMembers([m],['coordenacao'],[{id:m.id,cumulativeVoteWeight:0}]);
 assert.equal(m.cumulativeVoteWeight,4,'malformed stored weight must not overwrite a valid one');
 restoreDemoMembers([m],['coordenacao'],[{id:m.id,cumulativeVoteWeight:'900'}]);
 assert.equal(m.cumulativeVoteWeight,4,'untrusted storage cannot coerce strings into weights');
});


test('six preview modes expose only fixture choices and never institutional records', () => {
 assert.deepEqual(PREVIEW_BINARY_OPTIONS.map(x=>x.id),['sim','nao']);
 assert.deepEqual(PREVIEW_LIST_OPTIONS.map(x=>x.id),['a','b','c']);
 assert.equal(validatePreviewVote('binaria',{selected:'sim'}).ok,true);
 assert.equal(validatePreviewVote('binaria',{selected:'nao'}).ok,true);
 assert.equal(validatePreviewVote('binaria',{selected:'a'}).ok,false);
 assert.equal(validatePreviewVote('binaria',{selected:null}).ok,false);
 assert.equal(validatePreviewVote('nominal',{selected:'c'}).ok,true);
 assert.equal(validatePreviewVote('nominal',{selected:'sim'}).ok,false);
 assert.equal(validatePreviewVote('nominal',{selected:['a','b']}).ok,false);
 assert.equal(validatePreviewVote('nominal',null).ok,false);
 assert.equal(validatePreviewVote('unknown',{selected:'a'}).ok,false);
});

test('ordered voting requires a complete permutation without omissions or duplicates', () => {
 const accepted=validatePreviewVote('ordenada',{ranking:['c','a','b']});
 assert.equal(accepted.ok,true);
 if(accepted.ok)assert.deepEqual(accepted.vote.ranking,['c','a','b']);
 for(const ranking of [['a','a','c'],['a','b'],['a','b','x'],[],['a','b','c','a']])
  assert.equal(validatePreviewVote('ordenada',{ranking}).ok,false,JSON.stringify(ranking));
});

test('approval voting supports multiple distinct selections but never a blank ballot', () => {
 const accepted=validatePreviewVote('aprovacao',{approved:['a','c']});
 assert.equal(accepted.ok,true);
 if(accepted.ok)assert.deepEqual(accepted.vote.approved,['a','c']);
 for(const approved of [[],['a','a'],['x'],['a','unknown'],'a'])
  assert.equal(validatePreviewVote('aprovacao',{approved}).ok,false,JSON.stringify(approved));
});

test('scalar voting requires integer ratings 1 through 10 for every option', () => {
 const sample={a:1,b:10,c:5};
 assert.equal(validatePreviewVote('escalar',{scores:sample}).ok,true);
 for(const scores of [
  {a:0,b:10,c:5},{a:1,b:11,c:5},{a:1,b:4.5,c:5},
  {a:1,b:2},{a:1,b:2,c:'3'},{a:1,b:2,c:3,d:4},
  {a:1,b:2,c:Infinity},[]
 ])assert.equal(validatePreviewVote('escalar',{scores}).ok,false,JSON.stringify(scores));
});

test('cumulative voting requires configured weight, eligibility, nonnegative integers and bounded sums', () => {
 const distribution={a:2,b:1,c:0};
 const accepted=validatePreviewVote('cumulativa',{allocation:distribution},4);
 assert.equal(accepted.ok,true);
 if(accepted.ok)assert.equal(accepted.vote.weight,4);
 assert.equal(validatePreviewVote('cumulativa',{allocation:distribution}).ok,false);
 assert.equal(validatePreviewVote('cumulativa',{allocation:distribution},0).ok,false);
 for(const allocation of [
  {a:0,b:0,c:0},{a:5,b:0,c:0},{a:2,b:2,c:1},
  {a:-1,b:2,c:0},{a:1.5,b:1,c:0},{a:2,b:1},
  {a:2,b:1,c:'0'},{a:2,b:1,c:0,x:0}
 ])assert.equal(validatePreviewVote('cumulativa',{allocation},4).ok,false,JSON.stringify(allocation));
 assert.equal(validatePreviewVote('cumulativa',{allocation:{a:4,b:0,c:0}},4).ok,true);
 // This is a sandbox-only decision, not an unapproved institutional counting policy.
 assert.equal(validatePreviewVote('cumulativa',{allocation:{a:1,b:0,c:0}},4).ok,true);
});

test('scheduled custom option IDs are respected for nominal, ranked, scalar and cumulative previews',()=>{
 const ids=['opt-1','opt-2','opt-3','opt-4'];
 assert.equal(validatePreviewVote('nominal',{selected:'opt-3'},undefined,ids).ok,true);
 assert.equal(validatePreviewVote('nominal',{selected:'a'},undefined,ids).ok,false);
 assert.equal(validatePreviewVote('ordenada',{ranking:['opt-4','opt-2','opt-1','opt-3']},undefined,ids).ok,true);
 assert.equal(validatePreviewVote('ordenada',{ranking:['opt-1','opt-1','opt-2','opt-4']},undefined,ids).ok,false);
 assert.equal(validatePreviewVote('escalar',{scores:{'opt-1':2,'opt-2':3,'opt-3':5,'opt-4':10}},undefined,ids).ok,true);
 assert.equal(validatePreviewVote('cumulativa',{allocation:{'opt-1':1,'opt-2':2,'opt-3':0,'opt-4':1}},4,ids).ok,true);
 assert.equal(validatePreviewVote('cumulativa',{allocation:{'opt-1':1,'opt-2':4,'opt-3':0,'opt-4':1}},4,ids).ok,false);
 for(const bad of [[],['opt-1'],['opt-1','opt-1'],['a','bad/option'],Array(9).fill('opt-1')])
  assert.equal(validatePreviewVote('nominal',{selected:'opt-1'},undefined,bad).ok,false);
 assert.equal(validatePreviewVote('binaria',{selected:'sim'},undefined,['opt-1','opt-2']).ok,false);
});
