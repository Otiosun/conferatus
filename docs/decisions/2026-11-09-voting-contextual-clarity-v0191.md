# CONFFRATUS — CP143: votação contextual fiel e disclosure acessível (09/11/2026)

**Objetivo:** corrigir duas regressões objetivas da recém-aberta página de votação fictícia; **não** alterar votação real, Academy, a `main` ou a produção.

## Investigação proporcional à lei 21

Conferidos o fluxo existente `ballotPage()`, `previewVoteLab()` e o teste v0190, sem novos pacotes ou redesign. W3C [Disclosure Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) define `aria-expanded` e relação com o painel controlado; [MDN aria-expanded](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded) explica o estado aberto/fechado. Pesquisa conferida em 09/11/2026.

**Bug A — referência quebrada:** a ação `Abrir formulário de votação` dizia `aria-controls="preview-vote-lab"` mesmo quando o alvo não existia. Reproduzido em DOM Chromium: fechado = 0 alvos, aberto = 1, fechado = 0. Alternativas consideradas: remover `aria-controls` quando fechado (dispensa vínculo) ou preservar um destino oculto. Adotado um único `<div id="preview-vote-lab" hidden></div>` quando colapsado, substituído pelo formulário verdadeiro ao abrir. Os focos Enter/Espaço e o atributo `aria-expanded` são verificados; nenhuma região interativa indevida entra na sequência Tab.

**Bug B — resultados de outra votação no contexto:** ao acionar `Simular voto nesta programação` no calendário, a rota `#/ballot` renderizava primeiro os resultados de uma votação de fixture sem relação com a programação selecionada. Reproduzido com programação sintética válida, método nominal e duas opções: `.results` do fixture presente após a navegação. Corrigido com um retorno dedicado de `ballotPage()` quando há programação ativa no modo normal: cabeçalho compacto + formulário/contexto da programação, sem resultados do fixture. O modo comum e `?demo=1` mantêm o fluxo anterior.

**Linguagem/retorno:** no modo normal, a ação de deixar o contexto usa `Ver outras modalidades` em vez do rótulo interno `Voltar às alternativas de teste`. Ao sair, o método volta a ser selecionável, a programação é desvinculada e os resultados da votação simples retornam. O laboratório avançado preserva sua identificação anterior.

## Evidências reproduzíveis

- `src/main.ts` commits `f69d1f7`, `084d21f`, `03706d4`; nenhuma alteração CSS ou biblioteca neste checkpoint.
- `tests/browser_voting_normal_flow_v0190.py` ampliado nos commits `0548a20`, `ba2c7dd`, `84f33f8`. Blob GitHub e cópia executada **idênticos:** `696004a0d61eb226e3a360d292b07507f6bca0a2`.
- Chromium local: **4 larguras × 6 modalidades** de participação fictícia, **4 jornadas** calendário → voto contextual → comprovante → sair para modalidades, teste de cota cumulativa inválida, acesso por teclado, alvos ARIA estáveis; PASS, sem erros JS ou overflow nos cenários observados.
- Screenshot contextual 390 CSS px revisada: programação e proposição corretas, sem cartões de resultados não vinculados.
- Pacote ZIP privado Komekko: https://drive.google.com/file/d/1yMHAOlm9O2tKjsKaOE39rHh0U7fQi51n/view ; SHA256 `079cdef4708a237ddd375fae6687b22f91b81af4de42ffb6218b9c8e0e3a0d6b`. Inclui HTML **experimental**, teste exato, log, screenshot e hashes.

**Limitação obrigatória:** o HTML exercitado é o offline anterior `bb14e32a` com patches equivalentes a CP142–143, **não é build compilado do HEAD atual**. Nenhum `npm run build`, CI remoto verde, Android real, homologação visual Megalos nem backend Academy é afirmado. Repositório privado e `main`/produção preservados.

**Checklist:** 33/57 intactos. Acesso normal às seis modalidades avançou, mas o pedido de página de votação da Megalos e as decisões D1–D6 ainda requerem aceite; requisitos institucionais permanecem fora do escopo executável da nossa equipe. Próxima prioridade: QA real do bundle de prévia/HEAD quando os runners permitirem e conferência visual diretamente no aparelho de avaliação; não abrir GitHub público apenas para isso.
