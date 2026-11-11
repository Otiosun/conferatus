# CP171 — Atalho de primeira votação direto para redação (11/11/2026)

## Fato reproduzido e escopo
A auditoria visual do artefato HTML exato do CP170 demonstrou que a ação inicial **Criar uma votação** abria a lista de proposições, mas **Redigir proposição** só ficava abaixo da área visível em telas móveis compactas. O texto orientava corretamente o pré-requisito, porém não colocava a próxima ação ao alcance imediato do usuário. Isso não depende de decisão visual de Megalos, e não autoriza alterar as imagens/modelos dela nem a hierarquia da lista de proposições.

## Correção mínima
Reutilizada a ação existente `data-action="new-proposal"` diretamente no botão inicial. Ela limpa apenas o novo formulário em memória e abre a rota `compose` sem criar registro vazio persistido; o fluxo normal de finalizar, Socii opcional, programar e participar continua idêntico. A lista e seus controles existentes permanecem inalterados. **Não criar etapa nem regra**, não alterar estilos ou rearranjar as seis telas de referência. O botão `Ver programações` continua levando ao calendário.

O teste `tests/browser_first_time_voting_journey_v0211.py` foi ampliado para exigir que o atalho abra imediatamente o editor, com título vazio, permitir voltar à home e então testar normalmente toda a jornada Proposição → Conclusão → Programação → Participação → Comprovante nas quatro larguras. Nenhum cenário antigo foi desativado. Roteiro de apresentação atualizado para refletir a ação real.

A regra 21 de `AGENTS.md` foi atendida proporcionalmente ao risco: antes de criar solução nova, usou-se o manipulador `new-proposal` já existente, com contratos conhecidos, sem dependências ou alterações institucionais. Investigação e documentação extensivas do formulário e links de acessibilidade constam dos CP169 e CP170. Revisar GitHub Actions no SHA final; não declarar sucesso antes da execução. Nenhuma mudança autorizada em `main` ou produção. Aceite visual D1–D6, navegação física Android e envio para Megalos permanecem independentes.
