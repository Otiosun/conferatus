# CONFERATUS — Leis máximas de engenharia

> **Retomada obrigatória (01/11/2026):** consultar `docs/CHECKLIST_MESTRA.md` antes de iniciar qualquer tarefa e atualizá-la após os testes. A implementação atualmente mantida usa TypeScript, HTML e CSS sem framework; as sugestões antigas de React/Vite abaixo são históricas e **não autorizam reescrita**. Priorizar código humano, natural e legível, preguiça inteligente, fidelidade ao material da Megalos, revisões pequenas e distinção explícita entre simulação e funcionamento integrado.

Versão 1.0 — 28/10/2026. Este arquivo foi preparado para virar `AGENTS.md` na raiz do repositório. Leis válidas para humanos e agentes de IA. Uma exceção exige justificativa em `docs/decisions/` e aprovação explícita do responsável técnico.

## Constituição
1. **Preguiça inteligente.** Antes de criar código, procure recurso nativo, componente próprio, função existente e solução mais simples. Não implemente infraestrutura que já seja provida com segurança.
2. **Perfeccionismo verificável.** Não chame algo de concluído sem funcionamento observado, testes pertinentes e revisão visual. Perfeição não é polimento infinito: é cumprir integralmente critérios objetivos.
3. **Uma fonte de verdade por dado.** Cadastro institucional deve manter seu dono; CONFERATUS controla apenas seus dados de deliberação. IDs externos não são prova de autenticação.
4. **Nenhuma suposição de regra institucional.** Elegibilidade, voto secreto/identificado, alteração de voto, encerramento, empate e visibilidade precisam de definição antes de implementar lógica definitiva.
5. **Sem código cenográfico.** Botões clicáveis sem ação, valores fixos representados como reais, URLs quebradas, controles inertes e testes falsos são proibidos.
6. **Fidelidade visual.** Referências da Megalos são fonte de design. Preservar hierarquia, proporções, paleta, tipografia e estados; mudanças não previstas precisam de validação.
7. **Simplicidade estrutural.** Monorepositório simples, TypeScript estrito, módulos por domínio; sem microserviços, monorepo com muitos pacotes, ORM ou gerenciador global de estado sem necessidade demonstrada.
8. **Integração por fronteiras.** UI nunca lê o JSON bruto nem depende diretamente do esquema externo. Expor modelos públicos/DTOs e interfaces de fonte de dados.
9. **Segurança no servidor/banco.** Verificar autorização de leitura e escrita em cada operação; esconder botão é somente UX. RLS/grants, validação no limite de confiança e checagens de dono/perfil são obrigatórios.
10. **Integridade transacional.** Voto, encerramento, mudança de cargo e auditoria devem ser atômicos e seguros contra concorrência, tentativas duplicadas e repetição de requisições.
11. **Histórico preservado.** Rebaixamento/desligamento não apaga fatos institucionais. Registrar autoria, momento e estado relevante de cada evento.
12. **Privacidade por padrão.** Menor volume possível de dados pessoais; anonimizar fixtures; sem telefones, mensagens privadas, tokens ou arquivo-fonte real no bundle, logs ou repositório público.
13. **Uma dependência precisa pagar aluguel.** Só instalar pacote quando ganho de manutenção/tempo justificar custo. Preferir componentes próprios quando a abstração externa atrapalhar o design.
14. **Pequenas entregas verificáveis.** Uma alteração = objetivo delimitado, critério de aceite, execução do projeto, testes aplicáveis, revisão e commit/PR. Não misturar refatoração com recurso novo sem motivo.
15. **Nada de achismo sobre conclusão.** Informar o que foi executado, evidências, falhas, limitações e próximo trabalho. Não inventar testes, tempos, integrações ou conformidade.
16. **Não refazer o que funciona.** Mudanças novas devem preservar contratos e cenários antigos; quebrar compatibilidade exige migração/documentação explícitas.
17. **Acessibilidade e responsividade são requisitos.** Teclado, foco visível, contraste, feedback de erros/carregamento, dispositivos móveis e rótulos legíveis.
18. **Publicar sem sustos.** Dev/staging/prod separados, secrets fora do Git, migrations versionadas, backup/restauração testável, controle de versão e rollback documentado.
19. **Sem sobreengenharia em antecipação.** Pontos de extensão pequenos e reais; não criar plugins, eventos distribuídos, abstrações de banco e escalabilidade imaginária para cenários hipotéticos.
20. **Qualidade proporcional ao risco.** Desenhos experimentais podem ser protótipos; voto, autenticação, permissão, cargo e dados pessoais nunca são protótipos disfarçados de produção.

## Stack de partida
- TypeScript strict, React, Vite, React Router (modo simples), Tailwind.
- shadcn/ui somente onde poupar trabalho e puder ser restilizado fielmente.
- TanStack Query quando houver sincronização de dados assíncronos.
- Supabase/PostgreSQL para dados próprios do CONFERATUS, provisoriamente; compatibilidade com cadastro institucional via `MemberProvider`.
- Operações críticas por função transacional no Postgres ou endpoint de servidor; nunca implementação exclusiva no cliente.
- Vitest para lógica e Playwright para jornadas mobile, visual regression e autorizações.
- Publicação de preview como frontend estático; hospedar produção apenas após revisão de requisitos e custos.

## Processo obrigatório por tarefa
1. Ler plano, materiais e o código existente. Distinguir **confirmado**, **hipótese** e **pendente**.
2. Explicar em 3–6 linhas o objetivo, os arquivos impactados e como verificar.
3. Implementar a menor alteração coerente; reutilizar componentes e modelos públicos.
4. Executar typecheck, lint, testes relevantes e, quando UI, screenshot de celular comparado com a referência.
5. Revisar acesso a dados, erros e regressões; reportar falhas reais sem esconder.
6. Commit pequeno com descrição, checklist de aceite e links para evidências.

## Gate de liberação
Não afirmar **pronto para produção** quando qualquer um ocorrer: autenticação pendente; autorização não testada; votos duplicáveis; integridade sob concorrência não testada; dados pessoais expostos; ausência de caminho de recuperação; interface importante não conferida no celular; regras institucionais sem confirmação.
