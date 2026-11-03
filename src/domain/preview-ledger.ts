import type { DeliberationMethod } from './types.js';
import { validatePreviewVote } from './rules.js';
import type { PreviewVote } from './rules.js';

/**
 * Memory-only sample register. This is intentionally not an authenticated ballot store.
 * In production, idempotency and duplicate protection belong inside a server transaction.
 */
export type PreviewSampleRequest = {
  scope: string;
  requestId: string;
  method: DeliberationMethod;
  options: readonly {id: string; label: string}[];
  vote: PreviewVote;
};
export type PreviewSampleReceipt =
  | {ok: true; status: 'recorded' | 'replayed'; total: number}
  | {ok: false; reason: 'invalid' | 'conflict' | 'limit'; message: string};

type StoredSample = {requestId: string; fingerprint: string; vote: PreviewVote};
export function createPreviewSampleLedger(limitPerScope = 100) {
  if (!Number.isSafeInteger(limitPerScope) || limitPerScope < 1 || limitPerScope > 1000) {
    throw new RangeError('Limite de amostras inválido.');
  }
  const records = new Map<string, StoredSample[]>();

  function submit(request: PreviewSampleRequest): PreviewSampleReceipt {
    if (!request || typeof request !== 'object' ||
        typeof request.scope !== 'string' || !/^(?:fixture|schedule):[a-z0-9_-]{1,100}$/i.test(request.scope) ||
        typeof request.requestId !== 'string' || !/^[a-z0-9_-]{1,80}$/i.test(request.requestId) ||
        !Array.isArray(request.options) || request.options.length < 2 || request.options.length > 8 ||
        request.options.some(option => !option || typeof option.id !== 'string' ||
          typeof option.label !== 'string' || option.label.trim().length < 1 || option.label.length > 80) ||
        new Set(request.options.map(option => option.id)).size !== request.options.length ||
        !request.vote || request.vote.method !== request.method) {
      return {ok:false,reason:'invalid',message:'Amostra demonstrativa inválida.'};
    }
    const vote = request.vote;
    const payload = vote.method === 'binaria' || vote.method === 'nominal'
      ? {selected:vote.selected}
      : vote.method === 'ordenada' ? {ranking:vote.ranking}
      : vote.method === 'aprovacao' ? {approved:vote.approved}
      : vote.method === 'escalar' ? {scores:vote.scores}
      : vote.method === 'cumulativa' ? {allocation:vote.allocation} : {};
    const valid = validatePreviewVote(request.method, payload,
      vote.method === 'cumulativa' ? vote.weight : undefined,
      request.options.map(option => option.id));
    if (!valid.ok) return {ok:false,reason:'invalid',message:valid.error};

    const fingerprint = JSON.stringify({
      method: request.method, options: request.options.map(option => [option.id,option.label]), vote: valid.vote
    });
    const stored = records.get(request.scope) ?? [];
    const previous = stored.find(entry => entry.requestId === request.requestId);
    if (previous) {
      return previous.fingerprint === fingerprint
        ? {ok:true,status:'replayed',total:stored.length}
        : {ok:false,reason:'conflict',message:'A mesma solicitação já foi usada com um voto diferente.'};
    }
    if (stored.length >= limitPerScope) {
      return {ok:false,reason:'limit',message:'Esta simulação atingiu o limite de '+limitPerScope+' amostras. Limpe-as para reiniciar.'};
    }
    stored.push({requestId:request.requestId,fingerprint,vote:structuredClone(valid.vote)});
    records.set(request.scope,stored);
    return {ok:true,status:'recorded',total:stored.length};
  }

  function votes(scope: string): PreviewVote[] {
    return (records.get(scope) ?? []).map(entry => structuredClone(entry.vote));
  }
  function count(scope: string): number { return records.get(scope)?.length ?? 0; }
  function clear(scope: string): void { records.delete(scope); }
  function clearAll(): void { records.clear(); }

  return {submit,votes,count,clear,clearAll};
}
