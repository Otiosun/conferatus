# CONFFRATUS — prévia institucional

Aplicação em desenvolvimento a partir dos modelos da Megalos para a Academy. **Nome exibido na prévia: CONFFRATUS**, conforme correção solicitada pelo responsável no chat de 02/11/2026. A grafia CONFERATUS aparece em referências históricas e caminhos técnicos legados; essas fontes são preservadas. O aceite formal da Megalos continua pendente, assim como a eventual troca de domínio/repositório.

Endereço técnico existente: **https://conferatus.pages.dev** (domínio legado, não renomeado nem redirecionado).

## O que existe

- Diretório e perfis de membros fictícios, seções deliberativas CINSTIA, histórico demonstrativo e ações administrativas simuladas.
- Cada perfil fictício possui um link por ACDM ID sintético (`#/profile/acdm/DEMO-0002`), utilizado apenas como referência de cadastro na prévia. Um identificador não autentica ninguém nem concede permissão.
- Fluxo demonstrativo de votação e registros, sem integração institucional.
- Elaboração de proposições, salvamento de rascunhos na sessão quando disponível e confirmação de redação.
- Socii com participantes de demonstração e progresso de conclusão; não envia convites reais.
- Calendário mensal, seleção de dias, agendamento demonstrativo, acesso à proposição associada e consulta somente de leitura ao histórico de programações canceladas **desta sessão**. Não há trilha de auditoria institucional. Na sessão fictícia, também é possível navegar da programação ao perfil da autora demonstrativa e do perfil/proposição à programação ativa; itens cancelados deixam de aparecer como ativos.

**Não é um sistema de votação real:** não há autenticação Academy, banco de dados compartilhado, cadastro institucional nem colaboração entre contas. Os dados de exemplo são sintéticos. As alterações ficam apenas no navegador e podem desaparecer ao encerrar a sessão. O ACDM ID na interface não comprova identidade.

## Desenvolver

Node 20+ e TypeScript. O frontend é intencionalmente simples: **HTML, CSS e TypeScript**, sem framework, bundler de terceiros ou dependências de execução.

```bash
npm install
npm run build
npm run serve
```

- `npm run build`: compila TypeScript, monta a prévia independente e executa os testes Node.
- `npm test`: executa o mesmo build com testes.
- `dist/CONFFRATUS_demo_offline.html`: arquivo independente (a versão `CONFERATUS_demo_offline.html` também é gerada como alias de compatibilidade) para testar o protótipo. Alguns navegadores restringem JavaScript ou sessionStorage ao abrir arquivos locais.
- `publish/index.html`: artefato estático usado pela Cloudflare Pages.
- `?demo=1`: ferramentas de simulação adicionais para desenvolvimento; não correspondem a permissões reais da Academy.

Testes adicionais de navegação ficam em `tests/browser_*.py` e requerem Playwright Python + Chromium. Para executar a jornada de fumaça **atualizada e ativa** depois do build: `python tests/browser_smoke.py` (320, 390, 740 e 1280 px). Ela percorre votação **fictícia**, menu/teclado, perfis, histórico, permissões **simuladas**, calendário e editor; não verifica autenticação Academy, servidor ou persistência compartilhada. A matriz completa de navegadores e os limites de ambiente constam da checklist e do checkpoint mais recente. A publicação Cloudflare usa apenas `npm run build` e **não** executa automaticamente as suítes Python Playwright.

## Deploy

GitHub privado, Cloudflare Pages conectado ao repositório:

| Configuração | Valor |
| --- | --- |
| Framework | None |
| Branch de produção | `main` |
| Comando de build | `npm run build` |
| Pasta de saída | `publish` |
| Diretório-raiz | `/` |

Não existem segredos de autenticação para a prévia estática. Testar primeiro na branch de preview; promover a `main` somente após build e regressões aprovados.

## Manutenção e próximas etapas

- **`docs/CHECKLIST_MESTRA.md`**: roteiro oficial, estado de cada etapa e pendências.
- **`docs/DEMO_GUIDE.md`**: roteiro vigente para demonstrar a experiência, separar recursos locais dos institucionais e recolher decisões da Megalos.
- **`AGENTS.md`**: leis de código humano, preguiça inteligente, fidelidade ao material e entregas verificáveis.
- **`docs/MODELOS_31_10_NOVAS_TELAS.md`**: descrição dos seis modelos novos e do vídeo de calendário/proposições/Socii.
- **`docs/CHECKPOINT_V012_2026-11-01.md`**, **`docs/CHECKPOINT_V013_2026-11-01.md`** e **`docs/CHECKPOINT_V014_2026-11-01.md`**: registros recentes dos fluxos testados.

O sistema de login já pertence à Academy. O responsável por ele poderá integrar a identidade e os acessos posteriormente. Não criar outro login independente sem decisão explícita. Regras institucionais de deliberação e registro permanecem sujeitas à definição da Megalos.
## Fronteira de identidade Academy (prévia v0.10.49)

O arquivo `src/domain/academy-identity.ts` define `AcademyIdentityProvider`, uma interface assíncrona para **consultar uma referência institucional já autenticada pelo sistema da Academy**. A prévia usa `UnconnectedAcademyIdentityProvider`, que retorna `unavailable`: não há login, token, sessão nem permissão real. O ACDM ID é apenas referência, **nunca autorização**.

O painel `?demo=1` exibe o estado indisponível e distingue as permissões demonstrativas. A integração futura exige um adaptador de responsabilidade da Academy e autorização **verificada no servidor**, sob contrato aprovado. Nenhuma consulta a serviço real ou dado de produção ocorre nesta prévia.

### Recuperação de cancelamento na prévia

Quando o navegador não consegue salvar um cancelamento, ele permanece aplicado **somente nesta aba**. O calendário avisa explicitamente que o registro poderá voltar ao estado anterior ao recarregar e oferece **Tentar salvar cancelamento nesta sessão**. Esta tentativa não reativa registros nem cria uma trilha de auditoria institucional; a gravação continua sendo apenas `sessionStorage` e depende das permissões e limites do navegador.

### Gravação de alterações na prévia

As proposições, confirmações de autoria e Socii e programações usam exclusivamente `sessionStorage` do navegador. Se a gravação falhar, o projeto não considera o registro persistido: avisa que a mudança está apenas na aba e oferece **Tentar salvar alterações nesta sessão**. O cancelamento de programação mantém sua mensagem e recuperação próprias. **Não recarregue antes de salvar novamente** se quiser preservar um registro temporário que falhou; este mecanismo não é backup, sincronização, autenticação ou histórico institucional.

## Cópia local dos fluxos de demonstração (v0.10.58)

Na tela **Proposições e Socii**, abra a prévia com `?demo=1` para usar **Baixar cópia JSON** e **Restaurar cópia JSON**. O arquivo contém exclusivamente proposições, participantes Socii sintéticos e programações desta aba; não contém login, votos, tokens ou permissões da Academy. O arquivo **pode conter textos que você escreveu** e não é criptografado — não o compartilhe inadvertidamente.

A restauração exige confirmação e **substitui**, não mescla, os fluxos locais atuais. Antes de restaurar, exporte uma cópia do estado atual. Arquivos incompatíveis, duplicados ou com registros inválidos são recusados sem mudar o estado. Se a gravação da sessão falhar, os registros anteriores permanecem na aba. Não há servidor, sincronização entre contas nem recuperação automática de arquivos perdidos.

## Modalidades de deliberação (prévia v0.10.59)

A Megalos definiu em 03/11/2026 seis modalidades de votação: **Binária (Sim/Não), Nominal (escolha única), Ordenada (ranqueamento), Por aprovação (múltiplas opções), Escalar (1–10 por alternativa) e Cumulativa (cota proporcional de votos distribuídos)**. Na prévia, essa modalidade é escolhida ao programar deliberações e é armazenada com a agenda fictícia. Não substituir PDR/PR/Ofício, que classificam a proposição.

Em Gerenciamento Deliberativo, é possível informar uma quantidade positiva e inteira de votos cumulativos por membro sintético ao editar ou vincular um registro. Nenhum valor é atribuído automaticamente. Ainda não é cadastro real de usuários Academy nem voto compartilhado; apuração, elegibilidade, pesos institucionais, quórum e empates dependem de definição e integração seguras.


## Votação SQL experimental — SOMENTE CI isolada

Arquivos em experimental/postgres/ e tests/postgres/ formam um laboratório de PostgreSQL 16 que não é incluído no build estático, nem publicado no Cloudflare Pages e nem executado no banco da Academy. O workflow Preview voting checks inicia um contêiner PostgreSQL novo, executa os scripts com dados sintéticos e descarta o contêiner no final. A prévia pública continua sem acesso ao banco.

O laboratório exige liberação explícita de uma votação fictícia (fixture_enabled false por padrão), cadastro sintético prévio dos participantes e estado open. A função de gravação usa uma trava transacional na linha da votação, chave idempotente por votação, unicidade por participante fictício e uma escrita de auditoria na mesma transação. As seis modalidades são validadas de novo no banco. Os registros são somente de teste e não estabelecem fórmula para vencedor.

A função é restrita ao papel NOLOGIN conffratus_lab_gateway, que tem apenas USAGE no esquema e EXECUTE na função. Não possui SELECT ou INSERT direto nas tabelas; a concessão de acesso ao papel para contas reais não faz parte do projeto. O argumento actor_ref é um valor sintético do teste: **não pode ser aceito como identidade autenticada no mundo real**. Um gateway futuro precisará validar sessão, pertencimento, autorização, elegibilidade e decisão institucional no servidor antes de considerar qualquer fluxo real.

**Proibido aplicar este script a produção sem uma migração aprovada e validação de segurança.** A regra laboratorial de uma amostra por participante não significa que a Megalos aprovou proibição de alteração, identificação do voto, quota ou qualquer outro parâmetro oficial.
