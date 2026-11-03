import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

// Safety property: the experimental PostgreSQL lab must never be sent to the
// static browser client. npm run build materializes these artifacts first.
test('browser release contains no PostgreSQL lab schema, gateway role or disposable CI credentials',()=>{
 for(const path of ['publish/index.html','dist/CONFERATUS_demo_offline.html']){
  const html=readFileSync(path,'utf8');
  assert.ok(html.length>10000,path+' is not a meaningful bundle');
  for(const secret of ['conffratus_vote_lab','record_fixture_vote','conffratus_lab_gateway','ci-disposable-only']){
   assert.equal(html.includes(secret),false,path+' unexpectedly embeds '+secret);
  }
 }
});
