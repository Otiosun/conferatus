# CONFFRATUS — Foco não obscurecido em telas baixas (checkpoint 140, 09/11/2026)

## Regra 21: investigação fria e escopo

O teste `browser_stage7_short_viewport_v0187.py` já assegurava navegação funcional em alturas curtas, mas não demonstrava se os controles sob foco estavam *visíveis acima de camadas da interface*, especialmente o rodapé. A WCAG 2.2 AA SC 2.4.11 exige que controles com foco do teclado não fiquem **totalmente obscurecidos por conteúdo criado pelo autor**.

Fontes consultadas em 09/11/2026:
- W3C/WAI: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum
- W3C técnica F110 (rodapés/cabeçalhos fixos): https://www.w3.org/WAI/WCAG22/Techniques/failures/F110.html

## Reproduzir sem falsos positivos

Uma sondagem exploratória grosseira inicialmente contou como "obscurecido" o próprio botão do rodapé (que está visível) e o elemento `body` no fim do ciclo Tab, além de aferir o *skip link* no instante de uma transição CSS. O isolamento da rota mostrou que o skip link recebe foco e surge no topo após a transição. Alterar o CSS para mascarar isso introduziria regressão sem evidência.

Decisão: testar o **elemento efetivamente focado** com retângulo de interseção à viewport e nove amostras `document.elementFromPoint`, aguardando dinamicamente apenas a estabilização de foco/rolagem (Playwright `wait_for_function` até 1,5s); ignorar o `body`, que não é um controle, e **não** excluir o botão do rodapé, pois ele deve permanecer acessível. Se todos os pontos do elemento continuarem ocultos, falhar com captura de prova. Nenhum `sleep` fixo ou alteração estética.

## Implementação e testes

- Novo `tests/browser_stage7_focus_not_obscured_v0188.py`, commit `ec53226f2048dc33a820f47facbe202f195eaa49`; Git blob verificado `519e6fb1293518b1ab04c0ef17a7910bf62970c1`. SHA256 fonte local `3ff2ab1d9e3addb4c220a03ea6975433ad436d450367994d9f128e6dc993289e`.
- Workflow `.github/workflows/preview-voting-check.yml` passa a executar a v0188 dentro de `validate` junto à v0187; commit `e69f98face1bb73e094f4a3a1d42c8671f5a93e1`.
- HTML offline usado: artefato `CONFFRATUS-v0.10.60-preview` do run Actions 42708774184 (commit `bb14e32a`); após essa execução, até o checkpoint 139, a branch sofreu apenas alterações de testes/workflow/documentação, sem modificação de HTML, CSS ou JavaScript da aplicação.
- Teste local no Chromium: **192 controles focados examinados**, em **12 combinações** de três viewports (320×256, 390×320, 740×360) e quatro rotas (votação, membros, calendário, editor). Nenhum controle ficou totalmente fora da viewport ou sem ponto detectável sob seu próprio elemento, após a estabilização de transições; nenhum erro JS do documento nos casos examinados.
- Primeira versão de prova com leitura instantânea gerou falso positivo transitório de `skip-link`; teste final não ignorou a falha nem a suprimiu, mas introduziu espera condicional que observa sua visibilidade real, com timeout e captura caso nunca apareça.
- Não foi preciso corrigir a aplicação, CSS ou comportamento de voto/Academy; preservadas as regras, identidade visual e a `main`.

## Limites obrigatórios

**Isto não constitui certificação WCAG 2.2 AA.** A sondagem examina pontos amostrados da área focada, não todos os pixels/indicadores de foco; não testa VoiceOver/TalkBack reais, dispositivos físicos, zoom nativo de 400%, IME/teclado virtual Android/iOS nem todas as telas, estados e larguras. A CI remota da branch privada ainda pode falhar antes de alocar runners; somente a execução local está verificada e não podemos chamar o workflow de verde no novo SHA.

Contagem formal inalterada: Etapa 07 = 7/12; todas etapas = **33/57**. Itens 07.05, 07.06 e 07.10–07.12 continuam em aberto; decisões visuais D1–D6 e contratos Academy exigem homologação e integrações separadas.

Arquivo de evidência integral, JSON de 192 verificações e fonte exata serão arquivados no Google Drive Komekko e vinculados ao handoff mestre/checklist. Monitoramento de Actions de alta frequência segue desativado por pedido do responsável.

Próximo gate: buscar defeito objetivo adicional de reflow/IME ou preparar o pacote de aceite Megalos D1–D6 sem inventar respostas institucionais.
