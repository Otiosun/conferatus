# CP159 — Revisão de proposições com participantes e próximo passo
Data: 10/11/2026. Base privada: `11bf8f4de7f686cfc46833b9f55da96aec8fa235`. Escopo: UI de proposições da prévia, sem implementar identidade, convite real ou regra institucional.

## Evidência e decisão
A revisão normal já continha título, texto renderizado, seção e tipo, mas deixava participantes/estado do Socii dispersos fora da tela e não oferecia um passo de agendamento após a conclusão. A revisão passa a mostrar um resumo discreto dos estados de autoria e participantes fictícios, com instrução dinâmica sobre a etapa seguinte. A proposta concluída reutiliza a ação `contextualScheduleButton` já existente para abrir agendamento vinculado, sem criar roteador ou lógica duplicada. Status e nomes derivam diretamente do registro local em memória, nunca de autenticação Academy.

A variante opt-in `?demo=1&d3=single` não ganha novos elementos na modal; preserva a composição experimental e testes D3. O resumo foi integrado apenas à revisão normal e ao registro concluído.

Fontes oficiais revisadas em 10/11/2026: W3C WAI SC 3.3.2 (instruções claras e sem repetição desnecessária), W3C WAI Forms (labels/instruções), MDN sobre disclosure nativo. Preferimos seção sem colapso, evitando um clique extra antes da confirmação:
- https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions
- https://www.w3.org/WAI/tutorials/forms/labels/
- https://www.w3.org/WAI/tutorials/forms/instructions/
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details

## Arquivos e prova planejada
`src/main.ts`, `src/styles.css`, `tests/browser_review_next_steps_v0206.py`, `.github/workflows/preview-voting-check.yml`. Roteiro v0206 prepara duas proposições inteiramente fictícias (uma esperando Socii e outra concluída) e verifica, em 320/390/740/1280px, título, corpo, seleção, nomes/estados, próximo passo, ausência de agendamento em pendência, agendamento da concluída e ausência de erro/overflow.

**Execução local dos testes e screenshot de Android ainda não efetuados.** Verificar check Cloudflare no SHA exato; não equivaler publicação de prévia à validação PF-13. D1–D6 continuam dependentes da Megalos; PF-13 permanece aberto até evidência de navegador. Contagens funcional 8/38 e histórica 43/57 preservadas. Main e produção intocadas.

## Caso adicional — revisão individual
O roteiro v0206 foi estendido com uma proposição sem participantes do Socii. Verifica a ausência de barra de colaboradores, a indicação de que ninguém está vinculado, a próxima ação de confirmação e a conclusão individual. A prova está pronta e versionada, ainda sem execução no navegador real.
