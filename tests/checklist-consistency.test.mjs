import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const read = file => readFileSync(new URL(file, root), 'utf8');

function checklistSection(text, from, to) {
 const start = text.indexOf(from);
 const end = text.indexOf(to, start + from.length);
 assert.ok(start >= 0 && end > start, 'Checklist headings must be present');
 return text.slice(start, end);
}

function completed(section) {
 const entries = [...section.matchAll(/^- \[([ x])\] \*\*(07\.\d\d)/gm)];
 assert.equal(entries.length, 12, 'The stage 07 checklist must contain exactly twelve items');
 const ids = entries.map(([, , id]) => id);
 assert.equal(new Set(ids).size, 12, 'Each stage 07 item must be unique');
 return entries.filter(([, mark]) => mark === 'x').map(([, , id]) => id).sort();
}

test('stage 07 summary counts agree with actual completed checklist items', () => {
 const master = read('docs/CHECKLIST_MESTRA.md');
 const stage = read('docs/ETAPA_07_FRONTEND_PERFECCIONISMO_2026-11-02.md');
 const masterSection = checklistSection(master, '## 07 — Perfeccionismo', '## Leis permanentes');
 const stageSection = checklistSection(stage, '## Checklist exclusiva da Etapa 07', '## Execução inicial');

 const masterDone = completed(masterSection);
 const stageDone = completed(stageSection);
 assert.deepEqual(masterDone, stageDone, 'The canonical summary and stage-specific list must agree');

 const statedMaster = masterSection.match(/\*\*Estado da Etapa 07: (\d+)\/12\.\*\*/);
 const statedStage = stageSection.match(/Checklist exclusiva da Etapa 07 — (\d+)\/12/);
 assert.ok(statedMaster && statedStage, 'Both progress summaries must be explicit');
 assert.equal(Number(statedMaster[1]), masterDone.length);
 assert.equal(Number(statedStage[1]), stageDone.length);
});
