# CP158 — Validação da redação e retomada de rascunhos (10/11/2026)

Base: branch privada `preview/v0.10.60-six-vote-forms`, parent `35811dd05c757d9c81385236ad3f5ed0e5760b6f`. Escopo apenas de proposições fictícias, sem alteração de votação, Academy, main ou produção.

## Problema e correção
A ação “Concluir redação” podia retornar silenciosamente quando o título, após remoção de espaços externos, tinha menos de 3 caracteres. O editor tinha validação do corpo em dois pontos e dependia de `reportValidity()` para certos estados, com mensagens diferentes entre editor simples e formatado.

O formulário de redação passa a tratar validação de título/corpo explicitamente no evento de envio, mesmo quando os campos têm restrições HTML para descrever o contrato. A conclusão exige título com ao menos 3 caracteres e texto com ao menos 20; mostra mensagem inline com `role=alert`, aponta `aria-invalid` apenas para o campo pertinente, restaura foco e não perde texto digitado. “Salvar rascunho” **continua permitindo conteúdo incompleto**, mas nunca vazio. O aviso de sucesso agora explicita que o rascunho foi salvo só nesta aba.

## Teste novo
`tests/browser_compose_validation_v0205.py` exercita título com espaços, mensagem/foco, corpo curto, salvamento parcial e retomada de sessão a partir dos registros locais, depois revisão com texto completo, em 320/390/740/1280px. Incluído na matriz de testes da branch. Revisões anteriores v011 (múltiplos rascunhos), v0155 (falha de gravação), v0163 (editor rico), v0172 (saída sem salvar), v0115 (restauração) permanecem.

Fontes técnicas consultadas em 10/11/2026: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation (limites do `reportValidity` e entradas alteradas programaticamente); https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/minlength (restrição conta unidades UTF-16, não `trim`); https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event (aviso não confiável em celulares). Adotada validação explícita + sessão local existente, sem pacote nem autosave implícito.

## Gates
**Novo teste ainda não executado localmente.** Conferir Cloudflare no SHA exato, mas não confundir build remoto com provas Playwright/Android físico. PF-11/PF-12 permanecem abertos enquanto não houver evidências de navegador e feedback de persistência. Histórico 43/57 e funcional 8/38 inalterados; aprovação Megalos D1–D6 intacta.
