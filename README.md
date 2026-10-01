# PIPHPO

**Programa Institucional de Performance Humana e Prontidão Operacional**: proposta de projeto-piloto de inovação em gestão pública na **Guarnição de Patos de Minas** (10ª RPM / PMMG), de autoria do Cb PM Leandro Carvalho Delavy.

Este repositório reúne o material de apoio à proposta:

| Pasta | Conteúdo |
|---|---|
| `site/` | **Apresentação em site** (pitch navegável por teclado, usada no lugar de slides) |
| `docs/proposta/` | Proposta executiva (`v1` com 15º BPM, `v2` com Guarnição de Patos de Minas, a atual) |
| `docs/` | Análise crítica da proposta e requisitos do sistema de agendamento |
| `prototipo/` | Protótipo clicável do portal de pré-avaliação (HTML único, sem backend) |
| `video/` | Pitch animado de ~80 s: fontes HTML, scripts de render e trilha, vídeo final em `video/out/` |

## Apresentação (site)

Abra `site/index.html` ou publique no GitHub Pages (Settings → Pages → branch `main`, pasta `/ (root)`); a raiz redireciona para `site/`.

- 15 seções em tela cheia, navegação com **← →**, **espaço**, **Home/End**; **F** tela cheia; **?** atalhos.
- Ciclo de gestão interativo, contadores, cronograma animado, protótipo rodando ao vivo num celular e o vídeo do pitch.
- Precisa de internet para as fontes (Google Fonts); o restante é local.

## Protótipo

Abra `prototipo/index.html` no navegador. Duas visões:
- **Portal do militar**: dados → agendamento da bioimpedância → fotos posturais → anamnese (PAR-Q + triagem BIA) → recordatório 24h → revisão + consentimento LGPD.
- **Painel do avaliador**: agenda do dia, status de preenchimento (D/F/A/R), alertas de saúde e ficha completa.

Os dados são de exemplo e nada é salvo.

## Vídeo

```bash
cd video
npm install                     # fontes Barlow / Barlow Condensed
pip install playwright          # usa o Chromium do Playwright
python3 scripts/render.py       # gera out/PIPHPO_pitch.mp4 (sem áudio, com capa)

# com trilha de marcha sintetizada:
python3 scripts/trilha_marcha.py && python3 scripts/render.py --audio out/marcha.wav --out out/PIPHPO_pitch_marcha.mp4
```

A página `src/pitch.html` expõe `window.render(t)`, que posiciona tudo em função do tempo. O render captura quadro a quadro (30 fps), então é determinístico.

## Próximo passo

Transformar o protótipo em sistema real: veja `docs/sistema-agendamento.md`.
