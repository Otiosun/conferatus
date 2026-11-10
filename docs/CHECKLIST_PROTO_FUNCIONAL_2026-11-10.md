# CONFFRATUS — Checklist de conversão para protótipo funcional
10/11/2026 · Posição inicial: branch preview/v0.10.60-six-vote-forms · HEAD 5e9786c27cfce56b1a03bceed961253de18d2c5d

## Objetivo e regra de leitura
Entregar a EXPERIÊNCIA FUNCIONAL do Conffratus: site utilizável como produto em desenvolvimento, com dados inteiramente fictícios, sem laboratório ou tutoriais técnicos na navegação comum. Não equivale a votação, autenticação, convite Socii, assinatura ou histórico oficial da Academy.

Esta checklist é a NOVA fila de consolidação de UX/produto e não altera retroativamente 43/57 critérios históricos de engenharia. Um mecanismo tecnicamente testado pode continuar com [ ] aqui se sua EXPERIÊNCIA de produto ainda não foi aceita. Todos os [ ] abaixo são pendentes de aceite, não alegação de que o código inexiste.

Fonte confirmada no código: src/main.ts tem dois fluxos de votação distintos: o botão Participar na descrição da votação inicial (data-action toggle-demo) e o botão Abrir formulário de votação (data-action toggle-voting-forms) com escolha entre seis modalidades. Programações locais já possuem método, opções e vínculo com proposição (data-preview-schedule), mas exibem Simular voto nesta programação. Socii tem ação Simular conclusão de participante na navegação normal. As seis modalidades e os vínculos da sessão já passaram testes; o problema prioritário é consolidar a experiência, sem reescrever a lógica.

## P0 — A. Votação integrada ao produto (PRIMEIRO LOTE)
- [x] PF-01 Entrada única: clicar Participar em uma deliberação aberta leva diretamente ao formulário dessa deliberação; nenhuma etapa de laboratório obrigatória.
- [x] PF-02 Contexto inequívoco: título, seção, proposição, modalidade e opções reais da deliberação fictícia são exibidos e correspondem à programação selecionada.
- [x] PF-03 Modalidade definida pela deliberação, não escolhida pelo eleitor: binária, nominal, ordenada, aprovação, escalar e cumulativa mantêm suas particularidades e guardas existentes.
- [x] PF-04 Mover seleção global de modalidades e controles Nova amostra/Limpar amostras para ferramentas técnicas isoladas; nada de opção técnica na navegação comum.
- [x] PF-05 Unificar votos do exemplo inicial e votações programadas na mesma estrutura de UI; não manter dois produtos concorrentes com estados conflitantes.
- [ ] PF-06 Estados de interface: aberta, encerrada, cancelada, indisponível, preenchimento inválido, confirmação e retorno; nenhum botão que pareça acionável mas não opere.
- [x] PF-07 Comprovante local corresponde exatamente à escolha, sem alegar voto oficial, vencedor, quórum, dupla participação institucional ou gravação remota.
- [x] PF-08 Totais históricos de exemplo não mudam silenciosamente com escolhas locais nem se confundem com amostras anônimas.
- [x] PF-09 Rascunho de voto preservado enquanto navegável; reset, troca contextual, cancelamento e reentrada não vazam escolhas para outra deliberação.
- [ ] PF-10 Percurso completo de cada método validado com casos inválidos e recibo, teclado, celular e abertura do deploy real; manter os testes já existentes, reduzindo duplicação.
Critério de aceite A: pessoa consegue entrar, votar, entender o que aconteceu e voltar, sem saber que seis modalidades ou um laboratório existem por baixo.

## P0 — B. Proposição, revisão e Socii naturais (SEGUNDO LOTE)
- [ ] PF-11 Redigir, salvar, retomar e revisar em um percurso contínuo; nenhuma perda de dados na navegação, nos erros ou no retorno.
- [ ] PF-12 Mensagens de conclusão e persistência verdadeiras: local apenas = local apenas; falha de armazenamento sinalizada com recuperação possível.
- [ ] PF-13 Revisão apresenta título, texto, seção, tipo (PDR/PR/Ofício), participantes e próximos passos, sem controles internos de teste.
- [ ] PF-14 Colaboração Socii: convite e progresso demonstrativos integrados à proposição; evitar a expressão Simular conclusão repetida como ação do usuário final. Não fingir convite remoto ou autorização de outra pessoa.
- [ ] PF-15 Se for preciso demonstrar como outro ator fictício concluiria, oferecer contexto de revisão/representação de membro claramente identificado como PRÉVIA, separado de autenticação. Sem qualquer capacidade real de assumir identidade.
- [ ] PF-16 Edição material da proposição invalida confirmações anteriores; 0/N→N/N, estados pendentes e foco após atualização continuam corretos.
Critério de aceite B: autor consegue ir de rascunho a proposição pronta e vê Socii coerentemente, sem receber uma ferramenta de QA no lugar do produto.

## P0 — C. Calendário, deliberações e vínculos (TERCEIRO LOTE)
- [ ] PF-17 Programação nasce de proposição elegível, tem seção, título, descrição objetiva, datas, tipo, modalidade e alternativas corretas, reaproveitando as validações atuais.
- [ ] PF-18 Calendário mostra somente programações ativas nas consultas pertinentes; canceladas ficam no histórico e não aparecem como ativas.
- [ ] PF-19 A programação abre a votação contextual pela ação natural Participar, em lugar de Simular voto nesta programação.
- [ ] PF-20 Proposição → programação → votação → retorno contextual funcionam em celular sem perder estado nem permitir vínculos quebrados.
- [ ] PF-21 Não inventar permissões, procedimentos de início/encerramento ou quórum; estados com regras indefinidas ficam sob contrato demonstrativo explícito.
Critério de aceite C: a agenda parece um calendário deliberativo completo, não um configurador de demonstrações.

## P1 — D. Perfis, navegação e históricos
- [ ] PF-22 Perfil único: indicadores Votos/PDR/PR/Ofício/Socii, histórico, proposições e atalhos consistentes, sem registro fictício ser apresentado como fato oficial.
- [ ] PF-23 Fluxos de autoria e referências funcionam entre perfil, histórico, editor e calendário sem links mortos; outros perfis não recebem autoria da sessão.
- [ ] PF-24 Menu, Voltar, fechar, cancelar e reabrir têm nomes e comportamentos coerentes. Controles técnicos invisíveis na interface principal.
- [ ] PF-25 Estado vazio, dado corrompido, nome/texto extenso e sessão indisponível são legíveis e recuperáveis; preservar o trabalho feito.
Critério de aceite D: alguém navega todas as seções sem instruções técnicas nem diferença de linguagem entre as telas.

## P1 — E. Fidelidade e acabamento sem reinvenção
- [ ] PF-26 Revisar o painel azul grande e aparentemente vazio observado no Android real do responsável; identificar conteúdo/propósito no código e comparar com referências antes de redesenhar.
- [ ] PF-27 Alinhar composição, densidade, hierarquia, tipografia, espaço e estados à referência Megalos. Não adotar paleta/estilo pessoal.
- [ ] PF-28 Deliberações D1/D1b (calendário e rótulo de iniciar), D2 (local do agendamento), D3 (variante de confirmar), D4 (barra Socii e 127 horas), D5 (salvar rascunho), D6 (perfil). Aguardar respostas explícitas para decisões não inferíveis do material.
- [ ] PF-29 Corrigir a linguagem de laboratório nos fluxos comuns mantendo UM aviso claro e discreto no nível do ambiente: Prévia com dados fictícios; nenhuma operação enviada à Academy. Não esconder nem falsear a limitação.
- [ ] PF-30 Manter CONFFRATUS na prévia até decisão formal de grafia com Megalos; preserve imagens originais com CONFERATUS sem reescrever fontes históricas.
Critério de aceite E: aparência comparável às seis imagens/vídeo e UX profissional; onde existe ambiguidade, decisão registrada, não inventada.

## P1 — F. Qualidade, entrega e regras máximas
- [ ] PF-31 Investigar soluções oficiais e código existente ANTES de mudança material (regra 21): preferir HTML/TS/CSS nativos, evitar dependências, frameworks e infraestrutura nova; registrar por que a solução é a menor segura.
- [ ] PF-32 Acessibilidade: foco, ordem, rótulos, mensagens, estados dinâmicos e controles substituídos; regressão de teclado e leitor de tela real quando disponível.
- [ ] PF-33 Responsividade: 280/320/390/740/1280, texto 200%, reflow equivalente a 400%, aparelho Android físico, zoom nativo, teclado/safe-area e outras engines quando possíveis; documentar limites em vez de certificar sem teste.
- [ ] PF-34 Integridade e privacidade: dados sintéticos, nenhuma credencial no bundle, nada que simule autorização real; não misturar recibos locais com históricos fictícios.
- [ ] PF-35 Build e regressão: TypeScript strict, Node, Playwright por jornada, inspeção visual e prova do deploy efetivamente aberto em celular; verificar resultados do HEAD exato, sem contar CI skipped como sucesso.
- [ ] PF-36 Diagnosticar GitHub Actions (runner sem steps e checks skipped) sem aumentar cobranças, tornar repo público ou disparar reruns descontrolados; Cloudflare SUCCESS não substitui CI.
- [ ] PF-37 Gate de homologação: demonstrar jornada completa a Megalos; registrar resposta D1–D6 e aprovação de interface separadamente do contrato Academy.
- [ ] PF-38 Publicação: branch de prévia isolada, diff revisado, instruções e rollback; não alterar main/domínio principal/Academy/PM2 sem autorização expressa.

## Sequência de execução disciplinada
1. Primeiro implementar e TESTAR PF-01 a PF-10, com foco em transformar Participar no único caminho de votação e preservar as seis regras de UI existentes.
2. Em seguida PF-11 a PF-21, unificar redação/Socii/calendário.
3. Depois PF-22 a PF-30, navegação, cópia e fidelidade Megalos.
4. Em paralelo, PF-31 a PF-36 como gates de cada alteração; no final PF-37/PF-38.
5. Não abrir checkpoints cosméticos. Encerrar um lote apenas com comportamento comprovado, testes do código executado e lista de regressões. Registrar FEITO / TESTADO / PUBLICADO / PENDENTE.

## O que NÃO faremos
Não refazer em React, adicionar login próprio, backend ou base de votos oficiais, inventar peso/quórum/resultado de eleições, aprovar escolhas da Megalos unilateralmente, tornar repo público, alterar main/produção, PM2 ou Academy, ou apagar histórico sob pretexto de UX. Nunca ocultar que a prévia não grava votos reais.

## Referências e rastreabilidade
GitHub privado: Otiosun/conferatus, AGENTS.md (21 regras), docs/CHECKLIST_MESTRA.md, docs/KIT_DECISOES_MEGALOS_V0123_2026-11-01.md, docs/DEMO_GUIDE.md, src/main.ts.
W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/ ; APG modal focus: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
GOV.UK phase-banner (exemplo de identificação honesta de ambiente): https://design-system.service.gov.uk/components/phase-banner/
Esta checklist não afirma aprovação desses órgãos nem certificação WCAG.
## Lote inicial implementado — votação contextual (10/11/2026)

**Fonte:** branch preview/v0.10.60-six-vote-forms, aplicação TypeScript original, sem framework e sem tocar main/produção. **PF-01 a PF-05 [x] no escopo da prévia fictícia**: Participar abre diretamente o mesmo formulário que a agenda; a votação inicial usa suas opções mensais/quinzenais, tratadas como escolha única nominal; o formulário agendado mostra título/seção/proposição e método fixado pela programação; seleção global, resumo de amostras e botões de laboratório saíram da interface principal. O antigo laboratório de seis modos sobrevive em ?demo=1 para regressões. O botão de programações agora diz Participar nesta votação. O caminho legado por escolha simples fica restrito ao modo técnico; a interface normal não mistura os totais históricos fictícios com as escolhas feitas nesta aba.

**Verificações executadas no bundle JavaScript offline equivalente, antes de publicar TypeScript:** testes de entrada do voto inicial com escolha inválida, escolha nominal, recibo correto, alterar escolha e voltar em 320/390/740/1280px (4/4 PASS); seis métodos de programação com recusa de voto inválido e comprovante (24/24 combinações) PASS; vínculos entre quatro seções e seis modalidades (24/24) PASS; jornada completa de Socii→calendário→voto (4/4 larguras) PASS; smoke técnico do laboratório avançado (4/4 larguras) PASS; matriz de foco de 95 transições (5 larguras) PASS. Arquivos de regressão da branch adaptados para o comportamento novo: v0190, v0192, v0194, v0195, v0196, v0200. **Estas provas locais utilizaram o HTML do commit anterior com transformação equivalente à alteração TypeScript; a CI remota do HEAD ainda não foi executada com sucesso. Não descrever como build local do HEAD.** Cloudflare Pages compila e publica a branch; confirmação final por check SHA.

**Permanecem ABERTOS no lote de votação:** PF-06 estado completo, PF-07 comprovação aprofundada, PF-08 não mistura em todos os caminhos, PF-09 drafts em navegação e troca de contexto, PF-10 aceite visual/hardware Android e engines. A ação de alterar escolha limpa a única participação temporária do respectivo escopo antes de nova confirmação. Nenhuma escolha vai à Academy. O painel azul do cabeçalho não foi redesenhado; esse assunto permanece PF-26 e depende de análise/ref. Megalos.

**Métrica independente:** checklist funcional **5/38** (somente entregas de UX testadas em ambiente local). Checklist histórica de engenharia **43/57** inalterada. PF-06 a PF-38 que não foram listados como concluídos continuam pendentes. Não marcar homologação Megalos nem integração Academy.

## Lote seguinte — comprovantes, históricos e isolamento (10/11/2026)

**Falha real de PF-06 reproduzida antes da correção em quatro larguras:** cancelar uma programação com rascunho de voto aberto removia `previewScheduleId`, mas mantinha `votingFormsOpen=true`. Ao retornar à votação, a página apresentava **três alternativas genéricas** que não pertenciam à programação cancelada. Havia risco de registrar uma amostra no contexto errado. Correção em `src/main.ts`: fechamento do formulário ativo na confirmação de cancelamento, limpeza de recibo/draft/identificador e aviso acessível `role="status"`; barreira adicional quando o contexto agendado se torna inválido por outros motivos. O usuário pode iniciar a votação inicial normalmente, com formulário próprio e sem escolhas herdadas.

**Regressão publicada:** `tests/browser_cancelled_vote_context_v0201.py` cobre o bug (4/4 larguras) e `tests/browser_product_vote_isolation_v0202.py` cobre preservação ao navegar dentro do mesmo contexto, isolamento ao trocar de programação, recibos da alternativa nominal, rejeição de escolha vazia, reinício e totais históricos imutáveis (4/4). Ambos adicionados ao workflow da prévia. Suítes anteriores das 6 modalidades (`v0194`) e 24 combinações de seções (`v0192`) continuam protegendo os modos e vínculos. Investigação de status dinâmico: W3C WAI SC 4.1.3 e ARIA22 recomendam mensagem com papel programaticamente determinável, sem mover foco só para notificá-la.

**Aprovação delimitada:** PF-07, PF-08 e PF-09 [x] **no comportamento fictício local** demonstrado, agora **8/38**. Não equivale a recibo oficial, login, apuração real, persistência remota ou proteção de uma votação institucional. **PF-06 permanece [ ]** até inspecionar também encerramento/indisponibilidade por todos os caminhos e **PF-10 permanece [ ]** até teste do deploy em dispositivo físico e aceitação de UX.

**Precisão da execução:** as reproduções e asserções locais foram feitas num HTML compilado anterior com transformação JavaScript equivalente ao novo TypeScript, não em build local compilado do HEAD. Cloudflare Pages compilou a branch; a CI GitHub `validate` e `cross-browser-lab` continuam `skipped`, `postgres-lab` continua `failure`. Não considerar a CI integral aprovada. Cópia de testes/artefato local no Komekko: https://drive.google.com/file/d/1LF7Adb1pGtqkniUvOuVEsHhUuoQCoc1f/view (SHA256 c5605e1f89053ec35d1ca148fa557ad18ec75c261008bee14cc5edbb6c5cd09a). Branch de prévia privada, main e produção intocadas. Histórico 43/57 ainda separado.

## CP156 — Retorno contextual da agenda (10/11/2026)

Branch privada de prévia: commit `09b774abab0e9899d0e2845721a93a6fe2a138bd`, `src/main.ts` + teste novo `tests/browser_schedule_return_v0203.py` + decisão `docs/decisions/2026-11-10-cp156-calendar-return.md`. O formulário agendado agora retorna à programação de origem; se a programação ficar cancelada/indisponível, a página preserva o título e o contexto sem apresentar a votação inicial ou um formulário genérico. A saída do cancelamento retorna ao histórico no calendário; a votação inicial mantém seu caminho independente.

**Situação da prova:** revisão textual do patch confirmada e teste adicionado ao workflow; execução do novo teste, build local TypeScript, outras engines e Android físico **ainda pendentes**. Na consulta do SHA `09b774abab0e9899d0e2845721a93a6fe2a138bd`, Cloudflare Pages estava em andamento; `validate` e `cross-browser-lab` estavam `skipped`, `postgres-lab` estava `failure`. Verificar status novamente no HEAD após este commit. **PF-06 [ ] e PF-10 [ ]**, 8/38 funcional; 43/57 histórica. Nenhuma alteração em `main`, produção principal ou Academy.

## CP157 — Reconciliação das regressões e Socii natural (10/11/2026)

**Correções de testes:** `v0201` foi adequado ao retorno contextual cancelado do CP156, preservando prova de que não aparecem formulário nem resultados genéricos. `v0203` foi corrigido para preservar o identificador da programação durante o teste de cancelamento, em vez de apagá-lo antes. Ambos continuam na suíte da prévia, sem descartá-los.

**Avanço de PF-14/PF-15, ainda não aceite:** a página principal substitui “Simular conclusão de [participante]” por uma etapa de Socii fictício com declaração de escopo local, sem acesso ou notificação a contas de terceiros; “Convidar para Socii” passou a “Adicionar ao Socii”, pois a prévia não envia convites. O mecanismo de conclusão e os contratos do Socii existentes foram reutilizados. Novo `v0204` cobre a continuidade da conclusão da proposição para o calendário. Decisão técnica: `docs/decisions/2026-11-10-cp157-socii-product-regressions.md`.

**Status comprovado:** `dd4b2096a22452146d6444f7f6ea14ebef400962` foi commitado na branch privada; check Cloudflare Pages = SUCCESS, validate = SKIPPED, cross-browser-lab = SKIPPED, postgres-lab = FAILURE. O build remoto não equivale à execução dos testes Playwright novos nem à inspeção no Android físico. `main` inalterada. **Não marcar PF-06, PF-10, PF-14, PF-15 ou PF-11–21 como concluídos:** contagem funcional permanece **8/38**, histórica **43/57**. Próximo lote: executar evidências do HEAD exato quando houver runtime e validar PF-11/PF-12 sem novas regras Academy.
