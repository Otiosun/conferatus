import test from 'node:test';
import assert from 'node:assert/strict';
import {
 isValidPreviewChoices,
 isSavedDraft,
 isSavedSchedule,
 isRestorableSchedule,
 cleanDraftRecord,
 cleanScheduleRecord,
 uniqueSavedRecords,
 nextLocalRecordId
} from '../dist/domain/workflow-records.js';

const context = {
 memberIds: new Set(['m01', 'm02', 'm03']),
 deliberativeSectionIds: new Set(['integridade']),
 authorId: 'm01'
};
const original = {
 id:'draft-fixture',
 title:'Proposição de demonstração',
 body:'Texto demonstrativo com mais de vinte caracteres para verificar restauração.',
 sectionId:'integridade',
 type:'PDR',
 status:'concluida',
 authorComplete:true,
 partners:[{id:'m02',complete:true}]
};
const options=[{id:'opt-1',label:'Alternativa Azul'},{id:'opt-2',label:'Alternativa Vermelha'}];
const appointment={
 id:'sched-fixture', title:'Sessão de demonstração', objective:'Programação local e fictícia',
 proposalId:original.id,sectionId:'integridade',start:'2026-12-02T09:00',
 end:'2026-12-02T10:00',type:'PDR',method:'nominal',choices:options,status:'programada'
};

test('stable preview alternatives require distinct labels and sequential IDs',()=>{
 assert.equal(isValidPreviewChoices(options),true);
 assert.equal(isValidPreviewChoices([{id:'opt-1',label:'São'},{id:'opt-2',label:'Sao'}]),false);
 assert.equal(isValidPreviewChoices([{id:'opt-1',label:'A'},{id:'opt-3',label:'B'}]),false);
 assert.equal(isValidPreviewChoices([{id:'opt-1',label:' A '},{id:'opt-2',label:'B'}]),false);
 assert.equal(isValidPreviewChoices([{id:'opt-1',label:'A'}]),false);
 assert.equal(isValidPreviewChoices(Array.from({length:9},(_,i)=>({id:'opt-'+(i+1),label:'Choice '+i}))),false);
});

test('saved workflow proposal rejects invalid partner signatures and false completion',()=>{
 assert.equal(isSavedDraft(original,context),true);
 assert.equal(isSavedDraft({...original,partners:[{id:'m01',complete:true}]},context),false);
 assert.equal(isSavedDraft({...original,partners:[{id:'m02',complete:false}]},context),false);
 assert.equal(isSavedDraft({...original,partners:[{id:'m02',complete:true},{id:'m02',complete:true}]},context),false);
 assert.equal(isSavedDraft({...original,partners:[{id:'outsider',complete:true}]},context),false);
 assert.equal(isSavedDraft({...original,authorComplete:false},context),false);
 assert.equal(isSavedDraft({...original,body:'insuficiente'},context),false);
});

test('partial local drafts remain valid, but review requires completed content and known sections',()=>{
 assert.equal(isSavedDraft({...original,status:'redacao',title:'',body:'',sectionId:'',authorComplete:false,partners:[]},context),true);
 assert.equal(isSavedDraft({...original,status:'revisao',title:'',authorComplete:false},context),false);
 assert.equal(isSavedDraft({...original,status:'revisao',sectionId:'secret'},context),false);
 assert.equal(isSavedDraft({...original,status:'revisao',authorComplete:false,partners:[{id:'m02',complete:false}]},context),true);
});

test('schedule restoration accepts valid histories but rejects broken or unsupported metadata',()=>{
 assert.equal(isSavedSchedule(appointment),true);
 assert.equal(isSavedSchedule({...appointment,start:appointment.end}),false);
 assert.equal(isSavedSchedule({...appointment,end:'garbage'}),false);
 assert.equal(isSavedSchedule({...appointment,method:'unrecognized'}),false);
 assert.equal(isSavedSchedule({...appointment,choices:[{id:'bad',label:'A'}]}),false);
 assert.equal(isSavedSchedule({...appointment,method:'binaria',choices:options}),false);
 assert.equal(isRestorableSchedule(appointment,[original],context.deliberativeSectionIds),true);
 assert.equal(isRestorableSchedule(appointment,[{...original,status:'revisao'}],context.deliberativeSectionIds),false);
 assert.equal(isRestorableSchedule({...appointment,status:'cancelada'},[{...original,status:'revisao'}],context.deliberativeSectionIds),true);
 assert.equal(isRestorableSchedule({...appointment,sectionId:'not-a-section'},[original],context.deliberativeSectionIds),false);
});

test('local archive cleansing excludes unauthorized extra properties and copies nested entries',()=>{
 const draft=cleanDraftRecord({...original,authToken:'must-not-ship',partners:[{id:'m02',complete:true,secret:'x'}]});
 assert.equal(JSON.stringify(draft).includes('authToken'),false);
 assert.equal(JSON.stringify(draft).includes('secret'),false);
 assert.notEqual(draft.partners,original.partners);
 const copy=cleanScheduleRecord({...appointment,privateToken:'must-not-ship',choices:[...options]});
 assert.equal(JSON.stringify(copy).includes('privateToken'),false);
 assert.notEqual(copy.choices,appointment.choices);
 options[0].label='Alteração posterior';
 assert.equal(copy.choices[0].label,'Alternativa Azul');
});

test('duplicate IDs are quarantined and locally-generated IDs avoid clock collisions',()=>{
 const records=uniqueSavedRecords([original,{...original,title:'duplicated'},null,{...original,id:'draft-other'}],
  v=>isSavedDraft(v,context));
 assert.deepEqual(records.accepted.map(d=>d.id),['draft-fixture','draft-other']);
 assert.equal(records.rejected.length,2);
 const first=nextLocalRecordId('draft',[],1234);
 assert.equal(nextLocalRecordId('draft',[{id:first}],1234),first+'-1');
 assert.equal(nextLocalRecordId('draft',[{id:first},{id:first+'-1'}],1234),first+'-2');
});
