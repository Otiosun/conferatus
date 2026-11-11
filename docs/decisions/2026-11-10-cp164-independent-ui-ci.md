# CP164 — Executar as regressões da prévia independentemente de outros jobs (10/11/2026)

Base: branch privada `preview/v0.10.60-six-vote-forms`, commit `34905c9a9246c6fcdd9d5579cd59757cced2ae05`. Este ajuste incide apenas sobre o encadeamento de jobs de CI, não modifica código de aplicação, modelos, serviços nem comportamento institucional.

## Diagnóstico reproduzível no GitHub Actions
As últimas verificações mostravam repetidamente `validate=skipped`, mesmo havendo uma lista extensa de testes Playwright, enquanto outro job estava `failure`. No YAML vigente, `validate` tinha `needs: postgres-lab` sem consumir qualquer saída desse job. Segundo a documentação oficial do GitHub Actions, um job com `needs` não executa quando a dependência falha ou é ignorada. Isso impedia a produção de evidência independente sobre UX, responsividade, redação, Socii e calendário.

## Alteração mínima
Foi retirada somente a dependência `needs: postgres-lab` de `validate`. Todos os jobs, seus passos e seus critérios de resultado permanecem presentes: a suíte de interface pode ser executada de forma autônoma e sua falha será relatada separadamente. A alteração não usa `continue-on-error`, não ignora falhas, não modifica testes de laboratório e não libera a produção. `cross-browser-lab` continua opt-in.

Fontes oficiais (consultadas em 10/11/2026):
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

## Evidências e status
Este commit apenas habilita a execução efetiva da suíte de navegador no GitHub. **Não** declarar os testes aprovados sem ler o resultado do workflow do SHA correspondente. Continuar a distinguir build Cloudflare, testes Node, testes Chromium, Firefox/WebKit e Android real. Manter abertas PF-06, PF-10, PF-11–21; funcional 8/38, histórica 43/57 até evidências verificadas. Main e produção principal permanecem intocadas.
