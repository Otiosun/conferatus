# Modelos recebidos em 31/10 — calendário, proposições e Socii

## Referências
Seis capturas e o vídeo enviado pela Megalos. Este documento resume decisões visíveis no material sem substituir os originais.

## Fluxos
- Menu: quatro itens — membros, histórico, agendar/iniciar deliberação, elaborar proposição e Socii.
- Calendário: consultar programações, abrir o formulário, selecionar proposição concluída, seção deliberativa, início/encerramento, tipo, título e descrição objetiva.
- Proposição: redigir título e texto, revisar seção responsável e tipo, confirmar autoria.
- Socii: colaboração entre participantes. A conclusão da autora não finaliza o documento enquanto houver participante pendente.
- Indicadores: Votos, PDR, PR, Ofício e Socii.

## Estado da implementação v0.10.0
A interface utiliza dados exclusivamente demonstrativos. Calendário, rascunho, revisão e colaboração simulada persistem apenas na sessão do navegador. Não são convites compartilhados, login institucional nem publicação real de deliberações. A confirmação de parceiro é acessível somente no modo interno de testes.

## Pontos a confirmar antes de avançar além da demonstração
- Permissões e responsabilidades de convites/alterações/cancelamentos.
- Regras de edição e conclusão em equipe Socii.
- Regras institucionais de deliberação e registro.
- Grafia oficial do nome da aplicação.

## Publicação
Toda alteração deverá passar por compilação, testes e revisão de preview antes de promoção a produção.

## Ajuste de experiência v0.10.1 — redação
- Ação **Redigir proposição** inicia sempre um documento em branco, sem reutilizar a edição anterior.
- **Salvar rascunho** permite guardar uma redação incompleta sem tratá-la como concluída; o item reaparece na lista para continuação.
- A redação só segue para revisão quando os campos atendem aos critérios mínimos da prévia.
- O armazenamento continua limitado à sessão do navegador; nada é enviado a outros participantes.
- Teste de regressão: `tests/browser_drafts_v011.py` (320, 390, 740 e 1280 px).
