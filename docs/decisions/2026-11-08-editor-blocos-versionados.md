# Decisão 2026-11-08 — modelo de blocos versionados (prova isolada)

## Problema observado

O editor atual mantém `Draft.body` como texto simples e `Draft.bodyRuns` como marcas por trecho. `runsFromEditable()` extrai apenas texto e formatação, ignorando nós sem conteúdo textual. Um `<hr>` introduzido no `contenteditable` desapareceria do registro após salvar e reabrir. Inserir um botão sem contrato de persistência violaria as Leis 5, 15, 16 e 21 de `AGENTS.md`.

**Objetivo deste checkpoint:** elaborar, codificar e testar o modelo **fora da aplicação e do bundle público**, sem abrir um controle visual novo e sem converter registros reais ou sintéticos armazenados na sessão. Não houve alteração em voto, regras, Academy, autenticação, banco ou `main`.

## Pesquisa de engenharia (08/11/2026)

| Fonte técnica | Evidência relevante | Consequência |
|---|---|---|
| ProseMirror — Guide, https://prosemirror.net/docs/guide/ | Parágrafos são blocos com texto/marcas; `horizontal_rule` é um bloco folha sem texto, separado das marks | Modelar divisor como nó estrutural, nunca como string HTML em `bodyRuns` |
| ProseMirror — esquema básico, https://github.com/ProseMirror/prosemirror-schema-basic/blob/master/src/schema-basic.ts | `doc` define a sequência permitida; `paragraph` e `horizontal_rule` são nós distintos | Validar ordem, atributos, tipo, tamanho e versão do documento |
| Lexical — Serialization, https://lexicaljs.com/docs/serialization/ | O estado estruturado pode ser serializado em JSON a partir de nós | Usar esquema JSON tipado/versionado, sem armazenar DOM/HTML |
| MDN — `execCommand`, https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand | API obsoleta e com diferenças entre browsers; às vezes preserva o undo nativo | Não estender `execCommand` com `insertHorizontalRule` sem provar seleção, edição, desfazer, export e reabertura |

Foram consideradas (1) acrescentar `<hr>` ao editor atual; (2) substituir imediatamente a edição por Lexical/ProseMirror/Tiptap; (3) fazer um codec mínimo de blocos versionados em isolamento. Escolhida **(3)**, pois (1) perde o nó no esquema antigo e (2) reescreveria funcionalidades já aprovadas, custos e dependências, sem homologação e plano de migração. Nenhum pacote novo é introduzido.

## Contrato experimental V1

- `RichBlockDocumentV1` aceita apenas `{version:1,blocks:[...]}` mais `layout?` validado. Blocos válidos: `paragraph` com `text` e `runs?` já validados pelo módulo oficial; `horizontalRule` como nó sem atributos.
- `paragraph.text` não contém quebras de linha, pois cada separação é representada por outro parágrafo. Parágrafos vazios e quebras de linha finais são preservados.
- Máximo de 1.024 blocos, 2.048 runs e 200 mil unidades UTF-16 de texto; atributos adicionais, CSS, HTML, URLs proibidas, nós desconhecidos e divisor em posições inválidas são rejeitados.
- `migrateLegacyRichText()` recebe **cópia** do `body`, `bodyRuns?` e `bodyLayout?`, separa em parágrafos preservando o texto/cores/fonts/marcas e links HTTP(S) já sanitizados. **Não altera `sessionStorage`**. Quebras de linha formatadas de forma incompatível são rejeitadas com motivo explícito; nunca remover marcações silenciosamente.
- `insertHorizontalRule()` e `removeHorizontalRule()` são funções puras/imutáveis, exigem dois parágrafos adjacentes e não permitem divisor duplicado ou nas extremidades.
- `projectRichBlocksToLegacy()` devolve texto e runs no esquema antigo **somente quando a projeção é sem perda**. Se houver divisor, retorna `{ok:false,reason:'structural-blocks'}`; não exporta silenciosamente um documento sem seu separador.
- `renderRichBlockDocument()` é apenas uma saída de ensaio: escapa todo texto, reusa `renderRichText` e pode gerar somente `<p>` e `<hr>` conhecidos. **Não é um editor nem foi conectado à interface.**

## Aceite desta prova, sem antecipar homologação

Os testes Node `tests/rich-blocks.test.mjs` devem provar: migração e volta sem mudança semântica de `body`/`bodyRuns`, preservação de linhas vazias/trailing-newline e links, recusa de newline com estilo irrecuperável, operações imutáveis, serialização JSON e restauração do divisor, recusa de downgrades com perda, rejeição de entradas hostis e saída HTML escapada. O `npm run build` deve continuar executando a matriz antiga. Não dar o status de aprovado antes de consultar logs da CI vinculada ao SHA.

## Próximos gates antes de integrar ao editor

1. Mapear seleção por parágrafo/bloco e edição IME/clipboard/undo (Chromium, Firefox, WebKit e aparelhos físicos) sem depender de DOM acidental.
2. Decidir onde armazenar `bodyBlocks` versionado e como migrar `Draft`, histórico, backup/importação, assinaturas Socii e revisão com recuperação de falhas.
3. Provar alteração entre blocos, Enter, Backspace, cursor nos limites de `<hr>`, copiar/colar e exclusão com o teclado móvel. Fazer capturas e testes visuais da Megalos **antes** de disponibilizar o botão.
4. Somente após esses gates, liberar divisor realmente editável. Tabelas e controles por parágrafo requerem extensão do esquema e homologação específica. A página de votação permanece uma decisão separada D1–D6.

**Estado:** experimento de modelo, sem UI ativa, sem contagem de etapa encerrada e sem `main` alterada.


## Evidência de execução e correções — 08/11/2026

A CI do commit inicial `13e10b7` encontrou erros TS2571 ao ler vizinhos de tipos desconhecidos; corrigidos com narrowing explícito no `f8a0c70`. A segunda execução detectou um **defeito real de aliasing** na operação imutável: inserir divisor reutilizava objetos de parágrafos, de modo que alterar a cópia também alterava a versão anterior. O commit `2536215` introduziu cópia profunda dos metadados e marcas ao inserir/remover blocos e corrigiu a contagem de comprimento considerando apenas as separações de parágrafo. O teste que revelou o defeito foi mantido, não suavizado.

GitHub Actions [42447625273](https://github.com/Otiosun/conferatus/actions/runs/42447625273), SHA exato `2536215c05746566d6a05f9dd27601b2cf7917a4`: **SUCCESS** para `npm run build` (TypeScript e 64/64 Node, incluindo sete novos testes de blocos), 36/36 scripts Chromium históricos e PostgreSQL descartável. A matriz extra Firefox/WebKit foi `SKIPPED` intencionalmente: ainda não existe nenhum controle de bloco no aplicativo nem mudança de API de navegador.

Evidência arquivada com CRC e SHA-256 idênticos ao Actions: [HTML do CI (104.699 bytes)](https://drive.google.com/file/d/1J-k_IpeZIwBVVF7PGUyD4ApGl11bnmdP/view); [33 capturas de regressão (2.828.560 bytes)](https://drive.google.com/file/d/1ZFqPDdE-NXYYiZBhdwrBWTamJSCGsVKr/view). O HTML da aplicação permanece funcionalmente inalterado; as capturas mostram regressões anteriores, **não uma tela de divisor**.

**Decisão mantém-se:** schema/codec experimental comprovado no domínio, sem ativação em `Draft`, `sessionStorage` ou UI; não equivaler a entrega do editor de blocos, não marcar etapas 04/06/07 e não alterar `main`.


## Operações de cursor e investigação entre motores — 08/11/2026

Fontes adicionais consultadas antes da implementação:
- MDN `beforeinput` (https://developer.mozilla.org/en-US/docs/Web/API/Element/beforeinput_event): nem toda modificação dispara um evento cancelável; IME, autocorreção e autocomplete podem escapar dos handlers. Portanto, `preventDefault` isolado não garante integridade em celulares.
- MDN `InputEvent.inputType` (https://developer.mozilla.org/en-US/docs/Web/API/InputEvent/inputType): permite observar `insertParagraph`, `deleteContentBackward` e edição de texto, mas não normaliza o DOM resultante.
- ProseMirror GapCursor (https://prosemirror.net/docs/ref/version/0.24.0.html e https://github.com/ProseMirror/prosemirror-view/blob/master/src/selection.ts): nós folha como `horizontal_rule` precisam de estratégia explícita de cursor; diferenças históricas no WebKit entre nós não editáveis exigem teste de motor, não suposição.

A menor etapa selecionada é separar **operações puras** do navegador. `splitRichParagraph(document, blockIndex, offset)` e `joinRichParagraphs(document, leftIndex)` preservam texto e marcas, rejeitam índices inválidos, recusam unir parágrafos separados por divisor e não editam referências do documento de origem. `offset` é UTF-16, com guarda para não cortar um par de substitutos de emoji. A conversão para o editor atual não foi habilitada.

O diagnóstico `tests/browser_block_native_probe_v0168.py` cria um **editor sintético descartável**, diferente do site, e observa as operações nativas Enter/Backspace/undo perto de um `<hr contenteditable=false>` em Chromium, Firefox e WebKit. Salva observações em `dist/cross_engine_block_native_probe_*.json`; os resultados não são declarados homogêneos por definição, e nenhum assert contorna discrepâncias. Nunca chamar esse teste de validação de teclado móvel, IME, colagem real, edição de blocos integrada, Socii ou votação.

Aceite limitado: Node garante propriedades de divisão/união/imobilidade de divisoress, e o navegador fornece observações para escolher futura estratégia de edição. Somente após teste efetivo e consentimento de design da Megalos poderá surgir botão de divisor na prévia; tabelas não entram nesta rodada.
