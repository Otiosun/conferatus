# Decisão 2026-11-07 — investigação fria do editor

## Nova lei máxima e escopo

A Lei Máxima 21 exige pesquisa prévia proporcional ao risco, documentação das fontes, riscos conhecidos, alternativas, escolha fundamentada e teste de regressão. Aplica-se à prévia CONFFRATUS. Não autoriza alteração em main, Academy, autenticação, dados reais ou publicação institucional.

## Fontes e achados técnicos (consultados em 07/11/2026)

- MDN, `document.execCommand()`: obsoleto, não padronizado, comportamento inconsistente; ainda é usado por editores simples por preservar o buffer nativo de undo em situações nas quais DOM direto não preserva. https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand
- OWASP, XSS Prevention: URL de usuário exige validação de protocolo, canonicalização e escape contextual de atributos; HTML arbitrário em `contenteditable` não é confiável. https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet
- MDN, `URL()`: parser padrão de URL absoluta em navegadores modernos. https://developer.mozilla.org/en-US/docs/Web/API/URL/URL
- MDN, `<a>`, `noopener` e `noreferrer`: proteger a aba original, reduzir vazamento do referer e fornecer texto compreensível ao leitor de tela. https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a e https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/noopener
- ProseMirror: marcas de trechos (*marks*) são diferentes de blocos estruturais (paragraph/horizontal_rule). https://prosemirror.net/docs/guide/ e https://github.com/ProseMirror/prosemirror-schema-basic/blob/master/src/schema-basic.ts
- Lexical: estado versionável em árvore de nós, serialização JSON; recomendada migração aditiva e validação de blocos. https://lexicaljs.com/docs/serialization/
- Tiptap: schema restringe nós e atributos e horizontalRule é extensão de nó própria. https://tiptap.dev/docs/editor/core-concepts/schema e https://tiptap.dev/docs/editor/extensions/nodes/horizontal-rule

## Alternativas avaliadas

| Alternativa | Benefício | Problema comprovado / risco | Decisão |
|---|---|---|---|
| Guardar link como metadado do trecho selecionado em bodyRuns, usando editor existente | Pequena mudança; body plain intacto; sem nova dependência | ExecCommand está obsoleto; seleção precisa sobreviver ao foco do campo; diferenças Chromium, Firefox, WebKit | **Implementar experimentalmente na prévia**, exigir regressão 3 motores |
| Salvar HTML inteiro de contenteditable | Implementação fácil aparentemente | XSS e inconsistência de serialização, colagem e importação | **Rejeitar** |
| Range.surroundContents para cada link | API moderna | Erra com seleção que cruza nós ou texto já formatado; undo/redo menos previsível | **Adiar**, considerar apenas mediante prova em isolado |
| Migrar editor inteiro para Lexical/ProseMirror/Tiptap imediatamente | Bom para blocos, tabelas e histórico transacional | Custo real de dependências, bundle, migração de drafts e testes | **Não nesta fatia** |
| Inserir `<hr>` diretamente no DOM editável e salvar só body | Quase sem código | Perde divisor ao extrair texto; não há representação recuperável | **Proibido** |
| Novo modelo estruturado para documentos, com paragraph/horizontalRule/table | Solução correta para blocos reais | Exige política de migração, exportação, seleção, acessibilidade e reversibilidade | **Projetar separadamente** antes de divisor e tabela |

## Contrato da fatia de links

1. `href?:string` opcional em `RichTextRun`. O `body` original é a fonte textual; arquivos antigos continuam válidos.
2. Só URL absoluta HTTP(S), sem credenciais, espaços laterais ou controles; `new URL()` canonicaliza; máximo 2048 caracteres. `javascript:`, `data:`, `file:`, `mailto:`, URL relativa e `//exemplo` são rejeitadas.
3. A interface exige trecho realmente selecionado e URL válida. Mostra resposta legível. Inserir e remover funcionam, não há botão cenográfico.
4. No editor, apenas `<a>` criado pelo navegador é lido e transformado em metadado validado. A seleção é restaurada após foco no campo. Clicar no link durante edição não navega.
5. Na revisão, saída sempre com texto escapado e `href` escapada, `target="_blank" rel="noopener noreferrer"`. Nunca guardar ou renderizar HTML fornecido pelo usuário.
6. Alterar o link da redação modifica o conteúdo assinado por Socii e exige nova confirmação, sem mexer em votos nem Academia.
7. Testes: Node para URLs maliciosas, escapes, normalização, preservação e backup; Playwright para aplicar/remover, seleção, feedback, clique em edição, revisão, export/import, 280/320/390/740/1280 px em Chromium/Firefox/WebKit, sem overflow e erros JS.

## Próximas decisões obrigatórias

**Divisores:** criar tipo de bloco (`horizontalRule`), definir como representa `body` texto, revisão, documento concluído, importação e exportação; rejeitar `<hr>` solto em HTML. **Tabelas:** testar um protótipo isolado com esquema de bloco/linhas/células e avaliar tecnologia madura antes de escolher a dependência; não fingir persistência com HTML. **Formatação por parágrafo:** modelo de parágrafos/offsets versionados, operação sobre seleção, IME e recuo com teclado móvel, revisão da Megalos antes de fechar visual. Os modelos atuais para redação inteira não foram convertidos sem autorização.

## Gate

Pesquisa fundamenta a escolha, mas não garante resultado: qualquer afirmação de implementação ou compatibilidade depende do SHA e do teste real. Registros na checklist e no Drive são obrigatórios antes de encerrar a rodada.
