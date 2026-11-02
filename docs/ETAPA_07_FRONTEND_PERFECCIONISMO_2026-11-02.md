# CONFFRATUS — Etapa 07 | Perfeccionismo visual, front-end e responsividade

**Criada a pedido expresso do responsável em 02/11/2026.** Esta é a **sétima etapa autônoma** do projeto. Não substitui a Etapa 06 de entrega, nem modifica suas contagens. Seu objetivo é polir a experiência real em todos os tamanhos suportados, não apenas impedir que a página role horizontalmente.

## Princípios e critério de aceite

- **Fidelidade à Megalos sem adivinhação:** manter as seis imagens e o vídeo como evidências; mudanças conflitantes dependem de resposta D1–D6. Corrigir defeitos objetivos de uso e acessibilidade independentemente de decisões institucionais.
- **Responsividade verificável, não promessa de universalidade:** não existe garantia matemática para todos os dispositivos e conteúdos possíveis. Definir e testar uma matriz reproduzível, detectar regressões e validar em hardware real antes de chamar a etapa concluída.
- **Sem design cenográfico:** cada ação permanece operante, nenhum botão decorativo, nem alteração de regra de voto/Socii/Academy por motivo estético.
- **Código humano e previsível:** usar CSS fluido, minmax, flex/grid, padding e media queries focadas; não adicionar framework, polyfill ou dependência por conveniência superficial.
- **Matriz de referência:** 280, 320, 360, 390, 540, 740, 768, 1024, 1440 px, com alturas/rotações variadas. Explorar 1920 px, zoom 200%/400%, texto grande, nome longo, teclado virtual e área segura de telas com notch. Testar Chromium, Firefox/WebKit quando disponíveis e aparelhos reais; identificar lacunas explicitamente.
- **Alvos interativos:** trabalhar preferencialmente com 44×44 px em controles por toque, preservando espaçamento; respeitar ao menos os mínimos aplicáveis WCAG 2.2 AA (incluindo exceções justificadas). Foco de teclado visível e navegação sequencial coerente.
- **Telas/estados:** votação, diretório, perfis, histórico, gerenciamento, calendário, agendamento, proposições, editor, folha de revisão, estados Socii, menus, pesquisa, formulários, feedbacks e estados vazios/erro.
- **Regressão:** teste funcional de fluxo + medida DOM + captura visual antes/depois, relatório de divergências e decisão explícita sobre qualquer mudança de hierarquia da Megalos. Não usar `overflow-x:hidden` como remendo que esconda conteúdo inacessível.

## Checklist exclusiva da Etapa 07 — 4/12 subitens concluídos na v0.10.34

- [x] **07.01 — Inventário inicial de reflow:** sete rotas principais × nove larguras (280–1440 px) em Chromium, **63 verificações sem rolagem horizontal nem elementos escapando**, no HTML offline. Evidência: `tests/browser_frontend_reflow_v0126.py`. *Isto não cobre todos os estados/zoom.*
- [x] **07.02 — Primeiro alvo de toque corrigido:** botão Buscar do diretório media **18 px de altura** antes; teste falhou nessa condição. A prévia agora garante 44 px em 280–540 px, sem cobrir a primeira linha, mantendo busca e filtros funcionais. Evidência: `tests/browser_frontend_touch_target_v0126.py`, cinco larguras, capturas 320/390.
- [x] **07.03 — Auditoria dos alvos da prévia offline:** nove larguras, 19 estados mapeados, 2.769 ocorrências de controles; exceções do calendário, testes de clique, erros e retorno contextual. Cobertura restrita a Chromium offline, não dispositivo real.
- [x] **07.04 — Tipografia legível e conteúdo extremo:** textos muito longos, palavras sem separação, nomes extensos, dados ausentes, erros e validação, quebra sem sobreposição; evitar microtipografia em telas compactas.
- [ ] **07.05 — Zoom/reflow acessível:** 200% de texto e 400% de zoom onde aplicável, equivalência a viewport CSS de 320 px conforme WCAG; nenhuma perda funcional ou scroll bidirecional indevido.
- [ ] **07.06 — Telas compactas completas:** 280/320/360/390 px, orientação, altura curta, teclado virtual e safe-area; testar fluxos inteiros em vez de só página inicial.
- [ ] **07.07 — Tablets 600–1024 px:** retrato, paisagem, distribuição de colunas e densidade; evitar interface apenas de celular aumentada.
- [ ] **07.08 — Desktop largo 1280–1920 px:** composição intencional e leitura confortável, foco/hover coerentes, sem esticar o mockup nem desperdiçar a área de forma acidental.
- [ ] **07.09 — Teclado e foco:** Tab/Shift+Tab, Escape, controles de menu, formulários, revisão, seleção e retorno do foco; ordem lógica sem focus trap inadvertida.
- [ ] **07.10 — Acessibilidade e legibilidade:** contraste, rótulos, semântica, mensagens de erro/estado, leitores de tela, reduced motion e WCAG 2.2 AA nos critérios aplicáveis, com evidência e exceções.
- [ ] **07.11 — Regressão visual e Megalos:** capturas por estado, diferenças revisadas contra as seis imagens/vídeo, e aceite expresso das decisões D1–D6 antes de chamar fidelidade concluída.
- [ ] **07.12 — Matrizes finais e aparelhos reais:** Chromium + motores adicionais disponíveis, celulares/tablets reais, rotação/zoom, regressão completa e aceite final técnico/visual documentado.

## Execução inicial v0.10.26

**Defeito reproduzido antes:** `[data-action=search]` no diretório móvel possuía retângulo clicável de 18 px de altura em 280/320/390 px; teste específico falhou em 280 px com `Touch target too short`.

**Correção:** somente `src/styles.css` — dentro de `@media (max-width:540px)`, o diretório reserva mais 11 px de espaço superior, e o botão de busca usa `min-height:44px`, alinhamento central e deslocamento `top:-12px`. Teste confirmou ausência de interseção com o primeiro membro e o filtro segue funcionando. Não mudar a tipografia da Megalos, dados, scripts ou comportamento institucional.

**Verificação:** `npm run build` aprovou TypeScript, publicação HTML e 18/18 testes Node; `tests/browser_frontend_touch_target_v0126.py` passou 5/5 larguras e `tests/browser_frontend_reflow_v0126.py` passou 63/63 combinações. Capturas 320 e 390 px foram revisadas. As demais suítes do repositório são executadas e reportadas separadamente; nenhuma aprovação será presumida sem término. A prévia é offline e não certifica identidade Academy, WebKit/Firefox ou dispositivos físicos.

**Status preservado das etapas anteriores:** 01 4/5, 02 0/4, 03 1/5, 04 17/22 ativa, 05 0/4, 06 0/5. Etapa 07 **2/12**. Nenhuma produção alterada.

## 07.03 — lote técnico inicial, v0.10.27 (não encerrado)

O item 07.03 permanece **[ ] PENDENTE**. 63 cenários exploratórios de sete rotas em nove larguras mediram 810 nós interativos visíveis; quatro defeitos/fragilidades alvos receberam correção CSS pequena: perfil 19,2px, home 28px, participar na votação fictícia 23px, busca desktop 18px. Novo teste falhou antes (23px) e passou 9/9 depois, com dimensões 44px e ações funcionando. Reflow 63/63, regressão 07.02 5/5, build + 18/18 Node aprovados. O inventário ainda não cobre todos os estados e não certifica WCAG. Conferir `docs/CHECKPOINT_V037_2026-11-02.md`; prosseguir com expansão de calendário, abas, gerenciamento, editor e revisão antes de marcar 07.03, sem modificar D1–D6 ou lógica institucional.

## 07.03 — Lote 2, v0.10.28 (pendente de encerramento)

Novo ensaio `tests/browser_stage7_expanded_touch_v0128.py` comprovou 106 ocorrências de alvos menores que o objetivo de conforto entre 135 observações em nove larguras, **antes** da correção; 0/135 abaixo da meta **depois**, sem eliminar as interações. Ajuste apenas em `src/styles.css` para voto demonstrativo, abas, calendário, atalho para proposições, editor, gerenciamento e formulário local. Células de calendário a 280px mantêm 7 colunas e largura >=24px por viabilidade espacial e WCAG 2.2 AA; meta confortável de 44px aplica-se à altura. Regressão visual do título do mês em duas linhas foi reproduzida e corrigida. Testes de build 18/18 Node, teste novo 9/9 larguras, baseline de reflow 63/63 e suítes de regressão pertinentes aprovadas. Consulte `docs/CHECKPOINT_V038_2026-11-02.md` para limites e evidências. **07.03 permanece [ ]**, 07=2/12. Não há aceite da Megalos nem conformidade integral WCAG demonstrados.

**07.03, correção de identidade visual v0.10.29:** símbolo real da Academy fornecido pelo responsável substitui o ícone provisório no rodapé/menu. Sem criação de mockups, sem redesenhar arte, sem alterar navegação nem lógica. Ajustada área gráfica para não encobrir o último item do menu. Testes específicos em 9 larguras × 2 rotas e `npm run build` OK. Não altera a contagem oficial (07=2/12) nem encerra 07.03. Evidência: `docs/CHECKPOINT_V039_2026-11-02.md`.

**07.03 — Lote 3, v0.10.30:** auditoria isolada de quatro alvos contextuais (buscar sem resultados, desfazer alteração administrativa da prévia, reiniciar painel de simulação, perfil inexistente) em nove larguras × quatro estados = 36 medições. Antes 36 retângulos abaixo da meta de conforto em altura; depois 0 abaixo, com clique/hit-test comprovados, nenhuma rolagem horizontal e sem mudanças em lógica/arte. Ver `tests/browser_stage7_dynamic_targets_v0130.py` e `docs/CHECKPOINT_V040_2026-11-02.md`. **07.03 ainda [ ]**, 07=2/12, D1–D6 pendentes.

**07.03 — Lote 4, V041:** ao salvar um rascunho vazio, o aviso da validação não aparecia na tela embora existisse no estado interno. Falha reproduzida em Chromium; mensagem agora é visível no próprio editor como `role="alert"` e foco retorna ao título. O teste de nove larguras também cobriu campos inválidos de gerenciamento, salvamento, confirmação e cronologia de agendamento; **72/72** medições de alvos de menu/painel. CSS apenas amplia painel, botão Menu e duas entradas intermediárias. Build 18/18 Node, reflow 63/63 e testes de regressão selecionados aprovados; detalhes e limitações em `docs/CHECKPOINT_V041_2026-11-02.md`. **07.03 continua [ ]; 07=2/12.**


## Fechamento da 07.03 — v0.10.32 (02/11/2026)

O último lote mediu os controles que ainda faltavam em estados menos comuns: seletor de perfil simulado (35px), seletor de membro (35px), Vincular (28px), campo de busca (35px) e skip-link visível ao focar (35px). Antes, 45/45 ocorrências tinham altura inferior à meta de conforto. Após regras CSS específicas, 45/45 estão >=44px, com hit-testing no centro e funcionalidade preservada.

O inventário reproduzível `tests/browser_stage7_all_controls_v0132.py` cobriu 19 estados × 9 larguras (280, 320, 360, 390, 540, 740, 768, 1024, 1440 CSS px), coletou 2.769 ocorrências e registrou zero alvos abaixo dos mínimos previstos. Todos os controles com largura <44px eram **dias da grade** (300 medições; mínimo >=24px e altura >=44px), conforme a exceção espacial explicitada para sete colunas. O link de pular conteúdo foi medido quando efetivamente visível com foco, fora do scanner principal.

Regressões específicas concluídas após a última mudança: build 18/18 Node, formulário 72/72, lote expandido 135/135, dinâmicos 36/36, lote1 em nove larguras, reflow 63/63, pesquisa original em cinco, emblema Academy nove × duas rotas e smoke quatro larguras. Logs e capturas estão no backup delta. Há limites: nenhuma verificação WebKit/Firefox, zoom, hardware físico ou homologação Megalos; WCAG 2.2 AA global **não foi certificada**. Estas são etapas posteriores 07.05/07.09/07.10/07.12, não motivo para reabrir 07.03 sem defeito novo.

**07.03 [x] encerrada no escopo da prévia offline; 07=3/12.** Próxima tarefa: **07.04** — tipografia, nomes longos, textos extremos, estados vazios e microtextos. Etapa 06 e D1–D6 continuam pendentes.

## 07.04 — lote 1, V043 (02/11/2026)

Reprodução objetiva de overflow provocado por palavras/identificadores sem separação: **94/108** cenários em nove larguras falhavam antes; **0/108** falham após CSS local com `overflow-wrap:anywhere`, `min-width:0` para flex e código de atividade com quebra habilitada. Também testados títulos reais com 140 caracteres e corpos de 2.001 caracteres em nove larguras, de editor até registro final. Nenhum dado ou regra institucional foi alterado. `npm run build` com 18/18 Node e regressões de 07.03, reflow, formulários, rascunhos, folha de revisão, Academy passaram. Capturas foram revisadas. **07.04 ainda [ ]**, pois a varredura independente descobriu 174 ocorrências de elementos textuais visíveis abaixo de 10px em oito rotas × três larguras amostradas; examinar metadados, indicadores e disclosure com fidelidade à Megalos e sem corrigir indiscriminadamente fontes. Evidências em `docs/CHECKPOINT_V043_2026-11-02.md`; 07=**3/12**. Não afirmar WCAG completa, zoom/hardware real, D1–D6 ou etapa 07 concluída.


## 07.04 — lote 2 e fechamento, V044 (02/11/2026)

Após V043, a microtipografia de metadados (7–9px) ainda era difícil de ler. Uma auditoria de 8 rotas × 3 larguras registrou **174 ocorrências <10px**. O novo teste por grupos críticos (`tests/browser_stage7_microtype_v0134.py`) reproduziu **367/567** abaixo do piso legível antes da correção em quatro rotas × nove larguras. Ajuste CSS específico estabeleceu piso de **10px** nos dados de votação demonstrativa, rótulos de métricas, código/data de atividade, cargo do perfil e indicação de dados fictícios. O aviso da prévia quebra em duas linhas apenas na largura extrema 280px e não invade o emblema oficial/menu. As fontes desktop maiores foram preservadas.

**Depois:** 567/567 amostras de metadados conformes à meta interna, auditoria equivalente **174→0** ocorrências <10px; nove larguras sem colisão de métricas; reflow **63/63**, conteúdo longo **108/108**, Node **18/18**, inventário geral **2.870** alvos sem falhas, formulários, Academy e controles prévios aprovados em execução isolada. **10 CSS px não é uma exigência WCAG** e esta aprovação só vale à prévia Chromium offline. Provas, limitações e capturas: `docs/CHECKPOINT_V044_2026-11-02.md`.

**07.04 [x] CONCLUÍDA no escopo testado; 07=4/12.** Zoom, texto ampliado, acessibilidade global, motores adicionais, hardware e aprovação Megalos continuam nas tarefas posteriores. Próxima **07.05 — zoom/reflow acessível**.
