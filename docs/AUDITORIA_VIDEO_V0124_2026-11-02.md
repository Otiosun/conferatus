# CONFERATUS — Auditoria temporal do vídeo original da Megalos — v0.10.24 (02/11/2026)

> **Somente documentação de evidências.** Esta revisão não homologa a interface, não altera `src/`, não autentica identidade e não representa funcionamento institucional. O vídeo é uma gravação de tela que passa pelo WhatsApp e por mídia compartilhada; mostrar uma sequência de telas **não comprova** que as ações operavam num sistema integrado.

## Proveniência e método

- **Fonte exata:** `1001930216.mp4`, 25.041.156 bytes, SHA-256 `cd038526637541ed7ad960c7dbb7ac654278e0aa04e8124543daabb221f3570b`. O [arquivo original completo também está preservado no Komekko](https://drive.google.com/file/d/11rIyxCOFPX_zeWQOG59pLkbCdTkDgnuP/view): foi **baixado novamente do Drive** e seu SHA-256 conferido byte a byte com o arquivo original; 25.041.156 bytes idênticos.
- **Propriedades:** H.264, 720 × 1604 px, duração **54,662844 s**, aproximadamente 15 quadros/s na média.
- **Análise:** 109 amostras a cada 0,5 s, diferenças visuais de quadros reduzidos para localizar transições, com inspeção em resolução integral em ~22 instantes críticos; não houve OCR, identificação de pessoas ou transcrição automática. A gravação foi revisada visualmente em todo o intervalo, com maior densidade nos estados importantes.
- **Artefato visual privado:** [Adendo PDF de quatro páginas no Komekko](https://drive.google.com/file/d/1zp8vzL74uAnvi7ygb8zLZupnIWNUA591/view). São imagens do vídeo original, mantidas fora do repositório público. SHA-256 do PDF: `f3e2e3b84161d82d1716bdf5c04ed724c6e456b986f469996f5510420acbea66`.
- **Base comparativa:** seis referências 1001930221–1001930226.jpg e seis capturas v0.10.22 a 390 px do [kit anterior](https://drive.google.com/file/d/1M5NN_tT4VQ_-Vp7YF8PU48kzj4DT3Jz-/view). Nenhuma dessas fontes foi editada.

## Linha do tempo: evidência, não hipótese de produto

| Trecho aprox. | Observável na gravação | Limite |
| --- | --- | --- |
| 00,0–20,0 s | Chat da Megalos com imagens de agendamento, redação e revisão; mensagens descritas abaixo | WhatsApp não representa uma sessão autenticada no CONFERATUS |
| 23,5–25,0 s | Formulário azul de agendamento **sob o perfil**, com proposição, seção, início, término, tipo e Confirmar | Não prova se outra rota é permitida |
| 26,0–28,5 s | Perfil com cinco métricas e aba Proposições/Socii; painel Socii inferior, ações convidar/redigir | Contadores e nomes visíveis são ilustrativos |
| 29,2–30,2 s | Editor de título e texto com controles Concluir e Voltar | Não se observa salvamento real |
| 31,8–35,0 s | Faixa escura do Socii **no topo da revisão**, formulário seção/tipo e ação Confirmar visível | Não prova a condição para apresentar apenas Confirmar |
| 39,3–41,8 s | Revisão com faixa superior Socii, mensagem de confirmação pela autoria e **Cancelar + Confirmar** | Não prova a transição de estado, papel ou permissão |
| 42,7–50,0 s | Calendário com painel azul compacto, botão Iniciar uma Votação e lista com expansão da proposta/deliberação | A ausência de grade mensal no quadro não prova que ela seja proibida |
| 50,5–54,66 s | Retorno a chat e miniaturas de telas | Nenhuma evidência de integração remota |

### Mensagens escritas: confirmação mais forte que inferência visual

- **~04,1 s, Megalos:** “Concluindo uma Proposição; Seção Responsável por ela e o Tipo (PDR, PR, Ofício)”. O tipo **Ofício** não deve ser omitido.
- **~04,1 s e ~36,5–40,5 s:** a legenda explica a visão do parceiro Socii quando outro conclui a proposição e exige conclusão de todas as partes participantes antes de concluir.
- **~18,4 s, Megalos:** “Onde temos Votos, PDR, PR e Socii, você adiciona o Ofício”, instrução relativa às métricas do perfil.
- **~23–25 s:** a mídia mostra agendamento sob o perfil, não um botão de inicialização de voto efetiva.

### Confronto com o código: NÃO recriar uma implementação que já existe

`src/main.ts` publicado na v0.10.22 e **não modificado** na v0.10.23 já declara `type ProposalType = 'PDR' | 'PR' | 'Ofício'`, valida os três tipos no restauro, apresenta os três na revisão e no agendamento, e exibe métrica `Ofício` no perfil. Portanto as duas instruções sobre **Ofício** já estão refletidas na **prévia demonstrativa**. **Isso não valida regras de votação ou registro institucional de Ofícios**.

## Decisões D1–D6: reforço de evidência, aceite ainda aberto

- **D1 (calendário):** mais evidência a favor da aparência compacta sem grade visível (42,7 s); não definir proibição de grade nem alterar texto do botão sem Megalos.
- **D2 (agendamento):** agora evidência temporal adicional de posicionamento sob o perfil (23,5–25 s). A prévia atual usa a rota Calendário, portanto o posicionamento visual continua divergente; autorização institucional e fluxo completo não estão demonstrados.
- **D3 (botões da revisão):** o mesmo trecho de vídeo contém `Confirmar` aparentemente isolado (~31,8 s) e `Cancelar/Confirmar` (~39,3 s); ainda **não há critério confiável** para diferenciar estado/papel e portanto nenhum botão foi removido.
- **D4 (faixa Socii):** o vídeo mostra a faixa e “127 horas” também na revisão (~31,8 s), não só no editor. A prévia atual omite a faixa na revisão; **diferença visual confirmada**. O valor “127 horas” é visível, mas seu significado, origem e atualização são desconhecidos. Não criar temporizador.
- **D5 (editor):** Concluir e Voltar visíveis em 29,2 s; Salvar rascunho da prévia não aparece na fonte. Não apagar funcionalidade protetora antes de definir persistência.
- **D6 (perfil):** cinco métricas e aba Proposições/Socii reforçadas em 23,5–28,5 s; proporções e densidade aguardam aceite.

**Resultado importante:** este adendo **não transforma D1–D6 em decisões respondidas** e não cria artificialmente D7 pendente. `Ofício` é uma instrução explícita da Megalos **já atendida quanto às opções demonstrativas**.

## Leis máximas e checklist

- `AGENTS.md` / `docs/CHECKLIST_MESTRA.md` retomados antes do trabalho. Fonte de design original intacta, sem dependência, mudança de código, backend, políticas ou decisão de UX presumida.
- **Seis etapas invariantes:** 01=4/5, 02=0/4, 03=1/5, **04=17/22 ativa**, 05=0/4, 06=0/5; são itens marcados, não prontidão real.
- Branch isolada de documentos `preview/v0.10.24-video-evidence` a partir da v0.10.23; `main` congelada em `4b244591c2f42913d2dca051b7d1256b896d25d8`. Sem merge e sem alterações em `src/`, `tests/`, CSS, ativos e dados privados.
- **Testes desta rodada:** análise do arquivo + geração e renderização visual do PDF; inspeção da fonte e correspondência de tokens `Ofício`. **Não foram reexecutados os 22 scripts Playwright nem os 18 Node nesta rodada documental**. O último resultado desses testes é o da rodada v0.10.22; não converter o CI de documentação em homologação.
- **Próximo gate:** encaminhar o kit de sete páginas + este adendo à Megalos para respostas D1–D6 e validar a revisão no celular antes de implementar. Não enviar mensagens sem autorização; documento é entregável para comunicação externa.

## Ficheiros para restauração

- `docs/AUDITORIA_VIDEO_V0124_2026-11-02.md` — este documento.
- `docs/KIT_DECISOES_MEGALOS_V0123_2026-11-01.md` — matriz de aprovação antes da revisão temporal.
- PDF privado Komekko: https://drive.google.com/file/d/1zp8vzL74uAnvi7ygb8zLZupnIWNUA591/view
- [Vídeo original completo no Komekko](https://drive.google.com/file/d/11rIyxCOFPX_zeWQOG59pLkbCdTkDgnuP/view), baixado e comparado por SHA-256 idêntico à fonte local `1001930216.mp4`. O repositório **não** contém nem precisa conter o vídeo original.
