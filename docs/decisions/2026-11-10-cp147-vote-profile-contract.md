# CONFFRATUS — CP147 | Contrato fechado do protótipo: votação e vínculos de perfil (10/11/2026)

## Delimitação

O entregável da nossa equipe é um **protótipo inteiramente fictício** com jornada demonstrável. A autenticação, permissões, peso eleitoral, apuração oficial, auditabilidade e persistência compartilhada pertencem ao núcleo Academy e **não** são implicados pelos resultados desta rodada. A composição e decisões D1–D6 continuam sujeitas à Megalos. As leis de engenharia do `AGENTS.md` são preservadas, principalmente 2, 4, 5, 12, 14, 15, 16 e 21. A avaliação desta rodada aproveitou mecanismos já implementados, sem pacote nem alteração do aplicativo.

## 02.01 — modelo de votação demonstrativa e estados

O modelo de dados existente em `src/domain/rules.ts` diferencia seis modalidades: `binaria` (um Sim/Não), `nominal` (uma opção), `ordenada` (todas as alternativas sem repetir preferência), `aprovacao` (pelo menos uma opção), `escalar` (nota inteira 1–10 para cada opção) e `cumulativa` (quantidades inteiras não negativas, soma entre 1 e a cota sintética permitida). Na tela normal, a cota cumulativa é **5 unidades fictícias**; `?demo=1` conserva o modo técnico por membro de exemplo. Nenhuma dessas regras é política da Academy.

Estados e transições comprováveis na UI de prévia:
1. **Painel fechado:** o formulário é aberto explicitamente pela navegação normal, mantendo controles de referência e sem confundir a votação ilustrativa de início com uma programação.
2. **Escolha em elaboração:** preenchimentos não enviados ficam em memória da aba mesmo depois de fechar/reabrir ou navegar; a modalidade/programação é o escopo. Trocar modalidade ou contexto não reaproveita a escolha anterior.
3. **Entrada inválida:** mensagem no formulário e nenhum recibo/amostra. Exemplos: alternativa em branco, ordem duplicada, nenhuma opção aprovada, notas faltantes e seis unidades cumulativas numa cota de cinco.
4. **Amostra validada:** recibo demonstrativo e resumo descritivo **apenas em memória**, segregado por modalidade/programação. Não há envio à Academy nem atualização dos totais ilustrativos preexistentes.
5. **Nova amostra:** após recibo, `Registrar outra amostra` retorna ao formulário sem eliminar automaticamente os resumos já contabilizados.
6. **Limpeza:** requer confirmação humana e afeta somente as amostras daquele escopo; cancelar preserva as amostras.
7. **Programação ativa:** `programada`, método válido e alternativas válidas (quando aplicável) habilitam `Simular voto nesta programação`; a rota mostra título/proposição/método corretos, sem resultados de outra votação. A opção `cancelada` permanece apenas em histórico e não é tratada como votação ativa. `programada` é um status demonstrativo, **não autorização temporal ou eleitoral real**.
8. **Identidade ausente/sem integração:** a demonstração nunca produz login, trilha oficial ou permissão por ACDM ID. O máximo de 100 amostras por contexto, idempotência e isolamento são proteções da ferramenta local, não sistema transacional institucional.

Provas: `tests/browser_vote_states_v0194.py` rodou contra o **código compilado da aplicação**, 320/390/740/1280px, todos os estados de seleção inválida/recibo/repetição/limpeza por escopo, com ausência de overflow/JS pageerror. `browser_voting_normal_flow_v0190.py` comprova os seis modos em cada largura e quatro programações contextuais; `browser_voting_section_links_v0192.py` cobre quatro seções × seis modalidades. `tests/preview-ledger.test.mjs` e `tests/rules.test.mjs` verificam validação, idempotência, imutabilidade e isolamento.

## 03.05 — perfis e listas locais vinculados

No âmbito da **autoria fictícia identificada na própria sessão**, as proposições elaboradas ficam vinculadas ao perfil do autor `m01`; cada proposição concluída pode mostrar suas **programações ativas** como links, com destinos reproduzíveis ao calendário, descrição, seção, formulário e retorno contextual. Uma programação cancelada não aparece entre links ativos, mas permanece no histórico do calendário. Os outros perfis da fixture não herdam propostas do autor e mantêm os próprios registros históricos fictícios. O sistema **não** atribui autoria, voto ou papel institucional a pessoa real.

Prova específica: `tests/browser_vote_profile_links_v0193.py` em 320/390/740/1280px, duas proposições sintéticas independentes, duas programações válidas e uma cancelada, perfil→programação→revisão→calendário→perfil; nenhuma transposição para perfil `m02`, sem JS pageerror/overflow. Reuso de `linkedScheduleButtons`, `profilePage`, `calendarPage` e navegação já existentes, sem código cenográfico adicional.

## Evidência, limites e próxima fase

- Build recuperado localmente com fontes conferidas por Git blob do HEAD de aplicação `dd3388e` (funcionalmente idêntico ao código anterior `47069280` mais correção CP145). `npm run build` compilou TypeScript 5.8.3 e aprovou **73/73 Node**.
- Ambos os arquivos de teste acima foram **reobtidos do GitHub e conferidos pelo hash Git antes de executar**, com PASS nas quatro larguras; adicionados ao workflow `validate`. Isso **não** equivale a CI remota aprovada, avaliação WebKit/Firefox no SHA ou verificação em telefone.
- Nenhum arquivo `src/`, CSS, fixtures, `main`, Cloudflare principal ou Academy foi modificado. A documentação e os testes de regressão são o único delta.
- A checklist histórica passa **36→38/57**: 02=2/4, 03=3/5; 19 pendências estruturais permanecem, incluindo escopo real externo e homologação Megalos. A porcentagem histórica não representa esforço de entrega.
- Próximo P0: validar integralmente os três critérios restantes de fluxo da etapa 04 (agendamento, revisão e Socii) como protótipo fictício; separar regras de terceiros e D3/D4 antes de qualquer aceite. Manter QA visual/hardware e a página de votação para aprovação da Megalos.

Referências técnicas consolidadas: W3C/WAI Forms <https://www.w3.org/WAI/tutorials/forms/>, documentação oficial do Playwright <https://playwright.dev/python/docs/locators>, e MDN sobre substituição de nós DOM <https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML>. Nenhuma biblioteca ou solução externa nova foi introduzida.
