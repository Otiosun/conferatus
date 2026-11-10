# CP162 — Retorno coerente ao histórico do calendário (10/11/2026)

Base da branch privada: `03e4af020ab9b830d73daae759dfe45b50bff851`. PF-18 já separava programações ativas e canceladas: a lista ativa e os marcadores diários excluem registros cancelados, mantendo-os no histórico local somente para consulta. Esta lógica foi preservada.

A lacuna de experiência estava após a confirmação de cancelamento: o cartão desaparecia da lista e o foco caía no título da seção, distante do histórico. O texto de sucesso agora informa onde consultar o registro e o foco vai para o botão de histórico já existente, mantendo o conteúdo recolhido. Se o armazenamento local falhar, o foco vai ao controle de tentar salvar novamente. Nenhuma ação cenográfica ou regra institucional criada.

Teste `tests/browser_calendar_history_focus_v0209.py`: fixtures fictícias ativas e canceladas, contagem de histórico, indicadores de datas, filtro, foco no histórico, leitura de dois cancelamentos sem ações de ativo, persistência local, ausência de overflow em 320/390/740/1280 px; incluído no workflow, **não executado nesta sessão**. Manter v0153/v0177/v0196 na suíte.

Referências consultadas: https://primer.style/accessibility/design-guidance/focus-management/ (foco após remoção de elemento da interface); https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus (foco e rolagem). Revisão de UI sem alterar identidade visual. PF-18 [ ]; 8/38 funcional, 43/57 histórica; `main` e produção preservadas, bem como decisões D1–D6 Megalos.
