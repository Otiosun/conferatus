# CONFERATUS — demonstração v0.8.12

Prévia clicável da Parte 1 enviada pela Megalos. **Todos os dados são sintéticos.** Não há autenticação, banco de dados ou votação real. O cadastro institucional não é acessado nem alterado.

## Testar agora (sem instalação)

Abra `dist/CONFERATUS_demo_offline.html` num navegador moderno. Se o visualizador de arquivos bloquear HTML/JavaScript, use um servidor estático ou publique a pasta `publish/`.

## Publicar para compartilhar uma URL

**Mais simples:** envie o conteúdo da pasta `publish/` para um serviço de hospedagem de sites estáticos (Cloudflare Pages/Netlify Drop). Ela contém `index.html` (100% autossuficiente), `preview.png`, `robots.txt` e `_headers`. Não precisa instalar dependências ou ativar backend.

Se preferir um build com assets separados, também existe a pasta `dist/`; o app agora usa caminhos relativos. Um host como GitHub Pages funcionará em subcaminho, desde que sirva a pasta `dist/` e suporte navegação com `#`.

Para gerar um cartão de compartilhamento com `og:image` absoluto depois de escolher o endereço público, execute: `PUBLIC_URL=https://endereco-real.example npm run build` e publique `publish/` novamente. Sem `PUBLIC_URL`, o cartão terá título e descrição, mas **não** terá a imagem anunciada nas tags Open Graph. Nunca substitua por um domínio inventado.

**Importante:** o link do arquivo HTML anexado numa conversa não é a mesma coisa que um website. A URL compartilhável só passa a existir depois da hospedagem efetiva.

## Desenvolver

- Node 20+ e TypeScript 5.8.
- `npm install` para instalar a dependência de desenvolvimento.
- `npm run build` para gerar `dist/` e `publish/`.
- `npm test` para testar as regras.
- `python tests/browser_v08.py`, `python tests/browser_microversions.py`, `python tests/browser_v088.py` e `python tests/browser_v0812.py` para os testes de interface (necessita Playwright Python e Chromium).
- `npm run serve` para testar `dist/` em `http://127.0.0.1:5173` em ambiente sem restrições de navegador.

O protótipo utiliza **TypeScript puro**, CSS e HTML; não há React nem Vite instalados nesta versão de demonstração, por escolha deliberada de simplicidade. A camada de dados está isolada em `src/data` e `src/domain` para integração posterior.

## Checkpoints

- Regras de produção: `AGENTS.md`.
- Plano mestre: `docs/PLAN_MASTER.md`.
- Registro de mudanças: `docs/checkpoints/C1_V08_2026-10-28.md`.

Nenhuma alteração foi feita em sistema externo, repositório remoto ou conta de hospedagem.

## Apresentação v0.8

Abra **Menu → Como testar esta prévia** para ir diretamente a votação, perfis ou administração.
O botão **Reiniciar demonstração** restaura os estados simulados.

A hospedagem ainda não foi feita. Testes nesta sessão precisaram usar `set_content` e
simulação de armazenamento de sessão porque a navegação HTTP/file é bloqueada neste ambiente.

## Subversões v0.8.x

- **0.8.1:** pesquisa normalizada (maiúsculas/acentos/IDs fictícios) e validação defensiva de dados de sessão.
- **0.8.2:** retenção do foco em controles atualizados, modal acessível, tecla Esc e foco na edição.
- **0.8.3:** recuperação de URLs inválidas de perfis com caminho de volta.
- **0.8.4:** verificação automatizada dos arquivos de publicação e relatório de regressão.

Ver detalhes e limitações em `docs/checkpoints/C1_V084_SUBVERSOES.md`.

- **0.8.5:** mantém a posição da página ao expandir proposições e atualizar estados locais.
- **0.8.6:** botão de limpar busca com retorno do foco ao campo.
- **0.8.7:** validação de ACDM ID duplicado diretamente no formulário, com mensagem acessível e foco no campo.
- **0.8.8:** foco no botão Desfazer após edições, teste de regressão de scroll/erros e quatro larguras de tela.

O histórico detalhado está em `docs/checkpoints/C1_V088_SUBVERSOES.md`.

- **0.8.9–0.8.12:** busca com DOM estável no celular, validação explícita de identificadores, melhorias de acessibilidade e atalho para conteúdo principal. Ver `docs/checkpoints/C1_V0812_SUBVERSOES.md`.

## Cloudflare Pages (integração GitHub)

Usar o repositório com os arquivos desta pasta na **raiz** do GitHub. No Cloudflare Pages, selecionar o projeto via **Connect to Git**.

- **Framework preset:** None (não é Vite; TypeScript puro)
- **Production branch:** main
- **Build command:** `npm run build`
- **Build output directory:** `publish`
- **Root directory:** `/` (raiz do repositório)
- **Variáveis:** nenhuma para a demonstração atual

O comando gera `publish/index.html`, `publish/preview.png` e o restante dos arquivos estáticos. Sem autenticação nem dados reais.
