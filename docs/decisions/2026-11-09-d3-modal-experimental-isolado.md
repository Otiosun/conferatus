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
