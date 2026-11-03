import test from 'node:test';
import assert from 'node:assert/strict';
import {exportWorkflowArchive,parseWorkflowArchive,WORKFLOW_ARCHIVE_MAX_BYTES} from '../dist/domain/workflow-archive.js';

test('local archive holds only the two workflow collections, with a version marker',()=>{
 const text=exportWorkflowArchive([{id:'draft-a'}],[{id:'sched-a'}],new Date('2026-11-03T00:00:00Z'));
 const item=JSON.parse(text);
 assert.deepEqual(Object.keys(item), ['format','version','exportedAt','drafts','schedule']);
 assert.deepEqual(item.drafts,[{id:'draft-a'}]);
 assert.deepEqual(item.schedule,[{id:'sched-a'}]);
 assert.equal(item.exportedAt,'2026-11-03T00:00:00.000Z');
 assert.equal(parseWorkflowArchive(text).ok,true);
});

test('malformed, unknown-version, oversized and non-array archives are rejected',()=>{
 assert.equal(parseWorkflowArchive('{').ok,false);
 assert.equal(parseWorkflowArchive('null').ok,false);
 assert.equal(parseWorkflowArchive(JSON.stringify({format:'spoof',version:1,exportedAt:'2026-11-03',drafts:[],schedule:[]})).ok,false);
 assert.equal(parseWorkflowArchive(JSON.stringify({format:'conffratus-local-workflows',version:2,exportedAt:'2026-11-03',drafts:[],schedule:[]})).ok,false);
 assert.equal(parseWorkflowArchive(JSON.stringify({format:'conffratus-local-workflows',version:1,exportedAt:'2026-11-03',drafts:{},schedule:[]})).ok,false);
 assert.equal(parseWorkflowArchive('x'.repeat(WORKFLOW_ARCHIVE_MAX_BYTES+1)).ok,false);
});
