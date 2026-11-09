# CONFFRATUS — D3 candidata de confirmação com documento desfocado (09/11/2026)

## Decisão e limite de autoridade

**CANDIDATA VISUAL ISOLADA — D3 NÃO HOMOLOGADA.** Na imagem original da Megalos `1001930223.jpg`, há uma folha inferior clara, duas seleções (Seção Responsável e Tipo de Proposição), emblema central no topo e **uma** ação principal `CONFIRMAR`. O texto da proposição aparece desfocado; a barra superior inclui dados visuais de Socii e a inscrição `127 horas`, sem contrato sobre contagem ou transição.

A prévia funcional pré-existente mantém a confirmação normal com **Cancelar + Confirmar**, mensagem de conferência e documento legível. Não há decisão recebida da Megalos que estabeleça quando ou por que a variante de botão único deve substituí-la. Portanto ela não é promovida à experiência padrão, não altera a jornada nem representa regras de aprovação da Academy.

## Pesquisa e engenharia de interação

- [W3C WAI-ARIA APG, modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/): o conteúdo externo a um diálogo modal deve ser inerte; foco inicial dentro; Tab/Shift+Tab não saem; Escape deve permitir sair; há recomendação explícita de botão de fechar visível.
- [MDN, HTML dialog](https://developer.mozilla.org/pt-BR/docs/Web/HTML/Reference/Elements/dialog): `HTMLDialogElement.showModal()` oferece top layer, interação modal e `::backdrop`; não basta aplicar `filter:blur` em uma página comum e chamá-la de modal.
- A experiência prévia do próprio projeto detectou uma divergência do Chromium quando `window.confirm` era invocado dentro de `cancel`. A saída por Escape foi interceptada em `keydown` (captura) para impedir um fechamento nativo automático que descartaria escolhas, mantendo uma rota explícita.

**Alternativas consideradas:** recriar uma segunda confirmação independente (risco de divergir nas regras de Socii e salvamento, rejeitado); esconder Cancelar e deixar pessoas sem saída acessível (rejeitado); CSS de desfoque sem bloquear interação com a página (rejeitado). A solução candidata usa **o mesmo formulário e handler** já testados em um diálogo nativo, mantendo um botão principal Confirmar e um botão secundário discreto de fechar com rótulo acessível.

## Implementação sob flag

- **URL de teste:** `?demo=1&d3=single`. Sem ambos os parâmetros, a confirmação original é exibida com suas duas ações e nenhum diálogo D3.
- A flag altera somente a tela `review` de uma proposição em revisão; proposições já concluídas continuam exibindo seu estado final.
- O formulário existente `#confirm-proposal-form` entra dentro de `<dialog id="d3-review-dialog" closedby="none">`, acionado por `showModal()`. A mesma validação, mesmo método de submissão e mesmo estado local são reutilizados. Não há duplicação de IDs, formulário, persistência ou protocolo Academy.
- O fundo é visualmente desfocado via `::backdrop` e fica inerte enquanto o modal está aberto; foco inicial no primeiro seletor, não na ação destrutiva nem em campo fora da vista.
- A única **ação principal** é `CONFIRMAR`; um pequeno botão `×`, com área de toque de 44px e nome acessível `Voltar à redação sem confirmar`, oferece saída visível sem tornar obrigatório conhecer Escape. Ele é uma ação de navegação, não outra confirmação.
- Escape, fechar e navegação direta pelo histórico só descartam mudanças em `Seção responsável`/`Tipo` depois de confirmação explícita da pessoa. Recusar mantém a folha e o formulário; aceitar volta à redação. Há guarda `beforeunload` quando o formulário tiver mudanças pendentes, limitada pelas ressalvas normais de navegadores móveis.
- O controle anterior `data-review-draft`, que preserva seleções durante rerenders do mesmo documento, permanece vigente; não são transportadas escolhas para outra proposta.

## Testes e evidências exigidos

`tests/browser_review_d3_single_modal_v0184.py` cobre em 280, 390, 740 e 1280 CSS px: modalidade nativa, único CTA, botão Fechar acessível, foco e Tab/Shift+Tab contidos, fundo desfocado, Escape simples, recusa a descartar, botão Fechar e histórico recusados, preservação dos campos no rerender, confirmação pelo handler existente e isolamento de `?demo=1` sem D3 e `?d3=single` sem demo. O teste foi registrado para Chromium, Firefox e WebKit.

**A aprovação exige a CI exata do commit de código e teste**, uma captura do HTML que a CI realmente compilou e comparação visual com `1001930223.jpg` em múltiplos tamanhos. Um resultado de CSS/JavaScript isolado **não comprova** que a compilação final nem o comportamento Android/IME estejam corretos. Não declarar esta variante pixel-perfect: a imagem original não especifica os estados de erro, a saída acessível, a ordem de foco e a presença real de opções nos seletores.

## Decisões ainda abertas

1. Em qual estado específico essa variante entra (primeira revisão, após conclusão de Socii, confirmação final ou outro)? **Sem resposta da Megalos.**
2. O desenho do fundo desfocado indica realmente uma operação modal ou só uma convenção visual? Proposta atual de modal é hipótese revisável, não política oficial.
3. Onde ficaria a saída alternativa aprovada visualmente sem remover a acessibilidade?
4. O texto `127 horas` representa prazo real, tempo restante, tempo de colaboração ou apenas preenchimento do mockup? **Não gerar cronômetro fictício.**
5. O que acontece após Confirmar quando ainda existem coautorias pendentes? **Continuar usando o comportamento demonstrativo já aprovado tecnicamente**, sem alterar Socii.

**Escopo protegido:** nenhuma promoção para `main`, login institucional, voto real, PM2, banco de dados ou permissão Academy. Checklist formal permanece **04=17/22, 06=2/5, 07=7/12** até homologação.


## Revisão pós-CI: foco no fim da sequência e desfoque seletivo

A primeira CI do experimento (`42682761357`, commit `173db32`) **reprovou em Chromium** no novo teste v0184: depois de Tab ultrapassar o último botão, `document.activeElement` tornou-se temporariamente `body` em 280px. O modal permaneceu aberto, e outro Tab retornou ao primeiro botão, mas a regra W3C de foco **sempre dentro do diálogo** não estava cumprida pelo ciclo nativo. O teste foi preservado, sem rebaixar a exigência.

**Correção funcional localizada:** listener `keydown` em captura, somente enquanto a D3 está aberta, detecta Tab/Shift+Tab atravessando a primeira/última posição e transfere diretamente o foco ao primeiro/último controle visível e habilitado. Não altera controles intermediários nem a navegação normal de outras telas. No ensaio local com o HTML *exato da CI que reprovou* e a correção de foco injetada, 10×Tab + 5×Shift+Tab permaneceram continuamente dentro de `#d3-review-dialog`, sem o estado transitório `body`. A regressão v0184 original continua a exigir esse resultado no build mais novo.

**Ajuste visual com evidência:** a primeira captura do HTML da CI reprovada desfocava também o título da proposição, enquanto a arte `1001930223.jpg` mostra título nítido e **corpo da proposição** desfocado. CSS mudou para aplicar `filter:blur(5px)` somente à `workflow-review-body--d3`. O `::backdrop` permanece atenuando o fundo, mas sem filtro de desfoque geral; assim, o cabeçalho não fica borrado e o documento continua desviado de atenção. Ensaio local Chromium confirmou essa diferença. Teste v0184 atualizado para exigir `filter` de desfoque na **área do documento**, e `filter:none` no título. Não retirar a verificação de desfoque.

**Foco após saída:** ao sair da D3 para `compose` via Escape/fechar, o foco deve retornar ao botão `Concluir` do editor (ação que levou à revisão), em vez de cair genericamente no início da página. Regressão v0184 exige esse retorno após Escape. Não confundir retorno à edição com confirmação/gravação.

**Verificação independente das regras de negócio:** no HTML da CI anterior, um segundo ensaio Chromium em 280/390/740/1280 reproduziu que Escape sem mudanças volta ao editor; alteração de seção/tipo se mantém num rerender; recusar Esc, fechar ou mudança direta de hash preserva escolhas; o botão CONFIRMAR usa o mesmo handler e grava `diretoria/PR` na proposta local. O ensaio de fluxo não comprova o novo build nem os demais motores.

A CI do **SHA exato** com os três ajustes (foco cíclico, blur seletivo, retorno de foco) deve ser executada com opt-in `[cross-browser]` para Firefox/WebKit, além de Chromium e PostgreSQL. Falha anterior permanece registrada, não substituir o resultado negativo por prova isolada.
