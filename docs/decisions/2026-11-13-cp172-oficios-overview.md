# CP172 — Quantitativo de Ofícios no resumo que Megalos circulou (13/11/2026)

**Pedido explícito e referência:** Megalos enviou uma captura do histórico institucional com a região Votos/PDR/PR circulada, dizendo "tem que adiciona o quantitativo de oficio também". A prévia tinha o indicador Ofício no perfil pessoal, mas NÃO naquele resumo institucional. O primeiro diagnóstico anterior confundira as duas áreas; corrigido após consultar o código exato.

**Mudança mínima:** acrescentada a quarta figura `Ofícios` ao lado de Votos/PDR/PR na `overviewPage`. Quantidade derivada exclusivamente das `officialLetters` da fixture atual de membros sintéticos: `m01=23`, os demais sem quantidade declarada; portanto 23 Ofícios no exemplo, sem criar dado externo ou alegar total real. A linha de quatro figuras compactas usa grid de 12 colunas em telas até 360px; chips Aprovados/Arquivados permanecem em suas posições e demais valores não foram alterados. Não modificar dados de exemplo em produção.

**Teste:** `browser_first_time_voting_journey_v0211.py` visita a rota institucional, valida exatamente quatro figuras incluindo `23 Ofícios`, ausência de overflow horizontal e volta à home, prosseguindo com a jornada completa existente nas larguras 320/390/740/1280. Nenhum teste removido ou afrouxado.

**A segunda imagem** mostra `Grupo Votante`, semicírculo de assentos, `76%`, barras amarelas e uma descrição. É uma referência visual que AINDA não corresponde à estrutura atual de resultados/participação da prévia. Não interpretar os 80 votos/80% repetidos como cálculo consistente ou construir quórum, atualização em tempo real, resultado oficial, nem estados institucionais sem Megalos. Registrar a lacuna visual e solicitar definição após apresentação. A palavra e o material dela prevalecem na aparência e nos pedidos confirmados.

Esta correção não altera regras de votação, calendários, Socii, backend, `main` ou produção. CI do novo SHA obrigatória antes de reivindicar aprovação; decisões D1–D6 e avaliação da página de votação permanecem pendentes.
