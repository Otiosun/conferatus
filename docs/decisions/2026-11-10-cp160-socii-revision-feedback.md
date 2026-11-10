# CP160 — Explicação das etapas de revisão após alteração (10/11/2026)

Base privada: `a96bfde83d82f755a7f98cc772af9070c57683cb`. A edição de proposições já reiniciava as etapas fictícias anteriores quando o conteúdo mudava, mas a passagem direta “Concluir redação” → revisão não explicava os novos estados. Foi adicionada uma nota breve na revisão normal somente quando houve alterações com etapas concluídas previamente, reutilizando a variável existente `confirmationsReset`. A modalidade experimental D3 e o caminho de “Salvar rascunho” foram preservados.

Arquivos: `src/main.ts`, `src/styles.css`, `tests/browser_socii_revision_feedback_v0207.py`, workflow e checklist. A prova sintética cobre revisão inalterada, edição com aviso, progressão 0/N a N/N e feedback ao salvar rascunho em 320/390/740/1280px. Ainda não foi executada. Evidência de build Cloudflare será verificada pelo SHA final; PF-16 permanece aberto até aceitação real.

Referências W3C WAI / MDN consultadas em 10/11/2026: https://www.w3.org/WAI/WCAG21/Understanding/status-messages ; https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA22 ; https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus . A nota acompanha a nova tela, sem alerta invasivo. Dados continuam fictícios, sem login Academy; main e produção não são alvos. Contagens 8/38 e 43/57 inalteradas.
