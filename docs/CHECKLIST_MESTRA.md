# CONFERATUS — Checklist-mestra de execução

Atualização de referência: 01/11/2026
Responsável pelo acompanhamento: desenvolvimento CONFERATUS
Status verificado: `main` está em v0.10.5 (`4b24459`, check Cloudflare aprovado). O preview isolado `preview/v0.10.6-calendar-form-state` contém a correção de retenção do agendamento (Cloudflare aprovado em `3423ba4`; regressão Playwright adicionada, execução de navegador pendente). Todos os fluxos permanecem demonstrativos; a revisão final das telas continua pendente.

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
- [ ] Finalizar redação, revisão, confirmação e estados de proposições.
- [x] Aproximar folha de revisão e confirmação de proposição dos modelos `1001930222.jpg` e `1001930223.jpg` (preview v0.10.10; opções e regras preservadas; aprovado em quatro larguras).
- [x] Corrigir nova redação independente e salvar/retomar rascunho incompleto na prévia local (v0.10.1; testes em 320/390/740/1280 px).
- [x] Mostrar andamento de conclusão de Socii (0/2 → 1/2 → 2/2) na prévia, sem representar convites como reais.
- [ ] Consolidar a colaboração Socii e seus estados de conclusão.
- [x] Corrigir integridade de versões na prévia: alteração de título/texto reinicia confirmações anteriores de autoria e Socii sem remover participantes; texto idêntico preserva progresso; distinguir pendência de autoria/Socii (v0.10.13, teste de falha antes/depois).
- [x] Aproximar o editor Socii do modelo `1001930224.jpg` com faixa de participantes vinculados, identificação de prévia local e progresso 0/2–2/2, sem tempo fictício ou colaboração remota (v0.10.12; quatro larguras e regressões).
- [x] Aproximar o editor de proposições do modelo de redação minimalista, preservando título editável, rascunho e botões (v0.10.5; comparação visual local).
- [ ] Conferir as novas telas com as seis imagens e o vídeo da Megalos.
- [x] Alinhar perfil, indicadores, histórico de proposições e Socii com a referência `1001930225.jpg`; reusar componente de membro, filtrar proposições por autor e manter rascunhos identificados como dados locais (preview v0.10.11, verificação em quatro larguras).
- [x] Ajustar apresentação do formulário de agendamento para o painel azul da referência 1001930226.jpg, mantendo campos e regras existentes (v0.10.8; comparação local e regressão visual funcional).
- [x] Executar e validar em navegador a retenção de campos de agendamento durante a navegação do calendário (preview v0.10.6; Chromium em 320, 390, 740 e 1280 px; ainda não promovido a `main`).
- [x] Manter o botão Hoje e a marcação do dia consistentes após a meia-noite (preview v0.10.7; Chromium com relógio controlado em 390 e 740 px).
**Estado:** a `main` permaneceu na v0.10.5 (`4b24459`) durante a retomada. A branch de prévia avança até v0.10.11, com ajustes visuais e funcionais testados em quatro larguras; a integração e as regras institucionais definitivas continuam pendentes.
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
