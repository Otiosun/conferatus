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
- **`AGENTS.md`**: leis de código humano, preguiça inteligente, fidelidade ao material e entregas verificáveis.
- **`docs/MODELOS_31_10_NOVAS_TELAS.md`**: descrição dos seis modelos novos e do vídeo de calendário/proposições/Socii.
- **`docs/CHECKPOINT_V012_2026-11-01.md`**, **`docs/CHECKPOINT_V013_2026-11-01.md`** e **`docs/CHECKPOINT_V014_2026-11-01.md`**: registros recentes dos fluxos testados.

O sistema de login já pertence à Academy. O responsável por ele poderá integrar a identidade e os acessos posteriormente. Não criar outro login independente sem decisão explícita. Regras institucionais de deliberação e registro permanecem sujeitas à definição da Megalos.
## Fronteira de identidade Academy (prévia v0.10.49)

O arquivo `src/domain/academy-identity.ts` define `AcademyIdentityProvider`, uma interface assíncrona para **consultar uma referência institucional já autenticada pelo sistema da Academy**. A prévia usa `UnconnectedAcademyIdentityProvider`, que retorna `unavailable`: não há login, token, sessão nem permissão real. O ACDM ID é apenas referência, **nunca autorização**.

O painel `?demo=1` exibe o estado indisponível e distingue as permissões demonstrativas. A integração futura exige um adaptador de responsabilidade da Academy e autorização **verificada no servidor**, sob contrato aprovado. Nenhuma consulta a serviço real ou dado de produção ocorre nesta prévia.

### Recuperação de cancelamento na prévia

Quando o navegador não consegue salvar um cancelamento, ele permanece aplicado **somente nesta aba**. O calendário avisa explicitamente que o registro poderá voltar ao estado anterior ao recarregar e oferece **Tentar salvar cancelamento nesta sessão**. Esta tentativa não reativa registros nem cria uma trilha de auditoria institucional; a gravação continua sendo apenas `sessionStorage` e depende das permissões e limites do navegador.
