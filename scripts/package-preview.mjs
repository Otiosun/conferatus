import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const target = path.join(root, 'publish');
await mkdir(target,{recursive:true});
let html = await readFile(path.join(root,'dist','CONFERATUS_demo_offline.html'),'utf8');
const origin = (process.env.PUBLIC_URL || 'https://conferatus.pages.dev').trim().replace(/\/$/,'');
const meta = `<meta property="og:type" content="website"><meta property="og:title" content="CONFERATUS"><meta property="og:description" content="Votações, membros e histórico institucional da Academy."><meta name="twitter:card" content="summary_large_image">${origin?`<meta property="og:url" content="${origin.replaceAll('&','&amp;').replaceAll('"','&quot;')}"><meta property="og:image" content="${origin.replaceAll('&','&amp;').replaceAll('"','&quot;')}/preview.png?v=097"><meta name="twitter:image" content="${origin.replaceAll('&','&amp;').replaceAll('"','&quot;')}/preview.png?v=097">`:''}`;
html = html.replace('<title>',`${meta}<title>`);
await writeFile(path.join(target,'index.html'),html);
await writeFile(path.join(target,'robots.txt'),'User-agent: *\nAllow: /\n');
await writeFile(path.join(target,'_headers'), '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n  X-Robots-Tag: noindex, nofollow, noarchive\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n');
// Preview artwork is intentionally optional: the public URL and image meta are added only when a real URL is known.
try { await copyFile(path.join(root,'public','preview.png'),path.join(target,'preview.png')); } catch { /* visual snapshot not produced yet */ }
console.log(`Static publish folder ready: ${target}`);
