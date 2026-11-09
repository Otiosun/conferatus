# CONFFRATUS — Alternativas temporárias ao mudar a modalidade de votação (09/11/2026)

## Defeito reproduzido e gravidade
No HTML compilado da CI do checkpoint 129, com dados **fictícios** de uma proposição concluída, abri o formulário de agendamento na folha experimental `?demo=1&d2=sheet`. Escolhi a modalidade `nominal`, digitei três alternativas, mudei para `binaria` e voltei para `nominal`. O campo `choices` reapareceu **vazio**. Isso não dependia da folha visual: ambos os caminhos — calendário e folha D2 — usam a mesma função `scheduleFormMarkup()` e o mesmo `render()`, que preservava somente os campos ainda presentes no `FormData`.

**Por que acontece:** na troca para binária o `textarea[name=choices]` deixa de existir. A próxima renderização não tem valor para recuperar, mesmo que a pessoa retorne à modalidade anterior. Isso desperdiça texto já digitado e pode tornar a programação desconfortável em celular.

## Investigação e decisão
- GOV.UK Design System, [Question pages](https://design-system.service.gov.uk/patterns/question-pages/): evitar exigir que pessoas insiram novamente informações já fornecidas; preservar o estado ao voltar a uma etapa.
- GOV.UK Design System, [Check answers](https://design-system.service.gov.uk/patterns/check-answers/): campos previamente preenchidos devem permanecer preenchidos ao voltar para alterar uma decisão.
- W3C, [WCAG 3.3.6 Error Prevention](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-all): favorecer correção/revisão antes de uma submissão, não tratar a interface como irreversível.

Alternativas:
1. Manter a textarea permanentemente no DOM, escondida: poderia incluir alternativas indevidas em `FormData` da modalidade binária e alterar um contrato já testado. **Rejeitada.**
2. Gravar automaticamente alternativas em `localStorage`/`sessionStorage`: implica ciclo de vida e promessas de retomada não aprovados pela Academy. **Rejeitada.**
3. **Cache transitório na memória, associado apenas ao formulário atualmente aberto (adotado)**. Antes de rerenderizar, se o campo de alternativas existe, guardar o texto. Ao regressar a uma modalidade que apresenta alternativas, restaurar o texto somente quando não houver valor da textarea atual. Ao fechar ou salvar o formulário, zerar o cache. Nenhuma alternativa oculta entra na submissão binária.

## Mudanças delimitadas
- `src/main.ts`: `scheduleChoicesDraft` é um texto **temporário** em memória, não parte do banco de dados nem armazenado em Storage. O próprio `render()` mantém o texto durante a troca de modalidade e descarta-o assim que a sessão de edição deixa de exibir o formulário.
- `hasPendingScheduleChanges()` passa a considerar esse texto mesmo quando a textarea está provisoriamente oculta, para evitar fechar silenciosamente um formulário onde havia alternativas digitadas.
- O código atende tanto ao calendário normal quanto à candidata D2, sem abrir uma segunda lógica de agendamento, alterar a regra de votação, registrar votos ou adicionar permissões.
- Quando um novo agendamento é iniciado, o campo abre **vazio**. Quando o método binário é escolhido na submissão, as alternativas temporariamente ocultas não são materializadas no `FormData`.

## Provas e limites
- Ensaio **negativo** sobre HTML do checkpoint 129: após `nominal → binaria → nominal`, o campo retornou vazio.
- Ensaio **local** em Chromium do mesmo HTML com a correção JS injetada, nas larguras 280/390/740: o texto sobreviveu ao ciclo, o descarte autorizado fechou o formulário, a próxima abertura começou vazia; sem `pageerror`. Repetido tanto para folha do perfil quanto para calendário. Esses ensaios não substituem a compilação do SHA novo.
- Regressão `tests/browser_profile_schedule_sheet_d2_v0181.py` reforçada para o ciclo e isolamento do próximo agendamento.
- Nova regressão dedicada `tests/browser_schedule_choices_method_roundtrip_v0182.py` valida os dois caminhos em 280/390/740 CSS px. Está registrada nas suítes Chromium e Firefox/WebKit sem dispensar testes históricos. Deve passar no **HEAD exato** antes da aprovação.
- D2 permanece candidata opt-in sem aceite visual da Megalos; D1–D6 e a votação institucional real continuam pendentes. `main`, Cloudflare principal, Academy, PM2 e bancos reais não foram modificados. Etapas formais 04=17/22, 06=2/5, 07=7/12 não mudam por esta correção.
