# CONFFRATUS — Plano de fechamento por gates | 09/11/2026

**Status comprovado nesta data:** branch `preview/v0.10.60-six-vote-forms`, baseada no checkpoint 135 em `4ca172e`; `main` intocada. D2 (`?demo=1&d2=sheet`) e D3 (`?demo=1&d3=single`) são propostas experimentais, **não** escolhas aprovadas pela Megalos. Nenhuma persistência institucional, voto oficial ou autenticação Academy está operacional neste sistema demonstrativo.

Este plano distingue **entrega demonstrativa** e **entrega institucional**. Não converter subitem de checklist, commit, contagem de testes ou número de telas em porcentagem de trabalho restante.

## Inventário oficial antes deste lote

| Etapa | Fechados | Total | Pendências estruturais |
| --- | ---: | ---: | --- |
| 01 · Estabilização | 4 | 5 | Grafia oficial da marca |
| 02 · Votação e registro | 0 | 4 | Regras, acesso, registro e voto reais |
| 03 · Perfis/histórico | 1 | 5 | Dados e históricos institucionais |
| 04 · Calendário/proposições/Socii | 17 | 22 | Agendamento, confirmação, Socii e fidelidade |
| 05 · Academy | 2 | 4 | Login real e teste da integração |
| 06 · Entrega | 2 | 5 | Revisão, QA final e promoção autorizada |
| 07 · Acessibilidade/responsividade | 7 | 12 | Zoom, compactos, leitor de tela, aceite visual e dispositivos |
| **Total** | **33** | **57** | **24 critérios formais abertos** |

## Sequência crítica e limites de execução

### Gate A — recuperar verificações automáticas

**Problema confirmado:** a execução `42685990179` do SHA `4ca172e` falhou em duas tentativas sem alocar runner nem iniciar etapas. A página de commits registra Cloudflare Pages SUCCESS para o preview; isso **não** substitui Node/Chromium/Firefox/WebKit/PostgreSQL. A anotação do job falho existe, mas o conector disponível não consegue consultar `/check-runs/{id}/annotations`. Quota/billing são hipóteses, **não diagnóstico fechado**.

**Ação necessária do proprietário:** verificar a anotação do job e o estado GitHub Actions em Settings → Billing and licensing → Usage/Budgets/Payment information. Não aumentar limites, cadastrar pagamento, alterar visibilidade do repositório ou disparar repetidos reruns sem autorização. Se a causa for infraestrutura, resolver com a menor alteração autorizada e **executar a CI do HEAD exato**.

**Saída:** `validate`, `cross-browser-lab` e `postgres-lab` completos/success com URL do run e SHA exato; Cloudflare isolada verificada; artefato HTML baixado e screenshots produzidas desse build, não de patch sobre HTML antigo.

### Gate B — completar o que é independente de terceiros

- Regressões de navegação, redação, revisão e salvamento de campos, inclusive D2/D3 sob suas flags experimentais, sempre com resultados reproduzíveis e novos gates de CI.
- Etapa 07.05: matrizes de viewport equivalente a zoom 400%, **texto 200%**, controle de foco e legibilidade em formulário. A nova `tests/browser_stage7_interactive_text_zoom_v0185.py` soma 64 verificações sintéticas com jornada interativa em quatro larguras, Chromium local no HTML de CI anterior. **Não há teste de zoom nativo, hardware ou HEAD final comprovado. O item 07.05 continua aberto.**
- Etapa 07.06: fluxos inteiros em 280/320/360/390, altura curta, rotação e teclado virtual. Medição de viewport reduzido não é ensaio de IME real.
- Etapa 07.10: WCAG 2.2 AA por critério, árvore acessível, contraste, erro/estado, foco visível, reduced motion; TalkBack/VoiceOver em dispositivo quando possível.
- QA de recuperação, integridade e dados fictícios: impedir perda silenciosa, repetir casos negativos e separar cada prova local de aprovação de integração real.

**Saída:** checklist de evidências por teste e data, commits e capturas identificados; não fechar requisito com base em suposição.

### Gate C — decisões visuais da Megalos (externo)

Obter respostas com texto inequívoco e referência:
- **Grafia** CONFFRATUS ou CONFERATUS;
- **D1/D1b** calendário com grade sempre visível/compacta e rótulo real da ação;
- **D2** agendamento no calendário, perfil ou ambos; avaliar a folha azul candidata sem presumir aceite;
- **D3** em qual etapa existe a variante com um único botão; definir saída/foco e transição de estado;
- **D4** regra Socii/temporizador, origem de `127 horas`, se real;
- **D5** salvar rascunho visível e recuperação;
- **D6** proporção/densidade do perfil e métricas.

Não enviar mensagem à Megalos automaticamente; não simular resposta. **Saída:** decisões assinadas/identificadas, com data e critérios de comparação às seis imagens e ao vídeo. Só então implementar diferenças aprovadas, repetir gate A/B e obter aceite da interface.

### Gate D — contrato institucional com a Academy (externo)

Solicitar por canal autorizado: identidade e sessão confiável, autorização por papel/seção, endpoints autenticados, persistência, vínculos e IDs, assinatura/conclusão de Socii, calendário e fusos, quórum/métodos de voto, registro/auditoria, privacidade, ambientes de teste, owner do login e do backend. Não criar tabela nem sincronização de dados reais a partir de mockups.

**Saída:** interfaces e políticas documentadas, ambiente de homologação e testes de integração. O adaptador de identidade e o uso do ACDM ID existentes **não são autenticação**.

### Gate E — liberar entrega institucional

- Testes E2E reais autorizados, incluindo erros de autenticação, concorrência, conflitos, autorização, reconexão, histórico, voto e Socii; revisar logs e retenção conforme política.
- Revisão visual aprovada, dispositivos/zoom/acessibilidade com evidências, bundle e segurança verificados.
- Plano de deploy/rollback, revisores e aceite explícito antes de merge na `main` e Cloudflare principal. **Nenhuma promoção sem autorização.**

**Caminho rápido e honesto:** finalizar primeiro uma demonstração tecnicamente estável, segura e comparável às referências; obter decisões de Megalos e contratos Academy em paralelo; só depois integrar e liberar produção. A maioria dos 24 itens restantes **não são 24 correções equivalentes**.

## Arquivos/entradas prioritárias

- `docs/CHECKLIST_MESTRA.md` — fonte de verdade de critérios, contagens, exceções.
- `docs/KIT_DECISOES_MEGALOS_V0123_2026-11-01.md` — perguntas D1–D6, ainda sem aceite.
- `docs/ETAPA_07_FRONTEND_PERFECCIONISMO_2026-11-02.md` — matrizes de responsive/a11y.
- `tests/browser_stage7_zoom_reflow_v0135.py` e `tests/browser_stage7_interactive_text_zoom_v0185.py` — testes de reflow e interação.
- `docs/decisions/2026-11-09-d3-modal-experimental-isolado.md` — hipótese experimental D3, não regra institucional.

**Regra de integridade:** preservar a `main`, os dados Academy, PM2, aplicações externas e contas; nenhum resultado fictício deve ser apresentado como voto, registro ou autorização real.
