/** Explicit backup of synthetic session workflows. No account, vote or Academy data. */
export const WORKFLOW_ARCHIVE_FORMAT = 'conffratus-local-workflows';
export const WORKFLOW_ARCHIVE_MAX_BYTES = 2_000_000;
export type WorkflowArchive = {
 format: typeof WORKFLOW_ARCHIVE_FORMAT;
 version: 1;
 exportedAt: string;
 drafts: unknown[];
 schedule: unknown[];
};

export function exportWorkflowArchive(drafts: readonly unknown[], schedule: readonly unknown[], when = new Date()): string {
 return JSON.stringify({format: WORKFLOW_ARCHIVE_FORMAT, version:1, exportedAt:when.toISOString(), drafts, schedule}, null, 2);
}

// Envelope only; the app reuses its own record validation and reference checks
// before replacing anything. Never trust a downloaded filename or its extension.
export function parseWorkflowArchive(raw: string): {ok:true; archive:WorkflowArchive} | {ok:false; error:string} {
 if(new TextEncoder().encode(raw).length > WORKFLOW_ARCHIVE_MAX_BYTES) return {ok:false,error:'O arquivo excede o limite de 2 MB.'};
 let value:unknown;
 try{value=JSON.parse(raw);}catch{return {ok:false,error:'O arquivo não contém JSON válido.'};}
 if(!value||typeof value!=='object'||Array.isArray(value)) return {ok:false,error:'Formato de cópia não reconhecido.'};
 const data=value as Record<string,unknown>;
 if(data.format!==WORKFLOW_ARCHIVE_FORMAT||data.version!==1||
    typeof data.exportedAt!=='string'||!Number.isFinite(Date.parse(data.exportedAt)))
  return {ok:false,error:'Esta cópia não pertence à versão de exportação compatível.'};
 if(!Array.isArray(data.drafts)||!Array.isArray(data.schedule)||data.drafts.length>500||data.schedule.length>500)
  return {ok:false,error:'A cópia não contém listas de registros válidas.'};
 return {ok:true, archive:data as WorkflowArchive};
}
