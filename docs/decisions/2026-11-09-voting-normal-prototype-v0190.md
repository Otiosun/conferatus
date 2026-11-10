# CONFFRATUS — Votação demonstrativa na navegação normal (checkpoint 142, 09/11/2026)

## Objetivo e regra máxima

Entrega da equipe: **protótipo funcional com dados totalmente fictícios**, não integração com o sistema central Academy. A Megalos cobrou uma **página de votação** que não estava representada pelos seis formulários escondidos em `?demo=1`. Não presumimos que a cobrança esteja integralmente atendida nem que a criação/administração institucional esteja especificada. Priorização autorizada pelo responsável: reduzir a maior lacuna funcional, com reutilização do mecanismo e sem reescrita.

Fontes oficiais conferidas em 09/11/2026: W3C/WAI <https://www.w3.org/WAI/tutorials/forms/>, <https://www.w3.org/WAI/tutorials/forms/grouping/> (fieldset/legend), <https://www.w3.org/WAI/tutorials/forms/labels/> (rótulos) e Playwright <https://playwright.dev/python/docs/locators>. Reutilizar os campos nativos e validação existente é mais seguro que reinventar controles ou instalar dependências. A referência visual original Megalos permanece preservada; nenhuma política eleitoral é assumida.

## Mudança limitada

- `src/main.ts`: botão **Abrir formulário de votação** na tela normal `#/ballot`, que abre o mesmo componente das seis modalidades (binária, nominal, ordenada, aprovação, escalar e cumulativa). Rótulo e aviso distinguem a demonstração do laboratório `?demo=1`; formulário permanece fechável, com foco coerente.
- No formulário cumulativo normal, uma cota **fixa e explicitamente fictícia de 5 unidades** torna o protótipo testável sem simular identidade ou conceder papel de diretor. O modo técnico avançado preserva a exigência de cotas por membro fictício já existente.
- Programações locais válidas agora têm botão para abrir o formulário contextual, mesmo sem `?demo=1`, preservando método/alternativas do agendamento. Os recibos e resumos são amostras apenas em memória da aba, isolados de resultados existentes e de qualquer backend.
- `src/styles.css`: apenas o botão de abertura, com altura mínima 44px e foco visível, mantendo a composição original até a abertura explícita.
- Teste `tests/browser_voting_normal_flow_v0190.py` incluído em `validate`; não altera a `main`, Cloudflare principal, Academy, PM2 ou bancos.
- Nenhum login ou permissão real, voto oficial, persistência compartilhada, apuração normativa ou confirmação institucional é implementado.

## Evidência e limitações

Uma cópia de teste do HTML offline de `bb14e32a` recebeu a mesma alteração lógica do TypeScript, para exercitar o novo fluxo antes de registrar o código na branch. Em Chromium local, **seis modalidades passaram** em 320, 390, 740 e 1280px, com confirmação/recibo e rejeição de cota cumulativa inválida. **Quatro entradas contextuais** da agenda (dados de sessão sintéticos) chegaram ao formulário correto e produziram recibo. O laboratório `?demo=1` permaneceu disponível. Nenhum overflow horizontal ou erro JavaScript foi observado nos casos amostrados. Esses ensaios não equivalem a uma compilação/CI do HEAD; apenas check confirmado do Cloudflare e execução CI no SHA correspondente permitem ampliar as conclusões.

O HTML local não deve ser representado como arquivo gerado pelo HEAD novo. Checkpoint 141 já contém a versão de referência anterior. Arquivar captura/roteiro local no Drive Komekko, rotulado como ensaio, e verificar build real antes de enviar o link à Megalos.

## Próximo critério

Concluir o design de página de votação que Megalos pediu (confirmar se era votar ou criar/administrar, a partir das referências), revisar roteiro de entrada normal, erros, teclado e estados de encerramento com fidelidade visual. Depois obter aceite D1–D6 e da página de votação. A checklist **permanece 33/57**; nem a Etapa 02 (registro institucional) nem Etapa 06 foram declaradas concluídas. Separar critérios oficiais fora do escopo no plano, sem marcar [x] artificial.
