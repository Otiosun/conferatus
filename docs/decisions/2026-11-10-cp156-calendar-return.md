# CP156 — Retorno contextual da agenda (10/11/2026)

Base: `preview/v0.10.60-six-vote-forms` @ `c76995218664b02efc6bf7a0150f91f7d02851a7`. Edição isolada de prévia privada, sem mudança em main ou produção.

## Trabalho
O botão de retorno da votação contextual regressa à programação de origem no calendário, expandida e com foco. Em contexto cancelado/indisponível, mostrar o título da programação, a condição e o caminho para o calendário sem trocar pelo formulário/resultados da votação inicial. Retorno da votação inicial continua na página inicial. A modalidade e os dados são apenas fictícios, sem regras institucionais inventadas.

## Prova e limites
Criado `tests/browser_schedule_return_v0203.py` para percurso de confirmação nominal, retorno, cancelamento, reentrada indisponível e foco em 320/390/740/1280px, apenas com fixtures sintéticas. **Teste ainda NÃO executado. Não foi executado `npm run build` sobre este SHA; CI, deploy real, outras engines e Android físico ainda NÃO verificados.** Assim, PF-06 e PF-10 continuam abertos; 8/38 funcional e 43/57 histórico permanecem.

Investigação de interface em 10/11/2026: W3C WAI SC 4.1.3/ARIA22 e MDN `hashchange`, para aproveitar status e foco/roteador nativos:
https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22.html
https://www.w3.org/WAI/WCAG21/Understanding/status-messages
https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event

Próximo: build do SHA, v0203/v0202/v0201/v0194/v0192/v0190, inspeção do deploy e Android físico; depois PF-11 a PF-21. D1–D6 aguardam Megalos.
