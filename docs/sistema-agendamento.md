# Sistema de pré-avaliação e agendamento: requisitos

Objetivo: o militar agenda a bioimpedância e preenche **antes** os dados, as fotos posturais, a anamnese e o recordatório 24h. Quando chega à academia, o avaliador já tem a ficha pronta.

O protótipo de referência é `prototipo/index.html`.

## Perfis
- **Militar**: agenda, preenche e acompanha a própria ficha e a evolução.
- **Avaliador** (profissional de Educação Física designado): agenda, fichas, alertas, registro dos resultados.
- **Gestor/Comando**: só indicadores agregados e anonimizados (adesão, % avaliados, uso da academia, evolução média). **Nunca dados individuais de saúde.**

## Fluxo do militar
1. **Identificação**: nome, nº PM, posto/graduação, companhia/fração, nascimento, sexo, WhatsApp, altura, função e escala.
2. **Agendamento**: escolher dia e horário (slots de 30 min, manhã e tarde). Aceitar as orientações de preparo:
   - jejum de 4 h;
   - sem cafeína por 12 h;
   - sem álcool por 48 h;
   - sem treino por 12 h;
   - bexiga vazia;
   - sem metais;
   - evitar pós-plantão noturno.
3. **Fotos posturais** (4): frente, perfil direito, perfil esquerdo e costas, com instruções de como tirar. Podem ser feitas na hora.
4. **Anamnese**:
   - PAR-Q (7 perguntas);
   - triagem da bioimpedância (marcapasso, implante metálico, gestação);
   - condições e medicamentos;
   - lesões e dor ligada ao serviço;
   - rotina (atividade, sono, tabagismo, álcool, água);
   - objetivo.
5. **Recordatório 24h**: refeições do **dia anterior à avaliação**, em medidas caseiras, indicando se foi dia de serviço ou de folga.
   - ⚠️ Liberar o recordatório (ou mandar o link por WhatsApp) **só na véspera**. Preenchido no ato do agendamento, ele descreve o dia errado.
6. **Revisão e consentimento LGPD**: dados e horário obrigatórios, o resto pode ficar pendente.

## Painel do avaliador
- Agenda por dia, com status de preenchimento por militar (Dados / Fotos / Anamnese / Recordatório).
- **Alertas automáticos**:
  - qualquer "sim" no PAR-Q, marcapasso ou gestação: **bioimpedância contraindicada**, encaminhar ao médico;
  - implante metálico: registrar o local.
- Ficha completa e registro dos resultados (bioimpedância, perimetria, observações posturais).
- Histórico longitudinal por militar (comparar avaliações).

## Indicadores (critérios de avaliação da proposta, seção 8.4)
- Adesão do efetivo e % de militares avaliados.
- Uso da academia.
- Evolução dos indicadores físicos (média do grupo).
- Cumprimento dos protocolos.
- Relatórios gerados.
- **Linha de base de afastamentos** no mês 1, para comparar no mês 12 (lacuna apontada na análise).

## Requisitos não funcionais
- Login (e-mail/telefone + OTP). RLS no banco: cada militar só vê a própria ficha, e o avaliador vê as fichas da sua guarnição.
- Fotos em bucket **privado**, com URLs assinadas de curta duração.
- Registro de acesso aos dados de saúde.
- Exclusão a pedido do titular.
- Mobile-first: o militar preenche pelo celular.
- Lembrete por WhatsApp na véspera (preparo + link do recordatório).

## Pendências a decidir com o Comando
- Pode rodar fora da infraestrutura da PMMG? Quem é o controlador dos dados?
- A participação é voluntária ou obrigatória?
- Quem é o avaliador designado e quais as horas dedicadas.
