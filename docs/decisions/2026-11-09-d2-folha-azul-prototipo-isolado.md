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


## Revisão de composição — ordem original dos campos

A revisão direta da imagem `1001930226.jpg` evidenciou outra diferença: o formulário original começa por **Proposição → Seção → Datas lado a lado → Tipo**. A primeira candidata preservava a ordem do formulário do calendário (título/descrição antes da proposta), inadequada visualmente mesmo em um experimento.

A função compartilhada `scheduleFormMarkup(profileSheet=false)` foi dividida em pequenos fragmentos sem novos handlers nem novos estados. Na versão **calendar**, concatena os campos na ordem anterior, mantendo a regressão e o contrato existente. Na versão opt-in **profileSheet**, concatena proposta, seção, datas e tipo primeiro; depois uma seção visível **Detalhes da programação** reúne título, descrição, modalidade e alternativas condicionais — campos efetivamente exigidos pelo workflow demonstrativo. Esses campos não são ocultados nem têm validação reduzida. A ordem do DOM e a ordem visual/tabulação coincidem.

O teste `browser_profile_schedule_sheet_d2_v0181.py` agora exige a sequência `proposalId, sectionId, start, end, type` nas primeiras cinco entradas, sem perder `title`, `objective` e `method`. Não declarar a versão fiel integral ao desenho: a referência tem menos campos e não define o destino dos dados adicionais. Escolha final de conteúdo/hierarquia, altura em celular real, scroll e aceite da Megalos permanecem D2 aberta.

## Defeito encontrado na CI de Chromium: saída por Esc recusada

A execução `42561293016`, no SHA anterior à reorganização dos campos, obteve `cross-browser-lab=SUCCESS` (Firefox e WebKit) e `postgres-lab=SUCCESS`, mas `validate=FAILURE` em Chromium no novo teste `browser_profile_schedule_sheet_d2_v0181.py`: após preencher título, objetivo e alternativas, pressionar Esc e rejeitar a confirmação de descarte fez a folha desaparecer em 280px. Portanto a candidata NÃO estava protegida contra essa saída, apesar dos resultados positivos de outros motores.

**Pesquisa adicional Lei 21:** MDN, [HTMLDialogElement cancel](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/cancel_event) documenta evento cancelável e não-bolhante. A diretriz do Chrome, [Dialog – Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance/guides/ui-components/dialog), recomenda `closedby="none"` e uma ação explícita para formulários sujos, além de advertir contra confiar somente em `preventDefault()` sob Esc repetido sem ativação. A implementação anterior usava `window.confirm` dentro de `cancel` e `preventDefault()`, mas não impediu o fechamento observado no Chromium.

**Correção restrita:** a folha opt-in possui `closedby="none"`, com listener `keydown` em captura para Esc quando a folha está efetivamente aberta, chamando `preventDefault()` antes do default do navegador. Botão Fechar, tecla Esc e evento nativo `cancel` passam pela única função `dismissProfileScheduleSheet()`: se há dados pendentes e a pessoa recusa o descarte, nenhuma mudança de estado; se autoriza, a folha fecha e restaura o foco ao atalho da mesma proposição. O navegador mantém foco limitado ao modal pelo elemento `dialog`. Nenhuma mudança no fluxo padrão.

A correção foi registrada em `0e519ecf98ebc0184b5cf74ed648afcf6e32b854`. É **pendente de CI exata**: não marcar a falha corrigida até o Chromium e os motores adicionais concluírem sem regressões. Registrar explicitamente o FAIL anterior.

## Revisão de geometria — área do perfil visível

Capturas de prova da candidata inicial no HTML CI `42561293016`, com Chromium 280/390/740 CSS px, mostraram a folha ocupando cerca de 82% da altura útil em 390 px (y=153, altura=697 em viewport de 850), ocultando quase toda a página ao fundo, em desacordo com o desenho Megalos `1001930226.jpg`.

A regra opt-in foi reduzida a `max-height:min(58dvh,580px)` e, para telas até 380px, `max-height:68dvh`. Na prova CSS isolada sobre o HTML anterior, em 390px passou a ocupar altura 493px (y=357), em 280px altura 578px (y=272) e em 740px altura 493px (y=357), sem overflow horizontal. O conteúdo total era maior que a caixa (scrollHeight ~919/822), mantendo rolagem interna. **Não** é prova da última compilação nem de teclado virtual real; as capturas são comparativos isolados de CSS.

Como a imagem original mostra início/encerramento lado a lado, a versão atual preserva a quebra de datas em telas compactas quando duas entradas `datetime-local` completas lado a lado reduziriam a legibilidade. Trata-se de desvio de conforto a ser avaliado com a Megalos, não de aceite da D2.

O teste permanente `browser_profile_schedule_sheet_d2_v0181.py` inclui limite de cobertura visual (parte do perfil deve permanecer visível) e exigência de rolagem do painel; continua verificando os campos e a guarda de saída. A altura é exclusiva do experimento, não altera calendário nem perfil padrão.

## Preservação ao trocar entre perfis pela URL

Falha **negativa reproduzida** no HTML real da primeira CI da candidata: com D2 aberta no perfil da autoria, título digitado e a navegação direta `location.hash='#/profile/m04'`, o modal desapareceu e o campo deixou de existir sem `window.confirm`, porque a guarda verificava apenas **nome da rota** (`profile`), não mudança de identificador dentro da mesma rota. Isso pode ocorrer pelo histórico/links do navegador, mesmo que o fundo do modal esteja inerte.

Correção mínima em `src/main.ts`: `navigate()` distingue também `memberId` da pessoa atualmente selecionada. Qualquer `hashchange` enquanto a folha está aberta verifica primeiro `confirmScheduleDeparture()`; se negar descarte, restaura o hash antigo e mantém o documento aberto; se aceitar, fecha a folha e segue ao destino. O comportamento do calendário padrão permanece inalterado. Regressão em `browser_profile_schedule_sheet_d2_v0181.py` preenche o formulário, tenta mudar para `#/profile/m04`, rejeita e verifica hash original, título intacto e modal visível.

Até a CI do commit que contém essa regressão terminar, **não** considerar o novo caminho comprovado. Main, dados Academy, PM2 e produção sem alterações.

## Feedback explícito ao salvar no perfil

A candidata experimental retornava à lista da autoria depois de salvar, e o vínculo de programação aparecia no cartão, mas a frase `Deliberação programada.` (ou aviso de falta de persistência) era emitida só no anunciador de acessibilidade. Para uma pessoa que utiliza a visão do perfil, essa ação não dava confirmação textual direta do resultado.

Ao abrir o formulário D2 opt-in, `workflowNotice` é limpo para não confundir com ação anterior. Após o mesmo handler de `saveWorkflows()`, o perfil exibe `p.profile-schedule-result[role=status]` com o resultado real: programação gravada na sessão ou mantida apenas enquanto a página estiver aberta. O rótulo é produzido pelo handler existente e escapado antes da renderização. Nenhuma mensagem nova de integração ou publicação foi inventada; o fluxo padrão sem a flag continua igual.

A regressão `browser_profile_schedule_sheet_d2_v0181.py` exige mensagem visível `Deliberação programada` após submissão com storage disponível. A recuperação e a clareza de falha de gravação seguem os contratos e testes gerais de sessionStorage; não alegar garantia de armazenamento após fechar navegador ou autenticação Academy.
