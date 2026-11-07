# CONFFRATUS — Checklist-mestra de execução

Atualização de referência: 03/11/2026
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
- [x] Definir interface de identidade da Academy sem criar login próprio (v0.10.49; contrato tipado, adaptador sem sessão e testes locais).
- [x] Usar o ACDM ID como referência de cadastro de demonstração, com links diretos para perfis e resolução única (v0.10.50; sem criar cadastro nem autenticar).
- [ ] Deixar a integração do login para o responsável da Academy, conforme acordado.
- [ ] Validar os fluxos integrados quando a equipe fornecer a interface correspondente.
**Estado:** responsabilidade definida; integração externa pendente.

## 06 — Acabamento, validação e entrega
- [ ] Comparar o visual com os modelos originais e recentes.
- [ ] Revisar responsividade, textos, navegação e fluidez dos fluxos.
- [x] Separar da experiência normal os controles desnecessários de teste: sem `?demo=1`, não exibir laboratório avançado de voto, painel técnico de identidade/ferramentas nem botões de exportar/restaurar JSON. Manter somente os fluxos fictícios necessários à demonstração e avisos explícitos de que não são funções Academy. Regressão em quatro larguras na CI e inspeção independente em seis telas × quatro larguras; **não** equivale a aprovar a fidelidade visual da Megalos.
- [ ] Consolidar testes e publicar novos builds primeiro em preview, depois no `main`.
- [x] Atualizar documentação e preparar a demonstração à Megalos, distinguindo recursos reais dos simulados (`docs/DEMO_GUIDE.md`, revisado em 03/11/2026; não equivale a aceite Megalos).
**Estado:** 2/5 critérios cumpridos para a prévia demonstrativa (separação dos controles avançados e guia de apresentação). A comparação visual final, o acabamento integral e a promoção autorizada à `main` permanecem pendentes.

## 07 — Perfeccionismo visual, front-end e responsividade absoluta verificável

**Etapa adicional solicitada pelo responsável em 02/11/2026.** Independente da Etapa 06 de entrega e da Etapa 04 de Socii. Critérios de aceite em `docs/ETAPA_07_FRONTEND_PERFECCIONISMO_2026-11-02.md`.

- [x] **07.01** Reflow inicial: 7 rotas × 9 larguras 280–1440px, 63/63 sem rolagem horizontal/clipping (Chromium offline; não todos os estados).
- [x] **07.02** Alvo de toque Buscar: reproduzido com 18px de altura; corrigido para 44px em 280–540px sem cobrir a primeira linha, toque e filtro testados em 5 larguras.
- [x] **07.03** Auditoria da prévia offline: inventário dos controles mapeados, dimensões e estados dinâmicos; 19 estados × 9 larguras, 2.769 observações, com exceções documentadas dos dias de calendário. Evidência V042.
- [x] **07.04** Corrigir legibilidade tipográfica, microtextos, nomes extensos, erros e conteúdo de tamanho extremo.
- [ ] **07.05** Testar zoom 200%/400% e reflow de 320 CSS px sem perda de conteúdo/ação.
- [ ] **07.06** Testar todas as jornadas em celulares compactos, alturas curtas, rotação, teclado virtual e safe areas.
- [x] **07.07** Validar composição de tablets (600–1024px; retrato e paisagem).
- [x] **07.08** Validar composição desktop 1280–1920px, hierarquia e aproveitamento consciente da área.
- [x] **07.09** Revisar ordem de Tab/Shift+Tab, Escape, foco e navegação do teclado por fluxo.
- [ ] **07.10** Auditar contraste, semântica, rótulos e leitor de tela contra critérios aplicáveis WCAG 2.2 AA.
- [ ] **07.11** Manter diffs visuais reproduzíveis e obter aceite Megalos de D1–D6 antes de declarar fidelidade.
- [ ] **07.12** Rodar matriz final em Chromium/Firefox/WebKit quando disponíveis e aparelhos reais, documentando limites.

**Estado da Etapa 07: 7/12.** Início v0.10.26, com `npm run build` **18/18 Node**, `tests/browser_frontend_touch_target_v0126.py` **5/5 larguras**, `tests/browser_frontend_reflow_v0126.py` **63/63 estados-larguras**, regressões direcionadas **13/13 suítes Playwright**. Nenhuma dessas medições é certificação de responsividade absoluta ou substitui testes em dispositivos reais. A marca da prévia permanece **CONFFRATUS**; `main` intocada.

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

## Etapa 07.10 — lote 9, v0.10.48 — foco após formulários que desaparecem (02/11/2026)

- [x] Reproduzida perda de foco ao usar Enter para adicionar Socii, confirmar/cancelar programação e desfazer alteração fictícia; o botão acionado desaparecia após `render()` e o foco podia cair no `<body>`. O teste `browser_stage7_disappearing_forms_v0148.py` falhou na versão original de 280px. Corrigido **somente `src/main.ts`**, devolvendo foco a botão do convite, programação criada, título da lista e editor do membro, respectivamente. **28/28 PASS** depois, em sete larguras, sem mudança visual ou institucional.
- [x] Build 18/18 Node, regressões isoladas: teclado 76/76, revisão por teclado 24/24, ações removidas 14/14, Socii 36/36, anúncios 12/12, ARIA 28/28, erros 12/12 + 24/24, reflow 63/63, controles 2543, zoom simulado 70/70, contraste 87/87 + 40/40 + 2464/2464, calendário 36/36, Academy, tablet, desktop, fluxos de erro, editor Socii e retorno de calendário. Consultar `docs/CHECKPOINT_V058_2026-11-02.md` e logs; não contar execução conjunta expirada como aprovada.
- [ ] **07.10 permanece ABERTA**: verificação com leitores de tela reais, auditoria manual ampla WCAG, outros motores, mídia/gradientes e hardware. 07.05/07.06, 07.11 (D1–D6) e 07.12 continuam abertas.

**Contagem canônica sem alteração:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=0/4; 06=0/5; **07=7/12**. `main`/produção preservadas.


## Etapa 05 — primeira fronteira de identidade, prévia v0.10.49 (02/11/2026)

- [x] Contrato TypeScript `AcademyIdentityProvider` e resposta discriminada `unavailable`/`identified`, com `acdmId` como referência somente, **sem papel, permissão, token ou voto autorizado**. `UnconnectedAcademyIdentityProvider` retorna sempre indisponível; substituição futura depende do responsável pelo login da Academy.
- [x] Prévia e HTML offline realmente usam o adaptador. Em `?demo=1`, o painel informa que a identidade Academy não está conectada e que os perfis são simulações. Experiência normal, dados fictícios e chaves técnicas preservados.
- [x] Compilação TypeScript, bundle offline, 20/20 testes Node, smoke Chromium 4 viewports, painel avançado 9 larguras/45 alvos, novo teste de interface 4 larguras (sem login nem permissões falsas) aprovados. Detalhes: `docs/CHECKPOINT_V059_2026-11-02.md`.
- [ ] Nenhuma autenticação, autorização, sessão, banco institucional ou permissão real foi implementada. A equipe Academy continua responsável pela integração, que requer contrato real, verificações server-side e autorização explícita.

**Contagens oficiais desta rodada:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; **05=1/4**; 06=0/5; 07=7/12. Etapas 04 e 07 mantêm suas pendências e a Megalos não aprovou D1–D6. `main` e produção intocadas.

## Etapa 05.02 — referência de membro Academy, v0.10.50 (02/11/2026)

- [x] Perfil demonstrativo acessível por URL de referência `#/profile/acdm/DEMO-0002` ou pelo link ACDM ID no perfil; a navegação interna anterior `#/profile/m02` continua operante. A busca preexistente por ACDM ID foi reutilizada, não duplicada.
- [x] Nova função pura `resolveMemberReference` resolve apenas referência exata e única da coleção fictícia; desconhecida, inválida ou duplicada não abre perfil. Sem inferência de autenticação, papel, participação institucional ou direito de voto.
- [x] Build/Node **23/23**, teste novo de navegador quatro larguras (280/390/740/1280), regressões de perfil e navegação, reflow **63/63**, captura de 390px e área clicável de referência ≥44px. O inventário completo de controles foi interrompido no tempo máximo nesta rodada e não é contabilizado como aprovado.
- [ ] Login, sessão, vinculação real de cadastro, API da Academy e autorização no servidor requerem a equipe responsável e aprovação explícita. D1–D6 da Megalos permanecem pendentes.

**Contagens após v0.10.50:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; **05=2/4**; 06=0/5; 07=7/12. Sem alteração da `main` ou da produção.

## Etapa 03/04 — navegação de registros locais, prévia v0.10.51 (02/11/2026)

- [x] Vínculos **de sessão** bidirecionais: proposição concluída ou perfil da autora fictícia → programação ativa (seleciona dia e expande a programação); programação vinculada → perfil da autoria demonstrativa (aba de proposições); programação → proposição original permanece operante. Reaproveitados IDs locais existentes, sem alterar esquemas, autenticação, API ou regras.
- [x] Teste de quatro viewports reproduziu ausência do botão de autoria **antes** e percorreu ida/volta completa **depois**, incluindo cancelamento e isolamento de registros dos demais membros fictícios. TypeScript/build **23/23 Node**, perfil/proposições, retorno calendário, navegação, ACDM ID, smoke e reflow **63/63** passaram. Capturas 390 px revisadas. Checkpoint `docs/CHECKPOINT_V061_2026-11-02.md`.
- [ ] **Não concluir 03.05/04:** somente a primeira autora sintética da sessão dispõe dessa lista; autoria real multiusuário, colaboração Socii, agendamento institucional, integridade de permissões e aceite Megalos não estão disponíveis. A 07.10 continua aberta; testes físicos também pendentes.

**Contagens preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; **07=7/12**. A `main` e produção não foram alteradas. Próximo desenvolvimento pode ampliar vínculos dentro da prévia sem inventar identidade ou preferências da Megalos.

## Integridade de vínculos locais — preview v0.10.52, V062 (02/11/2026)

- [x] Defeito real reproduzido: `Date.now()` como único identificador gerou dois rascunhos distintos com o mesmo `draft-*` em relógio congelado, confundindo links e ações. Teste falhou antes da correção.
- [x] Correção pequena em `src/main.ts`: gerar sufixo incremental apenas se o ID já existir nos rascunhos ou programações da sessão, sem migrar IDs anteriores nem alterar dados fictícios. Novo teste `browser_workflow_id_collision_v0152.py` **4/4 larguras PASS**: rascunhos e programações distintos, cancelamento isolado, vínculo restante ativo, estado salvo íntegro.
- [x] Build TS/HTML + **23/23 Node**; regressões isoladas de quarentena/restauração, rollback parcial, assinaturas, navegação perfil-proposição-calendário, retorno, ACDM ID, reflow **63/63** e smoke quatro larguras PASS. Uma execução agrupada expirou; smoke foi repetido separadamente e aprovado. Ver `docs/CHECKPOINT_V062_2026-11-02.md`.
- [ ] Não equivale a histórico institucional ou persistência multiusuário: esses critérios dependem de backend, identidade/autorizações da Academy e decisões Megalos.

**Contagens não infladas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; **07=7/12**. `main` e produção intocadas. Próximo: examinar preservação/consulta de histórico de cancelamentos fictícios sem inventar política institucional.

## Entrega funcional v0.10.53 — Histórico local de programações canceladas (02/11/2026)

- [x] Corrigida a **invisibilidade dos cancelamentos já persistidos**: seção somente de leitura no calendário, oculta até haver registros cancelados e expansível por teclado, sem restaurar eventos ao calendário ativo ou inventar instante de cancelamento. Preservados vínculos locais e o símbolo oficial da Academy.
- [x] Teste novo falhou ANTES (`no cancelled history disclosure` em 280px), passou DEPOIS em quatro larguras incluindo restauração e segregação dos estados. `npm run build` **23/23 Node**, **6/6 regressões** de calendário, vínculos, integridade de IDs, reflow **63/63** e emblema oficial; screenshot 390px revisada. Veja `docs/CHECKPOINT_V063_2026-11-02.md`.
- [ ] **Histórico institucional real ainda pendente**: esta consulta usa apenas `sessionStorage`, sem identidade autenticada, timestamp do cancelamento, autorização de servidor ou trilha transacional. Não inflar as Etapas 03/04.

**Contagem canônica preservada:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. `main`/produção intactas; D1–D6 Megalos pendentes.

## Integridade local — v0.10.54, V064 — cancelamento sem gravação e recuperação (02/11/2026)

- [x] **Falha reproduzida ANTES:** se `saveWorkflows()` falhava ao cancelar, a interface dizia «Programação cancelada» embora o registro persistido continuasse `programada`, podendo reaparecer ao recarregar.
- [x] **Correção:** aviso explícito de cancelamento **somente nesta aba** e risco ao recarregar, mais ação secundária «Tentar salvar cancelamento nesta sessão». Segunda falha mantém aviso e foco; sucesso grava os registros locais, remove ação de recuperação e restaura o foco. Aviso permanece ao navegar para outro fluxo e voltar. Nenhuma mudança em backend, regras ou dados de produção.
- [x] **Antes/depois e regressões:** `browser_cancelled_save_recovery_v0154.py` falhou antes em 280 px e passou depois em quatro larguras, incluindo repetição da falha e recarga. `npm run build` **23/23 Node**, histórico 4 larguras, rollback parcial 4, quarentena de IDs, vínculos locais, teclado 28/28, restauração, reflow 63/63 e smoke quatro viewports concluídos. Capturas Chromium de falha e recuperação em 390px. `docs/CHECKPOINT_V064_2026-11-02.md`.
- [ ] **Histórico institucional ainda pendente:** esta recuperação é local e não substitui backend, autorização, logs imutáveis, autenticação Academy ou políticas Megalos.

**Contagens preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; **07=7/12**. Nenhuma promoção a `main`, deploy ou aprovação D1–D6.

## Integridade da prévia — v0.10.55 / V065 (02/11/2026)

- [x] Falhas de gravação **em autoria, conclusão/inclusão Socii e agendamento** reproduzidas com armazenamento bloqueado. O teste novo falhou antes em 280px por ausência de aviso; depois **16/16** cenários passaram em quatro larguras, incluindo falha repetida, recuperação, recarga e vínculo correto. Usa `saveWorkflows()` e seu rollback existentes, sem regra institucional nova.
- [x] Aviso de gravação não confirmada e botão de retry aparecem enquanto as alterações só existem na aba, com foco e região ARIA persistente. Mensagens não confundem conclusão local temporária com persistência. O calendário mantém o aviso especial para cancelamento sem duplicá-lo.
- [x] Build TypeScript/HTML + **23/23 Node**; regressões de rascunhos, revisão, Socii, integridade de assinaturas, históricos cancelados, recuperação de cancelamentos, armazenamento ilegível, navegação entre perfis/agendas, foco e anúncios, smoke quatro tamanhos e reflow 63/63 aprovados em execuções terminadas. Testes antigos corrigidos para não presumir armazenamento disponível em `about:blank`. Ver `docs/CHECKPOINT_V065_2026-11-02.md`.
- [ ] **Permanecem pendentes**: integração real, sessão compartilhada/autenticação, autorizações e auditoria institucional, regras Megalos D1–D6, telas/zoom reais e WCAG completa. Nenhuma promoção à `main`.

**Contagem oficial inalterada:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; **07=7/12**.

## Integridade de proposições restauradas — V066 / v0.10.56 (02/11/2026)

- [x] **Falha reproduzida e corrigida na prévia de sessão:** registros importados podiam declarar `revisao`/`concluida` com conteúdo inferior aos limites existentes no editor, ou declarar a própria autoria como seu Socii. Ajuste mínimo de `isSavedDraft`, sem novos direitos institucionais. Novos registros impossíveis ficam fora da lista válida e do agendamento; backups/quarentena existentes preservam a origem e rascunhos incompletos legítimos continuam utilizáveis.
- [x] Novo teste Chromium `browser_restored_proposal_integrity_v0156.py` **4/4 larguras** após reprovação antes do patch. Build TypeScript/offline **23/23 Node**, **14 suítes Playwright** concluídas (incluindo integridade de assinaturas, IDs, Socii, rascunhos, revisão, recuperação, perfil, calendário, reflow 63/63 e smoke quatro viewports). Uma execução agrupada teve timeout; os dois testes finais foram repetidos isoladamente com aprovação. Evidências em `docs/CHECKPOINT_V066_2026-11-02.md`.
- [ ] **Não é conclusão das Etapas 03 ou 04:** integrações de autoria, regras reais de colaboração e aceite Megalos permanecem pendentes. Nenhuma contagem avançou, nenhuma mudança em `main`, produção, login ou dados reais.

**Contagem canônica:** 01 4/5; 02 0/4; 03 1/5; 04 17/22; 05 2/4; 06 0/5; 07 7/12.

## Integridade referencial da prévia restaurada — V067 / v0.10.57 (02/11/2026)

- [x] **Falha reproduzida ANTES:** `sessionStorage` permitia Socii com participante inexistente, proposta em revisão/concluída com seção não encontrada e programação ativa vinculada a proposta presente ainda em redação. `browser_restored_links_integrity_v0157.py` reprovou em 280px com os registros fictícios `ghost-*` indevidamente restaurados.
- [x] **Correção mínima e segura:** `src/main.ts` valida referências contra as opções de membros/seções da própria prévia e impede agenda ativa para proposta existente não concluída. Mantém rascunhos parciais, cancelamentos históricos e links antigos explicitamente indisponíveis. Registros rejeitados são preservados em quarentena, sem reatribuir autoria, inventar regra institucional ou alterar CSS/arte.
- [x] **Testes concluídos:** novo navegador **4/4 larguras** (280/390/740/1280), `npm run build` **23/23 Node**, **12/12 suítes Playwright de regressão** concluídas e aprovadas, incluindo reflow **63/63** e smoke em quatro larguras. Uma chamada agrupada expirou, e os testes finais foram repetidos isoladamente com sucesso. Captura 390px revisada. `docs/CHECKPOINT_V067_2026-11-02.md`.
- [ ] Sem confundir consistência da sessão com autorização real, elegibilidade, assinaturas institucionais, colaboração multiusuário ou aprovação Megalos D1–D6. Etapas 03/04/05/07 permanecem pendentes nos mesmos critérios.

**Contagens canônicas mantidas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. `main`/produção inalteradas; nenhuma promoção ou deploy.

## Continuidade funcional — v0.10.58, backup local transportável (03/11/2026)

- [x] Exportação/importação **exclusivamente para ferramentas de demonstração** (`?demo=1`) do conjunto de proposições, Socii e programações locais, sem campos de votos, credenciais ou permissões Academy. JSON versionado, limite 2 MB/500 registros e apenas campos conhecidos; nenhuma conexão ou envio externo.
- [x] Validação integral da cópia antes da substituição: referências, assinaturas, IDs duplicados, seção, status e vínculos, com recusa sem mudança quando houver erro; confirmação explícita, rollback em memória e no armazenamento da sessão quando possível. Registros cancelados continuam somente no histórico.
- [x] Novo teste Node do envelope, teste Chromium em cinco larguras com download/restore/rollback e regressões direcionadas de integridade, calendário, reflow, smoke e Socci. Ver `docs/CHECKPOINT_V068_2026-11-03.md`.
- [ ] Não é backup seguro institucional, sincronização real ou solução de login. Dependências da Megalos, validação WCAG/hardware e integração Academy não foram concluídas.

**Contagens preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; **07=7/12**. `main` e produção intactas.

## Nova definição recebida da Megalos — 03/11/2026, prévia v0.10.59

**Origem:** mensagem da Megalos de 03/11/2026 às 08:38/08:41. Foram explicitamente definidas seis **modalidades de votação**, separadas das classificações de proposição PDR/PR/Ofício já utilizadas:

1. **Binária:** Sim ou Não, para aprovar ou não aprovar a proposição.
2. **Nominal:** escolha de uma opção; a mais votada vence (regras de empate ainda não informadas).
3. **Ordenada:** cada participante classifica as alternativas 1º, 2º, 3º etc. Método de apuração ainda não informado.
4. **Por aprovação:** participante pode aprovar múltiplas opções aceitáveis. Critérios de resultado ainda não informados.
5. **Escalar:** valor inteiro de 1 a 10 por alternativa; forma de agregação ainda não informada.
6. **Cumulativa:** membro distribui uma quantidade de votos proporcional à sua atribuição, definida por critérios específicos. A Diretoria de Projetos com quatro setores foi dada **como exemplo**, não como regra automática para todos os membros.

A pedido da Megalos, a prévia agora permite informar a **proporção de voto cumulativo** ao editar um cadastro fictício de membro ou ao vinculá-lo a uma seção na ferramenta demonstrativa. Campo opcional, inteiro positivo, sem peso presumido e sem dedução a partir de cargo/setor. O cadastro institucional efetivo pertence à Academy e requer integração posterior. Undo, reinício e restauração de sessão preservam a mudança conforme o modelo local; valores inválidos do armazenamento são ignorados.

No formulário de agendamento, novas programações exigem uma das seis modalidades. Classificação PDR/PR/Ofício permanece separada. Programações antigas sem modalidade continuam legíveis com indicação explícita de ausência; o novo campo participa das validações e da exportação/restauração local. Não se realizou contagem de votos real nem apuração de vencedor.

**Testes adicionados/adequados:** regras Node das seis modalidades e do peso cumulativo; scripts de agendamento em Chromium adaptados ao novo campo; regressão de configuração, edição e desfazer do peso no cadastro demonstrativo. A execução e resultados da nova branch devem ser registrados separadamente; alteração de teste não equivale a teste executado.

**Dependências que NÃO podem ser inventadas:** unidade/escopo do peso cumulativo (por membro, seção ou deliberação), quando ele é recalculado, distribuição parcial ou total dos votos, política de elegibilidade, quórum, abstenção, anonimato, alteração de voto, desempate, fórmula de apuração ordenada, escalar e por aprovação, auditabilidade, autenticação/autorizações Academy e voto transacional no servidor.

**Contagens permanecem:** 01=4/5; 02=0/4 (modelo ainda não consolidado para apuração institucional), 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. Nenhuma promoção da branch de prévia para `main`/produção.


## Continuidade funcional — v0.10.60, formulários das seis modalidades (03/11/2026)

- [x] As seis modalidades aprovadas na mensagem da Megalos têm controles **interativos de demonstração** isolados em `?demo=1`: binária (Sim/Não), nominal (escolha única), ordenada (permutação completa), por aprovação (várias alternativas), escalar (1–10 por opção) e cumulativa (distribuição sem ultrapassar a cota configurada de um membro fictício deliberativo).
- [x] Um validador tipado e independente da UI rejeita votos vazios, opções desconhecidas, posições duplicadas/ausentes, notas fora da escala, alocações negativas/fracionárias, ausência de cota e distribuição cumulativa acima do limite. A confirmação produz apenas **comprovante visual de simulação nesta aba**, sem somar votos ao resultado da votação anterior, salvar votos ou declarar vencedores.
- [x] Formulários em mobile e desktop com labels, campos de no mínimo 44px, erro visível e controle de correção. Cota cumulativa segue a edição/vinculação demonstrativa introduzida na v0.10.59; sem peso fictício automático.
- [x] Casos de teste **escritos** para validador Node (seis modalidades e rejeições), smoke Chromium (cinco modalidades, bloqueio cumulativo sem cota) e regressão de controles avançados (alocação acima da cota, distribuição válida e isolamento do resultado antigo). **Ainda não afirmar testes aprovados:** compilação e regressões da nova branch não foram executadas/confirmadas.
- [ ] Não é ainda a Etapa 02 completa: os votos são somente simulados em memória, as alternativas são fixas para avaliação de interface, não há voto vinculado a uma programação/proposição real, nem apuração institucional, persistência transacional, autenticação, quórum, elegibilidade ou registro auditável.
- [ ] A Megalos ainda precisa definir desempate, métodos de apuração ordenada/aprovação/escalar, uso parcial ou obrigatório da cota cumulativa, histórico, sigilo, alteração e encerramento. O uso parcial é **comportamento somente do laboratório**, não regra Academy.

**Contagens canônicas mantidas sem inflação:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. Trabalho restrito à branch `preview/v0.10.60-six-vote-forms`, sem merge/deploy em produção.

## Prévia v0.10.60 — vínculo das modalidades à programação (03/11/2026)

- [x] Programações novas com modalidade não binária exigem 2–8 alternativas distintas, fornecidas por quem agenda. Os IDs estáveis e rótulos são validados e preservados em arquivo local; programações antigas sem alternativas continuam legíveis, sem inventar opções.
- [x] No modo `?demo=1`, uma programação com modalidade definida pode abrir um **voto fictício contextual**, mostrando as alternativas cadastradas e a proposição vinculada. Não existe voto institucional, apuração, persistência de votos ou autorização Academy nesta prévia.
- [x] A navegação de perfil usa `data-member`; os formulários do laboratório usam `data-preview-member` para impedir que um clique de votação abra acidentalmente o perfil. Regressão Chromium específica adicionada.
- [ ] O intervalo de 2–8 alternativas e a permissão de cota cumulativa parcial são limites **somente do laboratório**, não regras institucionais aprovadas. Fórmulas de apuração, desempates, autorizações e votos transacionais continuam pendentes.
- [ ] A aprovação da compilação e dos testes do commit final será comprovada pelo workflow `Preview voting checks`; nunca marcar a Etapa 02 como encerrada com base nesta prévia.

**Contagens canônicas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. Branch de prévia isolada, sem promoção à `main` ou produção.


## Etapa 02 — contagens descritivas de amostras na prévia (03/11/2026)

- [x] O laboratório demonstrativo permite acumular até 100 amostras por modalidade ou programação, exclusivamente em memória da aba. Cada confirmação produz uma amostra; a próxima ação é Registrar outra amostra. Não há armazenamento em sessionStorage, exportação em backups nem associação com contas reais da Academy.
- [x] Seis resumos: Binária/Nominal registram escolhas; Ordenada mostra posições, incluindo primeiros lugares; Aprovação mostra marcações; Escalar mostra histogramas de notas 1 a 10; Cumulativa soma unidades fictícias sem perda de precisão. Nenhum destes resumos elege vencedor, aprova proposta, desempata ou estabelece quórum.
- [x] Limpeza das amostras da simulação atual exige confirmação e preserva outros contextos. Recarregar a página elimina amostras; a limpeza global da demonstração também.
- [x] Testes Node para as seis contagens e isolamento, e testes Chromium de múltiplas amostras, limpeza e programação contextual foram escritos. O resultado de execução desta alteração deve ser conferido no workflow antes de chamar de validado.
- [ ] Registro transacional, autenticação Academy, elegibilidade, sigilo, quórum, política de apuração, alterações de voto e encerramento permanecem indefinidos e não foram implementados.

**Checklist canônico inalterado:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. Main/produção não modificadas.

## Etapa 02 — guarda idempotente de amostras, sem persistência institucional (03/11/2026)

- [x] Registrador exclusivo de amostras em memória em src/domain/preview-ledger.ts: recibos recorded/replayed, repetição idempotente por contexto e solicitação, conflito para conteúdo diferente e limite de 100 por contexto.
- [x] Validação duplicada na fronteira de gravação, com snapshot de conteúdo e leitura defensiva; não associa votos a qualquer identidade institucional.
- [x] Interface de demonstração integrada ao registrador: token novo por amostra, limpar somente contexto ativo ou reiniciar tudo. Nenhum armazenamento de votos em sessionStorage, backend ou banco.
- [x] Testes específicos adicionados para seis modalidades, replay, conflito, limite, isolamento e imutabilidade. Resultados da CI pendentes antes de declarar conclusão técnica.
- [ ] Registro transacional oficial, autenticação e autorização de servidor, concorrência, auditoria, elegibilidade, sigilo, alteração e contagem institucional dependem da Megalos e da Academy; este módulo NÃO os implementa.

Contagens canônicas inalteradas: 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. Main e produção não alteradas.


## Etapa 02 — PostgreSQL transacional isolado (experimento de CI; 03/11/2026)

- [x] Preparada uma migração experimental SQL em esquema separado conffratus_vote_lab, com estado inicialmente bloqueado (fixture_enabled=false), participantes fictícios e seis estruturas de voto. Nada é aplicado a produção ou ao cadastro Academy.
- [x] Uma função SECURITY DEFINER de laboratório serializa operações por votação com SELECT FOR UPDATE, retorna recibos recorded/replayed/conflict/rejected, impede requisição duplicada e inclui gravação de voto e evento de auditoria na mesma transação.
- [x] A função não é EXECUTE para PUBLIC; papel NOLOGIN do laboratório tem USAGE do esquema e EXECUTE na função, mas sem acesso direto às tabelas. RLS habilitado como defesa adicional; nenhuma identidade oficial é inferida a partir do actor_ref fornecido na simulação.
- [x] Preparados testes SQL sintéticos para seis modalidades, entradas malformadas, quota, não inscrição, votação fechada, repetição, auditoria e proibição de update/delete; corrida de 12 chamadas iguais, 6 duplicatas distintas e verificação de acesso por papel. CI com PostgreSQL 16 descartável adicionada como bloqueio do build final.
- [ ] Integração com backend institucional, gateway autenticado Academy, autorização de leitura/escrita, regras aprovadas de eleitor, alteração de voto, sigilo, quórum, política de resultado e encerramento **não implementados**.
- [x] Job postgres-lab final aprovado em 03/11/2026, incluindo seis modalidades, entradas adversariais, concorrência, rollback de auditoria e encerramento concorrente. Evidência: Actions #41695893050.

**Contagem institucional mantida:** Etapa 02 0/4. Não tocar main, produção, banco ativo ou identidades reais.

## SQL experimental — fortalecimento de testes (03/11/2026)

- [x] Acrescentados casos adversariais para JSON com campos ausentes, arrays de tipos incorretos, alternativas duplicadas, modalidade binária incompatível, escala fora do limite, quota cumulativa negativa/fracionária/excessiva, números enormes e identificador malformado. Falhas não podem inserir votos nem registros de auditoria.
- [x] Adicionada injeção de falha controlada depois da inserção do voto e durante a escrita de auditoria; a transação deve reverter completamente. A repetição posterior com nova chave deve ser aceita. Uso exclusivo em PostgreSQL descartável.
- [x] A verificação SQL agora condiciona o job de compilação e navegação; o banco do CI é destruído após a execução. Nenhuma credencial institucional existe nos testes.
- [x] Logs da CI inspecionados; injeção de falha, rejeição adversarial e corrida de 12 solicitações confirmadas no job PostgreSQL 16 descartável, Actions #41695893050.

Etapa 02 0/4 permanece inalterada, sem conexão Academy nem alteração da branch main.
## SQL experimental — encerramento e simultaneidade (03/11/2026)

- [x] Teste de múltiplos atores fictícios em uma mesma votação: uma solicitação repetida não impede que outro ator cadastrado registre sua própria amostra com nova chave.
- [x] Teste concorrente de encerramento: transação separada mantém bloqueio na linha da votação depois de alterar seu estado para closed; um voto solicitado enquanto a trava está ativa deve aguardar e ser recusado, sem escrita de voto ou auditoria.
- [x] O teste de encerramento concorrente passou no PostgreSQL 16 descartável, Actions #41695893050. Políticas reais de encerramento, sigilo e alteração seguem indefinidas.

- [x] Defesa adicional no limite de entrada SQL: limite explícito de 8 KiB para o corpo JSON da amostra e search_path seguro com pg_temp por último; teste adversarial de payload grande adicionado. Não substitui limites nem autenticação na futura API institucional.

## Checkpoint confirmado — lote PostgreSQL de 03/11/2026

**Commit de código e testes verificado:** `45771b8f9b94a596bfbfc70dae678ab0819a3c12`.
**Evidência GitHub Actions:** https://github.com/Otiosun/conferatus/actions/runs/41695893050

- [x] `postgres-lab`: SQL e migração experimental aprovados em PostgreSQL 16 descartável. Seis modalidades, liberação padrão negada, RLS/permissões do papel, idempotência, entradas adversariais e limite do corpo JSON verificados.
- [x] Concorrência: 12 chamadas simultâneas com a mesma solicitação geraram 1 voto e 11 recibos de repetição; seis solicitações com chaves diferentes para o mesmo ator foram bloqueadas; outro participante fictício habilitado pôde votar.
- [x] Integridade: erro injetado na escrita de auditoria reverteu a inserção do voto; posterior tentativa válida foi aceita. Encerramento concorrente bloqueou nova gravação e não deixou voto nem auditoria.
- [x] `validate`: TypeScript, 44/44 testes Node e 5/5 suítes Chromium aprovados; artefato offline do CI gerado.
- [x] A versão de prévia **não incorpora** SQL ao HTML público: teste automatizado de exclusão da migração, papel e credenciais CI.
- [x] `main` verificada inalterada no SHA `4b244591c2f42913d2dca051b7d1256b896d25d8`, sem deploy ou conexão com banco/PM2/integrações reais.
- [ ] Aplicação institucional: não autorizar por ID fornecido pelo cliente. Acesso real depende de gateway autenticado Academy, regras aprovadas pela Megalos, autorização transacional no servidor, política de quórum/resultado, privacidade e homologação.

**Contagens sem inflação:** Etapa 01 = 4/5; 02 = 0/4; 03 = 1/5; 04 = 17/22; 05 = 2/4; 06 = 0/5; 07 = 7/12. O laboratório SQL não equivale à aprovação da Etapa 02.

## Integridade da prévia — programação cancelada e restauração (03/11/2026)

- [x] Cancelar uma programação local ativa invalida as amostras e o contexto de votação associados a ela, sem afetar outros contextos. Uma restauração de arquivo **bem-sucedida** limpa recibos e amostras anteriores, pois os IDs/alternativas importados podem ser diferentes. Restaurações recusadas ou revertidas preservam o estado anterior.
- [x] Regressões Chromium adicionadas às jornadas de calendário e backup/restauração em 4 e 5 larguras, respectivamente. Confirmar resultado de execução no CI antes de aprovar este checkpoint.
- [ ] As operações são locais; nenhuma regra institucional de cancelamento ou apuração foi presumida.

## Código humano / preguiça inteligente — validação de registros locais (03/11/2026)

- [x] Validação, limpeza de arquivos locais, detecção de IDs duplicados e geração de IDs extraídas do `src/main.ts` para `src/domain/workflow-records.ts`, com nomes explícitos e nenhuma dependência nova. O frontend continua em TypeScript/HTML/CSS puro.
- [x] O contexto de validação da prévia é passado explicitamente: IDs de membros sintéticos, seções deliberativas e autoria local. Não há autorização Academy implícita.
- [x] Testes Node adicionados para assinaturas, estados, opções personalizadas, propostas e programações restauradas, cópias limpas, duplicatas e colisões de ID. Build/Chromium do checkpoint ainda precisam ser verificados.
- [ ] A reorganização não é reescrita integral da UI: outros trechos extensos do `src/main.ts` merecem refinamento pontual **somente** quando houver melhoria de legibilidade ou defeito demonstrado. Nada de novos frameworks, microserviços ou infraestrutura sem necessidade.

**Contagens canônicas preservadas:** 01=4/5; 02=0/4; 03=1/5; 04=17/22; 05=2/4; 06=0/5; 07=7/12. Sem alteração da `main`.

## Etapa 03 — histórico local em visão geral (03/11/2026)

- [x] As proposições criadas nesta sessão agora também aparecem na guia Proposições do histórico geral, com status, trecho do documento e acesso à programação local associada. Não são confundidas com dados Academy, não alteram os indicadores históricos fictícios e não aparecem na guia de votos.
- [x] Perfil do autor não exibe mais o estado vazio enganoso quando há proposições locais mas nenhum registro antigo da mesma categoria.
- [x] Jornada Chromium adicionada: concluir proposição → programar deliberação → histórico geral → programação → votação fictícia. O resultado do CI deve ser confirmado antes de aprovar a execução.
- [ ] A vinculação multiusuário real continua fora do escopo desta prévia e dependerá da Academy.

**Contagens oficiais ainda não são alteradas por esta correção de coerência da prévia.**

## Qualidade de entrega — ampliação do teste contínuo (03/11/2026)

- [x] A CI passou a executar também as jornadas de perfis/proposições, navegação por autoria, Socii, integridade da revisão, falhas de gravação, foco do teclado e stress de reflow/zoom sintético. Total: 12 suítes Chromium, além dos testes Node e PostgreSQL.
- [ ] As sete suítes extras só serão tratadas como aprovadas depois de execução completa na branch de prévia; nenhum motor/dispositivo real adicional foi simulado.
- [ ] Não equivale a conformidade integral WCAG nem aceite visual da Megalos; a matriz objetiva será ampliada sem inventar aprovação das regras institucionais.

## Governança das regras máximas — revisão da checklist (03/11/2026)

- [x] Harmonizado o quadro-resumo de 07.04, 07.07, 07.08 e 07.09 com os fechamentos de seus próprios checkpoints e com a checklist específica da Etapa 07. **07=7/12**, sem concluir 07.05, 07.06, 07.10, 07.11 ou 07.12.
- [x] Atualizadas as leis de trabalho para deixar inequívocos código legível, preguiça inteligente, fronteiras com Academy, integridade local, testes e limites de publicação. Sem mudança de regras institucionais.
- [x] Criado teste automatizado que confere se os marcadores de conclusão correspondem à contagem anunciada no resumo e na Etapa 07. Qualquer divergência futura falha no build.

## Regressões reveladas pela CI ampliada (03/11/2026)

- [x] Dois testes antigos de agendamento agora preenchem explicitamente a modalidade binária obrigatória antes de enviar o formulário. O comportamento do produto não foi relaxado para satisfazer testes defasados.
- [x] Teste de retorno do histórico aguarda a atualização assíncrona da rota antes de interagir com a programação; clicar no controle durante um render anterior fechava a expansão indevidamente.
- [x] Corrigido o foco após «Registrar outra amostra»: se a modalidade contextual está bloqueada para edição, o primeiro campo real da votação recebe foco, e não o seletor desabilitado. Teste funcional de teclado adicionado.
- [ ] Confirmar nova execução integral das 12 suítes antes de marcar o gate de qualidade como aprovado.

## Histórico geral — retorno contextual da proposição (03/11/2026)

- [x] Ao abrir uma proposição concluída pelo histórico geral, «Voltar ao histórico» deve restaurar a guia Proposições da visão geral. O retorno pelo calendário continua apontando para a programação; o retorno pelas outras listas mantém seu fluxo existente.
- [x] Adicionada regressão Chromium na jornada já existente, sem novo pacote nem abstração. Verificar status completo da CI depois do commit.
- [ ] A lista permanece local para documentos da sessão; não representa publicação institucional nem sincronização Academy.

## Evidência visual reproduzível — revisão de entrega (03/11/2026)

- [x] A CI reaproveita as capturas `.png` que os testes Playwright existentes já produzem em `dist/`, e publica um artefato separado de evidências, mesmo quando uma regressão de navegador falha. Não captura identidades reais nem solicitações Academy, e não adiciona bibliotecas.
- [ ] As capturas mostram **apenas o produto demonstrativo**, não são comparações aprovadas com as referências Megalos. O gate 07.11 exige revisão humana contra D1–D6.

## Matriz estendida de regressão — 25 jornadas (03/11/2026)

- [x] Reutilizadas **13 suítes Playwright já presentes** no repositório, somadas às 12 executadas anteriormente: navegação, rascunhos, Socii, assinaturas, recuperação e duplicatas, colisão de IDs, programação/cancelamento, integridade de importação e controles de formulário. Não foi instalada nenhuma dependência.
- [x] Ajustado um teste de cancelamento antigo para informar a modalidade binária obrigatória e corrigido um erro de indentação em um script antigo; nenhuma validação foi removida do produto.
- [ ] O novo gate deve concluir integralmente em Chromium antes de registrar 25/25. Homologação Megalos, WCAG global e outras engines/dispositivos seguem pendentes.

## Navegação contextual de perfil e autoria — correção funcional (03/11/2026)

- [x] Uma proposição aberta a partir do perfil do autor passa a preservar a origem tanto no editor de rascunhos quanto no detalhe de proposição concluída; «Voltar ao perfil» regressa à aba Proposições do autor fictício.
- [x] O atalho de histórico no fluxo de elaboração aponta para o autor daquele fluxo (dados fictícios), não para outro membro que tenha sido selecionado previamente no diretório.
- [x] Regressão Chromium estendida em 320, 390, 740 e 1280 px, incluindo troca de membro anterior. Validar na CI antes de aprovar o checkpoint.
- [ ] A atribuição e a navegação aqui representam o autor sintético da prévia; não são identidade Academy.

## Clareza dos votos fictícios na experiência padrão (03/11/2026)

- [x] A seção de votação da prévia padrão informa, junto à descrição, que resultados e escolhas são fictícios e **nenhum voto é enviado à Academy**. A escolha exibida após clicar é chamada de **simulada**, não de registro oficial.
- [x] Mantido o layout e o rótulo da ação original onde as referências Megalos ainda aguardam decisão; não inventadas regras institucionais.
- [x] Reaproveitado o teste `browser_preview_disclosure_v0117.py`, estendido para verificar comportamento normal, reinicialização da escolha e escrita **exclusivamente** na chave fictícia `conferatus:demo-vote` do `sessionStorage`, além da prévia de agendamento. Agora são 26 suítes selecionadas na CI.
- [ ] Confirmar CI completa antes de marcar o lote como validado. Nenhuma interação implica voto remoto.

## Etapa 06 — guia vigente de apresentação (03/11/2026)

- [x] O guia antigo v0.6 foi substituído **no mesmo arquivo** `docs/DEMO_GUIDE.md`, sem adicionar documentos redundantes. Contém roteiro verificável do produto atual, modos normal/avançado, limitações de simulação, recuperação local, critérios de QA e decisões D1–D6.
- [x] `README.md` aponta para o guia vigente. O quinto critério da Etapa 06 está concluído no escopo de **preparação documental**, sem inventar aceite visual ou publicação institucional; **Etapa 06 = 1/5**.
- [ ] A apresentação à Megalos, feedback/assinatura de aceite, equipamentos reais e eventual promoção à produção seguem fora deste fechamento documental.

## Gerenciamento administrativo da prévia — transparência (03/11/2026)

- [x] O Gerenciamento Deliberativo passou a declarar explicitamente junto aos controles que edição e rebaixamento são operações sobre dados **fictícios deste navegador**, sem modificar cadastros Academy. A estrutura de botões, hierarquia e ações de demonstração permanecem preservadas.
- [x] O teste de divulgação também percorre, no modo normal, histórico geral → gerenciamento, verifica o aviso acessível e garante que o painel avançado de desenvolvimento não aparece sem `?demo=1`.
- [ ] Confirmar o gate completo da branch antes de declarar este lote validado; não implica autorização de um diretor real.

## Código humano — remoção de função não utilizada (03/11/2026)

- [x] Auditoria simples das funções locais encontrou apenas `resetDemoState()` sem chamada. A função morta foi removida, sem criar novo controle ou nova dependência.
- [x] **Preservado** o snapshot `initialMembers`, que é usado pela ação funcional `reset-admin` na prévia. A limpeza não altera o comportamento de desfazer nem de restaurar os dados administrativos fictícios.
- [ ] Confirmar build e regressões após a remoção deste protótipo.

## Verificação do armazenamento fictício de voto (03/11/2026)

- [x] Corrigida a expectativa do teste: a prévia básica **persiste a escolha simulada na chave local `conferatus:demo-vote`**, para manter o estado nesta aba. Isso não é um voto institucional, nem uma gravação em banco ou Academy.
- [x] O teste observa as chamadas de gravação em um `sessionStorage` simulado e exige apenas essa chave para a ação do voto. A ausência de toda gravação era uma suposição incorreta; a verificação foi ajustada ao comportamento real em vez de enfraquecer a interface.
- [ ] Confirmar nova execução da CI antes de declarar o conjunto validado.

## Acessibilidade: reutilização de testes existentes (03/11/2026)

- [x] A matriz contínua inclui três verificações Playwright já existentes: relacionamento ARIA entre controles e painéis, avisos de estado persistentes e vínculo de erros aos campos de formulário. **29 suítes** de navegador selecionadas, sem dependências novas.
- [x] Corrigidos dois scripts legados: indentação no ensaio de avisos e seleção explícita da modalidade binária na verificação de datas inválidas. Nenhuma validação do produto foi reduzida.
- [ ] Validar 29/29 no GitHub Actions antes de afirmar conclusão. Evidência de DOM/ARIA no Chromium não substitui leitor de tela real nem certificação WCAG.


## Auditoria de retomada para fechamento da prévia — 05/11/2026

- A branch `preview/v0.10.60-six-vote-forms` foi inspecionada no HEAD `2878343c9db87534d06c199514656d87cbc86e8f`; a `main` foi confirmada em `4b244591c2f42913d2dca051b7d1256b896d25d8`. Esta seção é somente reconciliação documental; não contém código de produto nem aprovação de publicação.
- Os **29 caminhos de suítes Playwright** declarados em `.github/workflows/preview-voting-check.yml` foram lidos com sucesso na branch. A CI contém PostgreSQL 16 descartável, build TypeScript/Node e execução de navegador; a presença de arquivos e configuração **não prova execução bem-sucedida**. Nenhum 29/29 é atribuído a este levantamento.
- Nos testes de agendamento inspecionados, as datas operacionais de dezembro/novembro futuro ainda são posteriores a 05/11/2026. Uma data histórica de arquivo restaurado permanece fixture de importação, sem justificativa para alterar código ou testes.
- A experiência de voto comum foi inspecionada: aviso de escolha fictícia, gravação somente em `sessionStorage` e nenhuma remessa Academy. A integração com contas, votos institucionais e apuração definitiva segue fora do escopo contratado da prévia.
- **Próximo gate objetivo:** obter execução completa e verificável da CI para este HEAD ou um descendente, corrigir exclusivamente falhas reais, preservar D1–D6 e solicitar homologação da Megalos quando couber. Relatório de auditoria também lançado no handoff mestre do Google Drive Komekko em 05/11/2026.


## Fechamento do gate técnico de prévia — CI #37 (05/11/2026)

- [x] A execução **GitHub Actions #42028651277**, no commit `ad25f6b435574aa88d23812847242f774b94fcdf`, encerrou com **success** em 05/11/2026. Evidência: https://github.com/Otiosun/conferatus/actions/runs/42028651277
- [x] O job `postgres-lab` passou em PostgreSQL 16 **descartável**, inclusive seis modalidades, entradas adversariais, idempotência, simultaneidade, auditoria atômica e bloqueio de voto após encerramento. Não houve contato com banco Academy.
- [x] O job `validate` passou: TypeScript/build, **51/51 testes Node**, **29/29 scripts Playwright Chromium** e empacotamento offline. Os logs foram lidos; não é inferência a partir de arquivos presentes. Os ensaios são sintéticos e não homologam Firefox, WebKit, leitor de tela real nem hardware.
- [x] Os artefatos de CI foram preservados na pasta privada do projeto no Drive Komekko: [prévia HTML testada](https://drive.google.com/file/d/1MbKMzURub0qf7zw78Zg63CKk6IyVsaEy/view) e [capturas de navegador](https://drive.google.com/file/d/1sMGu2DE6rv0EVQCUq34UjPmvAbPKOwEH/view), com leitura de metadados confirmando tamanho e pasta. O ZIP da prévia contém `CONFFRATUS_demo_offline.html`, sem backend institucional.
- [ ] A Etapa 06 continua **1/5** até revisão de fidelidade com Megalos, validação visual/hardware aplicável e decisão explícita de publicação. A Etapa 07 continua **7/12**; o laboratório não homologa integração Academy nem regras D1–D6.
- **Decisão de escopo:** nenhum defeito de código exigiu correção nesta rodada. Não desenvolver recursos extras, não alterar `main`, produção, autenticação ou serviços Academy. O próximo passo é **homologação da prévia pela Megalos**, não ampliação automática do sistema.


## Revisão com Socii — reprodução do cabeçalho da Megalos (05/11/2026)

- [x] Corrigida **diferença objetiva de apresentação**: a revisão de proposição com participante Socii agora reutiliza a mesma faixa de participantes e progresso que já existia na redação. A fonte visual `1001930222.jpg` e o vídeo mostram esta faixa na revisão; nenhum novo estilo ou componente foi inventado.
- [x] A faixa depende exclusivamente de participantes efetivamente vinculados à proposição local; não aparece em revisão individual. O texto distingue **prévia local** e conserva a contagem de confirmações sem inventar horas, convites remotos ou regras de conclusão.
- [x] O teste existente `tests/browser_review_metadata_integrity_v0119.py` foi estendido para verificar presença/ausência da faixa em quatro larguras e registrar a revisão com Socii a 390 px; nenhuma suíte adicional nem dependência de produção.
- [x] **CI #39 confirmada** no commit `77df922c6f07eaac950c9a04ae1a9f348eb57580`: PostgreSQL 16 descartável, build, **51/51 testes Node** e **29/29 scripts Chromium**, incluindo verificação da faixa Socii durante revisão e sua ausência em propostas individuais. Execução: https://github.com/Otiosun/conferatus/actions/runs/42050356493 . Ainda não equivale à homologação Megalos ou à publicação na `main`.

- [x] Artefatos da **CI #39** preservados no Drive Komekko: [HTML offline da versão corrigida](https://drive.google.com/file/d/1biAxLv4bH2rBgQiwx8uW8WmBMlXCW2O_/view) e [28 capturas automatizadas, incluindo Socii na revisão](https://drive.google.com/file/d/1VUjCkCjY9-TUiPt-QSYC9mHYqHZsDVOE/view).
- [ ] A captura de Socii do teste automatizado contém o aviso de gravação local não disponível, relacionado ao ambiente de teste em `about:blank`. **Não usar essa captura isolada como aprovação visual final**. Não foi possível abrir origem HTTP ou `file://` no Chromium local restrito; mantenha validação visual em origem real como pendência de homologação, sem inferir defeito do produto a partir desse aviso.


## Revisão Socii — aviso contextual de participante concluído (05/11/2026)

- [x] A comparação visual da prévia corrigida com `1001930222.jpg` identificou uma diferença objetiva: a referência nomeia a pessoa que concluiu sua parte, mas a revisão da prévia apresentava apenas o texto genérico. Quando existe uma confirmação local, o texto agora identifica o primeiro participante concluído que já consta da sessão; sem confirmação mantém o aviso antigo. Esse fato é **somente demonstração local**, nunca confirmação institucional.
- [x] O teste Playwright já existente `browser_review_metadata_integrity_v0119.py` valida a mensagem contextual e a ausência de mensagem fictícia em revisão sem Socii. Não altera dados, cargos, permissões, tela de rascunhos, modal de confirmação, conclusão final, regras de voto ou Academy.
- [x] **GitHub Actions #41 passou** no commit funcional `f16ce42181e827dfead3ba02812d663a21c6b501`: PostgreSQL 16 isolado, TypeScript/build, 51/51 testes Node, 29/29 jornadas Chromium. O teste `browser_review_metadata_integrity_v0119.py` validou o texto contextual e o texto genérico em revisão individual. Evidência: https://github.com/Otiosun/conferatus/actions/runs/42062445845

- [x] Artefatos originais da CI #41 preservados no Drive: [HTML corrigido](https://drive.google.com/file/d/1DOxRDBPeZeYWQeORFO7gtIQJwBcDB-3L/view) e [capturas Playwright](https://drive.google.com/file/d/1oojFA1W6WdlMkUx19arkE8U7QnQfNiYO/view). A execução automática encerrou SUCCESS, não só recebeu upload.
- [x] [Comparação privada com fonte Megalos + quatro capturas limpas de inspeção visual](https://drive.google.com/file/d/1Sul_brrnrNupZIuvwPSp1kwwUjSdIXeP/view), SHA-256 `2bd41e045359ab4a373ef67376101576c6ff74d3652ce29cce7228a564f9b0ac`. Reprodução por armazenamento **em memória** devido à política local que bloqueia HTTP/file; a captura **não é teste de persistência**.
- [x] QA adicional nesse HTML: longos parágrafos e palavras sem quebra em 280/320/390/740/1280 px, sem overflow; emulação de toque em 320×568, 360×640, 640×360 e 844×390, confirmação acionável e percurso concluído. A matriz é **sintética**: não comprova teclado virtual, safe-area ou hardware real, nem muda a contagem da etapa 07.
- [ ] Continua pendente a revisão visual de fidelidade pela Megalos e validação física/integrada quando cabível. Nenhuma autorização de mudança institucional ou publicação em `main` decorre deste commit.


## 07.05 / 07.10 — correção objetiva de rodapé e contraste na revisão (05/11/2026)

- [x] Reproduzida a quebra de marca `CONFFRATUS` no rodapé da prévia em 280px (normal) e 280–360px (texto sinteticamente ampliado a 200%); o aviso `DADOS FICTÍCIOS · PRÉVIA` e o botão Menu disputavam largura. Corrigida a grade **apenas até 360px**, preservando marca, logotipo Academy, aviso e Menu sem esconder elementos e sem dependências extras. O Menu ajusta altura quando o rótulo cresce.
- [x] Reproduzido contraste insuficiente no aviso de confirmação da revisão Socii (`#7b808e` sobre `#e7e9ee`, cerca de **3,25:1** para texto de 13px). Substituído por `#5b6275`, contraste calculado **5,01:1** na mesma superfície, mantendo a família cromática.
- [x] A matriz Chromium offline `browser_stage7_zoom_reflow_v0135.py` passa a incluir a **revisão com Socii vinculado** (antes ausente), inspeciona o número de linhas da marca, clipping do Menu, sobreposições do rodapé e contraste do aviso, em 320/640/1280px CSS equivalentes e sete larguras com texto sinteticamente ampliado. Total esperado **80 combinações rota×largura**; nenhuma alteração em regra institucional.
- [x] Ensaio exploratório local com HTML offline da CI #41 e CSS substituído apenas na página: **84 combinações rota×largura×modo** sem overflow, colisão, clipping ou baixo contraste. Esse ensaio antecede o commit definitivo e **não substitui a CI**. O aviso de armazenamento de `about:blank` foi isolado apenas no teste visual mediante um objeto de sessão em memória, nunca representado como persistência real.
- [x] **CI final #44 aprovada** no commit de código `05fe01fd6e754925f1a5dee54cbf4b40de998c98`: PostgreSQL 16 isolado, TypeScript/build, 51/51 testes Node e 29/29 jornadas Chromium; a suíte ampliada `browser_stage7_zoom_reflow_v0135.py` passou **80/80 combinações** e validou contraste do aviso e dos dois rótulos na revisão Socii, nome do rodapé em uma linha até 360px, Menu sem corte, sem colisões ou overflow. Link: https://github.com/Otiosun/conferatus/actions/runs/42068773791

- [x] Varredura complementar da revisão Socii identificou dois rótulos pequenos sobre a mesma superfície (`Seção responsável` e `Tipo de proposição`) com contraste **3,47:1**. Ambos passaram a usar `#5b6275` (aprox. **5,01:1**), mantendo tamanho e espaçamento. A suíte existente agora mede também o contraste de cada rótulo; QA local e CI final #44 passaram.

- [x] Artefatos **exatos do commit 05fe01f**, gerados pela CI #44 e preservados no Drive Komekko: [HTML offline](https://drive.google.com/file/d/1Y30vkpxnOrRdysRhRADGwsUxaj6rgiN0/view), [28 capturas do workflow](https://drive.google.com/file/d/1wHRzzrrz_uLDDWZ3s--UXKF2RIhakX2J/view), [QA complementar do HTML exato com 84 medições e capturas em quatro larguras](https://drive.google.com/file/d/19Amt_sVvUzA5EiWSbCNxp1cTfyO70D-L/view) e [comparação antes/depois a 280px](https://drive.google.com/file/d/1EuSDxFWXXetXMyV_atBrlp5mQNtCiCXr/view). Metadados de tamanho/pasta no Drive conferidos.
- [ ] A Etapa 06 continua **1/5** e a Etapa 07 **7/12**: faltam validação final em aparelhos e tecnologias assistivas, decisões visuais D1–D6 e aceite Megalos; nenhuma certificação WCAG global foi alegada. Não alterar `main`, produção ou Academy sem autorização.


## 07.10 — Contraste do botão Salvar no gerenciamento demonstrativo (05/11/2026)

- [x] Varredura adicional de estados ativos do Chromium offline detectou contraste insuficiente no botão `Salvar` da edição de membros fictícios: `#3d46a3` sobre `#afb7e6` resulta em aproximadamente **4,12:1** para texto de 11 px. A cor da classe `.small-action` foi corrigida para `#303b85`, resultando em aproximadamente **5,14:1** com o mesmo fundo. Nenhuma alteração de layout, dados, autorização ou ações do formulário.
- [x] Teste de contraste calculado a partir das cores reais do navegador adicionado ao script Playwright existente `tests/browser_stage7_form_edge_targets_v0131.py`, já incluído na CI, em nove larguras de 280–1440 px. Verificado localmente em 280, 320, 390, 740 e 1280 px que o botão continua com alvo >=44 px, formulário funcional e sem overflow com a cor corrigida.
- [x] CI #46 aprovada no commit `a18d63443005693cb1591b7142397514f5cb4559`: PostgreSQL descartável, 51/51 Node e 29/29 Playwright Chromium, incluindo contraste do botão Salvar nas nove larguras. Evidência: https://github.com/Otiosun/conferatus/actions/runs/42072577808 . Não equivale à certificação WCAG global.


## 07.10 — Contraste dos placeholders nos formulários de gerenciamento e agendamento (05/11/2026)

- [x] Auditoria dos campos vazios reproduziu contraste de **2,83:1** para os placeholders `DEMO-0001` e `Não definida` na edição fictícia de membro (`#757575` sobre `#c6c9e7`). Ajuste CSS localizado `.edit-form input::placeholder` para `#454d6d`, contraste calculado **5,09:1**.
- [x] No formulário azul de agendamento, `Título da deliberação` e `Descrição objetiva` apresentavam contraste composto de **3,84:1** por transparência do fundo e do texto. Ajustado o fundo dos controles de `#ffffff1d` para `#ffffff10` e os placeholders para `#fffffffa`, mantendo a composição azul e obtendo aproximadamente **4,81:1**. Texto preenchido continua branco, sem alterações de conteúdo ou lógica de agendamento.
- [x] A suíte Chromium existente `browser_stage7_form_edge_targets_v0131.py`, já no workflow, passa a medir contraste real dos quatro placeholders, calculando transparência do texto e camadas de fundo, em nove larguras. Prova exploratória sobre o HTML CI #46 com CSS aplicado somente no navegador passou em 280/320/390/740 px sem overflow ou perda do formulário. A CI #47 do commit funcional `b12f8e2b6ce965f77709a99056e60301ae1ace5a` confirmou 51/51 Node, 29/29 Playwright e PostgreSQL descartável: https://github.com/Otiosun/conferatus/actions/runs/42074157858 .
- [ ] Não marcar conformidade WCAG global, integração Academy, hardware ou homologação visual por esses ajustes. Main/produção preservadas.

- [x] Artefatos CI #47 preservados no Drive privado: [HTML offline exato b12f8e2](https://drive.google.com/file/d/12wq-E6GZV3MrpLQl62SYJDPgm0S_u9hh/view), [28 capturas Playwright](https://drive.google.com/file/d/1n2pxJJVfPjk-5wF3lOyepCvTxWBeJG__/view). ZIPs inspecionados, contendo as correções, digests SHA-256 idênticos aos da CI. [Comparação antes/depois do botão Salvar](https://drive.google.com/file/d/1COVEyaSoG-qP73glUYehHmJn-nkEE3Gr/view) é inspeção local e não captura da publicação HTTP.
- [x] Cloudflare Pages confirmou deploy de preview do commit b12f8e2 no alias de branch: https://preview-v0-10-60-six-vote-fo.conferatus.pages.dev. Endereço inserido também no README e roteiro de demonstração, e no documento privado de homologação da Megalos. O acesso HTTP real neste ambiente ficou bloqueado: não presumir teste direto do site publicado.
- [ ] Etapas 06=1/5 e 07=7/12 ainda abertas: faltam homologação Megalos, testes em aparelhos/tecnologias assistivas e autorização expressa para publicar na main. Nenhuma integração Academy ou promoção à produção.


## Gate de normalidade da prévia e segurança de texto (05/11/2026)

- [x] Inspeção independente do HTML offline **CI #47**: em 6 rotas × 4 larguras (320/390/740/1280 CSS px), o modo normal exibiu apenas navegação e ações demonstrativas previstas; sem laboratório avançado, exportação/restauração JSON, painel técnico ou ações de teste exclusivas de `?demo=1`. Aviso visível `DADOS FICTÍCIOS · PRÉVIA` preservado.
- [x] `tests/browser_preview_disclosure_v0117.py` estendido para cobrir, no modo normal, ocultação dos controles avançados em Proposições/Socii, botão Socii acessível e legenda preservada, em quatro larguras. O subitem 06 de separação dos controles de teste foi encerrado **no escopo demonstrativo**, sem alegar entrega institucional completa.
- [x] Prova exploratória independente do fluxo de proposições com texto HTML não confiável em título e corpo, em 9 larguras 280–1440 CSS px: HTML/eventos JavaScript ficaram como texto literal na lista, editor e revisão, com zero execução de eventos e zero rolagem horizontal. O teste permanente `tests/browser_stage7_long_draft_v0133.py` passou a verificar esse caso sem alterar o produto, commit `d8245a77b4f65b54f360d604ae9f8194f24b6fa0`.
- [ ] Confirmar a CI completa dos commits de testes antes de afirmar **29/29 scripts e 51/51 Node** na versão final da branch. A varredura sintética não equivale a pentest, leitor de tela, aparelhos reais, homologação Megalos, ou política de privacidade/sessão de produção.


## Auditoria horizontal dos modelos Megalos — 05/11/2026

- [x] Seis JPGs originais confrontados lado a lado com capturas do HTML da prévia. Os modelos 0221/0225/0226 centralizam o brasão e a marca no mesmo eixo; a versão anterior deslocava o emblema para x≈33 em viewport de 360px (erro ≈147px).
- [x] Brasão agora central ao fechar e no alto da gaveta ao abrir; marca e botões com eixo horizontal comum, ícones preservados à esquerda sem deslocar os rótulos. O Menu mantém ancoragem que evita +231px de rolagem. Teste `browser_footer_drawer_v0162.py` ampliado com 8 formatos e asserts de alinhamento.
- [ ] Gate da CI e avaliação em Android físico pendentes antes de promover à main. D1–D6 permanecem como diferenças reais de composição/posicionamento dependentes da revisão da Megalos, particularmente botões inferiores do perfil, local do agendamento e confirmação visual.

- [x] Comparação específica do perfil 0225 identificou um defeito de grade independente da navegação: cinco métricas com `grid-template-columns:repeat(4,...)` faziam “35 Socii” descer para outra linha. Corrigido para cinco colunas flexíveis; ensaio local em 280/320/360/390/540/740 CSS px sem overflow, com adaptação a 200% de texto. Teste de cinco indicadores e linha única acrescentado a `browser_footer_drawer_v0162.py`; CI final ainda pendente.


## Retomada de CI multimotor: diagnóstico de timeout — 05/11/2026

- [x] HEAD anterior conferido: preview `6b8f9acc1ca4eccbcd252596dc708e0cdbef0c81`; main/produção `81d0f55eb7772cbd1665df05cf05addb44db9723`. Quatro commits separavam a prévia da main antes deste lote. As regras em `AGENTS.md` seguem vigentes.
- [x] Logs da GitHub Actions `42100170732` lidos: `postgres-lab` SUCCESS, `validate` SUCCESS, TypeScript/build, **51/51 testes Node** e **31/31 scripts Chromium**. O script `browser_footer_drawer_v0162.py` reportou **8/8 PASS** nas verificações sintéticas do menu, centralização e indicadores. https://github.com/Otiosun/conferatus/actions/runs/42100170732
- [x] O `cross-browser-lab` desse mesmo run foi **CANCELLED na instalação de dependências Firefox/WebKit**, com downloads lentos do Ubuntu e limite de **22 minutos**. O passo de testes multimotor ficou `skipped`; **não atribuir 3/3 Firefox ou 3/3 WebKit ao SHA 6b8f9ac**. Não há falha de produto demonstrada por esse cancelamento.
- [x] Alteração estritamente de infraestrutura no commit `719bdb60595b0d2f36fab9c2ac62132a15613532`: `cross-browser-lab.timeout-minutes: 22 → 40`, sem alterar comandos, exclusões ou asserts; mensagem `[cross-browser]` opta pelo job. Arquivo único: `.github/workflows/preview-voting-check.yml`. https://github.com/Otiosun/conferatus/commit/719bdb60595b0d2f36fab9c2ac62132a15613532
- [ ] Ainda **não** foi confirmada a conclusão da CI para o novo HEAD. Guardar logs e artefatos do novo run quando verificados; não promover para `main` com base apenas no aumento de tempo.
- [ ] Android físico após correção, decisões D1–D6/"127 horas" e homologação Megalos permanecem pendentes. Contagens **Etapa 06 = 2/5** e **Etapa 07 = 7/12** não mudam. Academy, dados institucionais, autenticação, APIs e produção intocados.
- Handoff mestre no Google Drive Komekko atualizado com o checkpoint 84. Nenhum recurso novo ou alteração de aparência foi incluído neste lote.


## 07.05 — não fragmentar “Menu” com texto a 200% — 06/11/2026

- [x] Inspeção direta da captura `zoom_text200_calendar_320.png` do HTML offline da CI `42100170732` revelou que o rótulo do botão de rodapé aparecia como `Men` / `u` em 320 CSS px com ampliação sintética do texto a 200%. O teste legado verificava apenas clipping e colisões, não fragmentação de palavra.
- [x] QA exploratório local em Chromium, **sobre o HTML exato da CI anterior com CSS injetado apenas no navegador**, verificou 280/320/360/390 px. A declaração `overflow-wrap:normal` no próprio `.app-footer .footer-nav` reduziu o texto de três para duas linhas em 280/320 px (ícone separado, palavra Menu íntegra), mantendo largura do documento, marca centralizada, sem overflow do botão e sem colisão entre título/menu. Não representa execução da nova build nem aparelho físico.
- [x] Correção de uma declaração CSS aplicada somente à prévia: commit `1cd053350ff58b0ef74c6e8c57f6be4d374b85f9`, em `src/styles.css`. Nenhuma mudança de markup, fonte, nível de zoom, conteúdo, dados ou fluxo.
- [x] A suíte já existente `tests/browser_stage7_zoom_reflow_v0135.py` foi ampliada com contagem de linhas reais do texto do botão e asserção de no máximo duas linhas a 200% nas larguras compactas 280/320 px. Commit `f5c48f7a68460600d368e568ea3a11d914d0a872`. CSS e teste lidos novamente na branch.
- [x] Evidência privada de antes/depois (320 CSS px, texto 200%, **ensaio offline sintético, não CI do novo commit**): https://drive.google.com/file/d/1UolbSiQeSW2XXLpnuMbUqXXw6MkLhurj/view .
- [x] Pacotes temporários da CI anterior `42100170732` preservados no Drive Komekko, com integridade ZIP local e tamanhos verificados após upload: HTML 97.228 bytes https://drive.google.com/file/d/1gRwY13JhJc-rU7VLpsVCJz4gfAzqmBSB/view ; 33 capturas PNG, ZIP 2.918.371 bytes https://drive.google.com/file/d/1ugkpi60StA7FhXlvLuWUBBE06e0ngSM2/view . Esses pacotes são da base `6b8f9ac`, não do CSS novo.
- [ ] A CI de código do lote e o laboratório Firefox/WebKit **ainda precisam de resultado confirmado**. Não reportar aprovação automática do novo HEAD. Sem homologação Megalos D1–D6, regra de “127 horas” ou teste Android físico. Etapa 06=2/5 e Etapa 07=7/12, inalteradas.
- [x] `main` verificada intacta em `81d0f55eb7772cbd1665df05cf05addb44db9723`. Nada de Academy, banco real, autenticação, publicação principal ou novas modalidades.


## Gate final multimotor validado e pacote visual preservado — 06/11/2026

- [x] GitHub Actions `42162507726`, tentativa 2, **SUCCESS**, commit testado `968fa3871c0355c6cc2356734476e05e9ed23a3b`: jobs PostgreSQL isolado, `validate` e `cross-browser-lab` concluídos com sucesso. Logs conferidos: TypeScript/build, **51/51 Node**, **31/31 Chromium**, inclusive `browser_stage7_zoom_reflow_v0135.py` 80/80 e `browser_footer_drawer_v0162.py` 8/8; **Firefox 3/3** e **WebKit 3/3**. https://github.com/Otiosun/conferatus/actions/runs/42162507726 .
- [x] A primeira tentativa desse run foi cancelada por lentidão anormal na instalação de 181 pacotes Playwright em repositórios Ubuntu. Apenas o job multimotor foi reexecutado e passou; nenhum teste funcional do produto precisou ser relaxado, removido ou reescrito. O check `Cloudflare Pages` do mesmo SHA foi `success` na API GitHub. O sucesso de deploy não comprova HTTP direto no aparelho.
- [x] Backups exatos do **mesmo SHA**, íntegros por ZIP e SHA-256, enviados à pasta privada do Drive Komekko e conferidos por metadados: [HTML offline (97.256 bytes)](https://drive.google.com/file/d/1M-sqKsLQPcuUkHaVxkr2gZyDhC5Pwsmm/view), [33 capturas Chromium (2.950.011 bytes)](https://drive.google.com/file/d/1XuPfATKTp-M17Kwk0FRzQFiGRmjyZP37/view), [4 capturas Firefox/WebKit e 2 JSON (209.952 bytes)](https://drive.google.com/file/d/1OX93XY7T_Hp-oiTBU0t2n_NkGxXgse4L/view).
- [x] O formulário de homologação visual D1–D6 está atualizado com a diferença correta entre perfil/proposições e as evidências CI anteriores; manter questões em aberto para decisão da Megalos. Uma prévia demonstrativa está tecnicamente apta a ser submetida a essa **avaliação**, não a voto institucional ou integração Academy.
- [ ] Verificar acesso/navegação real no Android e obter feedback visual Megalos. A `main` permanece no commit `81d0f55eb7772cbd1665df05cf05addb44db9723`, sem as correções mais recentes; não promover automaticamente. Sem alterações em Academy, dados reais, login ou banco de produção.
- [ ] Etapa 06 = **2/5**, Etapa 07 = **7/12** permanecem formalmente abertas: teste multimotor sintético não prova dispositivos físicos, leitor de tela, WCAG global nem aceite da Megalos.


## Auditoria editorial: texto humano e avisos proporcionais — 06/11/2026

- [x] Pedido explícito do responsável: eliminar o aspecto artificial e repetitivo de textos como `Resultados fictícios. A escolha é simulada somente nesta aba; nenhum voto é enviado à Academy.` A análise alcançou os textos públicos no `src/main.ts`, as fixtures e as expectativas da regressão. Não inferir autoria por IA somente pelo estilo da redação.
- [x] Commit funcional `62793d06349f8fa08b6010e2c02bca0d87ee8c1e`: **27 ajustes localizados de redação no `src/main.ts`**, com seis scripts de teste sincronizados (43 substituições na soma de código e testes), sem alterar CSS, regras, armazenamento, APIs, identidade, layout ou botões da referência Megalos. Votação: `Resultados de exemplo`, `Sua escolha`, `Opção selecionada. Você pode alterá-la.`; calendário: `Defina a data e a modalidade da deliberação.`; gerenciamento: `Alterações nesta página não afetam cadastros oficiais.`; Socii: remover `prévia local` de rótulos, preservar o aviso curto de convite não enviado; histórico: excluir explicação redundante sobre indicadores fictícios.
- [x] Persistem somente avisos necessários: marcador global discreto `DADOS FICTÍCIOS · PRÉVIA`, esclarecimento funcional no ponto de agendar/alterar dados, erro real de gravação e confirmação de que nenhum convite foi enviado. Laboratório `?demo=1` mantém documentação técnica própria e **não aparece na navegação normal**. Não disfarçar dados de exemplo como registros institucionais.
- [x] GitHub Actions `42246415733` para SHA `62793d0` = **SUCCESS**: laboratório PostgreSQL descartável, TypeScript/build, **51/51 Node** e **31/31 scripts Chromium**; `browser_preview_disclosure_v0117.py` passou nas quatro larguras, assim como calendário/retorno, metadados Socii, zoom 80/80, menu 8/8, recuperação e mensagens acessíveis. https://github.com/Otiosun/conferatus/actions/runs/42246415733
- [x] Firefox/WebKit do código revisado **3/3 + 3/3 PASS**, conforme log do job `cross-browser-lab` SUCCESS no SHA documental `9a09f47a8e8b50cf85522e232d1432aa376b2998` (mesmo HTML/CSS/TypeScript e testes funcionais do `62793d0`), GitHub Actions `42247360345`. Evidência privada arquivada e verificada no Drive: [Firefox/WebKit, ZIP 201.566 bytes](https://drive.google.com/file/d/1sR6ms4yyMlqXOxP3nKhIAxdD1mwIjf1M/view). O job `validate` do commit documental ainda estava em execução durante essa anotação; já existe execução completa SUCCESS para o commit funcional `62793d0`.
- [ ] D1b permanece pendente: o rótulo original `Iniciar uma Votação` continua, mas o controle abre um **agendamento**; a instrução breve explica essa função sem inventar regra. Aceite Megalos, teste Android físico, etapas 06=2/5 e 07=7/12 continuam pendentes. `main` e Academy preservadas.
- **Regra editorial para próximas telas:** texto curto, direto e próprio da ação; não repetir explicações técnicas de sessão, Academy, simulação ou prévia em cada bloco. Manter informação de segurança verdadeira, visível e proporcional no ponto em que importa. Mensagens de erro devem explicar o que falhou e como recuperar.

- [x] Artefatos exatos do build de código aprovado `62793d0`, gerados pela CI `42246415733`, arquivados no Drive Komekko e verificados por tamanho/pasta: [HTML offline ZIP 97.066 bytes](https://drive.google.com/file/d/1S6yuWRIxuvN0zWoynXEWI7IdkwKoJPfb/view) e [capturas Chromium ZIP 2.828.146 bytes](https://drive.google.com/file/d/1JXv7JBdQK75gcf2s7oPeWkk343jp-4xw/view). Essa aprovação não é aceite de design da Megalos nem integração Academy.


## Editor rico — fatia 1 validada (texto e quatro marcas) — 06/11/2026

- [x] A Megalos pediu editor de redação com fontes, tamanhos, cores, marca-texto, formatos, espaçamento, divisor, links, subscrito/sobrescrito e tabela opcional. Antes de ampliar controles, isolamos uma fatia compatível: **negrito, itálico, sublinhado e tachado** com botão `Formatar texto` opt-in. As outras ferramentas não estão concluídas. Nenhuma alteração nas decisões D1–D6, em regras de votação ou no fluxo institucional da Academy.
- [x] `src/domain/rich-text.ts`: `bodyRuns` opcional em `Draft` conserva o `body` de texto puro como fonte de verdade. Restauração/exportação validam correspondência exata de texto e marcas reconhecidas; nenhum HTML livre é armazenado, importado ou renderizado. Registros antigos sem `bodyRuns` continuam válidos. `src/domain/rich-editor.ts` extrai apenas marcas autorizadas do `contenteditable`.
- [x] `src/main.ts`: toolbar de quatro comandos sem trocar o editor padrão; formatação persistida ao salvar/reabrir/revisar/concluir; revisão formatada segura; confirmações Socii antigas são invalidadas se o conteúdo/marcas mudarem. CSS pequeno limitado à nova toolbar; zero dependências de runtime e sem reescrita de arquitetura.
- [x] Causa-raiz de regressão reproduzida e corrigida: `scripts/build-standalone.mjs` tinha lista fixa de módulos e omitiu `rich-text.js`/`rich-editor.js`, afetando funções antigas de revisão/exportação no HTML único. Corrigido no commit `1ed0895`, sem desativar testes antigos. Erro TS de guarda do último run corrigido no `8c54db2`.
- [x] O teste novo falhou inicialmente por uma **verificação antes da navegação assíncrona hash terminar**. Diagnóstico da CI `42328309413` comprovou `bodyRuns` com `bold` efetivamente gravado; `#/compose` já constava no URL mas o editor ainda não havia sido reconstruído. Espera explícita de tela + verificação de texto potencialmente malicioso formatado no teste, commit `b0269708b5120a5a9888a88f2621a27f4429f1c3`. Não mexer em regras de negócio para corrigir temporização de teste.
- [x] GitHub Actions `42328858970` SUCCESS no **commit exato b0269708**: PostgreSQL descartável PASS, `npm run build`/TypeScript, **53/53 Node**, **32/32 scripts Playwright Chromium**, incluindo `browser_rich_editor_v0163.py` PASS em 320, 390, 740 e 1280 px; valida rascunho formatado, revisão, conclusão, reabertura, escape do texto hostil. As 31 suítes antigas passaram, inclusive histórico, Socii, exportar/restaurar, zoom 80/80 e menu 8/8. https://github.com/Otiosun/conferatus/actions/runs/42328858970
- [x] Arquivos da CI exata preservados no Drive Komekko, ZIPs íntegros CRC e SHA-256 iguais aos do GitHub: [HTML offline ZIP 99.869 bytes](https://drive.google.com/file/d/1myw-CP_h2FmxXYozBAdOIlvcjNl8UEOQ/view) e [33 capturas de regressão ZIP 2.828.538 bytes](https://drive.google.com/file/d/1HHHshwRAQBksYenVzpCpEb6rtwBPgAb1/view). Revisão visual independente do HTML exato, em Chromium sintético: [editor com texto formatado 390 px](https://drive.google.com/file/d/1_xsP3AVnZ8L4Zto_58vRWqIg6z0io0vT/view) e [740 px](https://drive.google.com/file/d/1QSKktOQXxt2NVIHV5-jdMnA4b_Qd4qEj/view), sem overflow horizontal. São provas de laboratório, **não** reprodução aprovada pela Megalos.
- [ ] Validar esta primeira fatia também em Firefox/WebKit: este commit somente documental solicita o laboratório opcional via `[cross-browser]`; registrar o resultado real antes de considerar prova multimotor. A tentativa de recarga por HTTP local falhou por bloqueio de acesso à origem loopback no ambiente, **não é teste de persistência após reload**. Preservar limite nas conclusões.
- [ ] Próximas fatias do editor: Aptos/fonte e tamanho (verificar licença/disponibilidade), cor/marca-texto, alinhamento/recuos e altura de linha, divisor, link seguro, subscrito/sobrescrito e tabela se viável; testes de edição móvel real, colagem, teclado, leitor de tela, persistência e compatibilidade com Socii. Não marcar o editor completo, a Etapa 04 ou a Etapa 07 por este avanço.
- [ ] “Página de votação” mencionada pela Megalos ainda requer uma delimitação: tela para votar vs criar/administrar votação. Seis formulários laboratoriais existentes não equivalem à página integrada, nem à votação institucional. D1–D6, grafia e aprovação Megalos continuam pendentes.
- [x] Main `81d0f55eb7772cbd1665df05cf05addb44db9723` preservada; sem deploy institucional, conta, bancos, Academy ou alteração no site principal. Etapas formais **04=17/22, 06=2/5, 07=7/12** inalteradas.


## Editor rico — fatia 2: fontes, tamanhos e cores (06/11/2026)

- [x] Complementar a fatia 1 com **fontes Aptos/Arial/Georgia**, tamanhos `12/16/18/24/30 px`, seleção de cor hexadecimal e marca-texto por cor. Aptos é apenas uma preferência CSS com fallback Segoe UI/sans-serif; nenhum arquivo de fonte licenciado ou dependência foi incorporado. Controles visíveis só após `Formatar texto` para preservar composição antiga.
- [x] Persistência segura: `body` simples continua fonte de verdade e `bodyRuns` opcional passou a aceitar campos tipados `font`, `size`, `color`, `highlight`. Validação rejeita fonte/tamanho ausente da whitelist, cor que não seja `#RRGGBB`, propriedades extras e texto divergente; as tags de edição transitórias `FONT/SPAN` viram runs seguros. Exibição só interpola tags permitidas e CSS de valores fixos/validados; importação/exportação preserva apenas os campos documentados e mantém rascunhos antigos legíveis.
- [x] Primeira execução `42331572545` detectou quatro erros do TypeScript estrito em `src/main.ts` (tipo do `EventTarget` e lookup de Record com valor indefinido). Corrigidos no commit `f931fa653ef672a52a552524fa02ae09e67c668d`, sem alterar regra de negócio ou relaxar o TypeScript.
- [x] CI `42331681506` no **SHA exato `f931fa6` SUCCESS**: PostgreSQL **somente laboratório** SUCCESS, build/typecheck, **54/54 Node**, **33/33 scripts Chromium**. Novo `tests/browser_rich_typography_v0164.py` PASS em 320/390/740/1280 px: fonte Aptos, 24 px, cor `#123abc`, realce `#ffef99`, salvar/reabrir/revisar/concluir; 32 suítes antigas sem regressão, incluindo arquivos, Socii, navegação, texto longo e zoom/reflow. https://github.com/Otiosun/conferatus/actions/runs/42331681506
- [x] Commit somente teste `0d50691367f58fc0e8d99cd43fa4baef892a1b7c` com `[cross-browser]`: `cross-browser-lab` SUCCESS na CI `42332215573`. **Firefox 3/3 smoke + 4/4 tipografia, WebKit 3/3 smoke + 4/4 tipografia**; 54/54 Node no job. Os mesmos quatro tamanhos e jornada de formatação foram executados em ambos os motores. O job de validação Chromium do commit documental ainda estava em andamento na anotação; já existe `validate` completo SUCCESS para o commit funcional sem alterações de produto desde então. https://github.com/Otiosun/conferatus/actions/runs/42332215573
- [x] Evidências da CI guardadas no Drive Komekko e verificadas CRC/SHA: [HTML aprovado 101.587 bytes](https://drive.google.com/file/d/1J9zpMC9ow2sZOK3yGzkNWDMxWbhFoskA/view), [33 capturas Chromium 2.859.982 bytes](https://drive.google.com/file/d/1xL95qQ4gBZaRJGfRTW7LC-iQMKvoW17d/view), [Firefox/WebKit 202.071 bytes (8 itens)](https://drive.google.com/file/d/1q-61lN28GsY5KxRBWoFh30MZl_qy7jwC/view). Imagens do editor com realce efetivamente visível: [390 px](https://drive.google.com/file/d/1PrnMptpNnHFmTfVlakweFfyQfzkttB5j/view), [740 px](https://drive.google.com/file/d/12IrkObCrl01b5oWtnru3m-INpPqSSP3t/view); sem overflow horizontal e sem erros JS nesses dois ensaios offline.
- [ ] **Não declarar o editor completo**: ainda faltam alinhamento/recuos, altura e espaçamento de linha, linha divisória, hyperlinks, subscrito/sobrescrito e tabela opcional, além de recuperação de sessão em HTTP real, dispositivos físicos, leitores de tela e avaliação de fidelidade pela Megalos.
- [ ] Pergunta pendente à Megalos sobre o que falta na **página de votação** (participação do eleitor vs criação/administração). As seis modalidades do laboratório `?demo=1` não substituem experiência final nem voto da Academy. D1–D6 e marca também aguardam validação.
- [x] `main` `81d0f55eb7772cbd1665df05cf05addb44db9723` preservada; nenhum banco real, login, voto oficial, integração Academy ou release de produção mudou. Etapas **04=17/22, 06=2/5, 07=7/12** continuam como oficialmente registradas.
