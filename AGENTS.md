# CONFFRATUS — Leis máximas de engenharia

> **Identidade de prévia (02/11/2026):** exibir **CONFFRATUS** conforme correção explícita do responsável. A arte original em alguns modelos contém **CONFERATUS** e deve ser preservada intacta como prova histórica, sem atribuir a mudança à Megalos. Não migrar automaticamente chaves de `sessionStorage`, nomes técnicos de repositório/domínio ou imagens-fonte. O aceite formal da Megalos continua pendente e a Etapa 01 não é marcada como concluída apenas por este ajuste.

> **Retomada obrigatória (01/11/2026):** consultar `docs/CHECKLIST_MESTRA.md` antes de iniciar qualquer tarefa e atualizá-la após os testes. A implementação atualmente mantida usa TypeScript, HTML e CSS sem framework; as sugestões antigas de React/Vite abaixo são históricas e **não autorizam reescrita**. Priorizar código humano, natural e legível, preguiça inteligente, fidelidade ao material da Megalos, revisões pequenas e distinção explícita entre simulação e funcionamento integrado.

Versão 1.0 — 28/10/2026. Este arquivo foi preparado para virar `AGENTS.md` na raiz do repositório. Leis válidas para humanos e agentes de IA. Uma exceção exige justificativa em `docs/decisions/` e aprovação explícita do responsável técnico.

## Constituição
1. **Preguiça inteligente.** Antes de criar código, procure recurso nativo, componente próprio, função existente e solução mais simples. Não implemente infraestrutura que já seja provida com segurança.
2. **Perfeccionismo verificável.** Não chame algo de concluído sem funcionamento observado, testes pertinentes e revisão visual. Perfeição não é polimento infinito: é cumprir integralmente critérios objetivos.
3. **Uma fonte de verdade por dado.** Cadastro institucional deve manter seu dono; CONFFRATUS controla apenas seus dados de deliberação. IDs externos não são prova de autenticação.
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
21. **Investigação fria antes de implementar (07/11/2026).** Para toda mudança técnica material, investigar na Internet as soluções já consolidadas, documentação oficial vigente, problemas conhecidos e correções existentes antes de escrever código. Confrontar soluções nativas, código atual e alternativas maduras; documentar fontes e datas, riscos de segurança, licenças, acessibilidade, interoperabilidade e manutenção, e a razão para aceitar/rejeitar abordagens. Registrar em `docs/decisions/`, na checklist e no Drive mestre. Reproduzir problemas conhecidos e testar regressões pertinentes (incluindo motores de navegador nas APIs de edição). Nunca copiar código sem revisão, inventar compatibilidade ou introduzir dependências sem evidência. A pesquisa não autoriza reescrever a arquitetura nem tocar produção. Profundidade proporcional ao risco, sem burocracia para ajuste trivial.

## Stack vigente e escopo de entrega

- Aplicação HTML, CSS e TypeScript strict, sem framework. Reutilizar módulos, estilos e controles que já funcionam.
- Testes Node nativos, Playwright e GitHub Actions. PostgreSQL é um **laboratório descartável** de CI, não um serviço da aplicação pública.
- O entregável da nossa equipe é a experiência CONFFRATUS coerente e integralmente testada com dados sintéticos: telas, calendário, proposições, Socii, históricos e seis formulários demonstrativos de voto.
- Autenticação Academy, contas, identidades reais, autorização institucional, banco compartilhado e integração efetiva **pertencem à equipe responsável da Academy**, não devem virar bloqueio artificial para finalizar nossa prévia.
- Preparar contratos claros de integração, mas **não desenvolver outro login, gateways de produção, infra redundante nem políticas eleitorais não aprovadas**.
- A prévia pode ser homologada como produto demonstrativo; nunca chamar de sistema institucional integrado ou pronto para registrar votos reais.

## Gates operacionais das 20 leis

1. **Código humano:** preferir funções pequenas, nomes claros e fluxo previsível. Nunca minificar a fonte ou comprimir várias decisões de negócio numa linha para economizar espaço. Separar validação pura da renderização quando isso realmente reduzir acoplamento. Não reescrever a aplicação por estética arquitetural.
2. **Preguiça inteligente:** antes de adicionar arquivo, dependência ou camada, demonstrar por que uma função ou componente existente não resolve. Manter zero dependências de runtime enquanto a prévia puder usar APIs nativas.
3. **Fidelidade com evidência:** não alterar a composição do material Megalos para agradar gosto pessoal. Mudanças de comportamento/identidade aguardam D1–D6; correções objetivas de bugs e acessibilidade podem avançar com regressão.
4. **Integridade de sessão:** todo estado criado pelo usuário deve sobreviver a navegação e falhas tratáveis; rejeitar importações inválidas; alterações locais que não puderem ser persistidas devem dizer a verdade e permitir recuperação. Nunca misturar amostras de voto com registros históricos fictícios.
5. **Sem funcionalidade cenográfica:** botão sem efeito, texto que finge autenticação, confirmação de Socii real ou resultado de votação institucional são defeitos. A ação deve funcionar ou estar claramente indisponível.
6. **Acessibilidade verificável:** validar teclado e foco após atualizações do DOM, tela estreita, zoom e textos longos, rótulos, mensagens de erro e contraste. Não afirmar certificação WCAG sem auditoria e hardware.
7. **Privacidade e segurança:** fixture sempre sintética; nenhuma chave real, dado Academy, arquivo original privado ou log sensível no bundle. Fronteiras externas negam acesso até autenticação e autorização confirmadas pelos responsáveis.
8. **Sem progresso inventado:** todo item concluído exige teste verificável e rastreável; contagens da checklist devem bater com os marcadores [x]. Diferenciar **implementado**, **CI aprovada**, **homologado pela Megalos** e **publicado**.
9. **Custo/produção:** mudanças somente na branch de prévia e CI isolada; nunca mesclar, publicar, alterar PM2, banco ativo, Cloudflare ou identidade Academy por iniciativa própria.
10. **Entrega responsável:** priorizar defeitos reais, fluxos incompletos e documentação de handoff. Experimentos técnicos sem relação direta com a entrega não passam à frente do produto.

## Processo obrigatório por tarefa
1. Ler plano, materiais e o código existente. Distinguir **confirmado**, **hipótese** e **pendente**.
2. Explicar em 3–6 linhas o objetivo, os arquivos impactados e como verificar.
3. Implementar a menor alteração coerente; reutilizar componentes e modelos públicos.
4. Executar `npm run build` (TypeScript + testes Node), suítes Playwright pertinentes e, quando UI, capturas de tela comparadas com as referências disponíveis. Não declarar lint executado sem script de lint.
5. Revisar acesso a dados, erros e regressões; reportar falhas reais sem esconder.
6. Commit pequeno com descrição, checklist de aceite e links para evidências.

## Gate de liberação
Não afirmar **pronto para produção** quando qualquer um ocorrer: autenticação pendente; autorização não testada; votos duplicáveis; integridade sob concorrência não testada; dados pessoais expostos; ausência de caminho de recuperação; interface importante não conferida no celular; regras institucionais sem confirmação.

## Nova etapa permanente — 07 (02/11/2026)

Por solicitação expressa do responsável, o projeto tem agora **sete etapas**. A Etapa 07 é dedicada **exclusivamente** a perfeccionismo visual, front-end, acessibilidade e responsividade por tamanho, zoom, conteúdo e tipo de interação. Seu checklist próprio está em `docs/ETAPA_07_FRONTEND_PERFECCIONISMO_2026-11-02.md`; ela não substitui a Etapa 06 de entrega. Todo novo ciclo deve retomar também a contagem `07=N/12`, publicar provas específicas antes de marcar itens e não chamar a responsividade de absoluta sem verificar motores adicionais e hardware real. A fidelidade à Megalos e a proteção de produção permanecem obrigatórias.
