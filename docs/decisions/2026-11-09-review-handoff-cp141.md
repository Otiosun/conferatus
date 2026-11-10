# CONFFRATUS — Checkpoint 141 | Pacote de revisão demonstrativa (09/11/2026)

## Objetivo e gates

Preparar um pacote de demonstração **sem promover a versão para produção** e sem confundir deploy de preview com homologação. Prioridade: entrega verificável a Megalos para coletar D1/D1b–D6, sem continuar acrescentando testes genéricos. Nenhum conteúdo privado original da Megalos foi incluído no ZIP; o único HTML deriva do bundle demonstrativo com dados fictícios.

## Evidências exatas

- GitHub `Otiosun/conferatus` PRIVADO, branch `preview/v0.10.60-six-vote-forms`. Status GitHub `Cloudflare Pages: success` constatado no commit `fafae4a35eba298010307a54872df1ab383946c8` em 09/11/2026. **A navegação ao endereço online não pôde ser verificada no ambiente atual**, logo o check de deploy não equivale a visita real.
- O commit `bb14e32a454cb2218a86e39abdf7fb2b41b83870` gerou o HTML arquivado no run [42708774184](https://github.com/Otiosun/conferatus/actions/runs/42708774184), tentativa 2, com `postgres-lab` e `cross-browser-lab` aprovados, mas `validate` reprovado. Diff GitHub de `bb14e32` até `fafae4a`: 11 commits em testes, workflow e documentos, **sem alteração em `src/`, HTML principal, estilos, scripts ou assets**.
- HTML original SHA-256: `ced554c4c58e68a0543c475d74da04a44ccb568cd948bd6ee9f6e0e97bcd85fa`. Cópia original, sem reescrita, já preservada no [Drive Komekko](https://drive.google.com/file/d/1h0wb4ug6C2UFSLvRvD0aOGoJQyTYU6CF/view).
- Jornada E2E local de revisão sintética: Chromium, 4 larguras **320, 390, 740 e 1280 CSS px**; perfil → redação/salvamento → convite Socii fictício → revisão → confirmação fictícia → agendamento local → tela de votação demonstrativa. **4/4 PASS**, sem pageerrors ou overflow lateral nos estados inspecionados. O armazenamento foi simulado em memória pelo harness, como nos testes do projeto; o browser desta infraestrutura impediu `localhost` com `ERR_BLOCKED_BY_ADMINISTRATOR`. Não declarar execução HTTP positiva.
- ZIP de revisão local `CONFFRATUS_KIT_REVISAO_CP141.zip`, com `CONFFRATUS_demo_offline.html`, `LEIA_PRIMEIRO.txt`, `MANIFESTO_QA.json`; `ZipFile.testzip()` PASS, bytes HTML conferidos. SHA-256 do ZIP: `3049c11b3171a993f4ba24aa779eb70463427da3de95ba2359bbf8e90025db89`. O ZIP também foi arquivado no [Drive Komekko privado](https://drive.google.com/file/d/1gJpV7_kUhWackSB2eishb2c-w9iHanZ7/view), além de estar disponível neste chat. O HTML original está no Drive Komekko.
- Roteiro de demonstração `docs/DEMO_GUIDE.md` corrigido no commit `b506b213a2e3bd1b5f6ac5fb33beeeba92849dcf`: substituição do estado desatualizado `CI #39 aprovada` pela distinção clara entre Cloudflare success no commit observado, Actions sem aprovação integral, QA sintético e aceite pendente.

## Pesquisa e alternativas (Lei 21)

Cloudflare explica o alias de prévia e o isolamento do domínio principal:
https://developers.cloudflare.com/pages/configuration/preview-deployments/
https://developers.cloudflare.com/pages/configuration/git-integration/

MDN explica que `sessionStorage` pode lançar `SecurityError` em origem `file:`:
https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage

Decisão: preferir URL de preview para avaliação em celular, com conferência direta antes de envio; para inspeção offline em computador, fornecer HTML e instruções de servidor **apenas local** `python -m http.server 8765 --bind 127.0.0.1`. Não publicar uma cópia da plataforma, não reescrever frontend, não confundir arquivo aberto diretamente com o ambiente HTTPS.

## Pendências reais

D1/D1b–D6 sem resposta; documento de homologação **já existe**, não duplicar: https://docs.google.com/document/d/1RFp2s-QzzigkQRDBhej_QIVr7bxYB7yhCvBWD7TERDw/edit . Não enviar mensagens automaticamente à Megalos. A Academy ainda deve definir contratos e regras de integração real. O HEAD pós-documentação precisa de CI aprovada quando possível; nenhum GitHub Actions antigo certifica o HEAD novo. Sem autorização para merge na `main` nem publicação de produção.

Checklist mantida em **33/57**: o pacote não fecha sozinho o gate de entrega, nem 07.05/07.06/07.10/07.11/07.12.

**Próximo passo com maior retorno:** apresentar o preview e o formulário existente para decisão Megalos; processar decisões recebidas; manter os gates de integração com a Academy separados. Evitar esforço cosmético antes de aprovação.
