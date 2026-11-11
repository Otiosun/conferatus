# CP169 — Orientar a primeira votação sem alterar regras (11/11/2026)

Escopo autorizado: pré-entrega, corrigir confusão de navegação de quem nunca usou o site, sem iniciar integração ou mudanças de votação institucional.

A navegação implementada já possuía redação, revisão, Socii opcional, agendamento, seis modalidades e confirmação local. O botão “Iniciar uma Votação” no calendário, contudo, apenas abria agendamento e exigia uma proposição concluída. A página inicial exibia números fixos sem identificá-los como exemplo. Programações próprias não têm apuração acumulada nessa prévia, e as datas não controlam automaticamente a participação. O site agora explica esses fatos no contexto da ação: entrada principal, lista de proposições se nenhuma concluída, calendário, formulário, registro de exemplo e ação de participar.

Alterações: `src/main.ts` (apenas apresentação e texto de retorno), `src/styles.css` (pistas discretas), `docs/DEMO_GUIDE.md`, `tests/browser_first_time_voting_journey_v0211.py`, checklist e handoff. Nenhuma opção de voto, validação, status da programação, armazenamento, calendário ou resultado foi alterado. Socii é opcional no roteiro fictício; regras futuras dependem de decisão Megalos, não assumir aprovação.

Referências oficiais consultadas em 11/11/2026: W3C WAI https://www.w3.org/WAI/tutorials/forms/ e https://www.w3.org/WAI/tutorials/forms/instructions/ . As instruções de pré-requisito são visíveis antes dos campos; não substituem rótulos nem criam wizard.

Teste v0211: browser real sem registros próprios, diferenciação inicial, calendário bloqueado antes de proposição concluída, criação, revisão, programação nominal, comprovante e retorno sem alterar números de exemplo, nas quatro larguras. Suíte existente mantida; verificar CI do SHA final antes de afirmar aprovação. Main e produção não foram modificadas. Contagens 8/38 funcional e 43/57 histórica, Android real, comparação Megalos D1–D6 e aprovação visual ainda abertas.
