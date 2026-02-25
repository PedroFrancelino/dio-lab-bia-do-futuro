# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Funcionalidade da JU |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Mostrar o historico de conversa entre a JU e o cliente, conhecendo o cliente de uma forma melhor e eficiente |
| `perfil_cliente.json` | JSON | Coletar os dados do cliente, junto com suas metas e duvidas|
| `tipos_investimento.json` | JSON | Mostrar ao cliente sobre os tipos de investimentos, e sugerir qual investimento ele deve fazer baseado no seu perfil e metas |
| `transacoes.csv` | CSV | Observar os gastos e recebimento do clinte para poder organizar suas metas |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

- Expandi os dados de "tipos_investimentos", adicionando produtos para investimento como por exemplo: (Criptomoedas, Poupança, Fundo imobiliario, Previdência privada e ETF de ações) para que a assistente virtual possa ter mais exemplos de investimentos.
- Acrescentei historicos de atendimento para que houbesse sempre uma conversa entre o cliente e o assistente, sobre seus planejamentos e metas.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (ctrl + c, ctrl + v) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import pandas as pd
import json

#------------------------------
Carregamento dos arquivos CSV
#------------------------------


historico = pd.read_csv('data/historico_atendimento.csv')

transacoes = pd.read_csv('data/transacoes.csv')


#-------------------------------
Carregamento dos arquivos Json
#-------------------------------

with open('data/perfil_cliente.json', 'r', encoding='utf-8') as f:
perfil = json.load(f)

with open('data/tipos_investimento.json', 'r', encoding='utf-8') as f:
investimentos = json.load(f)


```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos colocar os nossos dados diretamente no prompt, o que garante que o Agente tenha o melhor contexto das informações possivel. Mas o ideal é que essas informações sejam carregadas de forma dinâmica para que possamos ter flexibilidade.

```text

PERFIL DO CLIENTE: (data/perfil_cliente.json)

{
  "nome": "Alexsandro Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 12000.00,
  "renda_extra": 2000.00,
  "estado_civil": "Casado",
  "filhos": 2,
  "cidade": "Recife",
  "perfil_investidor": "Conservador",
  "objetivo_principal": "Concluir a meta de reserva de emergência e dar entrada na casa",
  "objetivo_secundario": "Viajar para Londres",
  "patrimonio_total": 9000.00,
  "reserva_emergencia_atual": 8000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 17000.00,
      "prazo": "2027-07"
    },
    {
      "meta": "Entrada da casa",
      "valor_necessario": 80000.00,
      "prazo": "2028-04"
    },
    {
      "meta": "Viajar para Londres",
      "valor_necessario": 45000.00,
      "prazo": "2027-12"
    }

  ]
}

HISTORICO DE ATENDIMENTO: (data/historico_atendimento.csv)

data,canal,tema,resumo,resolvido
2025-09-10,chat,reserva de emergência,Cliente foi ver quanto estava na sua reserva de emergência,sim
2025-09-11,chat,investimentos,Cliente perguntou quais investimentos ele poderia adquirir,sim
2025-09-11,email,investimentos,Cliente enviou e-mail solicitando orientação sobre opções de investimento de perfil conservador,sim
2025-10-03,chat,reserva de emergência,Cliente verificou saldo atual da reserva e perguntou se já cobre 6 meses de despesas enquanto planeja entrada na cas,sim
2025-10-04,email,investimentos,Cliente pediu simulação de investimentos conservadores para acumular valor para entrada da casa em 2 anos,sim
2025-10-05,telefone,reserva de emergência,Cliente ligou para confirmar rendimento mensal da reserva e avaliar possibilidade de aportar mais recursos,sim
2025-10-06,chat,investimentos,Cliente perguntou quais aplicações de baixo risco são indicadas para objetivo de compra de imóvel,sim
2025-10-07,email,planejamento financeiro,Cliente solicitou plano para dividir aportes entre reserva de emergência e fundo para entrada na casa,sim
2025-10-08,telefone,investimentos,Cliente quis entender diferença entre CDB e Tesouro para objetivo de médio prazo,sim
2025-10-09,chat,reserva de emergência,Cliente perguntou se pode manter reserva no mesmo investimento enquanto guarda dinheiro para imóvel,sim
2025-10-10,email,investimentos,Cliente solicitou simulação de aportes mensais visando acumular 80 mil reais para entrada,sim
2025-10-11,telefone,planejamento financeiro,Cliente pediu ajuda para organizar metas financeiras para compra da casa,sim
2025-10-12,chat,investimentos,Cliente questionou rentabilidade média de renda fixa para prazo de 24 meses,sim
2025-10-13,email,reserva de emergência,Cliente pediu extrato detalhado da reserva e projeção de rendimento anual,sim
2025-10-14,telefone,investimentos,Cliente buscou orientação sobre LCI isenta de IR para objetivo imobiliário,sim
2025-10-15,chat,planejamento financeiro,Cliente quer saber quanto precisa poupar por mês para dar entrada em 3 anos,sim
2025-10-16,email,investimentos,Cliente perguntou sobre fundos conservadores com liquidez para compra de imóvel,sim
2025-10-17,telefone,reserva de emergência,Cliente confirmou se reserva está aplicada em produto com liquidez imediata,sim
2025-10-18,chat,investimentos,Cliente solicitou sugestão de carteira conservadora para acumular entrada da casa,sim
2025-10-19,email,planejamento financeiro,Cliente pediu simulação considerando aumento salarial recente,sim
2025-10-20,telefone,investimentos,Cliente avaliou migração de poupança para CDB visando maior rentabilidade para entrada,sim
2025-10-21,chat,reserva de emergência,Cliente perguntou se reserva atual precisa ser ajustada após aumento de despesas,sim
2025-10-22,email,investimentos,Cliente pediu comparação entre Tesouro Selic e CDB liquidez diária,sim
2025-10-23,telefone,planejamento financeiro,Cliente solicitou plano financeiro combinando reserva e objetivo imobiliário,sim
2025-10-24,chat,investimentos,Cliente perguntou prazo ideal de aplicação para entrada em 30 meses,sim
2025-10-25,email,reserva de emergência,Cliente quis confirmar valor ideal de reserva antes de investir para imóvel,sim
2025-10-26,telefone,investimentos,Cliente buscou opções com garantia do FGC para acumular entrada,sim
2025-10-27,chat,planejamento financeiro,Cliente solicitou ajuda para organizar orçamento visando compra da casa,sim
2025-10-28,email,investimentos,Cliente pediu simulação com aporte inicial de 20 mil reais,sim
2025-10-29,telefone,reserva de emergência,Cliente confirmou se rendimento da reserva está acima da poupança,sim
2025-10-30,chat,investimentos,Cliente perguntou se vale investir parte da reserva no objetivo imobiliário,sim
2025-10-31,email,planejamento financeiro,Cliente solicitou acompanhamento mensal do progresso da meta,sim
2025-11-01,telefone,investimentos,Cliente quis saber risco de investir em renda fixa prefixada para 2 anos,sim
2025-11-02,chat,reserva de emergência,Cliente verificou saldo atualizado e rendimento acumulado,sim
2025-11-03,email,investimentos,Cliente pediu orientação sobre diversificação conservadora para entrada de imóvel,sim
2025-11-04,telefone,planejamento financeiro,Cliente pediu cálculo de meta para entrada de 100 mil reais,sim
2025-11-05,chat,investimentos,Cliente perguntou sobre liquidez de aplicações para saque no momento da compra,sim
2025-11-06,email,reserva de emergência,Cliente confirmou se valor atual cobre 8 meses de despesas,sim
2025-11-07,telefone,investimentos,Cliente solicitou carteira recomendada para prazo de 36 meses,sim
2025-11-08,chat,planejamento financeiro,Cliente pediu ajuda para ajustar aportes após aumento de aluguel,sim
2025-11-09,email,investimentos,Cliente perguntou sobre rendimento líquido considerando imposto de renda,sim
2025-11-10,telefone,reserva de emergência,Cliente verificou possibilidade de reforçar reserva antes de investir,sim
2025-11-11,chat,investimentos,Cliente quis saber qual produto tem melhor relação risco-retorno para 2 anos,sim
2025-11-12,email,planejamento financeiro,Cliente pediu simulação considerando financiamento em 2028,sim
2025-11-13,telefone,investimentos,Cliente avaliou Tesouro IPCA para proteger valor da entrada,sim
2025-11-14,chat,reserva de emergência,Cliente perguntou se pode manter reserva e meta no mesmo banco,sim
2025-11-15,email,investimentos,Cliente solicitou detalhamento de taxas de administração,sim
2025-11-16,telefone,planejamento financeiro,Cliente pediu orientação para manter disciplina de aportes mensais,sim
2025-11-17,chat,investimentos,Cliente solicitou simulação com aportes crescentes anuais,sim
2025-11-18,email,reserva de emergência,Cliente confirmou liquidez imediata em caso de imprevistos,sim
2025-11-19,telefone,investimentos,Cliente pediu comparação entre renda fixa e multimercado conservador,sim
2025-11-20,chat,planejamento financeiro,Cliente pediu resumo geral do plano para entrada na casa,sim
2025-11-21,email,investimentos,Cliente solicitou recomendação final para iniciar aportes mensais automáticos,sim

TIPOS DE INVESTIMENTO: (data/tipos_investimentos.json)

[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  },
  {
    "nome": "Tesouro IPCA+",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "IPCA + taxa prefixada",
    "aporte_minimo": 30.00,
    "indicado_para": "Proteção contra inflação e objetivos de médio/longo prazo"
  },
  {
    "nome": "Previdência Privada (PGBL/VGBL)",
    "categoria": "previdência",
    "risco": "variável",
    "rentabilidade": "Conforme a carteira escolhida",
    "aporte_minimo": 100.00,
    "indicado_para": "Objetivos de longo prazo e benefícios fiscais"
  },
 {
    "nome": "Criptomoedas (Bitcoin)",
    "categoria": "criptoativos",
    "risco": "muito alto",
    "rentabilidade": "Variável e especulativa",
    "aporte_minimo": 50.00,
    "indicado_para": "Perfil muito arrojado"
  },
  {
    "nome": "Poupança",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "TR + juros (enquanto regra vigente)",
    "aporte_minimo": 1.00,
    "indicado_para": "Reserva de emergência básica"
  },
  {
    "nome": "Fundo Imobiliário (FII)",
    "categoria": "fundos imobiliários",
    "risco": "médio",
    "rentabilidade": "Aluguel + valorização das cotas",
    "aporte_minimo": 100.00,
    "indicado_para": "Renda passiva com imóveis sem comprar imóvel físico"
  },
  {
    "nome": "ETF de Ações (Ex: BOVA11)",
    "categoria": "ações",
    "risco": "alto",
    "rentabilidade": "Variável (índice de mercado)",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem quer diversificação em ações com baixo custo"
  }

    
]

TRANSAÇÕES: (data/transacoes.csv)

data,descricao,categoria,valor,tipo
2025-09-01,Salario,Remuneração,12000.00,entrada
2025-09-03,Cartão,Divida,4000.00,saida
2025-09-05,Escola,Divida,1500.00,saida
2025-09-05,Aluguel,Residencia,1000.00,saida
2025-09-05,Conta de água,Residencia,350.00,saida
2025-09-05,Conta de Luz, Residencia,400.00,saida
2025-09-07,Feira,Comida,1200.00,saida
2025-09-09,Salario,Extra,2000.00,entrada
2025-09-10,Saude,Planos,650.90, saida
2025-09-11,Netlix,Planos,40.90,saida
2025-09-11,Spotify,Planos,42.90,saida
2025-09-11,Academia,Planos,120.00,saida
2025-09-20,Gasolina,Combustivel,200.00,saida
2025-09-25,Compras de roupas,Lazer,500.00,saida
2025-09-25,Antivirus,Planos, 150.00,saida
2025-09-26,Restaurante,Lazer,400.00,saida
2025-09-26,Farmacia,Planos,100.00,saida
2025-09-29,Praia,Lazer,250.00,saida




```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo abaixo é de um contexto da base de conhecimento, deixando apenas as informações importantes.

```
👤 Perfil Consolidado do Cliente
Nome: Alexsandro Silva (32 anos, Analista de Sistemas).

Localização: Recife/PE.

Perfil de Risco: Estritamente Conservador (Não aceita risco).

Saúde Financeira: Renda mensal de R$ 14.000,00 (Salário + Extra).

Patrimônio Atual: R$ 9.000,00 (sendo R$ 8.000,00 já em Reserva de Emergência).

📈 Diagnóstico de Gastos (Baseado em Transações de Setembro)
O agente processa a lista de gastos e identifica o seguinte fluxo:

Total de Entradas: R$ 14.000,00.

Total de Saídas: R$ 11.205,60.

Capacidade de Poupança: R$ 2.794,40/mês.

Maiores Ralos de Dinheiro: Cartão de Crédito (R$ 4.000) e Escola (R$ 1.500).

Lazer/Estilo de Vida: Consumo moderado (~R$ 1.150,00 entre restaurantes, praia e roupas).

🎯 Metas e Prazos
O agente prioriza os objetivos conforme a urgência:

Reserva de Emergência: Faltam R$ 9.000,00 para atingir o alvo de R$ 17.000,00 (Prazo: Julho/2027).

Entrada da Casa: Alvo de R$ 80.000,00 (Prazo: Abril/2028).

Viagem Londres: Alvo de R$ 45.000,00 (Prazo: Dezembro/2027).

🛠️ Filtro de Produtos Compatíveis
O agente cruza o perfil "Conservador" com o catálogo e seleciona apenas:

Tesouro Selic: Para a Reserva (Liquidez imediata).

CDB 102% CDI: Para a meta de curto prazo.

LCI/LCA: Para a entrada da casa (Isenção de IR para prazos acima de 90 dias).

Produtos descartados: Cripto, Ações e Multimercado (devido ao risco).

💬 Resumo do Histórico de Atendimento
O cliente é altamente engajado e preocupado. Realizou mais de 50 interações em 3 meses, focando sempre em:

Confirmação de rendimentos da reserva.

Simulações para a entrada da casa.

Diferença entre taxas (CDB vs Tesouro).

Status Atual: Resolvido, mas aguardando plano consolidado de aportes automáticos.
```
