import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
const root = new URL('../', import.meta.url);
test('static publish is self-contained and explicitly illustrative', async () => {
 const html=await readFile(new URL('publish/index.html',root),'utf8');
 assert.match(html, /<html lang="pt-BR">/);
 assert.match(html,/CONFERATUS/);
 assert.match(html,/noindex,nofollow,noarchive/);
 assert.match(html,/dados inventados|dados fictícios/i);
 assert.match(html,/<style>/);
 assert.match(html,/<script>/);
 assert.doesNotMatch(html,/<script[^>]+src=/i);
 assert.doesNotMatch(html,/file:\/\/|localhost:/);
 assert.match(html, /<title>CONFERATUS<\/title>/);
 assert.doesNotMatch(html, /<meta[^>]+(?:og:|twitter:|name="description")/i);
 await assert.rejects(stat(new URL('publish/preview.png',root)), {code:'ENOENT'});
});
test('offline preview is present and does not load external libraries', async () => {
 const html=await readFile(new URL('dist/CONFERATUS_demo_offline.html',root),'utf8');
 assert.match(html,/<script>/);
 assert.doesNotMatch(html,/<script[^>]+src=/i);
 assert.doesNotMatch(html,/https?:\/\/[^ ]+\.js/i);
});
