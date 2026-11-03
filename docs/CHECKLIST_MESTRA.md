# CONFFRATUS — Checklist-mestra de execução

Atualização de referência: 01/11/2026
Responsável pelo acompanhamento: desenvolvimento CONFFRATUS
Status de retomada (01/11/2026): `main` permanece em v0.10.5 (`4b24459`) sem alterações de produção. Última prévia funcional confirmada remotamente antes desta rodada: `preview/v0.10.22-socii-explicit-choice` (`8023643`, Cloudflare `completed/success`). A v0.10.20 restaurou o retorno contextual do calendário. A v0.10.21 corrigiu gravação local parcial por reversão de melhor esforço. A v0.10.22 corrige a seleção implícita do primeiro participante na inclusão do Socii; agora o campo exige escolha explícita via validação HTML nativa. A v0.10.23 é **somente documentação de validação Megalos**: seis capturas comparadas às seis imagens originais, PDF de 7 páginas e decisões D1-D6; nenhum código de produto alterado, nenhum aceite presumido. A v0.10.24 acrescenta auditoria temporal de 54,66 s do vídeo original, sem modificar o produto: a faixa Socii aparece também na revisão, há duas variantes visíveis de confirmação sem regra conhecida, e Ofício já está contemplado na prévia. Nenhuma regra institucional ou integração foi inventada. A Etapa 04 continua ativa (17/22 subitens), com cinco critérios centrais pendentes; votação, Academy e Socii continuam exclusivamente demonstrativos.

> **Marca exibida desde a prévia v0.10.25: CONFFRATUS.** Correção solicitada diretamente pelo responsável em 02/11/2026, substituindo a grafia de interface CONFERATUS. As capturas originais da Megalos exibem CONFERATUS e são preservadas como fontes históricas; validação formal de grafia com a Megalos não foi comprovada. Os endereços `Otiosun/conferatus`, `conferatus.pages.dev`, chaves `conferatus:*` e o arquivo offline legado são identificadores técnicos estáveis, não a marca pública. Sem migração automática que arrisque dados.

> Fonte oficial para retomar o trabalho. Nenhuma tarefa é concluída apenas por existir uma tela ou um commit. Não mudar o nome do produto sem confirmar a grafia com a Megalos.

## 01 — Estabilização e consolidação
- [x] Investigar e corrigir o build remoto da v0.9.9. Preview aprovado (`0bb4435`), produção aprovada (`3150cd2`).
- [x] Reconciliar a v0.10.0 com o GitHub; preview `fe4bbeb` e produção `8f50177` publicados.
- [x] Validar localmente as quatro seções e a separação entre deliberativos e membros comuns (base v0.9.9).
- [x] Validar localmente o gesto de arrastar o rodapé e manter o botão alternativo.
- [ ] Confirmar com a Megalos a grafia oficial: CONFERATUS ou CONFFRATUS.
**Estado:** quatro de cinco tarefas concluídas. Falta confirmar a grafia oficial com a Megalos.

## 02 — Votação e registro
- [ ] Consolidar o modelo de votação e seus estados.
- [ ] Associar deliberações, seções e proposições conforme a especificação.
- [ ] Implementar o registro institucional quando as regras forem confirmadas.
- [ ] Verificar o funcionamento do fluxo completo com dados fictícios e depois com a integração oficial.
**Estado:** simulação existente; comportamento institucional definitivo ainda não aprovado.
**Dependências:** participação por seção, peso por participante, visibilidade do registro, alteração de escolha e responsáveis pelos procedimentos.

## 03 — Perfis e históricos
- [ ] Consolidar históricos pessoais e institucionais com os dados da aplicação.
- [ ] Preservar registros antigos após mudança de cargo ou rebaixamento.
- [ ] Revisar os indicadores Votos, PDR, PR, Ofício e Socii conforme novos modelos.
- [x] Exibir proposições locais no perfil do autor, separadas do histórico demonstrativo (v0.10.3; testado localmente).
- [ ] Integrar as listas de proposições e deliberações aos respectivos perfis.
**Estado:** parcialmente implementado em demonstração.

**Ajuste v0.10.3:** o editor e o perfil do autor compartilham a lista de proposições da sessão. Mensagens de salvamento distinguem armazenamento efetivo de dados apenas em memória.

## 04 — Calendário, proposições e Socii
- [x] Construir calendário mensal interativo, dias programados e filtro de agenda (v0.10.2; verificação local).
- [ ] Finalizar a tela do calendário e a lista de programações após revisão de fidelidade com a Megalos.
- [x] Aproximar linhas e detalhes expandidos da referência 1001930221.jpg, exibindo Socii apenas quando vinculado a proposição da sessão, sem inventar códigos de registro (v0.10.9; testes locais e preview).
- [x] Ligar uma programação demonstrativa à proposição concluída e exibir a proposição vinculada.
- [ ] Finalizar o agendamento: proposição, seção, datas, tipo, título e descrição objetiva (regras institucionais pendentes).
- [x] Validar a integridade de registros de sessão e vínculos de programação: isolar entradas incompletas, preservar entradas válidas, arquivar localmente dados rejeitados antes da próxima gravação e identificar vínculos indisponíveis (prévia v0.10.14; regressões em quatro larguras).
- [x] Recuperação de sessão reforçada: preservar texto JSON ilegível e objetos em formato errado antes de sobrescrever armazenamento local, rejeitar registros falsamente concluídos sem assinaturas e reconstruir registros válidos (v0.10.15, teste em quatro larguras).
- [x] Impedir IDs duplicados em proposições, programações e participantes Socii restaurados. Preservar primeira ocorrência válida e versões rejeitadas em histórico de quarentena sem sobrescrever cópias antigas (prévia v0.10.16; teste de quatro larguras).
- [ ] Finalizar redação, revisão, confirmação e estados de proposições.
- [x] Aproximar folha de revisão e confirmação de proposição dos modelos `1001930222.jpg` e `1001930223.jpg` (preview v0.10.10; opções e regras preservadas; aprovado em quatro larguras).
- [x] Corrigir nova redação independente e salvar/retomar rascunho incompleto na prévia local (v0.10.1; testes em 320/390/740/1280 px).
- [x] Mostrar andamento de conclusão de Socii (0/2 → 1/2 → 2/2) na prévia, sem representar convites como reais.
- [ ] Consolidar a colaboração Socii e seus estados de conclusão.
- [x] Corrigir integridade de versões na prévia: mudança de título/texto reinicia confirmações de autoria e Socii (v0.10.13); alteração da seção responsável ou do tipo na revisão invalida confirmações anteriores do Socii (v0.10.19). Dados idênticos preservam aprovações, participantes não são removidos e pendências de autoria/Socii continuam distintas. Falhas reproduzidas antes das correções e testes em quatro larguras.
- [x] Aproximar o editor Socii do modelo `1001930224.jpg` com faixa de participantes vinculados, identificação de prévia local e progresso 0/2–2/2, sem tempo fictício ou colaboração remota (v0.10.12; quatro larguras e regressões).
- [x] Aproximar o editor de proposições do modelo de redação minimalista, preservando título editável, rascunho e botões (v0.10.5; comparação visual local).
- [x] Realizar comparação documental de cada uma das seis imagens e amostragem do vídeo da Megalos, registrando diferenças, decisões não autorizadas e critérios de aceite (auditoria v0.10.17; **não equivale a validação visual final**).
- [ ] Conferir as novas telas com as seis imagens e o vídeo da Megalos.
- [x] Alinhar perfil, indicadores, histórico de proposições e Socii com a referência `1001930225.jpg`; reusar componente de membro, filtrar proposições por autor e manter rascunhos identificados como dados locais (preview v0.10.11, verificação em quatro larguras).
- [x] Ajustar apresentação do formulário de agendamento para o painel azul da referência 1001930226.jpg, mantendo campos e regras existentes (v0.10.8; comparação local e regressão visual funcional).
- [x] Executar e validar em navegador a retenção de campos de agendamento durante a navegação do calendário (preview v0.10.6; Chromium em 320, 390, 740 e 1280 px; ainda não promovido a `main`).
- [x] Manter o botão Hoje e a marcação do dia consistentes após a meia-noite (preview v0.10.7; Chromium com relógio controlado em 390 e 740 px).
**Estado atualizado:** a `main` permanece na v0.10.5 (`4b24459`). A última prévia de produto aprovada foi a v0.10.17 (`b5e296f`); a v0.10.18 altera somente testes e documentação. Cinco tarefas centrais da Etapa 4 continuam abertas: fidelidade final do calendário, agendamento institucional, redação/revisão definitiva, colaboração Socii e aceite das seis imagens/vídeo. Os subitens técnicos anteriores são checkpoints, não aprovação dessas tarefas.
**Dependências:** regras detalhadas de Socii e atribuição de responsabilidades.

**Progresso incremental:** ajuste de rascunhos pronto e testado localmente; publicação da v0.10.1 aguardando confirmação do build de preview.

**Avanço v0.10.2:** compilação TypeScript, 18 testes Node e fluxos Playwright locais aprovados em 320/390/740/1280 px. Preview remoto em avaliação; sem alteração automática em produção.

## 05 — Integração posterior à Academy
- [ ] Definir uma interface simples para receber a identidade institucional.
- [ ] Usar o ACDM ID para referência de cadastro, sem criar cadastro independente.
- [ ] Deixar a integração do login para o responsável da Academy, conforme acordado.
- [ ] Validar os fluxos integrados quando a equipe fornecer a interface correspondente.
**Estado:** responsabilidade definida; integração externa pendente.

## 06 — Acabamento, validação e entrega
- [ ] Comparar o visual com os modelos originais e recentes.
- [ ] Revisar responsividade, textos, navegação e fluidez dos fluxos.
- [ ] Remover controles desnecessários de demonstração da experiência normal.
- [ ] Consolidar testes e publicar novos builds primeiro em preview, depois no `main`.
- [ ] Atualizar documentação e preparar a demonstração à Megalos, distinguindo recursos reais dos simulados.
**Estado:** revisão parcial e contínua; entrega final pendente.

## 07 — Perfeccionismo visual, front-end e responsividade absoluta verificável

**Etapa adicional solicitada pelo responsável em 02/11/2026.** Independente da Etapa 06 de entrega e da Etapa 04 de Socii. Critérios de aceite em `docs/ETAPA_07_FRONTEND_PERFECCIONISMO_2026-11-02.md`.

- [x] **07.01** Reflow inicial: 7 rotas × 9 larguras 280–1440px, 63/63 sem rolagem horizontal/clipping (Chromium offline; não todos os estados).
- [x] **07.02** Alvo de toque Buscar: reproduzido com 18px de altura; corrigido para 44px em 280–540px sem cobrir a primeira linha, toque e filtro testados em 5 larguras.
- [x] **07.03** Auditoria da prévia offline: inventário dos controles mapeados, dimensões e estados dinâmicos; 19 estados × 9 larguras, 2.769 observações, com exceções documentadas dos dias de calendário. Evidência V042.
- [ ] **07.04** Corrigir legibilidade tipográfica, microtextos, nomes extensos, erros e conteúdo de tamanho extremo.
- [ ] **07.05** Testar zoom 200%/400% e reflow de 320 CSS px sem perda de conteúdo/ação.
- [ ] **07.06** Testar todas as jornadas em celulares compactos, alturas curtas, rotação, teclado virtual e safe areas.
- [ ] **07.07** Validar composição de tablets (600–1024px; retrato e paisagem).
- [ ] **07.08** Validar composição desktop 1280–1920px, hierarquia e aproveitamento consciente da área.
- [ ] **07.09** Revisar ordem de Tab/Shift+Tab, Escape, foco e navegação do teclado por fluxo.
- [ ] **07.10** Auditar contraste, semântica, rótulos e leitor de tela contra critérios aplicáveis WCAG 2.2 AA.
- [ ] **07.11** Manter diffs visuais reproduzíveis e obter aceite Megalos de D1–D6 antes de declarar fidelidade.
- [ ] **07.12** Rodar matriz final em Chromium/Firefox/WebKit quando disponíveis e aparelhos reais, documentando limites.

**Estado da Etapa 07: 3/12.** Início v0.10.26, com `npm run build` **18/18 Node**, `tests/browser_frontend_touch_target_v0126.py` **5/5 larguras**, `tests/browser_frontend_reflow_v0126.py` **63/63 estados-larguras**, regressões direcionadas **13/13 suítes Playwright**. Nenhuma dessas medições é certificação de responsividade absoluta ou substitui testes em dispositivos reais. A marca da prévia permanece **CONFFRATUS**; `main` intocada.

## Leis permanentes
1. **Código humano:** legível, direto, com comentários úteis e sem abstrações artificiais; não falsificar autoria.
2. **Preguiça inteligente:** reutilizar tudo o que funciona, evitar duplicação, dependências e infra desnecessárias.
3. **Perfeccionismo verificável:** visual, linguagem, comportamento e testes coerentes; sem polimento infinito.
4. **Velocidade com controle:** mudança pequena, comparação, testes, branch de preview e publicação aprovada.
5. **Fidelidade:** o material da Megalos define o produto; hipóteses permanecem rotuladas como hipóteses.
6. **Custo mínimo:** preferir os recursos gratuitos já existentes e integrar-se ao ecossistema da Academy.
7. **Sem showcase disfarçado:** se algo está simulado, não declarar que está integrado ou concluído.

## Protocolo de retomada — aplicar antes e depois de cada rodada
1. Ler este documento, `AGENTS.md`, as últimas instruções da Megalos e o status atual do GitHub.
2. Escolher **uma prioridade** do checklist e registrar o critério de conclusão.
3. Implementar o mínimo necessário no código existente e testar o comportamento.
4. Atualizar o estado da tarefa neste arquivo, preservando histórico e pendências.
5. Informar: **feito / testado / publicado / pendente**. Nunca usar “publicado” sem confirmação de deploy.

## Decisões ainda aguardadas
- Grafia oficial CONFERATUS/CONFFRATUS.
- Regras completas da votação e dos registros pessoais.
- Funcionamento detalhado dos convites, edição compartilhada e conclusão Socii.
- Responsáveis e permissões das novas operações de agendamento e elaboração.

## Checkpoint — v0.10.0 (01/11/2026)
- **Feito:** branch de preview com calendário, agendamento, redação, revisão, Socii e indicador Ofício; produção recebeu exatamente a mesma árvore de código.
- **Testado:** compilação e 18 testes de lógica na v0.10.0 local; Chromium em 320, 390, 740 e 1280 px para proposição/agendamento; fluxo Socii pendente testado separadamente.
- **Publicado:** preview `fe4bbeb` e produção `8f50177`, ambos com compilação Cloudflare aprovada.
- **Pendente:** confirmação da grafia oficial, revisão visual integral das novas referências, regras finais de Socii e votação, integração com a Academy e validação física do domínio hospedado.

## Checkpoint de preview v0.10.6 (01/11/2026)
- **Feito:** correção mínima em `src/main.ts` para preservar campos de agendamento no calendário, branch isolada `preview/v0.10.6-calendar-form-state`.
- **Testado:** build remoto Cloudflare aprovado em `3423ba4`; build local e 18/18 testes Node aprovados; Playwright calendário, rascunhos, perfil, Socii e integração proposta-calendário aprovados em quatro larguras; menus em nove larguras.
- **Publicado:** nenhuma alteração promovida à produção; a branch possui apenas a prévia de desenvolvimento.
- **Pendente:** aceite visual pela Megalos e verificação física do deploy, regras definitivas, integração Academy e promoção deliberada para `main`. Ver `docs/CHECKPOINT_V016_2026-11-01.md`.

## Checkpoint de preview v0.10.7 (01/11/2026)
- **Feito:** correção da data atual dinâmica no calendário; branch isolada `preview/v0.10.7-calendar-current-day`, derivada da v0.10.6 validada.
- **Testado:** falha reproduzida antes da correção; teste da meia-noite aprovado após alteração em 390/740 px; TypeScript/build local, 18/18 Node, seis testes anteriores de navegação/fluxos; Cloudflare Pages do commit de código e teste concluído com sucesso.
- **Publicado:** somente prévia na branch; nenhuma promoção a `main` ou publicação institucional.
- **Pendente:** fidelidade/aceite visual da Megalos, integração Academy, regras institucionais e revisão física do site. Ver `docs/CHECKPOINT_V017_2026-11-01.md`.

## Checkpoint de preview v0.10.8 (01/11/2026)
- **Feito:** painel visual do formulário de agendamento aproximado do modelo azul da Megalos, apenas em `src/styles.css`, branch isolada `preview/v0.10.8-schedule-visual`.
- **Testado localmente:** compilação TypeScript/build offline; 18/18 Node; `browser_schedule_visual_v018.py` em 320, 390, 740 e 1280 px; regressões de calendário, virada do dia, rascunhos, perfil, Socii e rotas aprovadas.
- **Publicado:** build Cloudflare Pages de preview com `completed/success`. Nenhum merge e nenhuma promoção para `main`.
- **Pendente:** fidelidade e aceite final da Megalos, regras institucionais, autenticação Academy, revisão física do preview e acompanhamento dos demais itens da Etapa 4. Ver `docs/CHECKPOINT_V018_2026-11-01.md`.

## Checkpoint de preview v0.10.9 (01/11/2026)
- **Feito:** lista de programações e detalhes expandidos aproximados de `1001930221.jpg`, com tipo destacado, datas azuis, títulos em caixa alta, painel azul de largura completa e linha de Socii apenas quando o vínculo real da sessão existe. Foco teclado preservado ao expandir.
- **Testado:** `npm run build`, 18/18 Node; 9/9 scripts Playwright Chromium, com teste novo em 320/390/740/1280 px cobrindo também o ciclo Socii → proposição concluída → programação. Check remoto Cloudflare Pages `completed/success` em `83f342d`.
- **Publicado:** exclusivamente build de preview na branch `preview/v0.10.9-programacoes`; nenhuma promoção, merge ou deploy intencional na `main`.
- **Pendente:** aceite visual da Megalos, códigos/identificadores administrativos com fonte real, regras de votação, permissões, integração Academy, colaboração Socii definitiva e as demais etapas. Ver `docs/CHECKPOINT_V019_2026-11-01.md`.

## Checkpoint de preview v0.10.10 (01/11/2026)
- **Feito:** painel de revisão claro, arredondado, com símbolo Academy já existente, seção responsável e tipo, e ações paralelas Cancelar/Confirmar. Apenas `src/main.ts` e `src/styles.css`, branch `preview/v0.10.10-review-sheet`.
- **Testado:** build local TypeScript + 18/18 Node; dez scripts Playwright aprovados, incluindo novo teste da folha de revisão em 320/390/740/1280 px, cancelamento sem perder texto e confirmação. Capturas locais salvas no Drive Komekko.
- **Publicado:** build remoto Cloudflare Pages de preview confirmado como `completed/success` em `a59426e`; nenhuma promoção, merge ou alteração da `main`.
- **Pendente:** revisão e aceite da Megalos, regras definitivas de votação/Socii, integração Academy e acabamento de outras telas. Ver `docs/CHECKPOINT_V020_2026-11-01.md`.

## Checkpoint de preview v0.10.11 (01/11/2026)
- **Feito:** composição da tela Proposições e Socii aproximada do perfil original da Megalos (`1001930225.jpg`), com avatar, nome, função, cinco indicadores e abas; histórico demonstrativo filtrado pelo autor, registros expansíveis reutilizados e item ativo não inerte.
- **Testado:** build TypeScript/offline com 18/18 Node; **11/11** scripts Playwright/Chromium, incluindo novo `browser_proposals_profile_v0111.py` em 320/390/740/1280 px e regressões anteriores. Blobs GitHub de código e CSS conferidos contra arquivos que passaram no build local.
- **Publicado:** build remoto Cloudflare Pages da branch de preview confirmado **completed/success** em `96c56de`; nenhum merge nem promoção da `main`.
- **Pendente:** aprovação visual final da Megalos, as regras institucionais, Socii real, integração Academy e conclusão das seis etapas. Ver `docs/CHECKPOINT_V021_2026-11-01.md`.

## Checkpoint de preview v0.10.12 (01/11/2026)
- **Feito:** faixa superior Socii na redação somente quando há participantes registrados no rascunho local; identificação existente, progresso de conclusão, avatares neutros e ausência de prazo inventado. Fonte: `1001930224.jpg` da Megalos.
- **Testado:** build TypeScript, bundle offline, 18/18 testes Node; 12/12 testes Playwright/Chromium incluindo `browser_socii_editor_v0112.py` em 320/390/740/1280 px, confirmação da autora isolada (1/2) e do parceiro (2/2), sem overflow.
- **Remoto:** check Cloudflare Pages `completed/success` no commit `db41976` do código e teste; apenas preview, sem merge em `main`. Evidências de 390 e 740 px arquivadas no Drive Komekko.
- **Pendente:** aceite da Megalos, regras reais de colaboração/duração, Academy SSO, votação e definição da grafia. Ver `docs/CHECKPOINT_V022_2026-11-01.md`.

## Checkpoint de preview v0.10.13 (01/11/2026)
- **Defeito reproduzido e corrigido:** após autoria confirmar 1/2, editar a redação mantinha essa aprovação para texto novo. A prévia agora reinicia todas as confirmações somente quando título/texto mudam, preserva participantes e sinaliza a mudança. Se somente um parceiro confirmou, mostra corretamente **Aguardando autoria**.
- **Testes:** compilação/bundle offline/18 de 18 Node, mais 13 suítes Playwright/Chromium, incluindo `browser_signature_integrity_v0113.py` em 320/390/740/1280 px; falha reproduzida antes do patch e corrigida depois. Check remoto Cloudflare Pages `completed/success` no commit `01d25c3` (preview).
- **Isolamento:** branch `preview/v0.10.13-socii-reapproval`, sem merge/promoção para `main`. Capturas e estado do teste salvos no Drive Komekko. Consultar `docs/CHECKPOINT_V023_2026-11-01.md`.
- **Pendente:** regra institucional de assinatura/versionamento da Academy ainda precisa de aprovação, Socii compartilhado não implementado; não tratar esta proteção demonstrativa como decisão institucional final.

## Checkpoint de preview v0.10.14 (01/11/2026)
- **Defeito comprovado:** dados incompletos em `sessionStorage` eram aceitos só por `id/title` e podiam impedir a renderização de todas as propostas ou programações; vínculo de uma programação a proposta inexistente exibia ação sem efeito.
- **Corrigido:** validação estrutural de registros recuperados, aviso de entradas não carregadas, backup dessas entradas no navegador antes de sobrescrever os dados da sessão, preservação do calendário com aviso de vínculo ausente e funcionamento normal dos vínculos válidos.
- **Testado:** TypeScript + bundle offline + 18/18 Node; 14/14 suítes Playwright, incluindo novo `browser_restore_integrity_v0114.py` em 320/390/740/1280 px. Código/teste publicados com hash exatamente igual aos arquivos locais aprovados. Check Cloudflare Pages `completed/success` em `6e6db37`.
- **Isolado:** branch `preview/v0.10.14-session-integrity`; `main` não promovida, sem implementação de dados institucionais reais. Capturas e checkpoint no Drive Komekko. Ver `docs/CHECKPOINT_V024_2026-11-01.md`.
- **Ainda aberto:** regras finais de versões e assinaturas Socii, permanência de dados e autenticação compartilhada, aprovações e permissões, calendário definitivo e validação visual/institucional da Megalos.

## Checkpoint de preview v0.10.15 (01/11/2026)
- **Defeito reproduzido:** JSON quebrado no armazenamento local não gerava aviso nem backup, sendo sobrescrito na gravação seguinte. Um rascunho antigo marcado como concluído mesmo com assinatura pendente passava no filtro e podia ser selecionado para programação.
- **Feito:** cópia do valor bruto ilegível em chave específica `unreadable-session-backup-v0115` antes de sobrescrever; filtragem de conclusão inconsistente e preservação de dados rejeitados na chave v0114. Nenhum backend ou regra de assinatura institucional criada.
- **Testado:** `npm run build` (18/18 testes Node), 15/15 suítes Playwright, incluindo `browser_session_recovery_v0115.py` em 320, 390, 740 e 1280 px. Retomada validada por reconstrução de documento com valores exatos serializados no armazenamento simulado; **não** testada como reload nativo do browser ou persistência multiusuário.
- **Isolamento:** `preview/v0.10.15-session-recovery`; sem merge da `main`. Capturas de 390 e 740 px arquivadas no Komekko, ver `docs/CHECKPOINT_V025_2026-11-01.md`. Check remoto Cloudflare Pages `completed/success` em `c6ccf3d` (somente branch de prévia).
- **Ainda pendente:** backup remoto seguro e autenticação existente Academy, regras institucionais finais da Megalos, coautoria Socii e aceite visual/funcional de todas as fases.

## Checkpoint de preview v0.10.16 (01/11/2026)
- **Defeito reproduzido:** registros distintos com mesmo ID eram aceitos no armazenamento local; seus botões/cancelamentos utilizavam `find` por ID e podiam direcionar ações ao registro incorreto. Socii permitia contar o mesmo participante duas vezes em dados recuperados.
- **Corrigido:** manter a primeira ocorrência válida por ID, isolar entradas repetidas e participantes Socii duplicados, avisar o usuário e preservar entradas rejeitadas num histórico append-only de sessão `conferatus:quarantined-session-backups-v0116`, sem substituir o backup legado `v0114`.
- **Testado:** TypeScript + bundle offline + 18/18 testes Node. **16/16 suítes Playwright ativas**, incluindo `browser_unique_records_v0116.py` em 320/390/740/1280 px (falha comprovada antes do patch). Cloudflare Pages `completed/success` no commit `323aa9a` do código e teste; hash dos dois arquivos coincide com o executado localmente.
- **Limites:** não existe backend, login Academy integrado ou backup remoto; o histórico de quarentena está apenas em `sessionStorage`. Teste `browser_smoke.py` legado fora da matriz ativa precisa atualizar seletor de botão descontinuado; não contabilizá-lo como aprovado. Ver `docs/CHECKPOINT_V026_2026-11-01.md`.
- **Isolamento:** branch `preview/v0.10.16-unique-records`. `main` intocada, aceite Megalos e regras institucionais continuam pendentes.

## Retomada disciplinada — preview v0.10.17 (01/11/2026)
- **Item de prioridade:** Etapa 04 — fidelidade da jornada de calendário e honestidade da demonstração, com dependência da Etapa 06 (comunicação do estado real).
- **Achado verificável:** o botão **Iniciar uma Votação** — texto presente na referência da Megalos — abre apenas o formulário de programação de deliberação, não inicia votação real. Antes desta rodada, a tela não explicava isso perto da ação.
- **Ajuste mínimo:** preservar o título exato do botão, acrescentar uma nota legível sobre o comportamento demonstrativo, sem alterar estrutura, permissões, campos, regras, backend ou paleta; conferir em quatro larguras. Ver `docs/AUDITORIA_VISUAL_V0117_2026-11-01.md`.
- **Conferência visual:** as seis capturas de 710×1536 e amostragem do vídeo de ~55 s foram examinadas e comparadas com a prévia existente. Registro de observações **não substitui aceite da Megalos**. A tela final continua como pendência.
- **Qualidade/limites (histórico v0.10.17):** `npm run build` com 18/18 testes Node e 17/17 suítes Playwright ativas aprovadas. O smoke legado estava pendente nesta versão e **foi modernizado e aprovado na v0.10.18**; não reinterpretar este resultado histórico. `package.json` não possui comando `lint` (não chamar build de lint). Reload HTTP real e colaboração entre contas continuam não verificados.
- **Próximo passo após esta rodada:** apresentação das diferenças para validação de design da Megalos; depois, consolidar a experiência funcional conforme as regras recebidas. Não transformar correções preventivas de armazenamento em novas etapas sem necessidade observada.

## Revisão de qualidade — preview v0.10.18 (01/11/2026)
- **Lei máxima aplicada:** simplicidade, regressão confiável, mudança pequena, sem código cenográfico. Antes de ampliar funcionalidades, consertar o `browser_smoke.py` que era excluído por possuir seletores de uma UI antiga.
- **Falha antes do reparo:** o smoke antigo para em `Simular voto`, botão removido em versões anteriores. **Feito:** modernizar somente `tests/browser_smoke.py` para os controles atuais, preservar texto original dos protótipos e distinguir permissão simulada de autorização real; atualizar README e checkpoint. Sem mudança em `src/`, CSS ou dependências.
- **Testes concluídos:** build/TypeScript e **18/18 Node**; **18/18 suítes Playwright** agora incluindo o smoke, em 320/390/740/1280 px e outras larguras específicas; controle negativo removendo temporariamente o aviso da votação provocou falha `AssertionError: 320`; HTML foi restaurado e o teste voltou a passar.
- **Limite de evidência:** o smoke examina documentos offline com `about:blank?demo=1`, não valida login Academy, persistência compartilhada ou HTTP real. Cloudflare não executa Playwright automaticamente. `npm run build` não equivale a lint; não há script lint configurado.
- **Contagem canônica SEM ALTERAÇÃO:** etapas 01=4/5, 02=0/4, 03=1/5, **04=17/22** (ativa), 05=0/4 e 06=0/5. Modernização de teste não encerra nenhum desses critérios gerais. Aceite visual e funcional da Megalos ainda pendente. Ver `docs/CHECKPOINT_V028_2026-11-01.md`.
- **Próximo avanço:** decidir com Megalos divergências visual/funcionais registradas em `docs/AUDITORIA_VISUAL_V0117_2026-11-01.md`; não presumir ajustes de design nem criar lógica definitiva sem requisitos.

## Integridade da revisão Socii — preview v0.10.19 (01/11/2026)
- **Prioridade da Etapa 04, dentro do item já existente de integridade de versões:** reproduzido em 320 px que uma participante confirmava 1/2, a autoria mudava seção E tipo na folha de revisão e o sistema concluía 2/2 sem reapresentar a nova classificação à participante.
- **Correção mínima em `src/main.ts`:** verificar se `sectionId` ou `type` mudou na confirmação da autoria; somente nesses casos invalidar `partners[].complete`, manter os participantes e exigir novo aceite individual. A autoria confirma a classificação atual na mesma ação e a página informa claramente a invalidação. Quando ambos são idênticos, preservar a confirmação anterior.
- **Teste novo:** `tests/browser_review_metadata_integrity_v0119.py`, reproduzindo inicialmente a falha e, depois da correção, verificando quatro variantes (só seção, só tipo, ambas, sem mudança) em 320/390/740/1280 px, estados 1/2 e 2/2, pendência Socii, mensagem, ausência de erros JS e overflow.
- **Regressão efetivamente executada:** `npm run build` com 18/18 testes Node; 19/19 suítes Playwright `tests/browser_*.py` aprovadas. Código e teste foram comparados com seus Git blob SHA antes da publicação. O teste mantém navegação de HTML estático e `sessionStorage` local, sem alegar colaboração real.
- **Contagem NÃO ALTERADA:** 01=4/5, 02=0/4, 03=1/5, **04=17/22** (ativa), 05=0/4, 06=0/5. A ampliação de cobertura da integridade reforça um item já marcado; não conclui as cinco tarefas centrais abertas da etapa 4.
- **Pendências institucionais:** regra definitiva de versionamento e autorizações requer aceite Megalos; vínculo real de assinaturas, segurança concorrente, armazenamento compartilhado e integração Academy não foram implementados. Ver `docs/CHECKPOINT_V029_2026-11-01.md`.

## Retorno contextual calendário ↔ proposição — preview v0.10.20 (01/11/2026)
- **Objetivo da Etapa 04, sem criar nova tarefa:** quando a programação vinculada abria a proposição concluída, o botão `Voltar às proposições` perdia a data/linha escolhida e retornava à lista geral. Falha observada com teste novo ANTES da mudança: timeout esperando retorno à programação.
- **Feito:** um estado local explícito diferencia origem `calendar` de `proposals`. Ao acessar pelo calendário, o botão existente passa a `Voltar à programação`; o retorno preserva data selecionada e evento expandido. Pela lista, comportamento anterior mantido. Nenhuma nova dependência, tela, permissão, banco ou regra institucional.
- **Testado:** TypeScript/HTML independente + 18/18 Node; teste novo `browser_calendar_return_v0120.py` em 320/390/740/1280 px. Duas regressões antigas foram adaptadas ao retorno corrigido, mantendo validação de recuperação de IDs e links. O teste de perfil v0.10.11 ausente do snapshot base foi recuperado intacto da branch GitHub. Total de **20/20 suítes Playwright distintas aprovadas**; lotes interrompidos não foram contados antes da execução posterior.
- **Escopo/limite:** navegação verificada em HTML offline; não prova reload HTTP, banco compartilhado, autenticação Academy ou convite Socii real. Cloudflare executa build e testes Node, não Python Playwright. `lint` continua não configurado.
- **Checklist CANÔNICA inalterada:** 01 4/5; 02 0/4; 03 1/5; **04 17/22 ativa**; 05 0/4; 06 0/5. As cinco tarefas centrais da Etapa 04 ainda dependem de decisões institucionais e aprovação visual da Megalos. Consulte `docs/CHECKPOINT_V030_2026-11-01.md`.

## Integridade de gravação local — preview v0.10.21 (01/11/2026)
- **Objetivo da Etapa 04:** evitar que uma redação antiga e uma nova sejam misturadas na sessão quando o navegador aceita a primeira gravação e falha na segunda, embora a interface já indique que o rascunho não foi guardado.
- **Falha demonstrada antes do patch:** teste `tests/browser_session_partial_write_v0121.py` simulou `setItem` falhando somente na chave de programações; a proposta alterada permanecia salva na chave anterior, apesar de o sistema informar que os dados ficaram apenas em memória. AssertionError observado em 320 px.
- **Correção mínima:** `src/main.ts` mantém as chaves e formatos existentes; antes de gravar o conjunto, registra o valor anterior da primeira chave. Se a segunda escrita falhar, restaura o valor anterior ou remove a chave recém-criada. Em caso de falha também na restauração, a operação continua reportada como não persistida; a reversão é **melhor esforço**, não uma transação garantida pelo navegador.
- **Aceite verificado:** navegador em 320/390/740/1280 px testa rascunho anterior e primeiro salvamento, falha na segunda escrita, ausência de persistência parcial, segunda tentativa bem-sucedida, ausência de erros JS e de overflow. TypeScript e 18/18 testes Node passaram; após reiniciar em lotes individuais os scripts que ultrapassaram o limite do ambiente, **21/21 suítes Playwright distintas aprovadas**. Browser por HTML offline, sem prova de recarga HTTP nem backend.
- **Atenção às leis máximas:** zero dependências, migrações, novos módulos, alteração visual ou duplicação de armazenamento. Nenhuma permissão/votação/Socii real foi inferida. `npm run build` não é lint, pois ainda não há lint configurado.
- **Contagem CANÔNICA INALTERADA:** 01=4/5; 02=0/4; 03=1/5; **04=17/22 (ativa)**; 05=0/4; 06=0/5. O esforço reforça a integridade local já marcada, não encerra pendências centrais. Ver `docs/CHECKPOINT_V031_2026-11-01.md`.

## Socii — escolha explícita de participante (prévia v0.10.22, 01/11/2026)
- **Objetivo pontual da Etapa 04:** impedir que o navegador marque automaticamente a primeira pessoa no campo `Participante` ao abrir `Convidar para Socii` e que um clique em `Adicionar participante` inclua alguém sem escolha consciente.
- **Reprodução antes de modificar:** `tests/browser_socii_explicit_choice_v0122.py` falhou em 320 px, pois `[name=memberId]` já continha o ID da primeira pessoa sem interação.
- **Menor correção possível:** apenas `src/main.ts`, introduzindo `<option value="" selected disabled>Selecione uma pessoa</option>` em `select required`. A validação nativa impede envio enquanto vazio; após seleção expressa, o fluxo local já existente continua, sem novos estados, pacotes, categorias, filtros de elegibilidade ou alterações de design.
- **Testes realizados:** caso novo aprovado em 320/390/740/1280 px, incluindo não inclusão acidental, seleção intencional, status Socii 0/2, ausência de exceções JavaScript e overflow. `npm run build` passou compilação TypeScript, bundle HTML e **18/18 testes Node**. Após dividir lotes que expiraram, **22/22 suítes Playwright distintas** terminaram aprovadas, incluindo as antigas de convite, progresso, assinaturas, revisão, calendário, perfis e armazenamento.
- **Comparação visual:** captura em 390 px verificada; não há mudança de layout ou de paleta além do placeholder do campo. A referência `1001930224.jpg` trata do editor Socii, não do formulário de seleção; portanto ela **não determina a UI do convite**, nem autoriza alegação de aceite visual. Original preservado.
- **Limite:** a inclusão continua local e demonstrativa, sem convite remoto, identidade Academy, autorização real ou regras institucionais de elegibilidade. O script `lint` segue ausente, e Playwright usa documento offline. Ver `docs/CHECKPOINT_V032_2026-11-01.md`.
- **Contagem oficial intacta:** Etapas 01=4/5, 02=0/4, 03=1/5, **04=17/22 ativa**, 05=0/4 e 06=0/5. Esta melhoria reforça segurança de interação, não conclui as cinco tarefas finais da Etapa 04.

## Pacote de aprovação Megalos — preview v0.10.23 (01/11/2026)
- **Prioridade estratégica:** sair do ciclo de pequenas correções e destravar decisões de produto já documentadas na auditoria v0.10.17. Reproduzidas seis telas do build local v0.10.22 em Chromium **390 px**; comparadas com as seis imagens originais 1001930221.jpg a 1001930226.jpg, preservadas intactas.
- **Feito:** PDF visual de 7 páginas com pares de imagens e perguntas D1/D1b (calendário, nome da ação), D2 (local do formulário), D3 (variantes de confirmação), D4 (barra/tempo Socii), D5 (Salvar rascunho), D6 (perfil). **Evidência nova:** a barra de participantes está no editor mas **não** na captura da revisão, apesar de aparecer na referência 0222. Não alterar sem aprovar o estado esperado.
- **Artefatos:** `docs/KIT_DECISOES_MEGALOS_V0123_2026-11-01.md` (matriz factual, pergunta, estado, critério de aceite), `docs/CHECKPOINT_V033_2026-11-01.md` e PDF privado no Komekko: https://drive.google.com/file/d/1M5NN_tT4VQ_-Vp7YF8PU48kzj4DT3Jz-/view .
- **Verificações:** `npm run build` sobre a base v0.10.22 com TypeScript, HTML independente e **18/18 testes Node** aprovados. Captura local de seis estados em 390 px, sem exceções JavaScript ou overflow. PDF 7 páginas renderizado/inspecionado. **Não afirmar 22/22 suítes Playwright rodadas de novo**: passaram na rodada anterior, não nesta rodada documental. Sem script `lint`.
- **Resultado e limite:** nenhuma decisão da Megalos recebida nesta etapa; não marcar fidelidade visual final como concluída. Ações e integrações reais não foram construídas. Este pacote de perguntas **não fecha os cinco critérios centrais** da Etapa 4.
- **Checklist sem inflação:** 01=4/5; 02=0/4; 03=1/5; **04=17/22 ativa**; 05=0/4; 06=0/5. Próxima mudança de UI depende de respostas documentadas da Megalos, sem mexer na produção.

## Evidência temporal do vídeo original — v0.10.24 (02/11/2026)
- **Evidência recuperada:** [vídeo original completo no Komekko](https://drive.google.com/file/d/11rIyxCOFPX_zeWQOG59pLkbCdTkDgnuP/view), `1001930216.mp4` H.264 720×1604 de 54,662844 s, SHA256 `cd038526637541ed7ad960c7dbb7ac654278e0aa04e8124543daabb221f3570b` **verificado por download e recomputação local de hash contra o original**; 109 quadros amostrados em intervalos de 0,5 s, inspecionadas transições e quadros em alta resolução. É gravação de WhatsApp contendo uma sequência visual de interface, **não** teste comprovado do aplicativo institucional.
- **Resultado de fidelidade D1–D6:** D1 (~42,7s): painel do calendário sem grade aparente; D2 (~23,5s): agendamento sob perfil; D3 (~31,8/39,3s): Confirmar sozinho / Cancelar + Confirmar, ainda sem gatilho especificado; D4 (~31,8s): faixa Socii também na **revisão** com indicação 127 horas sem definição temporal; D5 editor Concluir/Voltar; D6 perfil com cinco métricas. Estas observações não aprovam unilateralmente mudanças.
- **Regra explícita já atendida na prévia:** a mensagem de Megalos (~04,1s) inclui `Ofício` entre PDR e PR como tipo da proposição; outra (~18,4s) pede Ofício na métrica do perfil. Confirmado por leitura de `src/main.ts`: união `ProposalType`, validadores, revisão, agendamento e métrica já contemplam Ofício. Não reimplementar esse suporte nem concluir regras institucionais de Ofício.
- **Entregáveis:** `docs/AUDITORIA_VIDEO_V0124_2026-11-02.md` e [adendo visual privado de 4 páginas](https://drive.google.com/file/d/1zp8vzL74uAnvi7ygb8zLZupnIWNUA591/view); `docs/KIT_DECISOES_MEGALOS_V0123_2026-11-01.md` recebeu atualização D1–D6. Original e capturas não foram incluídos no repositório público.
- **Escopo honesto:** mudanças somente em documentação; nenhum teste Node/Playwright foi reexecutado nesta rodada; o CI da branch documental não substitui testes de navegador. `lint` continua não configurado.
- **Contagem intocada:** 01=4/5, 02=0/4, 03=1/5, **04=17/22 ATIVA**, 05=0/4, 06=0/5. O gate de aprovação visual D1–D6 continua aberto, e a `main` não pode ser promovida sem autorização. Consulte `docs/CHECKPOINT_V034_2026-11-02.md`.


## Correção da marca solicitada pelo responsável — preview v0.10.25 (02/11/2026)
- **Mudança prioritária:** o responsável apontou erro no nome anterior. A prévia passa a exibir **CONFFRATUS** em título HTML, rodapé, telas de edição/revisão, textos acessíveis, pacote e arquivo offline canônico.
- **Fonte e conflito documentados:** algumas imagens da Megalos mostram literalmente **CONFERATUS**. A alteração para CONFFRATUS foi solicitada pelo responsável neste chat, **não** é atribuída a uma aprovação ou a uma nova imagem da Megalos; manter ambas as evidências e solicitar validação institucional de grafia quando houver oportunidade. O item 01 continua marcado 4/5, sem inventar aprovação da Megalos.
- **Compatibilidade:** arquivos `dist/CONFFRATUS_demo_offline.html` e `dist/CONFERATUS_demo_offline.html` têm bytes iguais; `publish/index.html` usa a marca nova. `sessionStorage` mantém chaves antigas `conferatus:*` para preservar drafts, backups e votos fictícios. O repositório GitHub e o domínio Cloudflare atuais NÃO foram renomeados; fazê-lo exige migração técnica e aprovação separadas.
- **Verificações locais:** TypeScript estrito e `npm run build` com **18/18 testes Node** aprovados; teste de marca `tests/browser_brand_v0125.py` passou em 320/390/740/1280 px, capturas conferidas em 390/740. O primeiro lote paralelo do navegador expirou; posteriormente, **18/18 scripts Playwright disponíveis na reconstrução local (17 herdados + 1 novo) foram individualmente concluídos e aprovados**, incluindo Socii, calendário, perfis, retorno, storage, assinatura e smoke. Ainda há testes legados adicionais no GitHub que não foram reexecutados nesta rodada; não alegar 22/22 da matriz anterior.
- **Leis máximas preservadas:** mínima alteração de marca e geração de alias; nenhum esquema, lógica de votos, persistência, permissão ou regra institucional alterado. Não recriar arquivos históricos de auditoria como se sempre tivessem usado a grafia nova.
- **Seis etapas SEM ALTERAÇÃO AUTOMÁTICA:** 01=4/5; 02=0/4; 03=1/5; **04=17/22 ativa**; 05=0/4; 06=0/5. Corrigir texto não significa homologar sistema nem concluir fidelidade visual.


## Front-end responsivo — início da Etapa 07 (preview v0.10.26, 02/11/2026)
- Nova etapa adicionada por solicitação expressa; a Etapa 06 continua independente e aberta. Sem alterar as seis contagens anteriores: **01=4/5; 02=0/4; 03=1/5; 04=17/22 ativa; 05=0/4; 06=0/5; 07=2/12 ativa.**
- A busca do diretório móvel possuía altura clicável de 18px. Falha reproduzida ANTES da correção; CSS adaptado e teste em 280/320/360/390/540px confirma 44px e distância da primeira linha. Apenas `src/styles.css` mudou em produto.
- Auditoria inicial sem overflow: 7 rotas × 9 larguras 280/320/360/390/540/740/768/1024/1440px, 63/63 no Chromium offline; não equivale a validar todas as jornadas, zoom elevado, outros navegadores ou aparelhos físicos.
- Build local com 18/18 Node, testes Playwright novos e 13/13 suítes direcionadas (não a matriz completa do repositório). Visual e decisões Megalos D1–D6 preservadas.
- Documento canônico: `docs/ETAPA_07_FRONTEND_PERFECCIONISMO_2026-11-02.md`. Checkpoint: `docs/CHECKPOINT_V036_2026-11-02.md`.

### Etapa 07.03 — lote 1 da v0.10.27 (02/11/2026; NÃO concluir 07.03)

- [x] Lote parcial: medir três controles móveis previamente suspeitos e o botão de busca desktop em Chromium, nove larguras, sete rotas principais; teste novo falhou antes da correção (`.demo-toggle` 23px em 280px).
- [x] Lote parcial: quatro alvos verificados com pelo menos 44×44px, interações de votação **fictícia**, perfil, busca e rodapé; eliminar colisão de 5px no desktop e preservar legenda de demonstração no rodapé.
- [x] Regressões pertinentes: build/18 Node, teste de toque novo 9/9 larguras, reflow 63/63, teste de toque 07.02 em cinco larguras. Ver `docs/CHECKPOINT_V037_2026-11-02.md`.
- [ ] **07.03 continua aberta:** auditar outros estados e controles (calendário, abas, ícones, gestão, editor, revisão, formulários), testar spacing, colisões e motores adicionais. Não converter esses subpassos em novos critérios da checklist 01–07.

**Contagens preservadas:** 01 4/5; 02 0/4; 03 1/5; 04 17/22 ATIVA; 05 0/4; 06 0/5; **07 2/12 ATIVA**. Nenhuma autorização/aceite da Megalos inferida. Marca CONFFRATUS, dependências legadas intactas.

### Etapa 07.03 — lote 2 v0.10.28 (02/11/2026; ainda NÃO encerrar)

- [x] Reprodução focal antes: 135 medições em nove larguras; 106 ocorrências abaixo das metas de conforto (não equivalem a 106 violações WCAG). Inclui calendário, votos demonstrativos, abas, gerenciamento, editor e revisão. Teste `tests/browser_stage7_expanded_touch_v0128.py` falhou antes.
- [x] Correção CSS mínima nesses controles, usando exceção consciente de largura de calendário de sete colunas (>=24px em 280px, altura >=44px). 135/135 medidas de conforto passaram depois; ações existentes preservadas. Título do mês quebrou inicialmente em 280px, defeito reproduzido em teste e corrigido por ajuste apenas do cabeçalho.
- [x] `npm run build` + 18/18 Node; matriz focal de 9 larguras; 26 scripts browser distintos executados e aprovados após patch principal. O último ajuste do mês tem regressões **selecionadas** reexecutadas (reflow 63/63, calendário, smoke, antiga busca e ambos lotes de toque). Não classificar isso como certificação WCAG nem como execução integral pós-último ajuste.
- [ ] **07.03 ainda ABERTA:** inventariar restantes dos controles dinâmicos, testes completos de hit-test/colisão, estados de erro/vazio e exceções, validação com motores/dispositivos adicionais. D1–D6, Academy, votos oficiais e Socii real sem aceites.

**Contagens preservadas:** 01 4/5; 02 0/4; 03 1/5; 04 17/22 ativa; 05 0/4; 06 0/5; 07 **2/12 ativa**.

**Registro v0.10.29 (02/11/2026) — símbolo oficial Academy:** o responsável forneceu `1001930329.png` e rejeitou o emblema de pixel art do rodapé. Substituição pontual em `public/assets/crest.png`, sem redesenhar a imagem; ajuste CSS para evitar sobreposição com o menu aberto. Compilação 18/18 Node e teste novo em nove larguras × duas rotas aprovados, além de regressões específicas. Ver `docs/CHECKPOINT_V039_2026-11-02.md`. 07.03 continua aberta e **07=2/12**, sem aceite Megalos presumido.

**v0.10.30 — 07.03, lote 3, 02/11/2026:** teste reproduzível em nove larguras revelou 36/36 instâncias com alvos abaixo de 44px nos estados dinâmicos de busca vazia, Desfazer, reset avançado e perfil inexistente. Correção **somente CSS**; depois 36/36 atendem a 44×44px e ações funcionam com hit-testing do centro, sem overflow. `npm run build` + 18 Node, reflow 63, lote2 135, smoke e regressões seletivas aprovados. Referência: `docs/CHECKPOINT_V040_2026-11-02.md`. **07.03 [ ] aberta; 07=2/12.**

**Registro V041 (02/11/2026) — 07.03 lote 4, erro visível de formulário e menu:** o botão “Salvar rascunho” vazio gerava aviso interno invisível; teste reproduziu falha antes e passou após `composeError` com `role="alert"` dentro do editor. Três famílias de alvos intermediários abaixo da meta (painel, botão do menu e duas entradas em 740px) também corrigidas apenas com CSS específico. Teste novo `browser_stage7_form_edge_targets_v0131.py` 72/72 alvos, 9 larguras, validação de ID, rascunho e agendamento; build 18/18 Node, reflow 63/63, anteriores 135/135 e 36/36, fluxos de revisão/rascunho/retorno/smoke reexecutados. **07.03 permanece ABERTA e 07=2/12**; ver `docs/CHECKPOINT_V041_2026-11-02.md`. Sem D1–D6 aceitas, produção, backend ou mudanças em voto/Socii real.


## Fechamento 07.03 — prévia v0.10.32 (02/11/2026)

- [x] Inventário automatizado dos controles habilitados e visíveis nas **nove larguras de 280–1440 px**, cobrindo **19 estados mapeados** de voto demonstrativo, membros e busca vazia, perfil, histórico, gerenciamento e painel avançado, calendário e agendamento, propostas, Socii, editor e revisão. O teste `browser_stage7_all_controls_v0132.py` observou **2.769 instâncias** sem alvos abaixo dos mínimos. Os **300 registros estreitos** eram apenas dias do calendário, todos com largura >=24px e altura >=44px, preservando a grade de sete colunas. Teste restrito ao Chromium offline, sem alegar conformidade global.
- [x] Reproduzidos **45/45 alvos menores que a meta de 44px de altura** no teste `browser_stage7_advanced_controls_v0132.py`: skip-link em foco (35px), seleção de perfil (35px), seleção de membro (35px), Vincular (28px), busca (35px), em nove larguras. Após ajuste **somente CSS**, **45/45 conformes à meta**; centro acionável e fluxos reais de filtro/limpar, inclusão demonstrativa e atalho de teclado funcionando, sem erros JS/overflow.
- [x] Regressões isoladas após a mudança: Node **18/18**; lote2 **135/135**; formulários **72/72**; alvos dinâmicos **36/36**; lote1 nove larguras; reflow **63/63**; antiga busca cinco larguras; emblema oficial Academy nove larguras × duas rotas; smoke quatro larguras. A tentativa de execução agrupada expirou e **não** foi contabilizada; as suítes pertinentes foram concluídas isoladamente.
- [x] **07.03 encerrada no escopo testável da prévia offline**, sem condicionar este subitem aos gates independentes. Não implica certificação WCAG AA/AAA, zoom 200/400%, WebKit/Firefox ou aparelhos reais, tratados em **07.05, 07.09, 07.10, 07.12**. D1–D6 ainda dependem da Megalos. Ver `docs/CHECKPOINT_V042_2026-11-02.md`.

**Contagem atual (não retroativa):** 01=4/5, 02=0/4, 03=1/5, 04=17/22, 05=0/4, 06=0/5, 07=**3/12**. Próximo item 07.04 (tipografia/conteúdo extremo). `main`/produção, autenticação, integrações e banco permanecem intactos.

## Etapa 07.04 — lote 1, V043 (02/11/2026)

- [x] Falha de palavras sem separação reproduzida em 94/108 cenários de 12 estados × 9 larguras. Correção CSS mínima; novo teste `browser_stage7_long_content_v0133.py` **108/108**, sem rolagem horizontal ou erros JS. Nome do diretório continua com reticências e nome integral acessível no botão.
- [x] Fluxo real de rascunho com título no limite de 140 caracteres e corpo de 2.001 caracteres: **9/9 larguras** em editor, revisão, listagem e registro final, sem overflow nem perda de texto. Teste `browser_stage7_long_draft_v0133.py`.
- [x] Build **18/18 Node**, reflow **63/63**, inventário 07.03 **2.769 alvos**, regressões específicas de painel avançado, controles expandidos, formulários, rascunhos, revisão e emblema Academy passaram individualmente. Handoff e backup vinculados ao `docs/CHECKPOINT_V043_2026-11-02.md`.
- [ ] **07.04 permanece ABERTA**: auditoria de fonte minúscula mostrou 174 ocorrências visíveis abaixo de 10px em três larguras/e oito rotas amostradas; rever legibilidade e proporcionalidade contra Megalos sem adivinhação. Explorar mensagens de erro extremas e texto ampliado, sem confundir com certificação WCAG/zoom (07.05/07.10).

**Contagens preservadas:** 01=4/5, 02=0/4, 03=1/5, 04=17/22, 05=0/4, 06=0/5, **07=3/12**. `main` e produção intactas, D1–D6 pendentes.

## 07.04 — fechamento da microtipografia na prévia offline, V044 (02/11/2026)

- [x] Confirmada a base v0.10.33 antes das alterações. A 07.04 havia passado com palavras longas **108/108** e rascunho extremo em nove larguras, mas ainda tinha **174 ocorrências visíveis de microtexto <10px** na auditoria de oito rotas × três larguras.
- [x] Novo teste específico falhou antes (**367 de 567 amostras** em 4 rotas × 9 larguras). CSS pontual aumentou metadados críticos a pelo menos **10 CSS px** sem achatar títulos, e o aviso `DADOS FICTÍCIOS · PRÉVIA` agora é legível em duas linhas aos 280px, sem cobrir o logotipo oficial nem o Menu.
- [x] Testes depois: **567/567** sem microtexto alvo, auditoria comparável **174 → 0**, métricas de perfil/diretório sem colisões em **nove larguras**, reflow **63/63**, long content **108/108**, Node **18/18**, inventário de controles **2.870**, além de regressões relevantes de formulários, Academy e outros estados. Relatório completo em `docs/CHECKPOINT_V044_2026-11-02.md`; teste interrompido por timeout não foi contado.
- [x] **07.04 encerrada no Chromium offline**, não inclui zoom 200/400%, hardware real, WCAG total ou aceite visual da Megalos. Estes continuam nos gates posteriores; sem qualquer efeito em produção/main, votos oficiais, Academy/Socii real ou autorizações.

**Contagem atualizada:** 01=4/5, 02=0/4, 03=1/5, 04=17/22, 05=0/4, 06=0/5, **07=4/12**. Próximo: **07.05**.

## Etapa 07.05 — lote de zoom/reflow V045 (02/11/2026)

- [x] Baseline idêntica à V044 e teste automatizado reproduziram **45/70** cenários de texto/zoom com defeito; CSS corrigiu mês e setas, título de gerenciamento, abas e rodapé sem trocar o emblema Academy nem ocultar conteúdo.
- [x] Depois: **70/70** verificações (21 equivalências de viewport 400/200/100% × sete rotas; 49 estresses sintéticos de texto 200%), navegação do mês funcional, nenhum overflow horizontal documental/colisão fundamental, sem erro JS; build com 18/18 Node, regressões relevantes executadas separadamente e documentadas em `docs/CHECKPOINT_V045_2026-11-02.md`.
- [ ] **07.05 ainda não encerrada:** validar zoom nativo e texto ampliado em motores reais. A barra de indicadores em 640px mantém rolagem horizontal interna: examinar operabilidade por teclado na 07.09/07.10. Não chamar a prévia certificada nem simulação de fonte equivalente ao zoom nativo.

**Contagens preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; 07=**4/12**. `main`, banco, autenticação, votos oficiais, Academy real, Socii e aceites D1–D6 inalterados.

## Etapa 07.06 — lote 1, V046 (02/11/2026) — NÃO ENCERRADO

- [x] Defeito reproduzido: a regra `padding:0` da 07.05 anulava a safe-area inferior. Teste sintético com inset 24px falhou (`padding-bottom:0`); o primeiro ajuste encontrou ainda emblema sobreposto ao inset 48px. Correção somente CSS: restaurar `env(safe-area-inset-bottom,0px)` e ancorar emblema acima da área reservada. Depois **12/12** testes de inset em 4 larguras × 3 valores, sem overflow/interseção.
- [x] Teste novo de alturas curtas/paisagem, **63/63** rotas × dimensões + **9/9** fluxos completos de busca → menu → redação com redução artificial da altura útil. Campos continuaram alcançáveis por rolagem, foco preservado e rascunho salvo. Não confundir simulação de teclado com teclado real.
- [x] `npm run build` 18/18 Node; zoom simulado 70/70, reflow 63/63, emblema 9×2, inventário 2.880 controles e lote expandido 135/135 passaram. Teste de microtipografia impresso PASS mas com execução conjunta expirada: não computado como suíte terminada.
- [ ] **07.05 e 07.06 permanecem ABERTAS**: zoom nativo, teclado OS, rotação física, safe-area real, motores/dispositivos externos. Referência `docs/CHECKPOINT_V046_2026-11-02.md`. **07=4/12**, D1–D6 e etapas de produção inalteradas.

## Etapa 07.07 — tablets, verificação da prévia offline, V047 (02/11/2026)

- [x] Matriz reproduzível de **8 dimensões tablet (600–1024 CSS px)** × **8 rotas/estados** = **64/64 verificações Chromium**, sem rolagem horizontal nem colisões entre título do rodapé, Menu e símbolo oficial Academy. Capturas reais do navegador para 600, 768 e 1024px foram revisadas; coluna central limitada conscientemente a 740px, sem redesenho não aprovado.
- [x] **11 sequências funcionais:** oito navegações de menu → membros → busca → limpar → visão geral → aba de proposições, e três rotações **simuladas** por mudança de viewport, com navegação mensal e preservação do texto de rascunho. Nenhum erro JavaScript observado.
- [x] Regressões após a criação do teste: `npm run build` 18/18 Node, reflow 63/63, emblema Academy 9×2, zoom/reflow sintético 70/70, inventário 2.847 controles e conteúdo extremo 108/108. Nenhum CSS, TypeScript ou asset alterado neste lote. Evidência: `tests/browser_stage7_tablet_v0137.py` e `docs/CHECKPOINT_V047_2026-11-02.md`.
- [x] **07.07 concluída para o escopo da prévia Chromium offline**, sem alegar uso de hardware real; validação de tablet físico, Firefox/WebKit, rotação de sistema e aprovação visual continuam em 07.12/07.11. **07.05/07.06 permanecem abertas.**

**Contagem atualizada:** 01=4/5, 02=0/4, 03=1/5, 04=17/22, 05=0/4, 06=0/5, **07=5/12**. Próximo item independente: 07.08 (desktop largo). `main`, produção, D1–D6, autenticação, dados, votos oficiais e Socii permanecem intactos.

## Etapa 07.08 — desktop largo, V048 (02/11/2026)

- [x] **07.08 concluída na prévia Chromium offline:** matriz 7 desktops (1280–2560 CSS px) × 8 rotas/estados, **56/56 layouts**, sem rolagem horizontal, fuga da coluna de leitura de 740 px, colisões do emblema e erros JavaScript.
- [x] Corrigir retorno visual de **hover exclusivo de mouse/trackpad** nas abas inativas de visão geral/perfil e na navegação do calendário. Falha comprovada **antes** do CSS: aba sem mudança de cor ao hover; **depois**: 21/21 estados de hover, aba selecionada preservada, modo touch sem a regra.
- [x] Sete jornadas de menu, busca/limpeza, aba, calendário e rascunho; Node 18/18, reflow 63/63, tablet 64/64, Academy 9×2, zoom sintético 70/70, controles 2.805, microtipografia 567 e conteúdo longo 108 aprovados em testes separados. Consultar `docs/CHECKPOINT_V048_2026-11-02.md`.
- [ ] **Gates ainda abertos em outros subitens:** 07.05 zoom nativo, 07.06 teclado virtual/safe-area e rotação reais, 07.09 teclado/foco extensivo, 07.10 WCAG, 07.11 D1–D6 com Megalos, 07.12 browsers/dispositivos. Firefox/WebKit indisponíveis localmente, sem alegar certificação.

**Contagem oficial atual:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=6/12**. `main` e produção intactas. Próximo item independente: **07.09**.


## Fechamento 07.09 — prévia v0.10.39 (02/11/2026)

- [x] **Fluxos de teclado testados antes/depois:** 76 verificações em quatro larguras, com 20 falhas antes e 76/76 aprovados depois (menus, Tab, Shift+Tab, Enter, Escape, campo de busca, perfil, gerenciamento, editor, seleção e navegação).
- [x] **Rascunho e revisão com teclado:** 24/24 verificações em duas larguras. Mantidos título, texto, foco e ordem entre campos e botões.
- [x] **Controles que desaparecem após ações:** 12 falhas em 14 verificações antes; 14/14 após correção em duas larguras. Contextos: escolha de voto fictício, expansão de membros/histórico, reset e vínculo demonstrativo de gerenciamento, retorno às programações.
- [x] **Regressões:** Node 18/18; reflow 63/63; navegação (9 tamanhos); perfil/proposta; auditoria de 2783 controles × 19 estados × 9 larguras; emblema Academy oficial 9 larguras × 2 rotas; desktop 56 layouts/7 jornadas/21 hover; zoom/reflow simulado 70/70; formulários 72/72 (testes completados individualmente; não confundir timeout de execução agrupada com aprovação).
- [x] **07.09 concluída no escopo Chromium offline**, sem alterar CSS, estética, backend, voto real, Academy real, dados ou os aceites D1–D6. Sem testes de WebKit/Firefox/tecnologias assistivas reais; 07.10 e 07.12 abertos. Ver `docs/CHECKPOINT_V049_2026-11-02.md`.

**Contagens canônicas (novo fechamento):** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. A 07.05/07.06 (testes reais), 07.10, 07.11, 07.12 seguem pendentes. Próximo avanço independente: **07.10 — semântica, contraste e acessibilidade**.


## Etapa 07.10 — lote 1, v0.10.40 (02/11/2026) — AINDA ABERTA

- [x] Teste reproduzível de contraste e semântica básica: 87 observações em 8 rotas × 3 larguras, **51 ocorrências reprovadas antes**; **87/87 PASS depois**. Cinco telas sem título principal agora recebem `<h1 class="sr-only">` apenas quando não existe heading. Contraste dos principais rótulos/estados de menu, aviso de prévia e resultados elevado acima de 4,5:1, sem trocar identidade. Arquivos: `src/main.ts`, `src/styles.css`, `tests/browser_stage7_contrast_semantics_v0140.py`.
- [x] Build 18/18 Node; regressões de teclado 76/76 e editor 24/24, desktop, tablet, reflow, emblema Academy, capturas visuais. Checkpoint `docs/CHECKPOINT_V050_2026-11-02.md`.
- [ ] **07.10 NÃO concluída**: faltam demais cores/estados, contraste não textual/foco, semântica ARIA profunda, leitor de tela, navegador/hardware adicional. Sem alegar conformidade WCAG global.

**Contagens não alteradas:** 01=4/5, 02=0/4, 03=1/5, 04=17/22, 05=0/4, 06=0/5, **07=7/12**. D1–D6 Megalos ainda sem aceite; main/produção intactas.

## Etapa 07.10 — lote 2, v0.10.41 (02/11/2026) — AINDA ABERTA

- [x] Reproduzir relações ARIA incompletas em controles expansíveis (teste falhou no menu) e associar sete tipos de botão/painel com `aria-controls` válido quando abertos: menu, votação demonstrativa, busca, seção, ferramentas, agendamento e detalhe de programação. Grupos de indicadores e região de diretório recebem papel semântico adequado.
- [x] Reproduzir erro de rascunho não associado ao campo (teste falhou antes), aplicar `aria-describedby` a título/redação, e identificar o período inválido do agendamento com `role=alert`, `aria-invalid`, associação e foco; limpar o erro após correção.
- [x] Testes depois: 28/28 relações ARIA, 12/12 verificações de erro, Node 18/18, auditoria de contraste anterior 87/87, teclado 76/76, editor 24/24, formulários 72, reflow 63, zoom simulado 70, tablets 64, desktop 56, inventário 2.583 controles. Ver `docs/CHECKPOINT_V051_2026-11-02.md` e logs de regressão.
- [ ] **07.10 permanece aberta**: contraste não textual e foco, totalidade dos estados e tecnologias assistivas/motores/dispositivos reais não certificados. Nada de presumir aceitações D1–D6.

**Contagens inalteradas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. Produção e `main` preservadas.

## Etapa 07.10 — lote 3, v0.10.42 (02/11/2026) — AINDA ABERTA

- [x] **Contraste não textual nos campos amostrados:** teste reprodutível em Chromium offline/4 larguras com proposta fictícia habilitando a seleção. **20 falhas em 40 medições antes**, por bordas de agendamento a 2,392:1 e revisão a 1,280:1. Correção CSS mínima: `rgba(255,255,255,.88)` no agendamento e `#747c9a` na folha de revisão. **40/40 PASS depois**, contrastes de contorno 3,838:1 e 3,712:1.
- [x] **Foco em teclado, amostra ampliada:** teste permanente em 3 larguras e 7 rotas/estados, **273/273 paradas de Tab** com `:focus-visible` e `outline` CSS presente. A verificação não mede contraste de todos os focos e não substitui leitor de tela.
- [x] Build TypeScript/Node **18/18**; regressões isoladas: contraste textual **87/87**, ARIA **28/28**, mensagens de erro **12/12**, foco **76/76**, editor **24/24**, reflow **63/63**, zoom sintético **70/70**, inventário **2.742 controles**, Academy oficial 9×2, conteúdo extremo **108/108**, desktop 56 layouts/7 jornadas/21 hovers e formulários **72/72**. Capturas de agendamento/revisão antes/depois. `docs/CHECKPOINT_V052_2026-11-02.md`.
- [ ] **07.10 AINDA ABERTA:** mais estados/pares de cores, contraste de foco integral, tecnologias assistivas, motores/navegadores adicionais; nada de afirmar conformidade WCAG completa.

**Contagens preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. `main`, dados, produção, Academy real e D1–D6 sem alterações/aceites.

## Etapa 07.10 — lote 4, v0.10.43 (02/11/2026) — AINDA ABERTA

- [x] Auditoria de contraste textual de fundos sólidos em **56 estados/larguras, 2.464 trechos**. Teste novo `tests/browser_stage7_dynamic_text_contrast_v0143.py` falhou antes em **24 ocorrências** de dois componentes: indicadores Aprovados/Arquivados (3,71:1) e botão Convidar para Socii (3,59:1); depois **2.464/2.464 PASS**, razões calculadas aproximadamente 5,62:1 e 6,61:1. Somente CSS alterado; arte Megalos e emblema Academy preservados.
- [x] Build **18/18 Node** e regressões isoladas: 87/87 contraste anterior, 40/40 bordas/foco, 28/28 ARIA, 12/12 erros, 76/76 teclado, 24/24 revisão por teclado, 63/63 reflow, 56 layouts desktop, 2.827 controles, 70/70 zoom sintético, Academy 9×2 e 108/108 conteúdo extremo. Capturas antes/depois 390px.
- [ ] **07.10 continua aberta**: motor/leitor de tela real, contraste em gradientes/imagens, revisão manual global WCAG e todos os estados restantes pendentes. Consulta `docs/CHECKPOINT_V053_2026-11-02.md`.

**Contagem canônica não alterada:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. Nenhum merge/deploy, autorização institucional ou aprovação D1–D6 presumida.


## Etapa 07.10 — lote 5, v0.10.44 (02/11/2026) — avisos ARIA persistentes

- [x] Defeito demonstrado em `workflowNotice`: os avisos visíveis eram recriados com a tela e a região ARIA não persistia. Baseline reprovou. Implementado um `#app-live-announcer` persistente fora do `#root`, estado educado (`role=status`), `aria-atomic`, atualizações só para novas mensagens e esvaziamento. Mantidos avisos visíveis, sem `role=status` duplicado, CSS/visual, dados e lógica inalterados.
- [x] Novo `tests/browser_stage7_live_announcer_v0144.py`: 12/12 fluxos em quatro larguras, identidade DOM estável, árvore AX Chromium e sincronização de avisos; quatro testes históricos agora miram somente `.workflow-status` visível, preservando toda a cobertura.
- [x] Build 18/18 Node, typecheck, ARIA 28/28, erros 12/12, teclado 76/76 + 24/24 + 14/14, contraste 87/87 + 40/40 + 2464/2464, reflow 63/63, Academy oficial, rascunhos/revisão/perfil/calendário. Detalhes e limitações: `docs/CHECKPOINT_V054_2026-11-02.md`.
- [ ] **07.10 segue ABERTA:** atualização na AX tree não é teste de fala em leitor de tela. WCAG completa, dispositivos reais, gradientes/imagens/vídeo e motores adicionais ainda pendentes.

**Contagens sem alteração:** 01 4/5; 02 0/4; 03 1/5; 04 17/22; 05 0/4; 06 0/5; **07 7/12**. `main`/produção intocadas, D1–D6 Megalos sem aceite.

## Etapa 07.10 — lote 6, v0.10.45 (02/11/2026) — AINDA ABERTA

- [x] **Recuperação de erros reproduzida:** formulário de rascunho vazio não sinalizava campos com `aria-invalid`; mensagem de erro do rascunho e identificador de membro permanecia após correção. Teste `browser_stage7_error_recovery_v0145.py` falhou antes em `draft-title`, e passou **24/24** após pequena correção em `src/main.ts`, sem salvamento automático nem mudança de regras. Capturas de antes/depois do estado de validação em 390px. Checkpoint `docs/CHECKPOINT_V055_2026-11-02.md`.
- [x] Regressões executadas isoladamente: build/Node **18/18**, erros **12/12**, ARIA **28/28**, avisos persistentes **12/12**, contraste/semântica **87/87**, teclado **76/76**, formulários **72 controles**, rascunhos/revisão, reflow **63/63** e inventário **2.850 controles**. O timeout de execução agrupada **não** foi contabilizado; reflow foi repetido isoladamente com aprovação.
- [ ] **07.10 continua aberta**: testes com leitores de tela reais, contraste sobre imagens, mais estados e revisão manual WCAG. 07.05/07.06, 07.11 e 07.12 seguem abertas. D1–D6 Megalos aguardam aceite.

**Contagem oficial preservada:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. Nenhum merge, deploy, alteração institucional, backend ou produção.

## Etapa 07.10 — lote 7, v0.10.46 (02/11/2026) — AINDA ABERTA

- [x] **Semântica do calendário reproduzida e corrigida:** `role=group` nomeado na grade, nomes completos de domingo a sábado acessíveis sem mudar as letras visuais; anúncio persistente de mês, seleção de dia e contagem de programações via a região ARIA existente. O teste novo `browser_stage7_calendar_semantics_v0146.py` falhou antes (sem papel nomeável) e passou **36/36** depois, em seis larguras. Não se pressupõe leitura efetiva por NVDA/TalkBack/VoiceOver.
- [x] **Regressões concluídas separadamente:** `npm run build`/Node **18/18**, Hoje/retorno/calendário, relações ARIA **28/28**, região persistente **12/12**, teclado/foco **76/76**, formulários **12/12**, contraste **87/87**, reflow **63/63**, inventário de **2.703 controles observados** (19 estados × nove larguras). Captura de 390px inspecionada; arte, paleta, layout e emblema Academy sem alteração visual. Checkpoint `docs/CHECKPOINT_V056_2026-11-02.md`.
- [ ] **07.10 segue ABERTA**: leitores de tela reais, WCAG completo, contraste de imagens/gradientes e hardware/motores adicionais; 07.05/07.06, 07.11 e 07.12 também não encerradas.

**Contagens preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. Sem merge/deploy, mudança em produção, backend, regras institucionais ou aceite D1–D6 da Megalos.

## Etapa 07.10 — lote 8, v0.10.47 (02/11/2026) — convite Socii acessível, ABERTA

- [x] O botão "Convidar para Socii" alternava um formulário sem anunciar estado expandido nem identificá-lo como conteúdo controlado. Teste novo `browser_stage7_socii_disclosure_v0147.py` falhou ANTES em 280px e passou **36/36 DEPOIS**, em nove larguras, com Enter para abrir/fechar, nome acessível do formulário, fluxo completo de rascunho e inclusão fictícia, status visível e anúncio persistente. Alteração somente em `src/main.ts`; nenhuma regra de Socii, convite real, dado ou estética modificados.
- [x] Build/Node **18/18**; regressões isoladas ARIA **28/28**, avisos **12/12**, foco **76/76**, recuperação de erros **24/24**, contraste/semântica **87/87**, reflow **63/63**, inventário **2.732 controles**, fluxo de Socii no editor, perfil/proposições e erros de campos aprovados. Zoom sintético da execução adicional não completou e **não** foi contabilizado.
- [ ] **07.10 ainda ABERTA:** tecnologias assistivas reais, gradientes/imagens, revisão manual WCAG abrangente e outros motores/hardware. D1–D6 Megalos não aprovadas.

**Contagem preservada:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. Veja `docs/CHECKPOINT_V057_2026-11-02.md`. `main`/produção intactas.

## Etapa 07.10 — lote 9, v0.10.48, foco após ações removidas (02/11/2026)

- [x] Teste novo reproduziu foco no `body` ao confirmar Socii na prévia (280px). Exploração isolada confirmou a perda no botão Desfazer; outros formulários que se fecham não tinham retorno de foco explícito. Sem implementar convite ou programação institucional real.
- [x] Correção mínima somente `src/main.ts`: foco retorna ao botão de convite, agendamento recém-criado, título da lista após cancelamento e edição do membro afetado após Desfazer. `tests/browser_stage7_disappearing_forms_v0148.py` **28/28 PASS** (4 trajetórias × 7 larguras). Node **18/18**. Regressões concluídas: teclado 76/76, revisão 24/24, ações 14/14, Socii 36/36, ARIA 28/28, erros 24/24, reflow 63/63, Academy 9×2. Teste agrupado de anúncios expirou e não foi contabilizado. Ver `docs/CHECKPOINT_V058_2026-11-02.md`.
- [ ] **07.10 continua ABERTA**: leitores de tela reais, contraste imagem/gradiente, WCAG integral e outros dispositivos/motores; D1–D6 dependem de Megalos.

**Contagens oficiais preservadas:** 01 4/5, 02 0/4, 03 1/5, 04 17/22, 05 0/4, 06 0/5, **07 7/12**. Sem merge, deploy ou mudança em `main`.
