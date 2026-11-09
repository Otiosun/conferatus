# CONFFRATUS — QA de altura curta / Reflow de viewport (checkpoint 139, 09/11/2026)

## Contexto e regra máxima 21

A Etapa 07 mantém abertos 07.05 (zoom nativo), 07.06 (celular/IME/orientação) e 07.10 (a11y). A consulta W3C em 09/11/2026 confirma que WCAG 2.2 SC 1.4.10 exige reflow em largura equivalente a 320 CSS px (correspondente a 1280 px a 400% de zoom) e que SC 1.4.4 exige texto redimensionável a 200% sem perda de conteúdo/função:
- https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html

**Decisão:** ampliar regressão testável de tela baixa e drawer, sem inventar compatibilidade com zoom físico/IME. Evitar a alternativa de marcar 07.05/07.06 completos por equivalência de viewport; não reescrever CSS sem defeito observado.

## Mudança de código

- Novo `tests/browser_stage7_short_viewport_v0187.py` (commit `a7711ce16620ecb7bca1f5f5417ee78b6a6b68dd`).
- Inscrição no `validate` da branch `preview/v0.10.60-six-vote-forms` em `.github/workflows/preview-voting-check.yml` (commit `bc4827fa261cf81f36503040bff9d0415221a395`).
- NENHUMA mudança em HTML, CSS, JS, dados, Academy, `main`, PM2 ou produção.

## Prova delimitada

Artefato da CI anterior `42708774184`, HTML correspondente ao commit `bb14e32a`. O diff GitHub `bb14e32a...fb918fa` continha exclusivamente um teste e documentação; não alterou o aplicativo. O teste novo foi recuperado do GitHub e seu hash de objeto verificado (`c8563d9868dbcda3e2922c30fc23c7b2891e1cc3`) antes de nova execução local.

Matriz local Chromium: 6 dimensões (280×256, 320×256, 390×256, 280×320, 320×360, 640×256) × 8 rotas/estados = **48/48**, além de 6 jornadas do menu via foco, Enter, rolagem até a quarta ação e clique, sem erro JS ou scroll horizontal nos estados examinados; botão Menu com altura >=44 CSS px. Capturas 280×256 e 390×256, JSON de 48 resultados, script e hashes armazenados no **Drive Komekko privado**:
https://drive.google.com/file/d/1xKPx-nShvFZMoGrjzb6jSt5p4y1g4s3n/view

SHA256 do ZIP: `8f423988bc232dee3cc2de7c5f17a85d0e4bdf0f984512ae93a8d45491e723db`.

## Limites e próximo gate

Isto NÃO demonstra zoom nativo 400%, redimensionamento real de cada campo, Android/iOS, teclado virtual real, TalkBack/VoiceOver, WCAG 2.2 AA integral nem aprovação Megalos. A CI do novo commit em repositório privado pode falhar antes do runner por cota. Não prometer aprovação remota sem um job executado no SHA correspondente.

Checklist formal mantida: 01=4/5, 02=0/4, 03=1/5, 04=17/22, 05=2/4, 06=2/5, 07=7/12, total 33/57. D1–D6, identidade Academy, votação institucional e publicação autorizada permanecem gates próprios.

Próximo objetivo independente: aprofundar 07.05/07.06 com revisão de *foco/scroll/teclado virtual* no dispositivo quando possível, corrigir somente defeitos reproduzidos; no paralelo preparar decisões Megalos D1–D6, sem publicar alterações na `main`.
