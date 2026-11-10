# CONFFRATUS — roteiro de demonstração e entrega da prévia

**Referência:** branch `preview/v0.10.60-six-vote-forms` · demonstração por navegador ou HTML offline, novembro de 2026.

Este roteiro apresenta **o produto que nossa equipe entrega**, sem sugerir autenticação ou autorização Academy. Os membros, resultados e dados institucionais exibidos na prévia são fictícios. As propostas, os Socii e os agendamentos criados pelo demonstrador pertencem somente à sessão do navegador. A integração efetiva com a Academy cabe à equipe responsável por ela.

## Preparar a apresentação

1. Abra a [prévia da branch no Cloudflare Pages](https://preview-v0-10-60-six-vote-fo.conferatus.pages.dev), **nunca o domínio principal**, para a revisão. O check **Cloudflare Pages SUCCESS** foi conferido no GitHub para o commit `fafae4a` (09/11/2026), mas **não conseguimos verificar diretamente a abertura/navegação do endereço neste ambiente**. Confira-o no navegador do aparelho antes de compartilhá-lo com a Megalos. O check de deploy não substitui a CI: o GitHub Actions do mesmo commit falhou antes dos testes, sem runner disponível.
2. Use a interface **sem** `?demo=1` para a apresentação principal. O parâmetro `?demo=1` é reservado às ferramentas avançadas de teste.
3. Trabalhe apenas com os registros fictícios. Não introduza dados pessoais, credenciais ou informações privadas da Academy na demonstração. Para aprovação visual, reutilize o [formulário D1/D1b–D6 já existente no Drive Komekko](https://docs.google.com/document/d/1RFp2s-QzzigkQRDBhej_QIVr7bxYB7yhCvBWD7TERDw/edit), sem criar outro questionário nem presumir a resposta da Megalos. Se baixar o HTML offline para um PC, prefira servir a pasta com `python -m http.server 8765 --bind 127.0.0.1`, pois a origem `file://` pode bloquear o `sessionStorage` ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage)).

## Jornada principal: mostrar, não prometer

1. **Votação fictícia:** na tela inicial, mostre os resultados de exemplo. Abra a descrição, escolha uma opção e depois use **Alterar escolha**. O painel esclarece que nenhuma escolha é enviada à Academy; a alteração é visual e local.
2. **Diretório e perfis:** em **Menu → Membros e Serviços da Cúpula Cíntia**, use a busca, abra um perfil, consulte as abas e observe os indicadores sintéticos. Um ACDM ID mostrado na tela é uma referência, nunca um login.
3. **Redação de proposição:** em **Menu → Elaborar Proposição e Socii**, crie um documento fictício, salve um rascunho e retome a redação. Preencha título e corpo e avance à revisão. A conclusão de autoria e o armazenamento são simulados/localizados nesta aba.
4. **Socii:** antes de encerrar uma proposta, abra **Convidar para Socii**, escolha explicitamente um membro fictício e observe o progresso de confirmações no modo de demonstração. Nenhuma pessoa recebe convite ou aprovação remota.
5. **Agenda e vínculo:** finalize uma proposição elegível na prévia; em **Menu → Agendar e Iniciar Deliberação**, abra o formulário de programação, selecione a proposição e a modalidade, preencha título, descrição e datas válidas. Para métodos não binários, configure as alternativas que o formulário exigir. A ação cria somente uma programação local.
6. **Navegação e cancelamento:** no calendário, expanda a programação, abra a proposta ou o perfil do autor e volte pelo vínculo contextual. Cancele uma programação fictícia e mostre que sai da lista ativa, permanecendo no histórico local de cancelamentos.
7. **Histórico geral:** em **Menu → Histórico de Votações e Proposições**, abra a guia Proposições. Os documentos criados nesta sessão aparecem em bloco próprio, separados dos indicadores e registros fictícios antigos. Abra um deles e use **Voltar ao histórico**.

## Modo de testes avançados (`?demo=1`)

- O laboratório apresenta **seis modalidades demonstrativas**: binária, nominal, ordenada, por aprovação, escalar e cumulativa. Não declara quórum, vencedores, elegibilidade ou voto institucional.
- A modalidade cumulativa só aceita pesos configurados para participantes sintéticos; não assume regras da Megalos.
- Ferramentas administrativas simulam permissões e alterações de vínculo **sem conceder autorização real**.
- Em **Proposições e Socii**, as ações **Baixar cópia JSON** e **Restaurar cópia JSON** permitem testar a recuperação dos fluxos desta sessão. A restauração substitui os registros locais; exporte primeiro o que quiser preservar. O arquivo pode incluir textos que você digitou, não é criptografado e não deve ser compartilhado inadvertidamente.

## O que a entrega não faz

Não possui login Academy, votos institucionais, envio remoto de convites Socii, persistência compartilhada, apuração oficial, auditoria institucional nem sincronização entre contas. O laboratório PostgreSQL da CI é **isolado e descartável** e não integra a aplicação pública. IDs externos e seleção de perfil não autenticam usuários.

## Critérios objetivos de qualidade

- `npm run build` deve concluir o typecheck, a geração de HTML estático/offline e os testes Node.
- O workflow **Preview voting checks** é o gate de navegador e banco isolado. A lista vigente de testes está em `.github/workflows/preview-voting-check.yml`; qualquer falha impede considerar o novo checkpoint aprovado.
- A CI conserva um HTML offline e um conjunto separado de capturas Playwright, ambos com retenção limitada. Consulte a execução mais recente da branch no [GitHub Actions](https://github.com/Otiosun/conferatus/actions).
- Confirmar rotas, formulários, foco, feedback após erro, restauro de sessão, agendamentos, Socii e ausência de overflow nas larguras verificadas. Teste Chromium não certifica Firefox, WebKit, leitor de tela nem aparelho físico.
- Preservar a `main`, os dados reais e a produção até autorização expressa para promover a versão.

## Decisões visuais da Megalos ainda em aberto

Consultar `docs/KIT_DECISOES_MEGALOS_V0123_2026-11-01.md` e `docs/AUDITORIA_VIDEO_V0124_2026-11-02.md`. **D1/D1b:** calendário e nome da ação; **D2:** posição do agendamento; **D3:** variantes Cancelar/Confirmar; **D4:** barra Socii já exibida no editor e na revisão quando há participantes vinculados (CI #39); significado de duração ainda indefinido; **D5:** salvar rascunho; **D6:** proporções e densidade do perfil. As seis imagens e o vídeo originais são referências, não material autorizado para publicação no repositório.

**Status de entrega atualizado em 09/11/2026:** prévia demonstrativa com implantação de branch confirmada via check GitHub no SHA `fafae4a`, **sem aprovação integral da CI para esse SHA**, sem verificação direta da navegação no aparelho da Megalos, **sem homologação D1/D1b–D6** e **sem integração com a Academy**. O run [42708774184, tentativa 2](https://github.com/Otiosun/conferatus/actions/runs/42708774184), em `bb14e32`, aprovou PostgreSQL e Firefox/WebKit, mas reprovou `validate` por uma condição de corrida no teste de importação; correção posterior foi testada localmente. De `bb14e32` a `fafae4a`, o diff registrado contém apenas testes, workflow e documentação, não arquivos do aplicativo. HTML offline da execução anterior preservado no [Drive Komekko](https://drive.google.com/file/d/1h0wb4ug6C2UFSLvRvD0aOGoJQyTYU6CF/view). Uma revisão local Chromium de fluxo sintético em 320/390/740/1280 px passou com armazenamento simulado, **não por HTTP nem como CI do HEAD**. Não publicar na `main` nem entregar como votação real sem autorizações. Registre a aprovação de D1–D6 antes de modificar a composição que depende dessas decisões.
