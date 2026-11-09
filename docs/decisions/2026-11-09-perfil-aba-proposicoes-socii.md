# CONFFRATUS — rótulo do perfil “Proposições e Socii” (09/11/2026)

## Origem e diferença comprovada
Na captura original da Megalos `1001930226.jpg`, a segunda aba do perfil da autora está identificada como **PROPOSIÇÕES E SOCII**. O HTML da prévia até o checkpoint 128 apresentava somente **PROPOSIÇÕES** no mesmo lugar, ainda que a aba do perfil da autoria já fornecesse ações para redigir proposições e convidar Socii.

Isto é uma divergência **textual e visual**, não uma autorização de mudar convites, dados ou elegibilidade dos participantes. A fidelidade à imagem histórica não implica que todo outro membro tenha recursos de Socii disponíveis.

## Alteração mínima
- `src/main.ts`: `tabBar(tab, personalVotingHistory, hasSociiContext)` usa o título **Proposições e Socii** apenas na rota `profile` da autoria fictícia (primeiro membro da fixture); mantém **Proposições** em perfis alheios. Não altera atributo `data-tab=proposicoes`, ação, localização de dados ou lógica de votação.
- `src/styles.css`: os botões de abas sob `.profile-head` têm `min-height:44px`, acolhem quebra de linha e preservam espaçamento. Isso evita redução da área de toque e palavras cortadas em 280/320px.
- `tests/browser_profile_proposals_v013.py`: exige rótulo exato na autoria, altura mínima do controle e rótulo antigo no perfil de outra pessoa. Aguarda a transição de rota antes da asserção para não confundir o estado anterior com o novo.
- **Fontes de desenho e ergonomia:** captura original privada `1001930226.jpg` e W3C [WCAG 2.2 2.5.8 — Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum) — mínimo de 24×24 CSS px (com exceções); 44px foi escolhido como meta de conforto reforçada, não como requisito mínimo AA.

## Verificação, segurança e limites
Protótipo isolado do HTML exato da CI `42564900935` com as três mudanças injetadas no bundle de demonstração, **não o build do novo commit**: Chromium 280/320/390/740/1280 CSS px sem overflow horizontal, altura 50.4px nos dois primeiros e 44px nos demais; autoria mostra Proposições e Socii e o perfil alheio continua Proposições. Captura a 320px evidencia duas linhas legíveis, sem corte. A primeira tentativa do teste revelou leitura antes do fim do hashchange: corrigido com espera explícita e `text_content()` sem CSS text-transform.

A **CI do HEAD exato ainda deve ser confirmada** antes de aprovar o ajuste técnico. A imagem original tem outros detalhes diferentes; D1–D6, incluindo a folha azul D2 e a página institucional de votação, continuam com aceite pendente. Este ajuste não toca `main`, PM2, votação real, credenciais ou dados da Academy; Etapas formais 04=17/22, 06=2/5, 07=7/12 não foram aumentadas.


## Complemento de fidelidade — indicador PR

A mesma referência da Megalos exibe os indicadores `80 Votos · 12 PDR · 06 PR · 23 Ofício · 35 Socii`. A prévia usava `6 PR` para o mesmo valor **numérico**. A função `metricRow()` agora formata o contador PR como texto de no mínimo dois dígitos (`String(m.approved).padStart(2,'0')`); não altera `m.approved`, os dados, os IDs ou o significado do número. Não foram copiados os números pessoais da imagem original para fixtures.

A regressão `browser_profile_proposals_v013.py` exige `06` no terceiro indicador da autoria sintética. Este ajuste de apresentação não representa integração com estatísticas Academy.
