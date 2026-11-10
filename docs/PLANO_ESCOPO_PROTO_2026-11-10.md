# CONFFRATUS — Matriz de escopo e fechamento do protótipo (10/11/2026)

**Fonte de verdade:** `docs/CHECKLIST_MESTRA.md`, `AGENTS.md`, testes e código da branch. Esta matriz NÃO substitui o histórico nem autoriza `main`, pagamentos, login próprio ou votos reais.

## Regra de interpretação

**Nosso entregável = protótipo inteiramente funcional com pessoas/votos/proposições fictícias.** Academy responde por autenticação, cadastro real, autorização institucional, banco transacional e sistema central. Megalos responde por decisões de aparência/comportamento ainda não determinadas nos seis modelos e vídeo. Para não esconder progresso, mantemos duas métricas distintas: **checklist histórica (57 critérios)** e **fila realmente executável de protótipo**, sem atribuir porcentagem artificial aos dois escopos.

Auditoria da lista histórica em 10/11: **24 critérios abertos** na contagem anterior 33/57. Abaixo, todos os 24, preservando a ordem e o texto central.

Legenda: **C** = critério já atendido e revalidado nesta rodada no escopo explícito do protótipo; **P** = fechar internamente com QA e contrato demonstrativo; **M** = decisão/aceite visual Megalos necessária; **A** = responsabilidade/integração real Academy, fora do escopo de implementar; **H** = critério misto que exige separar entrega de protótipo de liberação institucional. Um P pode ter código parcial ou completo, mas **não é [x] enquanto o aceite integral não estiver provado**.

| ID | Critério histórico aberto em 33/57 | Faixa | Situação concreta / saída para fechar |
|---|---|:---:|---|
| 01.05 | Confirmar grafia CONFERATUS/CONFFRATUS | M | Perguntar à Megalos, preservar ambas as fontes e grafia de prévia até resposta |
| 02.01 | Consolidar modelo de votação e estados | P | Seis modalidades já funcionam; consolidar estados e fluxos de demonstração numa especificação e testar transições/erros, sem regras institucionais |
| 02.02 | Associar deliberações, seções e proposições | C | **Concluído apenas na prévia fictícia:** 24/24 combinações de 4 seções × 6 modalidades, método, opções, proposição e calendário corretos; contratos reais Academy fora do escopo |
| 02.03 | Implementar registro institucional quando regras confirmadas | A | Backend/eleição real é da Academy, não declarar implementado nem bloquear protótipo |
| 02.04 | Verificar fluxo fictício e depois integrado oficial | H | Dividir evidência: jornada fictícia já passou, teste de integração não é responsabilidade direta nem pode ser simulado como aprovado |
| 03.01 | Consolidar históricos pessoais e institucionais | P | Validar separação dos registros fictícios históricos e dos novos registros locais, inclusive vínculos e rotas |
| 03.02 | Preservar registros após mudança de cargo/rebaixamento | C | JS preserva dados; testes de regra e navegador em 320/390/740/1280 mostram histórico/contadores mantidos; não é banco oficial |
| 03.03 | Revisar métricas Votos/PDR/PR/Ofício/Socii conforme modelos | M | Cinco métricas existem; falta revisão/aceite visual de D6 |
| 03.05 | Integrar listas de proposições/deliberações aos perfis | P | Existe parte do cruzamento local; provar todos os destinos, estados e retorno sem vínculos inertes |
| 04.02 | Finalizar calendário e programações com fidelidade | M | Depende D1/D1b, confirmar disposição com Megalos |
| 04.05 | Finalizar agendamento, campos e integridade | P | A UI e validações de sessão já existem; fechar como protótipo, explicitar pendências das regras reais |
| 04.09 | Finalizar redação, revisão, confirmação e estados | P | Construção ampla já testada; verificar transições completas e rascunho, decidir variantes D3 com Megalos separadamente |
| 04.13 | Consolidar Socii e estados de conclusão | P | Progresso 0/2→2/2, guardas e autoria demonstrativos; validar versão, associação, retorno e mensagens, sem convite remoto |
| 04.19 | Comparar telas com seis imagens e vídeo | M | Comparações e PDF existem, mas o aceite final dos desvios requer Megalos |
| 05.03 | Deixar login para equipe Academy conforme acordado | C | Delegação acordada explicitamente; `AGENTS.md` define fronteira, `academy-identity.test.mjs` prova adaptador sem credencial |
| 05.04 | Validar fluxos integrados quando Academy fornecer interface | A | Espera API e ambiente da equipe externa; não confundir simulação com integração |
| 06.01 | Comparação visual final original/recente | M | Aceite Megalos D1–D6 e página de votação |
| 06.02 | Revisar responsividade, textos, navegação e fluidez | P | Regressões grandes existem; falta QA final conjunta por jornada e relatório de falhas remanescentes |
| 06.04 | Testar e publicar preview, depois main | H | Preview publicado e build exato passou local; promoção a main depende aprovação explícita e não é condição para revisar protótipo |
| 07.05 | Zoom 200%/400%, reflow | P | Testes sintéticos existentes, falta ensaio nativo/limites com evidência válida |
| 07.06 | Compactos, rotação, IME, safe-area | P | Altura curta e compactos examinados; teclado móvel/safe-area em hardware pendentes |
| 07.10 | WCAG/semântica/leitor de tela | P | Há testes de foco, contraste e campos; leitor de tela real/avaliação WCAG AA não comprovados |
| 07.11 | Diffs visuais e aceite D1–D6 | M | Preparado kit no Drive, ainda sem decisões oficiais |
| 07.12 | Matriz final multi-engine + dispositivos | P | Firefox/WebKit anteriores e Chromium recente; falta rodada final e aparelhos reais |

**Contabilidade sem dupla contagem:** nesta lista de 24, C=2, P=12, M=6, A=2, H=2. Depois de concluir os dois C: **35/57 critérios históricos, 22 ainda abertos** (P=12, M=6, A=2, H=2). Este 35/57 é documental e técnico; não representa porcentagem de trabalho.

## Execução acelerada — lotes de encerramento, não micro-checkpoints

**Lote 1 — protótipo de votação + vínculos (P0):** 02.01, 02.02, parcela demonstrativa 02.04, 03.05. Evidência única: seis modalidades + calendário→deliberação→proposição→perfil/históricos, incluindo erros, reset e ausência de vínculos cruzados. Publicar critério por critério somente se o conteúdo integral for provado.

**Lote 2 — autoria/Socii/agendamento (P0):** 04.05, 04.09, 04.13 e interfaces de 03.01. Rodar uma jornada ampla, com casos negativos de assinatura, mudança de texto, rascunho e recuperação. D3/D4 são hipóteses externas: não inventar o temporizador de 127 horas ou autorização institucional.

**Lote 3 — qualidade/entrega da prévia (P1):** 06.02, 07.05, 07.06, 07.10, 07.12; acrescentar validação física e navegadores reais onde possível. Anotar limites, não inflar WCAG.

**Lote de revisão Megalos em paralelo:** 01.05, 03.03, 04.02, 04.19, 06.01, 07.11, mais delimitação de página de votação e D1/D1b–D6. Perguntas já existem no documento Komekko `1RFp2s-QzzigkQRDBhej_QIVr7bxYB7yhCvBWD7TERDw`; não duplicar nem enviar contato sem consentimento.

**Lote externo Academy, explicitamente separado:** 02.03, 05.04 e parcelas 02.04/06.04; manter interfaces e documentação técnica, não construir login ou banco real. Códigos da `main` nunca alterados sem autorização.

## Provas para fechar 03.02 e 05.03 agora

- `tests/rules.test.mjs`: desvinculação/rebaixamento mantêm votos, contador, histórico e metadados; restauração mantém o direito de **consultar** dados passados sem permitir novo voto.
- `tests/browser_demoted_history_v0191.py`: foco no perfil `m01`, rebaixamento em gerenciamento, retorno ao perfil e prova de que os registros pessoais de voto e métricas fictícias não foram apagados, em **320/390/740/1280px**; sem JS page errors.
- `tests/academy-identity.test.mjs` e `tests/member-reference.test.mjs`: sem credencial, role ou autorização derivadas do ACDM ID. `AGENTS.md` registra quem implementa a integração real.
- Subconjunto Node reexecutado em 10/11: **33/33 PASS**. Não houve modificação funcional da aplicação para esses dois fechamentos.

**Sem atalhos falsos:** `03.02 [x]` afirma somente a preservação no protótipo fictício; `05.03 [x]` afirma somente o acordo de responsabilidade. Não significa integração, votação institucional, aceite visual, nem implantação na `main`. Todos os critérios P/M/A/H continuam [ ] até evidência adequada.

## Auditoria incremental 146-B (10/11/2026)

Mais um critério histórico comprovado: **02.02**. O teste `tests/browser_voting_section_links_v0192.py` foi executado em Chromium 390px e cobre 24/24 combinações de modalidade e seção, sem cruzamento indevido de resultados. **Classificação atual da fila:** C=3, P=11, M=6, A=2, H=2; 21 pendências formais após 36/57. A tabela preserva as **24 pendências originais** do momento 33/57 para auditoria histórica.
