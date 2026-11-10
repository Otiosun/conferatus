# CP157 — Coerência de regressões e Socii como produto

Origem: branch privada `preview/v0.10.60-six-vote-forms`, base `1e60c9921bb1a117fd9c6c84c1fa4dc6a83451e5`.

Revisão de dois testes: `v0201` esperava a antiga tela inicial após cancelamento; CP156 passou a apresentar a programação contextual cancelada. A prova agora exige título, estado, ausência de formulário e totais alheios, retorno ao histórico e entrada independente na votação inicial. `v0203` esvaziava o contexto no retorno antes de testar cancelamento; o roteiro agora reabre a programação e navega sem descartar o identificador.

Na interface comum, “Simular conclusão de participante” foi substituído por um botão de etapa do Socii associado à pessoa fictícia, com explicação de que não acessa outras contas. “Convidar para Socii” foi substituído por “Adicionar ao Socii” porque nenhuma mensagem real é enviada. O fluxo, os modelos e a finalização já existentes permanecem. Novo teste v0204 integra proposição fictícia, conclusão Socii e agendamento.

Critérios de prova: apenas revisão estática de origem e testes gravados; `npm run build` / Playwright locais / Android físico / Firefox / WebKit NÃO executados neste ambiente. Acompanhar build Cloudflare do SHA após escrita, sem equiparar a CI integral. PF-06, PF-10 e PF-11–21 seguem abertos, contagens 8/38 funcional e 43/57 histórica.

Reuso da aplicação TS/HTML/CSS sem dependências; D1–D6 Megalos e Academy intocados. Pesquisa de roteamento: https://developer.mozilla.org/en-US/docs/Glossary/Hash_routing e https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22.html .

## Ajuste final da rodada — aviso único
O aviso de que as etapas Socii não acessam outras contas foi retirado de cada cartão e concentrado uma vez na área de proposições, somente quando houver pendências. Assim, a prévia continua inequívoca sem repetir linguagem técnica para cada participante. O roteiro v0204 também verifica a nota única e ausência de repetição no cartão. Não altera o contrato de conclusão.
