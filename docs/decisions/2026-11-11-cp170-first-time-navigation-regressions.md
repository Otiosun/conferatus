# CP170 — Regressões do roteiro de primeira votação (11/11/2026)

Base exata: `43c252232228a7cd8933a05af070916c8e69aeaf` na branch privada de desenvolvimento `preview/v0.10.60-six-vote-forms`. Relatório completo: https://github.com/Otiosun/conferatus/actions/runs/43114663738 .

A primeira execução CP169 confirmou build TypeScript/Node SUCCESS, PostgreSQL SUCCESS e Cloudflare SUCCESS, e percorreu 77 scripts Chromium. Seis scripts anteriores falharam **apenas nas verificações de navegação e rótulos alterados**: `browser_smoke.py` esperava o antigo texto de orientação do calendário; `browser_local_archive_v0158.py`, `browser_profile_proposals_v013.py`, `browser_socii_multiple_drafts_v0176.py` e `browser_calendar_v012.py` procuravam `[data-route=proposals/calendar]` em toda a página, que agora corresponde tanto ao novo atalho da home quanto ao item do menu aberto; `browser_preview_disclosure_v0117.py` ainda esperava “Iniciar uma Votação”, “Programar deliberação” e o texto de datas anterior. A regressão nova v0211 **não falhou**, evidenciando que o percurso novo funcionou no CI.

Os seis scripts foram reconciliados mantendo as ações reais de menu `.menu-item[data-route=...]`, os testes de cópia local, perfis, Socii e calendário, e verificando os rótulos atualizados. Não houve remoção de testes ou afrouxamento das asserções sobre funcionalidade. O mesmo conjunto de 77 scripts continua na CI. **A execução desse novo SHA é necessária para declarar a suíte verde.**

Regra máxima: o botão chama “Programar votação” porque abre um agendamento, não controla abertura/encerramento temporal. O material visual/histórico da Megalos permanece como referência, decisão formal sobre nomenclatura final pertence a ela. Não alterar `src/main.ts`, `main`, produção, dados nem integração. Seguimos em prévia para avaliação; Android físico e decisões D1–D6 permanecem pendentes.

Referências: https://playwright.dev/python/docs/locators (correspondência estrita e composição de localizadores) e https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions . Nenhuma dependência adicionada.
