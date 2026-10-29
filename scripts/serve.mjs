import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const distRoot = path.join(projectRoot, 'dist');
const mime = {
  '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8',
  '.css':'text/css; charset=utf-8', '.png':'image/png', '.svg':'image/svg+xml',
};
const port = Number(process.env.PORT ?? 5173);
createServer(async (req, res) => {
  try {
    const url = new URL(req.url ?? '/', 'http://localhost');
    const candidate = path.resolve(distRoot, '.' + decodeURIComponent(url.pathname));
    if (candidate !== distRoot && !candidate.startsWith(distRoot + path.sep)) {
      res.writeHead(403).end('Forbidden'); return;
    }
    const file = (await stat(candidate).catch(() => undefined))?.isFile() ? candidate : path.join(distRoot, 'index.html');
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] ?? 'application/octet-stream', 'X-Content-Type-Options':'nosniff' });
    res.end(body);
  } catch(err) { res.writeHead(500).end('Internal server error'); }
}).listen(port, '127.0.0.1', () => console.log(`Preview: http://127.0.0.1:${port}`));
