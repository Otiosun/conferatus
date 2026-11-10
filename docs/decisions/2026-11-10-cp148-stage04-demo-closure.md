# CONFFRATUS — Fechamento demonstrativo da Etapa 04 (CP148, 10/11/2026)

## Objetivo e fronteira
A responsabilidade desta equipe é **protótipo funcional com dados sintéticos**, não as contas, assinaturas, backend de colaboração, registro de votos ou regras finais da Academy. O teste anterior `browser_full_workflow_journey_v0173.py` só permitia concluir participantes Socii sob `?demo=1`; a apresentação normal terminava em **Aguardando Socii** sem poder continuar. Falha reproduzida em Chromium 320px: `[data-confirm-partner]` ausente. Isto impedia demonstrar a transição até proposta concluída, agendamento e votação.

## Mudança menor
- `src/main.ts`: disponibiliza **Simular conclusão de [participante]** na lista de proposições também no modo normal. A ação já existente e validada apenas altera os objetos fictícios da sessão, com o rótulo explícito de simulação; não transmite convite, assinatura ou aprovação institucional. Usa os guardas atuais de vínculo, versão e conclusão. Feedback recebe `role="status"` para exposição assistiva.
- `src/styles.css`: garante altura mínima de **44 px** e foco de teclado visível para esses controles. Nenhum framework, backend, regra de timer `127 horas`, redesenho do modelo Megalos ou alteração de `main`.
- Investigação fria: a estrutura existente já implementava as transições; nenhuma biblioteca foi necessária. W3C WAI, técnica ARIA22 para avisos de mudança de estado <https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA22> e entendimento do critério 4.1.3 <https://www.w3.org/WAI/WCAG21/Understanding/status-messages>. Um `role=status` não comprova acessibilidade integral.

## Provas reproduzíveis (testadas antes de enviar ao GitHub)
- Build local pelo TypeScript 5.8.3 / Node 22.16.0: **73/73 testes Node PASS**; HTML offline gerado SHA256 `3f54cd21a4e0e541715870a01cd9a873b0f52d24123ef3fd388c6dc649ca03fd`.
- `tests/browser_stage04_normal_socii_v0195.py` PASS em **320/390/740/1280px**, sem `?demo=1`: perfil, redação, Socii, revisão, conclusão de parceiro, calendário e votação contextual.
- `tests/browser_stage04_complete_v0196.py` PASS **4/4 larguras**: impede agendar sem proposição concluída; valida rascunho vazio; dois parceiros fictícios; progresso 0/3→1/3→2/3; edição material reinicia as confirmações; nova autoria + dois parceiros concluem 3/3; agendamento rejeita data final anterior e alternativas duplicadas; cria programação PR nominal com seção e proposta vinculada; permite **Manter** ou **Confirmar cancelamento**, histórico consultável; sem erro JS nem overflow nos cenários.
- Regressões `v0173`, `v0193`, `v0194`, `v0192` e `v0191` PASS sobre o mesmo build em 4 larguras (exceto `v0192`: 24 pares de seção/método em 390px). Uma repetição da matriz ampla `v0190` excedeu o limite local; não contamos como aprovação nesse lote. O teste já havia passado no commit anterior e o novo código não altera a lógica de voto.
- Arquivos de produto e testes conferidos por **Git blob** local versus repositório: `src/main.ts` = `678889f3b3d1d61f2f74443244bdbc95b4b42e4a`; `src/styles.css` = `c82df4a7000e6e0215fa0b17df6aabb47f5d3834`; v0195 = `6f3ac24f8ac858ccd7ce8188ad846a77c9196fd6`; v0196 = `a4a714c03e14df1ff1bc70914e00d53249ff8685`.

## Decisão de encerramento e reservas
No **escopo da prévia fictícia**, subitens **04.05 (agendamento)**, **04.09 (redação/revisão/estado)** e **04.13 (colaboração e conclusão Socii)** receberam prova funcional completa e são encerrados com nota de escopo. **Os itens 04.02 e 04.19 continuam aguardando escolhas/aceite visual da Megalos**, incluindo D1–D6. O contrato de Soc ii remoto e as políticas reais da Academy não foram implementados, nem são declarados como tais. Integridade de arquivo e armazenamento/HTTP reais em hardware permanecem dependências de homologação, não falsos PASS.

**Contagem histórica após o lote: 41/57 (04=20/22)**; não traduzir 71,9% em “percentual de obra” nem alegar produção. `main`, Cloudflare principal, Academy e PM2 intocados. CI GitHub pode permanecer sem runner; o fato de o deploy Cloudflare de preview funcionar não certifica a CI.

## Adendo de QA — foco depois de concluir Socii (10/11/2026)

**Defeito antes:** quando o botão `data-confirm-partner` desaparecia após a confirmação, o foco do navegador caía no elemento `BODY`. Reproduzido no Chromium em **320, 390, 740 e 1280 px**; o formulário do Socii era visualmente funcional, mas o usuário de teclado perdia a posição da navegação.

**Pesquisa e solução nativa:** W3C/WAI, [Keyboard Interface — Persistence of Focus](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) e [WCAG 2.2 SC 2.4.3 Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order). Após o render da confirmação, reusar os controles existentes no mesmo cartão: priorizar outro participante pendente; quando todos concluírem, o botão de agendamento; se indisponível, o botão da proposição. Sem `tabindex` artificial, dependência, CSS, novo endpoint ou regra institucional.

**Teste:** estendido o `tests/browser_stage04_complete_v0196.py` para confirmar com **Enter** e assegurar foco em `data-confirm-partner` e `data-schedule-draft`, respectivamente. Passou no Chromium em **320, 390, 740, 1280 px**, incluindo toda a jornada de redação/revisão/agendamento/cancelamento. Uma execução local adicional passou em **280 px**. `npm run build` aprovado com **73/73 testes Node**. SHA Git blob do código testado: `f4b8c3a65dbdda4bcb8dc057f48e4a173471fb43`; do teste: `0d9442d1bfd1b81103e71eba093b6f13cbc476c7`, ambos confirmados após envio ao GitHub.

**Limites:** nenhum novo item da checklist é marcado [x]; **43/57** permanece. A correção é pontual, não substitui WCAG AA completo, TalkBack/VoiceOver, zoom nativo, hardware, CI GitHub integral ou homologação Megalos. Apenas prévia; `main`, Academy e produção preservadas.
