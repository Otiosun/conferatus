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

test('demotion preserves activity and role becomes common member',()=>{
 const before={...fixtures[0],sectionIds:[...fixtures[0].sectionIds]};
 const {member,change}=demoteToCommonMember(before);
 assert.equal(member.role,'membro');assert.deepEqual(member.sectionIds,['membros']);
 assert.equal(change.previousRole,'diretor');assert.equal(change.kind,'rebaixamento');
 assert.equal(member.totalVotes,before.totalVotes);assert.equal(member.proposals,before.proposals);
});
test('closed vote is blocked; open vote can be simulated',()=>{
 assert.equal(canRecordVote({status:'encerrada'}),false);
 assert.equal(canRecordVote({status:'aberta'}),true);
});
test('sixteen invented accounts in preview',()=>{
 assert.equal(fixtures.length,16);
 assert.ok(fixtures.every(m=>m.acdmId?.startsWith('DEMO-')));
});

test('demonstration gives each profile distinct proposals', async () => {
 const {activities, sections}=await import('../dist/data/fixtures.js');
 assert.equal(new Set(activities.map(a=>a.id)).size,activities.length);
 const validSections=new Set(sections.map(s=>`Seção: ${s.name}`));
 for(const member of fixtures){
  const relevant=activities.filter(a=>a.memberId===member.id);
  const proposals=relevant.filter(a=>a.type==='proposicao');
  assert.ok(proposals.length>=2);
  assert.equal(new Set(proposals.map(a=>a.title)).size,proposals.length);
  assert.ok(relevant.every(a=>a.title.length>10 && a.summary.length>=30));
 }
 assert.ok(activities.filter(a=>a.id.startsWith('sample-')).every(a=>validSections.has(a.section)));
});
test('sample proposal titles are not duplicated across members', async () => {
 const {activities}=await import('../dist/data/fixtures.js');
 const proposals=activities.filter(a=>a.type==='proposicao');
 assert.ok(new Set(proposals.map(a=>a.title)).size>=proposals.length-1);
});

test('official CINSTIA sections, with ordinary members separated',async()=>{
 const {sections}=await import('../dist/data/fixtures.js');
 const ds=sections.filter(s=>s.category==='deliberativa');
 assert.deepEqual(ds.map(s=>s.name),['Diretoria','Coordenação','Conselho de Integridade','Representantes Devos']);
 assert.deepEqual(ds.map(s=>s.places),[4,8,12,24]);
 assert.equal(sections.filter(s=>s.category==='comum').length,1);
});
test('administrative role does not determine deliberative voting eligibility',async()=>{
 const {sections}=await import('../dist/data/fixtures.js');
 assert.equal(isDeliberativeMember({...fixtures[0],role:'membro',sectionIds:['coordenacao']},sections),true);
 assert.equal(isDeliberativeMember({...fixtures[0],role:'diretor',sectionIds:['membros']},sections),false);
});
test('demoted deliberatives keep old personal votes; common members do not',async()=>{
 const {sections,activities}=await import('../dist/data/fixtures.js');
 const demoted=demoteToCommonMember(fixtures[0]).member;
 assert.equal(isDeliberativeMember(demoted,sections),false);
 assert.equal(hasPersonalVoteHistory(demoted,sections),true);
 assert.equal(hasPersonalVoteHistory(fixtures[11],sections),false);
 assert.equal(activities.some(a=>a.memberId==='m12'&&a.type==='voto'),false);
});
test('restored session retains prior deliberative status',async()=>{
 const {sections}=await import('../dist/data/fixtures.js');
 const before={...fixtures[0],sectionIds:[...fixtures[0].sectionIds]};
 const after=demoteToCommonMember(before).member;
 restoreDemoMembers([before],sections.map(s=>s.id),[{id:before.id,sectionIds:after.sectionIds,role:after.role,hadDeliberativeHistory:after.hadDeliberativeHistory}]);
 assert.equal(hasPersonalVoteHistory(before,sections),true);
});
