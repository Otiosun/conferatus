# CONFFRATUS — CP144 | Build local do HEAD exato e regressões de votação (10/11/2026)

## Problema e método de menor custo

O workflow `Preview voting checks` permanecia sem execução integral na branch privada. Testes anteriores sobre HTML instrumentado não demonstravam compilação da versão GitHub atual. Em vez de abrir novamente o repositório, cadastrar pagamento ou insistir em reruns, o código do commit `47069280fc93165edab9cd53751c0da0abfb10d3` foi reconstruído **localmente** por meio dos arquivos recuperados com o conector GitHub.

A árvore do commit foi consultada, as **44 fontes textuais necessárias** foram transferidas em partes privadas, conferindo o SHA Git blob de **cada arquivo**, e os **quatro PNGs** extraídos do HTML de referência anterior tiveram seus SHA Git blob novamente comparados com a árvore atual. Assim, **48/48 arquivos** usados no build coincidem com os arquivos do commit. Não houve patch local ou modificação de código para conseguir aprovação. Dependências de runtime continuam vazias. Snapshot privado foi preservado em Komekko.

## Execuções concluídas no build real

- `npm run build` no ambiente Node **22.16.0**, TypeScript **5.8.3**: TypeScript compilado, arquivos estáticos/standalone gerados, **73/73 testes Node aprovados**, nenhum erro ou falha.
- HTML offline resultante, SHA-256: `16ea03aaed5ea23f38ae6138371383dc2585756531dab3fb83c77f6b66630597` (arquivo incluso no ZIP de QA).
- `tests/browser_voting_normal_flow_v0190.py`, Playwright Chromium local: **PASS em 320, 390, 740 e 1280 CSS px**; seis modalidades, validações, erro cumulativo, recibo, reabertura, quatro entradas contextualizadas calendário→votação e laboratório avançado preservado.
- `tests/browser_full_workflow_journey_v0173.py`: **PASS em quatro larguras**, percorrendo perfil→proposição→Socii→revisão→calendário→votação.
- `tests/browser_calendar_return_v0120.py`: **PASS** em quatro larguras.
- `tests/browser_smoke.py`: **PASS** em quatro larguras, com navegação, formulários, perfil, gerenciamento e estados de volta.
- `tests/browser_stage7_short_viewport_v0187.py`: **48/48** cenários de altura/viewport + seis jornadas de menu com teclado, sem JS errors ou overflow horizontal nos casos verificados.
- `tests/browser_stage7_focus_not_obscured_v0188.py`: **192 amostras** de foco/teclado nas rotas/larguras examinadas, sem obstrução completa observada.
- Captura visual da página de votação em 390 px foi examinada; o laboratório demonstrativo permanece visualmente separado do resultado fictício preexistente. Não alterar hierarquia/modelo da Megalos sem aceite.

As APIs Playwright `page.set_content` e `page.goto` têm características distintas: ver documentação oficial https://playwright.dev/python/docs/api/class-page#page-set-content e https://playwright.dev/python/docs/navigations . O browser Chromium deste ambiente devolve `net::ERR_BLOCKED_BY_ADMINISTRATOR` para `http://127.0.0.1`, portanto a execução HTTP real local não pôde ser atestada; as suítes aprovadas usaram `page.set_content` no HTML compilado. Isso **não** invalida os ensaios funcionais, mas mantém a limitação de origem, armazenamento real e navegação de rede.

## Estado da distribuição e artefato

- No SHA exato `47069280`, check **Cloudflare Pages = success**, sem comprovação de carregamento da URL no celular. O endereço da prévia não respondeu por esta ferramenta de leitura de páginas.
- GitHub Actions run `42746530965`: `postgres-lab` failure, `validate` skipped, `cross-browser-lab` skipped. **Não existe CI integral verde para esse SHA**. Não confundir um deploy Cloudflare com aprovação do workflow.
- ZIP privado com **HTML compilado real, scripts de QA, logs, manifesto e capturas**: https://drive.google.com/file/d/1mGNuYvpaQ3xoTiQZ_lHGCdkZ4eIjjoDn/view
- SHA-256 ZIP: `af6c857fa6f5ed2df7d37914ef6403fdfd66be72f521569906c27e30e517fb8a`.

## Política de escopo e próximos gates

Nosso entregável é **protótipo funcional integralmente fictício**, não autenticação institucional, registro oficial de votos, backend de contas ou transações da Academy. Sem presumir regras de voto. As decisões visuais Megalos D1–D6, a aceitação expressa da página de votação e a verificação em Android real continuam pendentes. A Etapa 07 também não recebeu certificação WCAG 2.2 AA completa. Checklist **33/57** mantida. Nenhuma alteração em `src`, `tests`, `main`, Cloudflare principal, Academy ou produção foi necessária neste checkpoint; a documentação é o único commit novo.

**Próxima ação de maior valor:** reunir aceite da Megalos para a variante de página de votação e decisões D1–D6, validando o link de prévia no aparelho. Resolver somente diferenças comprovadas, depois fazer a QA final e solicitar aprovação explícita para publicação.
