# CONFERATUS — Kit de decisões da Megalos | v0.10.23 | 01/11/2026

> **Não é aprovação nem mudança de interface.** Seis imagens originais (1001930221.jpg a 1001930226.jpg; 710 × 1536) foram comparadas com seis capturas NOVAS do build local v0.10.22 no Chromium, viewport 390 px. O vídeo 1001930216.mp4 foi anteriormente amostrado na auditoria v0.10.17, não revisto integralmente nesta rodada. A versão continua demonstrativa. **[PDF visual de 7 páginas no Komekko](https://drive.google.com/file/d/1M5NN_tT4VQ_-Vp7YF8PU48kzj4DT3Jz-/view).**

## Questões objetivas de aprovação

### D1 — Painel azul / calendário — imagem 0221
**Original:** painel azul grande com “CALENDÁRIO”; não há grade mensal visível naquele quadro; botão “Iniciar uma Votação”; lista com programação expandida. **Prévia:** grade mensal interativa dentro do painel azul; mudança de mês e dia; botão com texto original e aviso explícito de que apenas agenda, não inicia votação.
**Decidir:** (A) grade sempre visível; (B) painel compacto, grade ao toque; (C) outra instrução. **D1b:** manter “Iniciar uma Votação” com aviso ou substituir por texto que reflita o agendamento? Não alterar a terminologia sem validação.

### D2 — Local do agendamento — imagem 0226
**Original:** painel azul de agendamento na parte inferior do perfil com seleção de proposição, seção, duas datas e tipo. **Prévia:** formulário funcional de prévia na rota Calendário, contendo também título e descrição objetiva.
**Decidir:** (A) manter no calendário; (B) também acessível pelo perfil compartilhando o mesmo formulário; (C) deslocar para o perfil. Não inferir do quadro a rota completa, autorização ou integração.

### D3 — Variantes de confirmação — imagens 0222 e 0223
**Original 0222:** folha inferior com campos seção/tipo e ações Cancelar e Confirmar. **Original 0223:** somente Confirmar na porção visível. **Prévia:** folha com Cancelar/Confirmar.
**Decidir:** qual estado/etapa/papel distingue as duas variantes? A ausência de Cancelar na imagem 0223 não basta para apagá-lo da interface.

### D4 — Socii na revisão e duração — imagens 0222 e 0224
**Original:** barra escura de participantes com referência a 127 horas no editor e na revisão da imagem 0222. **Prévia:** barra de participantes e progresso **local** no editor, mas a captura **0222_review_socii.png** mostra que a barra **não aparece na revisão**. A prévia não exibe duração porque a regra de contagem não foi definida.
**Decidir:** barra também na revisão, só no editor, ou conforme estado? O que mede o tempo: prazo, tempo desde convite ou participação? Não inventar contador sem regra.

### D5 — Ações do editor — imagem 0224
**Original:** Concluir e Voltar, área ampla para texto, cabeçalho de Socii. **Prévia:** Concluir redação, Salvar rascunho e Voltar; salvar é funcional somente na sessão local.
**Decidir:** manter botão Salvar rascunho visível, reposicioná-lo ou aprovar outro mecanismo real de persistência. Sem esconder risco de perda de dados.

### D6 — Perfil/histórico — imagem 0225
**Original:** faixa azul, avatar, cinco métricas, duas abas, lista de proposições e painel inferior Socii. **Prévia:** blocos correspondentes, porém diferença de densidade, tipografia, espaçamento e conteúdo fictício.
**Decidir:** aprovar a hierarquia, altura e densidade em celular; se não, indicar blocos a corrigir. Não confundir contagens e nomes fictícios com informações reais.

## Matriz auditável de capturas (v0.10.22, 390 px)

| Original Megalos | Captura nova | Decisão | Situação |
| --- | --- | --- | --- |
| 1001930221.jpg | 0221_calendar.png | D1/D1b | Aguardando Megalos |
| 1001930222.jpg | 0222_review_socii.png | D3/D4 | Aguardando Megalos |
| 1001930223.jpg | 0223_review_simple.png | D3 | Aguardando Megalos |
| 1001930224.jpg | 0224_editor.png | D4/D5 | Aguardando Megalos |
| 1001930225.jpg | 0225_profile.png | D6 | Aguardando Megalos |
| 1001930226.jpg | 0226_schedule.png | D2 | Aguardando Megalos |

As imagens originais são de Megalos; as seis capturas foram produzidas no Chromium com HTML offline v0.10.22, sem erro JS ou overflow a 390 px. As imagens foram incluídas no PDF Komekko, não num repositório público, conforme proteção de material original. O vídeo não está incluído no PDF. Não há comparação pixel a pixel nem aceite formal.

## Gate de retomada

1. Registrar respostas da Megalos D1 a D6 com autor/data, e anexar referência nova quando existir.
2. Converter somente decisões confirmadas em implementação pequena, ramo **preview** novo, sem alterar `main`.
3. Para UI, capturar em 390 px, testar teclado/acessibilidade e regressões pertinentes; submeter para avaliação.
4. Somente após aceite visual explícito marcar na checklist a fidelidade final.
5. Regras reais de votação, convite Socii, autenticação Academy e persistência compartilhada seguem bloqueadas sem especificação.

**Seis etapas inalteradas:** 01=4/5; 02=0/4; 03=1/5; **04=17/22 ativa**; 05=0/4; 06=0/5. Não confundir o kit de decisão com finalização de etapa. **Limites de execução:** `npm run build` aprovou TypeScript, HTML offline e 18/18 testes Node da v0.10.22. As capturas da v0.10.22 foram feitas em 390 px, sem erros JS ou overflow; **não foram executadas 22 suítes Playwright nesta rodada docs-only**, ainda que tenham passado na rodada anterior. Ausência de `lint` segue registrada.

**Arquivo distribuível:** [PDF de comparação no Drive Komekko](https://drive.google.com/file/d/1M5NN_tT4VQ_-Vp7YF8PU48kzj4DT3Jz-/view). Documento original da auditoria: `docs/AUDITORIA_VISUAL_V0117_2026-11-01.md`.
