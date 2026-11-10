# CP163 — Integração de participação contextual e agendamento (10/11/2026)

Base `75e5e3402478226d34735729295183144bc88ec3` na branch privada `preview/v0.10.60-six-vote-forms`, sem alteração de main/produção ou contratos Academy.

## Defeito e correção
CP161 passou a pré-selecionar a seção e o tipo de uma proposição concluída ao abrir agendamento; a comparação de alteração não salva continuava usando `integridade` e `PDR`. Assim, apenas abrir o formulário com outra classificação podia provocar um aviso indevido de descarte. A rotina `hasPendingScheduleChanges()` agora usa os mesmos valores iniciais da proposição de origem e permanece capaz de identificar mudanças reais.

A ação **Participar nesta votação**, que já existia no cartão do calendário, preparava o estado de participação antes de chamar `navigate('ballot')`. Ao desistir de sair de um agendamento incompleto, esse contexto podia ficar preparado apesar da permanência no calendário. A ação agora tenta a navegação protegida primeiro e seleciona a programação somente quando a rota efetivamente muda. Preservados o formulário contextual, as alternativas fictícias e o retorno com foco implementado em CP156.

Teste `tests/browser_contextual_schedule_guard_v0210.py`, incluído no workflow, cobre pré-preenchimento sem falsa alteração, saída recusada preservando o texto e a rota, abandono autorizado sem contexto residual, participação após saída autorizada e retorno à programação correta. Larguras 320/390/740/1280px. Regressões v0179, v0180, v0203 e v0208 continuam relevantes.

Fontes consultadas: MDN `hashchange` e `HTMLElement.focus`: https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event e https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus. `hashchange` é o evento de troca de fragmento, e os controles existentes preservam foco contextual; não foi introduzido roteador adicional.

**Limites:** a regressão foi adicionada, mas não executada localmente. Verificar o check de build Cloudflare do SHA exato; não confundir publicação com testes Chromium/Firefox/WebKit, Android físico ou aceite Megalos. PF-19/PF-20 abertos, contagens 8/38 funcional e 43/57 histórica preservadas. Nenhuma regra institucional ou integração real criada.
