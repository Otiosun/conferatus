# CONFFRATUS — D3, variantes de confirmação da proposição (09/11/2026)

## Evidência original e diferença visual

A imagem privada da Megalos `1001930223.jpg` apresenta um **estado adicional** de confirmação: texto da proposição desfocado atrás, cabeçalho superior com Socii/tempo (incluindo a inscrição `127 horas`), folha inferior clara, emblema da Academy centralizado, duas entradas `Seção Responsável` e `Tipo de Proposição` e **um único botão CONFIRMAR** abaixo da folha.

Na prévia funcional (`reviewPage()`, screenshot Chromium 390×850 do HTML exato do checkpoint 129), há texto legível **sem desfoque**, folha inferior com emblema e mensagem explicativa, os dois campos com rótulos e ações **Cancelar** e **Confirmar**. Os seletores da prévia são nativos e editáveis, com valores locais efetivos. A composição não reproduz literalmente a imagem 0223.

Isso **não comprova que o estado atual esteja errado**: o material histórico também evidencia uma versão de confirmação de duas ações, e **não define a transição** entre as duas variantes. D3 permanece decisão do responsável/Megalos, não aprovação por dedução.

## Definições que ainda dependem de homologação

- Quando exatamente surge a variante de **botão único**: primeira confirmação, segunda confirmação, conclusão de Socii, revisão final, ou outro momento?
- O desfoque de fundo é uma propriedade visual de um modal que deve prender foco e impedir edição do documento atrás, ou apenas uma ilustração de estado?
- Onde fica a ação de **voltar/cancelar** quando o desenho mostra apenas Confirmar? Remover a ação atual sem saída equivalente prejudicaria navegação e acessibilidade. Considerar Escape/Voltar ou um alvo claramente disponível caso D3 seja aprovada.
- Os dois campos devem mostrar **valores já selecionados** ou placeholders? A imagem não fixa a regra de escolha, e os dados não podem ser alterados só para simular o visual.
- O cabeçalho `127 horas` é evidência visual, **não uma regra temporal aprovada**. D4/contagem Socii permanecem independentes e não podem ser implementados por inferência.

## Evidências e proteções

- No pacote privado `CONFFRATUS_D3_COMPARATIVO_CHECKPOINT_132.zip` do Komekko: imagem original, captura atual da revisão em 390×850 e 280×850, comparativo lado a lado, README que distingue fontes. **Não publicar arte original no GitHub.**
- A tela atual `reviewPage()` já preserva as validações de seção/tipo e a colaboração Socii demonstrativa. O checkpoint 132 corrigiu um **defeito distinto e real**: valores não confirmados eram perdidos por um rerender de menu, agora preservados exclusivamente por ID da proposição.
- **Não foi implementado um novo fluxo D3 nesta etapa.** O teste `browser_review_unsaved_selection_v0183.py` cobre o defeito de retenção em Chromium e motores Firefox/WebKit via CI, mas não constitui teste de homologação visual.
- Antes de alterar D3, pesquisar o padrão de diálogo e foco e produzir candidata isolada, preservando o fluxo funcional até o aceite. Recomendações relevantes: [W3C APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) e [GOV.UK checks before confirmation](https://design-system.service.gov.uk/patterns/check-answers/).

## Fronteiras

D1–D6 e página institucional de votação ainda não homologadas. `main`, PM2, Academy, contas, banco real e produção preservados. Etapas formais 04=17/22, 06=2/5, 07=7/12 não são incrementadas por essa comparação. A decisão D3 permanece **ABERTA**.
