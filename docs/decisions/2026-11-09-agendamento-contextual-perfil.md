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
