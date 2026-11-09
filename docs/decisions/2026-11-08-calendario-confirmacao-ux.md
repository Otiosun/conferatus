# CONFFRATUS — Cancelamento seguro e confirmação fiel no celular (08/11/2026)

## Referências e alcance

- Originais de Megalos, **sem alterar as imagens**: `1001930221.jpg` (calendário e cancelamento), `1001930222.jpg` (leitura da proposição e folha com dois botões), `1001930223.jpg` (variante desfocada com um botão), `1001930226.jpg` (agendamento sob perfil). Comparação privada: https://drive.google.com/file/d/1rb4M7iNxmY6qfRWKq0EFB8-S0SNFr-Mh/view .
- Base funcional aprovada antes do lote: SHA `0a640cb8da0faa27e87f8504fba4151f45e694a6`, GitHub Actions `42534417726`: `validate`, `cross-browser-lab`, `postgres-lab` e Cloudflare Pages SUCCESS.
- Este trabalho diz respeito **só à prévia demonstrativa local**, nunca à votação Academy nem a uma ação de cancelamento institucional.
- Decisões **D2 e D3 seguem abertas**. A referência coloca o agendamento sob o perfil; o aplicativo ainda permite criar programações via calendário. A variante desfocada de confirmação com um botão **não** autoriza deduzir o momento ou a regra de um segundo estado.

## Problemas reproduzidos

1. O botão `Cancelar programação deliberativa` aplicava o cancelamento imediatamente em `src/main.ts`, sem um caminho para desistir antes da mudança. A programação sumia dos registros ativos. A operação preservava histórico, porém um toque involuntário podia produzir a alteração sem confirmação.
2. Em uma proposta longa no modo de revisão, a folha de confirmação era renderizada **após todo o texto**, fora do campo visível em celulares 320/390px, diferentemente do painel inferior exibido na referência 1001930222. A pessoa precisava percorrer todo o documento antes de encontrar as opções.

## Investigação (Lei 21)

- MOJ Design System, **Confirm an action**: confirmar operações difíceis de reverter, explicando consequências e oferecendo uma saída. https://design-patterns.service.justice.gov.uk/patterns/confirm-an-action/
- W3C WAI APG, **Disclosure (Show/Hide)**: botão nativo com `aria-expanded` e `aria-controls`, teclado Enter/Space e informações expandidas previsíveis. https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
- MDN, **CSS position**: `position:sticky; bottom:0` preserva fluxo do documento, mas depende do contêiner de rolagem; verificar ocultação de conteúdo, zoom e desempenho. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position
- Alternativas recusadas: `window.confirm()` nativo sem composição do projeto; modal novo com foco preso e comportamento não especificado; integração externa/dependências; fluxo duplo de confirmação da proposição presumido do desenho 1001930223.

## Implementação delimitada

- Calendário: clique no botão existente abre **confirmação inline**, sem mutação. `Manter programação` e `Escape` revertem a intenção; somente `Confirmar cancelamento` aplica a transição existente, limpa amostras de voto vinculadas, salva o registro e preserva o histórico. O foco inicial vai ao grupo de confirmação e retorna ao botão correto ao desistir. A confirmação pendente é descartada ao trocar de item/rota. O item fixo de exemplo continua inalterável.
- Revisão: a folha de dois botões recebe classe explícita `workflow-review-panel--pending`; em retrato até 600px de largura e pelo menos 680px de altura, adota posicionamento `sticky` inferior com altura limitada. O documento continua rolável. Em telas curtas e no desktop, mantém fluxo normal. O estado de proposição **já concluída** não recebe essa classe. Nenhum novo passo ou regra de conclusão foi criado.
- Arquivos: `src/main.ts`, `src/styles.css`, teste novo `tests/browser_calendar_cancel_confirmation_v0177.py`, teste `tests/browser_review_sheet_portrait_v0178.py`, correções de compatibilidade em testes históricos de cancelamento/backup/IDs e atualização da CI.

## Verificação e rastreabilidade

- Protótipo local, anterior ao merge do código, mostrou folha visível na base de 320/390/540px e texto rolável; **não equivale à compilação do novo HEAD**.
- Teste de cancelamento: estado permanece ativo após primeiro clique; grupo de confirmação visível; `Escape` e `Manter` preservam o registro e restauram foco; confirmação explícita migra para histórico; 280/320/390/740/1280px.
- Teste da folha: 280/320/390/540px em retrato e 390px com baixa altura, mais 740px; caixa visível, documento rolável, `Cancelar` devolve redação intacta, `Confirmar` conclui o documento.
- As primeiras execuções 42538926526 e 42539270967 identificaram regressões nos *testes antigos* que pressupunham cancelamento em um clique, e uma asserção de fixture que ignorava o filtro de data. **Não** foram apagados os testes de integridade: passaram a confirmar expressamente antes de checar registros e histórico. A CI dos commits posteriores precisa ser lida pelo **SHA exato** antes de classificar aprovada.
- Nenhuma evidência desta rodada afirma teste de hardware Android real, teclado móvel, leitor de tela ou validação direta do domínio Cloudflare.

## Gates pendentes

1. CI **SUCCESS** do HEAD após corrigir compatibilidade e opcionalmente Firefox/WebKit no mesmo código; capturas do HTML dessa execução.
2. Comparar em celular físico com Megalos: panel inferior, conforto de leitura, tamanho de alvos, foco e calendário real; decidir D1/D2/D3.
3. Não concluir página de voto institucional ou regras Academy por analogia visual. `main`, produção, PM2 e bancos reais não foram tocados.

Etapas formais mantidas: 04=17/22; 06=2/5; 07=7/12.
