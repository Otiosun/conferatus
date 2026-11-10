# CP161 — Metadados da proposição no agendamento (10/11/2026)

Base privada: `974dab074550be70ce17316afcd9b34cafd49d63` no ramo `preview/v0.10.60-six-vote-forms`. Integração de produto PF-17, somente dados fictícios.

A navegação desde uma proposição concluída já carregava o seu identificador e reaproveitava o calendário. Porém, o formulário iniciava a seção e o tipo com valores genéricos (`integridade` e `PDR`), mesmo quando a proposição exibida tinha outra seção ou outro tipo. O usuário precisaria corrigi-los manualmente para manter a continuidade documental.

Foi reutilizado o registro da proposição já selecionada para definir os valores **iniciais** dos campos de seção e tipo. Os controles continuam editáveis; não se introduziu regra institucional de obrigatoriedade de coincidência, elegibilidade, votação ou quórum. A abertura direta da agenda sem proposta de origem mantém os valores anteriores; o formulário normal e a folha de perfil reutilizam o mesmo componente.

Arquivos: `src/main.ts`, `tests/browser_schedule_proposal_defaults_v0208.py` e workflow. A regressão nova cobre pré-seleção de proposição/seção/tipo, alteração voluntária dos campos, persistência do agendamento local, independência da entrada por calendário e viewport 320/390/740/1280px.

Pesquisa de 10/11/2026: documentação MDN para `<select>` e `HTMLSelectElement.value` descreve `option selected` e o valor de opção selecionada; usamos HTML nativo e dados existentes, sem dependência ou lógica de rede.
https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select
https://developer.mozilla.org/en-US/docs/Web/API/HTMLSelectElement/value

Teste v0208 criado e incluído no workflow, **não executado** neste ambiente; acompanhar build Cloudflare no SHA exato. PF-17 [ ] até ensaio de navegador, Android e aceitação. Critérios 8/38 funcional e 43/57 histórica; main, produção principal e decisões D1–D6 preservadas.
