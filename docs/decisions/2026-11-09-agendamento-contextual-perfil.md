# CONFFRATUS — Agendamento contextual a partir do perfil (09/11/2026)

## Referência, problema e limite da decisão
A imagem original privada `1001930226.jpg` fornecida pela Megalos mostra **Proposições e Socii no perfil** e uma folha inferior de agendamento com **Selecione a Proposição**, **Seção Deliberativa**, datas, tipo e confirmação. A interface existente antes desta rodada só abria o formulário de programar deliberação dentro da rota calendário. Para programar uma proposição acabada, a pessoa precisava voltar ao calendário e encontrar a mesma proposição em um menu, gerando navegação e seleção redundantes.

**A decisão D2 não está homologada:** a localização final do agendamento (sobreposição diretamente no perfil, somente no calendário ou ambas) continua pendente da Megalos. Esta intervenção é uma **ponte funcional e reversível** na prévia: acesso a partir de um registro próprio e concluído, reaproveitando integralmente o formulário existente do calendário. Não se apresenta essa ponte como reprodução integral da folha original.

## Investigação e alternativas
- W3C WAI, Disclosure Pattern: o acionamento de uma região adicional deve expor ação e destino de forma clara, com botão de teclado e foco previsível. https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
- MDN, HTMLSelectElement.value: usar a seleção nativa por valor de opção, sem menu customizado desnecessário. https://developer.mozilla.org/en-US/docs/Web/API/HTMLSelectElement/value
- MDN, constraint validation: conservar `required`, submissão/validação nativa e a validação de domínio já existente; preseleção não autoriza pular verificações. https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation

Alternativas consideradas:
1. Duplicar o formulário no perfil, com segundo handler de salvamento: **rejeitada**, pois diverge da lei 3, duplica validações e facilita registros inconsistentes.
2. Criar de imediato uma nova folha sobreposta com o desenho da referência: **adiada** enquanto D2 não for confirmada, já que depende de regras de fechamento, foco, conteúdo, rolagem e reentrada.
3. Reutilizar o formulário atual com link contextual por proposta: **adotada provisoriamente**, sem backend ou autorização institucional.

## Implementação na branch de prévia
- Ações `Programar deliberação sobre esta proposição` aparecem **somente** para proposições `concluida` da sessão da autoria demonstrativa, nas telas de Proposições e no perfil do autor fictício. Rascunhos e o perfil de terceiros não recebem essa ação. Nenhuma suposta permissão Academy é concedida por isso.
- O acionamento abre `#/calendar` com `#schedule-deliberation-form` já visível e `proposalId` previamente selecionado **para o mesmo registro**. Ao abrir, a seleção recebe foco e é trazida à área visível. Os demais campos continuam a exigir preenchimento. A programação é salva somente pelo handler existente.
- `schedulePrefillProposalId` é estado transitório apenas da interface; não vira chave em banco ou storage. Ao fechar, salvar ou navegar para fora, é descartado.
- A seleção contextual sem nenhuma edição **não deve disparar um alerta de dados não salvos**; uma alteração feita pela pessoa continua protegida contra descarte.
- CSS mantém o novo comando visualmente secundário, legível em celular, com altura mínima de 44px e foco visível.
- Regressão `tests/browser_profile_schedule_context_v0180.py` em 280/320/390/740/1280 px e nos motores Chromium, Firefox e WebKit: duas propostas concluídas, rascunho inacabado, vínculo exato à segunda, foco, alerta falso ausente, fechamento normal, criação programada e associação correta, ausência de botão em perfil alheio, ausência de overflow/erros JS. CI registra teste de forma obrigatória no `validate` e no `cross-browser-lab`.

## Não concluído e gates
- **D2 aberta:** ainda falta a Megalos decidir se a folha final será no perfil, no calendário ou em ambos. Este acesso contextual é uma facilitação, não aceite visual.
- **D1/D3–D6** e página de votação institucional continuam com definição e homologação pendentes; não inferir da imagem as regras de participação ou administração.
- O laboratório usa dados sintéticos e `sessionStorage`. Sem login, autorização institucional, gravação de voto ou integração com a Academy.
- CI do SHA exato do lote, revisão de capturas do artefato, Android físico e usabilidade assistiva ainda precisam ser verificadas antes de afirmar conclusão técnica.
- `main`, dados reais e produção permanecem intocados. Contagens formais preservadas: Etapa 04 17/22, 06 2/5, 07 7/12.

## Revisão 126 — ordem de foco no início do agendamento

**Problema reproduzido, não presumido:** ao clicar `Programar deliberação sobre esta proposição`, o seletor `proposalId` recebia foco apesar de já estar preenchido. No HTML exato da CI `42553046517` (SHA `12359bd`), Chromium a 390 CSS px: foco inicial em `proposalId` e o primeiro **Tab** levava a `sectionId`, pulando título e descrição (campos anteriores na ordem visual). O cabeçalho do formulário permanecia visível nos tamanhos ensaiados; **não alegar que estava escondido**. A regressão concreta é a sequência ilógica do teclado.

**Investigação (Lei 21):**
- Home Office User-Centred Design Manual, [Keyboard for forms](https://design.homeoffice.gov.uk/accessibility/interactivity/forms/keyboard): avançar pelos campos na ordem visual, sem saltos.
- VA.gov Design System, [Focus management](https://design.va.gov/accessibility/focus-management): SPA deve orientar foco para o título da nova rota, rolar elemento focalizado à vista e usar contexto compreensível.
- Chrome Lighthouse, [Managed focus](https://developer.chrome.com/docs/lighthouse/accessibility/managed-focus/): após mudança de rota sem recarga, direcionar foco para o conteúdo recém-exibido.

**Opções consideradas:** manter foco no seletor (mais rápido para alterar proposta, porém confunde ordem inicial); colocar foco no primeiro `input` (teclado mobile pode abrir inesperadamente e omite o título); focar o `h2` do formulário com `tabIndex=-1`, sem incluí-lo na tabulação (escolhido). Sem dependência e sem alterar permissões, validações ou valores.

**Alteração delimitada:** somente quando aberto pelo atalho contextual, o `h2` `Programar deliberação` recebe foco programático e rolagem ao início. CSS `scroll-margin-top:16px` dá respiro antes do título. Primeiro **Tab** segue para o `input` de título, depois descrição e demais campos em ordem. `proposalId` continua previamente selecionado por ID. Entrada direta via calendário permanece inalterada.

**Prova:** ensaio original confirmou `proposalId → sectionId`. Protótipo do JS compilado, sobre o HTML do mesmo SHA, passou em Chromium 280/320/390/740/1280px: `h2 → Tab → title`, seletor preservado, sem erros JS nem overflow; com CSS 16px, o cabeçalho ficou a aproximadamente 16px do topo em 280, 390 e 1280px. Não tratar o protótipo isolado como compilação do HEAD. A regressão permanente `tests/browser_profile_schedule_context_v0180.py` agora exige foco no `h2`, rolagem visível e primeira Tab para título. Confirmar build e Firefox/WebKit do **novo SHA** antes de marcar a implementação como tecnicamente validada.

D2 **permanece aberta**: o atalho e a ordem de teclado não significam homologação da folha azul sobreposta originalmente mostrada pela Megalos. Sem alteração de `main`, produção, dados Academy ou PM2.
