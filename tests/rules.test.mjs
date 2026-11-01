import assert from 'node:assert/strict';
import test from 'node:test';
import { totalVotes, resultPercentage, updateSectionAssignment, demoteToCommonMember, canRecordVote, escapeHTML, restoreDemoMembers, searchKey, isDeliberativeMember, hasPersonalVoteHistory } from '../dist/domain/rules.js';
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
