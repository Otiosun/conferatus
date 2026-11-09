# CONFFRATUS — folha azul D2 em protótipo opt-in (09/11/2026)

## Estado da decisão
**CANDIDATA, NÃO HOMOLOGADA.** A Megalos forneceu a imagem `1001930226.jpg` com a aba Proposições e Socii no perfil, lista da autoria ao fundo e uma folha azul elevada por baixo, com cantos superiores arredondados, emblema central, seleção da proposição, seção deliberativa, data e hora de início/encerramento em duas colunas, tipo da deliberação e ação CONFIRMAR. Esta imagem **não estabelece** autorização real, modalidades de voto, persistência, papéis da Academy, campos necessários de programação ou comportamento de fechamento.

A prévia aprovada até o checkpoint 126 utilizava ação contextual em proposição concluída que abria a rota calendário e preselecionava o registro. Isso resolve vínculo, não a composição da imagem. Para testar a composição sem mudar o comportamento existente nem atribuir aceitação à Megalos, um experimento **somente opt-in** foi adicionado à branch `preview/v0.10.60-six-vote-forms`.

## Pesquisa antes da implementação — Lei 21
- W3C WAI-ARIA Authoring Practices, [Modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/): foco dentro do diálogo, fundo inerte, Tab/Shift+Tab contidos, Escape e retorno ao acionador.
- WCAG 2.2 técnica [H102: diálogo nativo](https://www.w3.org/WAI/WCAG22/Techniques/html/H102): o `HTMLDialogElement.showModal()` implementa essas garantias nativamente.
- MDN, [HTML dialog element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog): usar `showModal()`, `cancel`, backdrop e `close` adequadamente; não adicionar `aria-modal=true` manual a um painel que não bloqueie o fundo.

Alternativas: painel genérico `div` com trap manual foi recusado (mais pontos de falha); novo formulário duplicado no perfil foi recusado (contraria fonte única de validação); alterar o padrão para o mockup antes da aprovação foi recusado (D2 aberta).

## Implementação limitada e reversível
- Endereço: URL da prévia acrescentando **`?demo=1&d2=sheet`**. Sem esses parâmetros, a pessoa continua vendo **o caminho atual perfil → calendário**, totalmente inalterado.
- Para proposição **concluída** da autoria fictícia no perfil, o atalho abre `<dialog id=profile-schedule-dialog>` com `showModal()` sobre o perfil, estilo azul, cantos arredondados superiores, emblema da Academy e botão Fechar explícito. O fundo fica inerte. O modo não habilita nada para perfis terceiros ou rascunhos.
- O código extraiu a marcação do formulário do calendário para a função única `scheduleFormMarkup()`, reutilizada dentro da folha. A submissão continua tratada pelo **mesmo handler**, com as mesmas validações de período/proposição/modalidade/alternativas e o mesmo arquivo de sessão local; não existe endpoint/voto institucional novo.
- Cancelar pelo botão ou Escape só fecha após verificar alterações pendentes. Se a pessoa recusar o descarte, o preenchimento permanece; se aceitar, o foco volta ao atalho da mesma proposição. Ao salvar, a folha fecha e a proposta passa a mostrar o vínculo com a programação.
- No experimento inicial, os campos adicionais `Título`, `Descrição objetiva` e `Modalidade de votação` foram mantidos: fazem parte do formulário real demonstrativo e não podem ser silenciosamente excluídos para reproduzir a imagem. Sua disposição final, assim como altura/rolagem e apresentação da folha, precisa de comparação e aceite.

## Regressões e limites
- `tests/browser_profile_schedule_sheet_d2_v0181.py`: em 280/390/740/1280 CSS px, verifica modalidade nativa, rota preservada no perfil, proposta vinculada, foco e Tab contidos, Escape, recusa de descarte, alteração de modalidade que preserva valores, submissão real da programação fictícia, ligação correta e ausência de overflow/erros JavaScript.
- Teste registrado para Chromium e para o laboratório opt-in Firefox/WebKit, além de todas as regressões anteriores. **A CI do SHA exato deve terminar SUCCESS antes de se afirmar aprovação**. O experimento não substitui a captura visual de navegador real nem o aceite da Megalos.
- Verificar: rolagem do painel com teclado virtual e entradas longas, Escape em Firefox/WebKit, ordem lógica de campos, exibição de erros, retorno ao acionador, contraste, altura segura no Android e possibilidade de continuar após falhas de gravação. Nenhuma homologação real concluída.
- Nenhuma alteração de `main`, banco/Academy/PM2/produção. As etapas formais **04=17/22, 06=2/5, 07=7/12** permanecem intocadas. D1–D6 e a página institucional de votação continuam pendentes.

Este experimento não constitui autorização para mover a folha à versão padrão.
