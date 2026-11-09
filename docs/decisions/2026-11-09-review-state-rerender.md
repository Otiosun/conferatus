# CONFFRATUS — Revisão de proposição: campos de seção e tipo preservados (09/11/2026)

## Defeito reproduzido

No HTML **compilado e aprovado** do checkpoint 129 (`9cc1055`, Actions `42567632176`), entrei no formulário `#confirm-proposal-form` de uma proposição fictícia em revisão, mudei a seção responsável de `integridade` para `diretoria` e o tipo de `PDR` para `PR`. Apenas abrir a gaveta do menu reconstruía a rota e os dois seletores retornavam silenciosamente aos valores antigos, **sem a pessoa ter confirmado nem cancelado**. O defeito também se reproduzia ao fechar a gaveta.

O formulário era desenhado a partir de `drafts`, mas o `render()` só recuperava valores ainda não submetidos do editor e do agendamento. A revisão não recebia esse tratamento. A perda não dependia de autenticação, backend ou votação real.

## Pesquisa e opções

- [GOV.UK — Recover from validation errors](https://design-system.service.gov.uk/patterns/validation/): reexibir os valores fornecidos para a pessoa corrigir sem redigitar.
- [ONS Design System — Correct errors](https://service-manual.ons.gov.uk/design-system/patterns/correct-errors): manter as informações do formulário para ajustes, em vez de descartá-las durante a interface.
- [CMS Design System — Error validation](https://design.cms.gov/patterns/Forms/error-validation/): preservar entradas válidas e inválidas durante atualização de formulário.

Embora o caso seja um **rerender sem erro de validação**, o mesmo princípio de preservar respostas aplica-se. Não se deve inventar salvamento automático ou mutação de `drafts` enquanto a pessoa não confirma.

**Opções rejeitadas:** salvar imediatamente `sectionId` e `type` em armazenamento (mudaria o contrato de confirmação e de Socii); criar cache permanente entre propostas (poderia contaminar outra autoria). **Adotada:** leitura temporária dos dois `select` antes de substituir o DOM e reaplicação após renderização **somente se o ID da proposta revisada for o mesmo**.

## Implementação

- `src/main.ts`: `#confirm-proposal-form` recebe `data-review-draft`, com o ID local da proposta (escapado).
- `render()`: captura `sectionId` e `type` do formulário anterior. Após reconstruir o DOM, recupera valores apenas quando `data-review-draft` é igual nas duas versões e a opção ainda existe no novo `select`.
- Nenhuma alteração automática é feita na proposta ou em suas confirmações Socii: o submit existente continua responsável por validar e concluir. Ao abrir uma **segunda** proposta, os valores da primeira não são transportados.

## Provas e aceite técnico

**Reprodução negativa no HTML original:** `integridade/PDR → diretoria/PR → abrir menu → integridade/PDR` (Chromium 390 px).

**Protótipo do mesmo HTML com JS corrigido:** ensaio Playwright em Chromium **280/390/740/1280 px**, abertura e fechamento da gaveta mantendo `diretoria/PR`, submissão com valores corretos em `conferatus:proposals-v010`, segunda proposta com seus próprios valores padrão, sem erros JS ou overflow. Esta prova isolada não é build do commit novo.

A regressão `tests/browser_review_unsaved_selection_v0183.py` executa esses passos com registros fictícios, foi incluída nas suítes Chromium, Firefox e WebKit e continua **pendente da CI completa do SHA atual**. Não desabilitar nem afrouxar as verificações em caso de falha; investigar o log e corrigir a causa.

## Fronteiras

Esta correção não resolve nem decide a **D3** da Megalos (visual definitivo da confirmação, sobreposição/fundo desfocado/botão único). Mantém o desenho e a lógica demonstrativos existentes até aceite expresso. Não acrescenta persistência institucional, conta, assinatura Socii, voto ou privilégio. `main`, ambiente de produção, Cloudflare principal, bancos Academy e PM2 continuam intocados. Contagens formais preservadas: 04=17/22, 06=2/5, 07=7/12.
