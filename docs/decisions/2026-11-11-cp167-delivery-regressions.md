# CP167 — Reconciliação de regressões para a entrega à Megalos (11/11/2026)

Branch `preview/v0.10.60-six-vote-forms`, base `60f70be4705d055ac27b0b76bf1efe7155ab198d`. Mudanças estritamente de experiência de prévia e tests de seus contratos anteriores, sem alterar Academy, regras institucionais ou a `main`.

## Evidência real e escopo
Primeira execução integral após GitHub Actions começar a funcionar: https://github.com/Otiosun/conferatus/actions/runs/42942831185/job/130788653612 . **76 scripts de navegador executados, sete falharam**, TypeScript e testes Node passaram, screenshot/HTML foram publicados como artefatos. As regressões v0204–v0210 e `browser_full_workflow_journey_v0173.py` passaram em todas as larguras programadas. O job de navegador como um todo não passou.

Classificação dos sete problemas:
1. `browser_calendar_return_v0120.py`: seletor genérico `.workflow-finished strong` tornou-se ambíguo após novo resumo de revisão. Restringido ao forte título direto da mensagem, mantendo a verificação funcional do retorno.
2. `browser_product_vote_isolation_v0202.py`: retorno de participação contextual vai ao calendário, não diretamente aos resultados fictícios. Regressão atualizada para verificar calendário e retorno explícito à página inicial, com espera pelo DOM entre rotas.
3. `browser_history_isolation_v0197.py`: botão técnico `toggle-voting-forms` foi removido da interface normal. Fluxo atualizado para a única ação natural `Participar` e formulário nominal predefinido, mantendo a verificação dos históricos.
4. `browser_stage7_dynamic_focus_v0200.py`: CP162 corrigiu o foco após cancelamento para o botão de histórico, não para o cabeçalho. Atualizada apenas a expectativa.
5. `browser_preview_disclosure_v0117.py`: cobertura antiga tentava selecionar os botões do laboratório numa página normal. Agora verifica a participação direta, o recibo local, totais históricos imutáveis e a ausência do seletor técnico; segue conferindo avisos, calendário e Socii.
6. `browser_stage7_live_announcer_v0144.py`: defeito de acessibilidade; mensagem visual `.workflow-status` tinha `role=status` adicional ao anunciador persistente `#app-live-announcer`. Removido o papel duplicado do texto visual, mantendo anunciador estável e texto.
7. `browser_stage7_error_fields_v0141.py`: ao salvar rascunho completamente vazio, erro se aplica a **ambos** os campos. Introduzido valor `both` em `composeErrorField`; título curto ou redação curta na conclusão continuam marcando somente o campo pertinente, preservando a regressão v0205.

Sem falhas ocultadas e sem suprimir scripts. Fontes oficiais consultadas em 11/11/2026: https://playwright.dev/python/docs/locators (estrita unicidade, auto-wait), https://www.w3.org/TR/wai-aria/ (papel status cria região de anúncio), https://www.w3.org/WAI/tutorials/forms/notifications/ (erros e seus campos). Escolhidas alterações mínimas de testes antigos e duas correções de acessibilidade.

## Gate
Código proposto deve passar `npm run build`, regressões Chromium e inspeção de navegador em artefato do SHA exato. Ainda exige abertura no Android físico, comparação visual com materiais da Megalos e decisões D1–D6 para homologação; não marcar como entregue/publicado na main. 8/38 funcional, 43/57 histórico mantidos até evidências conclusivas.
