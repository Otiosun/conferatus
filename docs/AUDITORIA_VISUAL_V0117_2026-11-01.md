# CONFERATUS — Auditoria visual das referências da Megalos (01/11/2026)

**Escopo:** comparação de 6 imagens originais `1001930221.jpg`–`1001930226.jpg` (710 × 1536 px cada) e uma amostragem do vídeo original `1001930216.mp4` (~54,7 s, quadros conferidos em aproximadamente 0, 10,9, 21,9, 32,8, 43,7 e 54,2 s). Foram examinadas as capturas locais de telas da prévia v0.10.16 e, para a v0.10.17, o calendário em 390/740 px. **Não é aceite formal da Megalos nem análise quadro a quadro do vídeo inteiro.**

| Referência | Elementos que podemos identificar | Situação na prévia / pendência |
| --- | --- | --- |
| `0221`: calendário e programação expandida | Grande painel azul; item `Iniciar uma Votação`; linhas de programação; detalhe azul expandido com PDR, descrição e ação de cancelamento | Grade mensal interativa no painel azul, linhas de programação, detalhe azul, seção e datas estão implementados. **Diferença relevante:** referência mostra painel azul sem grade visível; a prévia expõe calendário mensal, o que pode ser um aperfeiçoamento funcional, mas não tem confirmação visual da Megalos. A ação de cancelamento do evento de exemplo da prévia é desabilitada por ser fictício. |
| `0222`: revisão com Socii | Barra escura com participantes/tempo; faixa azul de título; texto cinza; folha de confirmação clara, com seção e tipo; ações Cancelar/Confirmar | Revisão e confirmação estão presentes. Na prévia, a barra Socii não inventa duração e informa progresso local; tempo exibido no modelo **não foi implementado** sem uma regra real. Conferir densidade, espaçamento e altura da folha com a Megalos. |
| `0223`: confirmação sem ação dupla | Folha de revisão posicionada no rodapé do texto e um botão Confirmar, sem Cancelar aparente | A prévia usa cancelamento explícito para preservar a navegação de volta à redação. Diferença de decisão entre as referências `0222` e `0223`; Megalos deve definir contexto/estado de cada variação, antes de retirar a ação. |
| `0224`: editor Socii | Barra de coautores, faixa azul do título, área ampla de escrita, botões Concluir e Voltar | Área de redação e barra Socii local presentes; o fluxo demonstrativo também possui Salvar rascunho, que não é visível na referência. Não transformar isso em convite real; confirmação externa existe somente em modo demo. |
| `0225`: perfil/proposições | Avatar sobre faixa azul, métricas Votos/PDR/PR/Ofício/Socii, duas abas, histórico e ações Socii/Redigir | Esses blocos existem em prévia com dados fictícios. Comparar detalhe de tipografia/posicionamento, em particular indicador de avatar, abas e altura do painel inferior. Sem aceite final. |
| `0226`: agendamento em painel inferior | Perfil com histórico e, no rodapé, painel azul que solicita proposição, seção, duas datas e tipo; botão Confirmar | A prévia reúne título e descrição objetiva com os campos citados, mas mostra o formulário na **rota calendário**, não diretamente como painel inferior no perfil. A posição/fluxo deve ser validada pela Megalos. Não deslocar sem aprovação. |

## Observações do vídeo
- O vídeo exemplifica a navegação entre **Proposições e Socii**, a opção de **Agendar e iniciar deliberação** e a apresentação de calendário e da folha de revisão. Há conteúdo mostrado dentro da interface de conversa (WhatsApp) no início; **não confundir a interface do telefone com uma tela do produto**.
- Não é possível inferir do vídeo regras de autenticação, votação real, convite remoto, durações, permissões ou tecnologia de backend.
- O título `Iniciar uma Votação` foi mantido por fidelidade ao material; a prévia **somente programa uma deliberação**. Em v0.10.17, uma nota curta aparece imediatamente após o botão com esta limitação, antes e durante a abertura do formulário. A alternativa de renomear o botão exige validação de produto.

## Critério para marcar a revisão visual final como feita
A Megalos (1) confirmar a grafia oficial e a distinção entre tela de programação e votação, (2) decidir se mantém a grade mensal dentro do painel azul, (3) validar a localização do formulário de agendamento e as duas variantes da folha de confirmação, (4) revisar no celular as principais telas em 390 px (inclusive estados abertos/fechados) e (5) aprovar a hierarquia, densidade, tipografia e navegação. Até lá, manter a tarefa de **fidelidade final** aberta.

## Verificações de engenharia
- Nenhum cadastro institucional, API, senha, regra de voto ou sistema multiusuário criado nesta rodada.
- Sem novas dependências; a pequena nota de limitação usa HTML e CSS existentes, com teste de acessibilidade/fluxo em quatro tamanhos.
- `package.json` contém `typecheck` e `build`, mas não `lint`; não descrever a compilação como auditoria lint.
- Arquivos oficiais e vídeo permanecem preservados, sem modificação.
