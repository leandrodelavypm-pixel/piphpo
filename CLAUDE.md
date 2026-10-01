# CLAUDE.md: contexto do projeto PIPHPO

## O que é
Material de apoio a uma proposta interna à PMMG (10ª RPM) para um projeto-piloto de gestão da performance humana na **Guarnição de Patos de Minas**. O autor da proposta é o **Cb PM Leandro Carvalho Delavy** (Educação Física, CREF-MG). O desenvolvimento técnico é do **Maiton**.

Use sempre **"Guarnição de Patos de Minas"**, nunca "15º BPM" (nomenclatura antiga, só na v1 do documento e nos arquivos `variantes_*`).

## Idioma e tom
- Todo texto de interface, documentação e commits em **português do Brasil**.
- O público final é militar e o Comando: linguagem institucional, objetiva, sem jargão de TI.

## Identidade visual
- Cores institucionais (padrão das viaturas e da farda): **preto** `#111213`, **cáqui** `#B7A076`, **cinza** `#6E7275`. O vermelho do triângulo do brasão `#C21F2B` entra só como destaque.
- Tipografia: Barlow Condensed (títulos) + Barlow (texto).
- Brasão oficial em `video/assets/brasao.png` (PNG transparente). Não redesenhar nem alterar.
- Grafismo: faixas diagonais cáqui e cinza (referência às viaturas).

## Estrutura
- `prototipo/index.html`: protótipo autocontido (HTML/CSS/JS vanilla, estado em memória). Base para o sistema real.
- `video/src/pitch.html`: animação do pitch. Cada cena é controlada em `render(t)` por janelas de tempo (`fade(el,t,in0,in1,out0,out1)`). Para mudar o texto, edite o HTML. Para mudar o tempo, edite os números em `render`.
- `video/scripts/render.py`: render Playwright para ffmpeg. Capa de 2 s com crossfade no início (a miniatura do WhatsApp usa o 1º quadro).
- `docs/sistema-agendamento.md`: requisitos do sistema real.

## Regras importantes
- **Dados de saúde são sensíveis (LGPD art. 11).** Anamnese, fotos posturais e bioimpedância: acesso restrito ao avaliador, consentimento explícito e nunca usados para escala, promoção ou avaliação de desempenho.
- Os nomes do painel de exemplo (Araújo, Moreira, Fontes, Rezende…) são fictícios. Não use dados reais de militares em exemplos.
- Não fazer promessas de resultado (redução de afastamentos etc.) em material do programa: a proposta só se compromete a **medir**.

## Stack sugerida para o sistema real
Next.js + Supabase (Auth, Postgres com RLS, Storage privado para fotos) + Vercel, no mesmo padrão de outros projetos do Maiton (OnTrac). Lembretes por WhatsApp na véspera, com o preparo da bioimpedância e o link do recordatório 24h.
