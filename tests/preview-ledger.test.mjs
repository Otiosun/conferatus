import test from 'node:test';
import assert from 'node:assert/strict';
import { createPreviewSampleLedger } from '../dist/domain/preview-ledger.js';

const options=[{id:'a',label:'Alternativa A'},{id:'b',label:'Alternativa B'},{id:'c',label:'Alternativa C'}];
const base=(id='try-1',vote={method:'nominal',selected:'a'},scope='fixture:nominal')=>({
 scope,requestId:id,method:vote.method,options,vote
});
test('record once, replay exactly and reject same token with changed payload',()=>{
 const ledger=createPreviewSampleLedger();
 const first=ledger.submit(base());
 assert.deepEqual(first,{ok:true,status:'recorded',total:1});
 assert.deepEqual(ledger.submit(base()),{ok:true,status:'replayed',total:1});
 const changed=ledger.submit(base('try-1',{method:'nominal',selected:'b'}));
 assert.equal(changed.ok,false);
 assert.equal(changed.reason,'conflict');
 assert.equal(ledger.count('fixture:nominal'),1);
 assert.deepEqual(ledger.votes('fixture:nominal'),[{method:'nominal',selected:'a'}]);
});
test('reject invalid method, illegal choice, invalid request IDs, and fake cumulative weight',()=>{
 const ledger=createPreviewSampleLedger();
 assert.equal(ledger.submit(base('bad!',{method:'nominal',selected:'a'})).ok,false);
 assert.equal(ledger.submit(base('valid',{method:'nominal',selected:'missing'})).ok,false);
 const wrong=base('method',{method:'nominal',selected:'a'});
 wrong.method='binaria';
 assert.equal(ledger.submit(wrong).ok,false);
 const cumulative=base('quota',{method:'cumulativa',allocation:{a:3,b:0,c:0},weight:2},'fixture:cumulativa');
 assert.equal(ledger.submit(cumulative).ok,false);
 assert.equal(ledger.count('fixture:cumulativa'),0);
});
test('idempotent replay works at capacity while new submissions are blocked',()=>{
 const ledger=createPreviewSampleLedger(2);
 assert.equal(ledger.submit(base('id-1')).status,'recorded');
 assert.equal(ledger.submit(base('id-2',{method:'nominal',selected:'b'})).status,'recorded');
 assert.equal(ledger.submit(base('id-1')).status,'replayed');
 assert.equal(ledger.submit(base('id-3',{method:'nominal',selected:'c'})).reason,'limit');
 assert.equal(ledger.count('fixture:nominal'),2);
});
test('other scopes have separate ledgers and clearance is isolated',()=>{
 const ledger=createPreviewSampleLedger();
 ledger.submit(base('once'));
 ledger.submit(base('once',{method:'nominal',selected:'b'},'schedule:example-1'));
 assert.deepEqual(ledger.votes('schedule:example-1'),[{method:'nominal',selected:'b'}]);
 ledger.clear('fixture:nominal');
 assert.equal(ledger.count('fixture:nominal'),0);
 assert.equal(ledger.count('schedule:example-1'),1);
 ledger.clearAll();
 assert.equal(ledger.count('schedule:example-1'),0);
});
test('stored ballot remains immutable when caller changes source or returned snapshots',()=>{
 const ledger=createPreviewSampleLedger();
 const ballot={method:'aprovacao',approved:['a','b']};
 const submission=base('one',ballot,'fixture:aprovacao');
 assert.equal(ledger.submit(submission).ok,true);
 ballot.approved.push('c');
 const snapshot=ledger.votes('fixture:aprovacao');
 assert.deepEqual(snapshot,[{method:'aprovacao',approved:['a','b']}]);
 snapshot[0].approved.pop();
 assert.deepEqual(ledger.votes('fixture:aprovacao'),[{method:'aprovacao',approved:['a','b']}]);
});
test('all six methods can be stored using the same preview register',()=>{
 const ledger=createPreviewSampleLedger();
 const cases=[
  {method:'binaria',scope:'fixture:binaria',options:[{id:'sim',label:'Sim'},{id:'nao',label:'Não'}],vote:{method:'binaria',selected:'sim'}},
  {method:'nominal',scope:'fixture:nominal',options,vote:{method:'nominal',selected:'a'}},
  {method:'ordenada',scope:'fixture:ordenada',options,vote:{method:'ordenada',ranking:['b','a','c']}},
  {method:'aprovacao',scope:'fixture:aprovacao',options,vote:{method:'aprovacao',approved:['a','c']}},
  {method:'escalar',scope:'fixture:escalar',options,vote:{method:'escalar',scores:{a:1,b:5,c:10}}},
  {method:'cumulativa',scope:'fixture:cumulativa',options,vote:{method:'cumulativa',allocation:{a:2,b:1,c:0},weight:4}}
 ];
 for(const item of cases)assert.equal(ledger.submit({...item,requestId:'sample-1'}).status,'recorded',item.method);
 for(const item of cases)assert.equal(ledger.count(item.scope),1);
});
