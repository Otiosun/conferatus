import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const cwd = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const files = ['data/fixtures.js', 'domain/rules.js', 'domain/providers.js', 'domain/academy-identity.js', 'main.js'];
const sources = await Promise.all(files.map(async file => {
  const source = await readFile(path.join(cwd, 'dist', file), 'utf8');
  return source.replace(/^import .*?;\s*$/gm, '').replace(/^export /gm, '');
}));
let js = `const __fixture = (()=>{${sources[0]}; return { members,sections,ballots,activities };})();
const __rules = (()=>{${sources[1]};return {escapeHTML,resultPercentage,totalVotes,updateSectionAssignment,restoreDemoMembers,searchKey,demoteToCommonMember,canRecordVote,isDeliberativeMember,hasPersonalVoteHistory};})();
const __providers = (({members,sections})=>{${sources[2]};return {FixtureMemberProvider};})(__fixture);
const __academyIdentity = (()=>{${sources[3]};return {UnconnectedAcademyIdentityProvider};})();
await (async ({activities,ballots},{FixtureMemberProvider},{UnconnectedAcademyIdentityProvider},{escapeHTML,resultPercentage,totalVotes,updateSectionAssignment,restoreDemoMembers,searchKey,demoteToCommonMember,canRecordVote,isDeliberativeMember,hasPersonalVoteHistory})=>{${sources[4]}})(__fixture,__providers,__academyIdentity,__rules);`;
for (const name of ['crest', 'editar', 'rebaixamento', 'painel']) {
  const asset = await readFile(path.join(cwd,'public','assets',`${name}.png`));
  js = js.replaceAll(`./assets/${name}.png`,`data:image/png;base64,${asset.toString('base64')}`);
}
const css = await readFile(path.join(cwd,'src','styles.css'),'utf8');
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#515dc7"><meta name="robots" content="noindex,nofollow,noarchive"><title>CONFFRATUS</title><style>${css}</style></head><body><div id="root"></div><script>(async()=>{\n${js}\n})().catch(error=>{console.error('Falha ao iniciar prévia:',error);document.querySelector('#root').textContent='Não foi possível iniciar a prévia.'});</script></body></html>`;
const outfile = path.join(cwd,'dist','CONFFRATUS_demo_offline.html');
await writeFile(outfile,html);
// Keep the historical file path for already-distributed previews and browser regressions.
await writeFile(path.join(cwd,'dist','CONFERATUS_demo_offline.html'),html);
console.log(`Preview offline gerado (${(Buffer.byteLength(html)/1024).toFixed(0)} KB).`);
