# CONFFRATUS — página de votação: evidência e fronteira de escopo (08/11/2026)

## Objetivo e fontes
Evitar concluir ou reconstruir uma tela diferente daquela pedida pela Megalos. Este é um mapeamento da prévia, **não um aceite**.
- Originais de 27/10/2026: `IMG-20261027-WA0175.jpg` (resultados), `WA0174.jpg` (menu) e `WA0172.jpg` (variação de menu), no pacote privado `Conversa do WhatsApp com Megalos Saey.zip`.
- Vídeo da conversa compartilhado em 06/11/2026: `1001954523.mp4`, mantido privado na biblioteca do projeto. **Não reproduzir frames pessoais no GitHub.**
- Modelo funcional verificado: HTML exato da CI `42522809136`, SHA `8e7c6d252b3628e5158541903d39e67e38126764`, branch `preview/v0.10.60-six-vote-forms`.
- Comparativo visual privado original × prévia: https://drive.google.com/file/d/19EODUyvzxknY1u50TYuTALPvIsERko_Q/view .

## Fatos comprovados
1. Os modelos originais 1–3 representam **resultados, percentuais, descrição da votação e estados do menu**. Não mostram os seis formulários de voto nem uma tela de administração.
2. A rota normal `#/ballot` reproduz os resultados/descrição e possui botão `Participar` para duas alternativas **apenas simuladas**. Não envia voto à Academy; não afirma autenticação.
3. O laboratório opt-in `?demo=1` contém seis modalidades (binária, nominal, ordenada, aprovação, escalar, cumulativa) e testes. Isso **não** equivale à navegação normal da pessoa que vota, nem a gestão institucional.
4. O calendário normal permite programar deliberação local com modalidade e opções. O rótulo `Iniciar uma Votação` ainda abre agendamento (D1b em aberto).
5. A Megalos escreveu que, para concluir, faltava a página de votação. Na conversa do vídeo há resposta `Segunda` à pergunta sobre qual das duas perguntas anteriores havia sido negada; **não** é evidência de escolha entre interface do eleitor e interface administrativa.
6. A auditoria atual reproduziu as três composições em Chromium, viewport 370×800 CSS px/DPR 2, sem `pageerror`/overflow; capturas fazem parte do comparativo privado. Isto não é homologação do site publicado ou de dispositivo físico.

## Lacuna de produto, sem inferir autorização
A presença de tela de resultados não fecha o ciclo completo da votação. A diferença entre a tela atual e a página faltante pode ser:
- **Participação:** visão de deliberações elegíveis, abertura de votação, escolha e revisão, confirmação, feedback, estados de encerramento e resultado.
- **Administração:** elaboração/publicação, opções e modalidade, acompanhamento, encerramento e resultados.
- **Ambas:** jornadas distintas, ligadas ao mesmo registro institucional, com permissões conferidas.

Essas alternativas são hipóteses a **validar**, não escopo aprovado. O laboratório de seis modalidades pode ser reaproveitado como componente técnico, **sem** promover seu armazenamento local a banco institucional.

## Gate obrigatório antes de implementação da lacuna
- [ ] A Megalos delimita, pelo exemplo ou instrução, qual jornada esperava ao dizer que faltava a página: participante, administração ou ambas.
- [ ] Há definição dos estados da jornada e dos campos visíveis; não deduzir regras de tela pelo mock de resultados.
- [ ] A Academy define autorização/elegibilidade e política oficial para mudar voto, sigilo, encerramento, quórum, apuração e histórico, caso o escopo passe a ser institucional. Nunca inventar essas regras no front-end.
- [ ] Antes de mudanças visuais, confrontar original vs HTML e proteger dados locais, acesso por teclado, erros, 280–1440px e navegação. D1–D6 permanecem pendentes de aceite.
- [ ] Em homologação de **prévia demonstrativa**, distinguir claramente o protótipo dos votos reais. Não promover `main` nem afirmar integração institucional.

## Decisão desta rodada
**Não introduzir uma nova tela presumida.** Primeiro produzir a comparação material e registrar a lacuna. Se houver decisão de que o objetivo é só a prévia demonstrativa, implementar a jornada correspondente usando os mecanismos testados e sem credenciais reais. Se o objetivo for voto institucional, aguardar o contrato formal da Academy.

Contadores formais preservados: 04=17/22, 06=2/5, 07=7/12. `main`, Cloudflare de produção e bancos não foram alterados.
