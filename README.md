# CONFERATUS — prévia institucional

Aplicação em desenvolvimento a partir dos modelos da Megalos para a Academy. **A grafia oficial ainda precisa ser confirmada** (CONFERATUS/CONFFRATUS); não renomear o código ou o domínio sem essa confirmação.

Prévia pública: **https://conferatus.pages.dev**.

## O que existe

- Diretório e perfis de membros fictícios, seções deliberativas CINSTIA, histórico demonstrativo e ações administrativas simuladas.
- Fluxo demonstrativo de votação e registros, sem integração institucional.
- Elaboração de proposições, salvamento de rascunhos na sessão quando disponível e confirmação de redação.
- Socii com participantes de demonstração e progresso de conclusão; não envia convites reais.
- Calendário mensal, seleção de dias, agendamento demonstrativo e acesso à proposição associada.

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
- `dist/CONFERATUS_demo_offline.html`: arquivo independente para testar o protótipo. Alguns navegadores restringem JavaScript ou sessionStorage ao abrir arquivos locais.
- `publish/index.html`: artefato estático usado pela Cloudflare Pages.
- `?demo=1`: ferramentas de simulação adicionais para desenvolvimento; não correspondem a permissões reais da Academy.

Testes adicionais de navegação ficam em `tests/browser_*.py` e requerem Playwright Python + Chromium. Os scripts mais recentes cobrem CINSTIA, rascunhos, calendário, perfis e Socii. Testes antigos podem refletir estados anteriores do menu; consultar o checkpoint mais recente.

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