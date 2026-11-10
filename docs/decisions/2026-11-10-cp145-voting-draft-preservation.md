# CONFFRATUS — CP145: preservação de escolha não enviada (10/11/2026)

## Falha reproduzida e escopo
No protótipo da votação em `#/ballot`, a seleção em um dos seis formulários podia desaparecer ao **fechar e reabrir** o painel antes de confirmar a amostra. Caso reproduzido em Chromium a 320/390/740px: preencher quatro unidades na modalidade cumulativa, fechar painel, abrir novamente → valor voltava a zero, sem alerta. A conservação em re-render do menu já existia, mas não sobre o painel fechado. Isso viola o requisito interno de não perder estado digitado silenciosamente.

## Investigação fria (lei 21)
Conferência do código existente: `render()` usa `root.innerHTML` para reconstruir a interface e tem restauro de valores apenas para formulários presentes nos dois renders consecutivos. Ao fechar o painel, o formulário deixa de existir e o próximo render não tem fonte de valores. A API DOM `innerHTML` substitui os nós filhos; ver documentação MDN consultada em 10/11/2026: <https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML>.

**Decisão:** sem pacote, banco, `localStorage`, `sessionStorage` ou novo framework. Preservar os valores apenas em memória da aba, com contexto de método/programação e membro fictício; descartar explicitamente ao mudar método, trocar programação, confirmar/resetar amostra, importar cópia ou cancelar a programação relacionada. Não persistir a escolha em arquivo/URL nem converter amostra em voto institucional.

## Implementação
- `src/main.ts`: `PreviewVoteDraft`, cache de entradas selecionadas associado ao escopo `previewSampleScope()` e membro fictício. Reutiliza restauro já existente, agora também entre painel fechado/aberto e navegação.
- `tests/browser_voting_normal_flow_v0190.py`: regressão verifica quatro larguras 320/390/740/1280, preenchimento cumulativo quatro unidades preservado ao fechar/reabrir e após menu, radio nominal preservado após reabertura, mudança de método sem escolha antiga, e programação contextual sem vazamento de seleção da votação fictícia livre.
- Commits exclusivos na branch de prévia: aplicação `66bd1ba6f383a2faec40a7abfda552db1d5bfc42` (Git blob `638cebf67eefd965ef1c22830a27a8c4f9b441b7`), teste `bf3dba5ce3aec496f3173187affd4ca7efff9b1a` (Git blob `34b1c22a8ebc74bb5b247183419405dc602b6203`). Os blobs GitHub **coincidem** com os arquivos testados localmente.

## Evidência
Antes: `0` ao reabrir depois de preencher `4`; depois: `4` em 320/390/740px, sem erros JS. Build local recompilado diretamente dos arquivos testados: `npm run build` PASS, TypeScript estrito, **73/73 testes Node**. `browser_voting_normal_flow_v0190.py` PASS: seis modalidades e entradas de calendário em 4 larguras, inclusive sem transposição de escolhas entre contextos. `browser_full_workflow_journey_v0173.py` PASS em 4 larguras; `browser_smoke.py` passou em execução anterior do mesmo build, mas uma repetição adicional travou no processo Playwright; não contamos essa repetição como sucesso. Teste HTTP local e hardware reais permanecem fora do escopo destas provas.

ZIP privado no Drive Komekko com HTML compilado, diff, testes, capturas e hashes: <https://drive.google.com/file/d/1PJrEdMI5SFA586C-Kpin4XR_wYbUuWiT/view> (SHA256 `4855a3420bd8c5a9de3036ed5bec248c9be5ad4cc8789ff6a291329f0237879c`). HTML SHA256 `9b277b20d7b36afa8d5df43631b9c3b491c1858eba753da9e013f8b6c9cb72f9`.

## Limites e próximos gates
O protótipo permanece fictício, não implanta infraestrutura Academy nem regras de eleição. A autorização Megalos para página de votação (votar versus criar/administrar) e decisões D1–D6, revisão visual e teste em dispositivo real continuam pendentes. Não declarar CI remota verde sem check integral no SHA exato. `main`, Cloudflare principal, PM2 e dados reais não foram tocados. Contagem oficial mantida em **33/57**; nenhuma pendência institucional foi artificialmente marcada como concluída.

**Próximo objetivo:** eliminar falhas verificáveis na jornada de votação e consolidar o roteiro comparativo da Megalos, preservando as referências originais até haver decisão expressa.
