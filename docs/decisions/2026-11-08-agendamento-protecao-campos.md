# CONFFRATUS — proteção de dados em agendamento incompleto (08/11/2026)

## Defeito demonstrado
No HTML offline gerado pela CI da prévia (build de referência `57153f8`), foi realizada a jornada **proposição concluída → calendário → abrir agendamento → preencher título, objetivo e proposição → clicar Fechar agendamento → reabrir**. O resultado foi perda silenciosa dos três valores, inclusive antes de trocar de rota. Captura do teste executado: título `Sessão importante com vários campos`, objetivo `Objetivo longo que não pode sumir` e proposição selecionada; reabertura com todos os campos vazios. O mesmo risco afetava mudança de rota e recarga, embora re-renderizações enquanto o formulário permanecia aberto já conservassem valores via `FormData`.

## Soluções consideradas (Lei 21)
- **Autosave do formulário de agendamento:** permitiria retomada mesmo após fechar o navegador, mas exigiria política própria de armazenamento, duração, colisões com registro programado e estados de recuperação. Não foi adotado sem contrato: a fonte de verdade já é `sessionStorage` somente para registros válidos confirmados.
- **Interceptar fechamento sem diferenciação:** criaria alertas falsos no formulário vazio, aumentando atrito. Recusado.
- **Proteção local condicional:** adotada. Só perguntar sobre descarte quando o formulário aberto difere dos valores iniciais. Mantém o conteúdo em caso de recusa; ao confirmar descarte, fecha ou sai. Também registra aviso de descarregamento da página quando houver alteração, como proteção adicional, nunca como garantia de salvamento.

### Documentação externa verificada
- MDN, `Window.beforeunload`: aviso só quando há alterações, não funciona confiavelmente em celulares; restringir o listener ao período com dados pendentes. https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event
- GOV.UK One Login, interrupção de formulário não salvo: avisar claramente antes de perder progresso. https://www.sign-in.service.gov.uk/documentation/design-recommendations/save-progress

## Mudança delimitada
- `src/main.ts`: função `hasPendingScheduleChanges()` percorre `FormData` e ignora os valores originais (`sectionId=integridade`, `type=PDR`); qualquer campo realmente alterado aciona `confirmScheduleDeparture()` ao fechar ou navegar. O menu fecha após recusa, sem perder os campos.
- A navegação pelo histórico (`hashchange`) também protege o formulário, inclusive quando não usa o botão normal. Ao sair, limpa o estado `scheduleFormOpen` para impedir abertura involuntária em outra visita.
- O `beforeunload` compartilhado com a redação também observa o agendamento, sendo ligado/desligado ao entrar, alterar, salvar ou descartar valores. Re-renderizar o mesmo calendário **não** cria alerta indevido.
- O formulário concluído continua usando a transação local de sessão já existente. Nenhuma alteração em dados Academy, autenticação ou votos.
- `tests/browser_schedule_unsaved_guard_v0179.py`: quatro larguras e Chromium/Firefox/WebKit via laboratório opt-in. Verifica campos vazios sem aviso, perda evitada ao fechar, menu e histórico, descarte aceito, formulário vazio ao reabrir, gravação normal sem aviso residual e ausência de overflow/erros JS.

## Evidências, riscos e gates
- Teste negativo da versão anterior foi reproduzido no Chromium a 390 CSS px.
- A nova CI é o critério para aprovar o código; não atribuir sucesso da CI `42540752954` (HEAD anterior) aos novos commits sem verificar execução e SHA.
- `beforeunload` é explicitamente insuficiente para garantir retomada após fechamento de aplicativo no Android. Sessão em memória nos testes offline **não comprova** persistência real após reiniciar o navegador. Isso continua pendente.
- D2 (agendamento no perfil ou calendário/ambos), D3 (estado desfocado da revisão), D1–D6 e jornada institucional de votação permanecem sem aprovação; **não** foram implementados por inferência.

As contagens formais seguem 04=17/22, 06=2/5, 07=7/12. A `main`, Cloudflare de produção, dados institucionais e PM2 não foram alterados.
