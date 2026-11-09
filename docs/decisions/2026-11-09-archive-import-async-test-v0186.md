# CONFFRATUS — Regressão v0158: aviso de importação assíncrona (09/11/2026)

## Evidência e causa

A tentativa 2 de [Preview voting checks 42708774184](https://github.com/Otiosun/conferatus/actions/runs/42708774184), SHA `bb14e32a454cb2218a86e39abdf7fb2b41b83870`, aprovou `postgres-lab` e `cross-browser-lab`, mas `validate` registrou uma única exceção no `tests/browser_local_archive_v0158.py`, linha 74, com viewport 390. A exceção mostrava `(390, 'O arquivo não contém JSON válido.')`, embora o `assert` aceitasse a substring `não`.

Isso não demonstra falha de rejeição da aplicação. A função antiga `message(page)` aguardava apenas que `.local-archive-message` estivesse visível; um aviso anterior já podia estar visível. `set_input_files` desencadeia um handler `change` que lê `await file.text()`, faz `render()` e substitui o input. Assim, várias chamadas a `message(page)` na mesma expressão podiam obter estados diferentes.

## Decisão mínima (Lei 21 e Lei 14)

Alterar somente o teste Playwright; preservar a lógica de importação, as mensagens brasileiras, as chaves `sessionStorage` e a UI. O auxiliar `upload` conserva o handle do input anterior, envia o arquivo e aguarda o input antigo ficar desconectado por `render()`; quando há confirmação, também aguarda `dialog` e registra a decisão (`accept`/`dismiss`), sem aguardar um render que não ocorre quando se cancela. Para entradas inválidas, exigir a mensagem específica de cada classe (JSON, versão, IDs), e não um `or` genérico nem `sleep` arbitrário. O método evita falso positivo entre duas entradas distintas que exibem a mesma mensagem.

Alternativas rejeitadas: trocar a frase correta para passar no teste; adicionar `sleep` fixo; retirar o caso de 390 px; ou aceitar qualquer aviso genérico. Não adicionar biblioteca nem reconstruir o frontend.

Documentação revisada: [Playwright Python — Locators](https://playwright.dev/python/docs/locators), [LocatorAssertions](https://playwright.dev/python/docs/api/class-locatorassertions), [Locator](https://playwright.dev/python/docs/api/class-locator). A documentação recomenda `expect(locator).to_have_text`/`to_contain_text` para verificações de texto com espera automática. Consultada em 09/11/2026.

## Evidência de QA e limite

O HTML extraído do próprio artefato do run 42708774184 (`CONFFRATUS-v0.10.60-preview`, commit `bb14e32a`) foi testado localmente com Chromium, em 280/320/390/740/1280 CSS px; cinco fluxos de JSON inválido/versão errada/IDs duplicados/referência órfã, rejeição, cancelamento e rollback passaram no ensaio de correção. Esta execução usa o HTML anterior e uma versão de teste reproduzida localmente, portanto **não certifica o commit que altera o teste** nem todo o conjunto da CI. Guardar script, logs, artefato e hashes no Drive privado.

Branch isolada: `preview/v0.10.60-six-vote-forms`. Alteração de teste feita no commit `5abec97c5c21334a0d791fbe7bdea069c24802b3`. Em repo privado, reexecução futura do GitHub Actions pode continuar bloqueada por limite de minutos. Não tornar repositório público novamente por iniciativa própria. Main/produção/Academy/PM2 intactos.

Checklist 01 4/5, 02 0/4, 03 1/5, 04 17/22, 05 2/4, 06 2/5, 07 7/12: **33/57** inalterados. Este conserto do harness não encerra a Etapa 07.05 nem a homologação da Megalos.
