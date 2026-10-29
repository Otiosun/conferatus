# CONFERATUS — Plano mestre de produção

Data: 28/10/2026 | Edição 1.0 | Escopo: primeira parte apresentada pela Megalos, não o aplicativo completo.

## 0. Mandato
Entregar o mais rápido possível um sistema institucional de votação e gerenciamento confiável, visualmente fiel, simples de manter, e que aceite novos módulos e integração com os sistemas da Academy. O padrão é: **preguiça inteligente + perfeccionismo verificável + entregas verticais pequenas**.

## 1. Inventário verificado
O pacote do WhatsApp possui 11 imagens de modelos, três PNGs auxiliares (`editar`, `rebaixamento`, `Painel`), um JSON com 16 registros de teste e descrição textual. Screenshots em 740×1600 pixels. Os 11 modelos representam aproximadamente estes fluxos, não 11 aplicativos: (1–3) tela de votação/resultados e estados do menu inferior; (4) diretório de membros; (5) histórico de votações de pessoa; (6–7) histórico de proposições e navegação; (8) visão geral; (9) painel de seções; (10) seção com membros; (11) entrada/edição de membro. Alguns rótulos e estados ainda estão em rascunho. As telas não são prova de que já haja backend ou regras fechadas.

O JSON contém `_id`, `__v`, `acdmId`, `cargos` e outros campos típicos de modelo de documento MongoDB/Mongoose; é **indício, não confirmação**, de base institucional pré-existente. Inclui dados pessoais: não colocar integralmente no Git, ambiente público ou navegador.

## 2. Decisão de arquitetura
**Padrão inicial:** React + Vite + TypeScript estrito, React Router, Tailwind, pequenos componentes próprios, shadcn/ui apenas para controles úteis, TanStack Query quando necessário, e Supabase/PostgreSQL para dados próprios e autenticação provisória **se não houver SSO institucional utilizável**. GitHub; dev/staging; preview em Cloudflare Pages ou serviço adequado às condições da contratação. Não exigir SSR, ORM, microserviços, filas, Redis, GraphQL, Redux ou PWA nesta fase.

**Fronteiras:** interface → serviços do domínio → `MemberProvider`, `BallotService`, `GovernanceService` → fontes de dados. `MemberProvider` terá adaptador `mock` de dados fictícios e, futuramente, adaptador HTTP para cadastro oficial. Não replicar nem alterar registro-mestre institucional sem acesso e acordo formal. Atuação com identidade externa deverá usar autenticação confiável; `acdmId` não autentica ninguém. Operações críticas no servidor/banco em transações, com autorização revalidada.

**Hospedagem:** Vercel Hobby não serve automaticamente como opção para projeto comercial remunerado; Supabase Free pode pausar por inatividade. Preview e produção são decisões de custo/risco distintas. Preferir conta/infra de propriedade institucional.

## 3. Modelo de dados conceitual
- `external_member`: identificador local, origem, `source_id`, `acdm_id`, campos públicos permitidos e possível snapshot mínimo, conforme necessidade. Só quando a integração exigir persistência; caso contrário consumir diretamente a fonte.
- `section`: seções e regras de visibilidade.
- `membership_role_history`: atribuições de cargos com período, autor e motivo; nunca sobrescrever fatos históricos.
- `proposal`: autores, seção, conteúdo, status, timestamps.
- `poll`: seção, proposta relacionada, estado, período, regras e autorização; `poll_option`.
- `ballot`/`vote`: vínculo com eleitor habilitado e opção, conforme voto identificado/anônimo. A privacidade deve ser definida antes do desenho físico.
- `audit_event`: ações administrativas e mudanças relevantes, com dados estritamente necessários e retenção definida.

Regras importantes a confirmar quando a implantação real chegar: quem é elegível; voto secreto ou nominal; possível alterar/cancelar voto; possibilidade de múltiplos votos; empates; encerramento e reabertura; quem enxerga totais; integração de identidade e origem oficial de cargos.

## 4. Primeiros checkpoints e entregas
**C0 — Fundamentos (primeira sessão):** repo privado, README, AGENTS.md, especificação da parte 1, mapa de rotas/estados, tokens visuais, pasta de referência, mocks anonimizados, execução local e lint/typecheck.

**C1 — Preview fiel (1 a 3 sessões focadas, meta operacional; não prazo contratual):** telas principais em mobile, navegação e estados, sem botões inertes, dados fictícios claramente marcados. Comparação lado a lado com as imagens; screenshots de viewport consistente. Entrega URL privada de preview.

**C2 — Um fluxo completo real:** autenticação de teste, membro de demonstração, seção, proposta/votação, emissão de voto permitida pelo servidor, contagem persistente, visualização do resultado; testes de voto duplicado, não autorizado e concorrência; nenhuma publicação institucional real ainda.

**C3 — Administração e histórico:** lista de seções, membros, edição permitida, rebaixamento sem perda do histórico, trilha de auditoria; testes cruzados de perfis.

**C4 — Endurecimento e entrega da parte 1:** fluxos pendentes resolvidos, responsividade e acessibilidade revisadas, privacidade, backups, migrations, correção dos bugs encontrados, entrega validada com a cliente. Os modelos futuros entram em novas fatias, sem reescrever as antigas.

O esforço da primeira parte completa ainda não pode ser prometido em dias. O protótipo visual pode ser rápido, mas votos e acesso institucional requerem segurança e regras definidas.

## 5. Ciclo rápido por fatia
1. Compreender uma tela/ação + cenário real.
2. Escrever 2–5 critérios verificáveis (visual, estado, permissão, erro).
3. Implementar UI usando dados/mock da camada de serviço.
4. Ligar a implementação real onde a regra está definida.
5. Rodar `typecheck`, `lint`, teste unitário/funcional; Playwright com viewport de celular e desktop; screenshot/overlay contra referência.
6. Revisar código, reduzir duplicação, confirmar que não alterou comportamentos antigos.
7. Publicar preview, colher uma aprovação objetiva, registrar checkpoint.

**Paralelização segura:** visualização e dados podem avançar em tarefas distintas se tiverem contrato de resposta estável; não alterar o mesmo componente e os mesmos arquivos de esquema simultaneamente. IA é ferramenta de implementação e revisão, não fonte de verdade do produto.

## 6. Layout e qualidade visual
- Respeitar composição, paleta azul/lavanda/cinza dos modelos, conteúdo, hierarquia, rodapé e painéis inferiores; extrair tokens com a referência, sem copiar pixels JPEG como medidas CSS cegamente.
- Design mobile-first, mas validar também desktop. Estados: vazio, carregando, erro, sucesso, acesso negado, tela longa, texto longo e dados reais.
- Sem gradiente inventado, dashboard genérico, skeleton decorativo ou cards só por estética.
- Revisão por screenshot comparativo e checklist humano; não aceitar um percentual mágico de similaridade como prova.
- Acessibilidade: teclado, foco visível, contraste WCAG, rótulos, tamanho utilizável de áreas de toque, feedback não exclusivamente por cor.

## 7. Segurança, privacidade e integridade
- Supabase: RLS e grants por tabela exposta; testar os casos de allow/deny. Chaves privilegiadas apenas no servidor. Funções `security definer` só se inevitáveis, com search_path explícito e EXECUTE restrito.
- Voto: chave de unicidade apropriada **somente após confirmar a regra**, checagem de elegibilidade e encerramento no servidor, transação atômica e idempotência; resultados calculados a partir da fonte de verdade.
- Papel de diretor: derivação de fonte confiável e verificações de autorização em toda ação. UI não é mecanismo de segurança.
- API externa: versionar contrato `/api/v1` apenas quando houver consumidores externos reais; documentar com OpenAPI; não expor banco nem credencial administrativa como suposto contrato.
- Privacidade: LGPD, minimização de dados, retenção/remoção conforme responsabilidade de quem controla os dados, dados de teste fictícios, logs sem PII e controle de acesso nos históricos.
- Operação: ambientes separados, secrets no provedor, dependências fixadas, migrations e rollback de app, política de backup e restauração ensaiada.

## 8. Definition of Done (gates)
**Visual:** comparação com imagem aprovada; mobile e desktop; estados vazios, erros e carregamento; acessibilidade básica.
**Funcional:** cada ação opera, rejeita entradas inválidas e mostra feedback; não há números fictícios apresentados como reais.
**Dados:** migração reproduzível; invariantes no banco; auditoria e histórico preservados.
**Segurança:** autenticação e autorização testadas para usuário comum, diretor e não autenticado; exposição de dados pessoais inspecionada.
**Operação:** build e testes passam; preview demonstrável; instruções de recuperação e limites conhecidos escritos.

Os gates para votar, mudar cargos, autenticar e acessar dados sensíveis são **bloqueadores absolutos** de produção. Melhor entregar preview parcial claro que sistema inseguro rotulado como concluído.

## 9. Estrutura de repositório
```
conferatus/
├── AGENTS.md
├── README.md
├── package.json
├── pnpm-lock.yaml
├── src/
│   ├── app/             # Bootstrap e rotas
│   ├── components/      # UI reutilizável
│   ├── styles/          # tokens e CSS global
│   ├── modules/
│   │   ├── members/     # modelos, MemberProvider, páginas
│   │   ├── voting/      # regras, serviços e páginas
│   │   └── governance/  # diretoria, cargos e auditoria
│   └── lib/             # cliente, validação, utilitários
├── supabase/
│   ├── migrations/
│   └── tests/
├── tests/
│   ├── e2e/
│   └── visual/
└── docs/
    ├── SPEC_PART_1.md
    ├── decisions/
    ├── integration/
    └── checkpoints/
```

## 10. Método de colaboração
Uma branch/PR por fatia e uma pessoa/agente responsável por cada mudança. `main` sempre compilando. CI mínima: instalação com lockfile, lint, `tsc --noEmit`, testes de regras e fumaça; testes de RLS/migração quando presentes. Não dar deploy de banco remoto por mudanças manuais de painel. Checkpoints com screenshot e resultado dos testes, não com relato genérico de progresso.

## 11. Fontes verificadas (seleção)
- Vite: https://vite.dev/guide/
- React Router: https://reactrouter.com/start/modes
- Supabase RLS: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase SQL functions: https://supabase.com/docs/guides/database/functions
- Supabase migrations: https://supabase.com/docs/guides/deployment/database-migrations
- Supabase auth externa: https://supabase.com/docs/guides/auth/third-party/overview
- Playwright visual: https://playwright.dev/docs/test-snapshots
- Playwright devices: https://playwright.dev/docs/test-projects
- shadcn: https://ui.shadcn.com/docs/new
- Vercel Hobby: https://vercel.com/docs/limits/fair-use-guidelines
- Cloudflare Pages React: https://developers.cloudflare.com/pages/framework-guides/deploy-a-react-site/
- Supabase Free: https://supabase.com/docs/guides/platform/free-project-pausing
- WCAG 2.2: https://www.w3.org/TR/wcag/
- ANPD privacidade: https://www.gov.br/saude/pt-br/acesso-a-informacao/lgpd/principios
- Mongoose docs: https://mongoosejs.com/docs/guide.html
- OpenAPI: https://spec.openapis.org/oas/
- AI instructions: https://learn.chatgpt.com/docs/agent-configuration/agents-md

## 12. Estado honesto
Planejamento e pesquisa feitos. Nenhum repositório do CONFERATUS foi criado ou conectado neste trabalho; não há código funcional nem teste executado do CONFERATUS. A parte 1 é conhecida visualmente, mas as regras finais do ato de votar e da autenticação não foram enviadas. Não trocar estes fatos por promessas de prazo.
