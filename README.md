# **Análise e Relatório de Vendas  - E-Commerce Olist**

O objetivo deste projeto é analisar e descobrir gargalos nas vendas de E-Commerce da empresa Olist. Utilizando ferramentas que possibilitem filtrar, transformar e apresentar os dados encontrados, facilitando assim a análise final.

*Primariamente este projeto foi criado como forma de demonstrar e praticar minhas habilidades com ferramentas de análise de dados e suas interações, não possuindo vinculo trabalhista com a empresa citada*

**Link para o dashboard:** [Acesse o Dashboard em PowerBI](https://app.powerbi.com/view?r=eyJrIjoiOTg5MjY4ODAtYjg5Zi00M2YzLTgwMzgtMTRjYzQxNmI4MjdlIiwidCI6Ijg4MWUzOTM1LTE5MzktNGVmOC05MWEzLTkwNjcxYTFmNWU2ZSJ9)

## Realização do Projeto

### Escolha da base de dados

O primeiro passo foi a escolha de uma base de dados. Selecionei a base do E-Commerce Olist pela robustez dos dados e pela grande possibilidade de análises e transformações que ela oferece.

Além disso, a aplicação prática da análise de dados em um E-Commerce é muito relevante hoje em dia, sendo uma tarefa fundamental dentro desse ramo para entender o negócio, possuindo assim, uma aplicação prática consideravel.

**Link para a Base:** [Acesse a base via Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)


### Manipulação e Preparação dos Dados (SQL)

O primeiro desafio foi a disponibilidade dos dados, que não estavam em formato .db, mas sim divididos em 9 tabelas .csv separadas.

Para facilitar o trabalho com o SQL, decidi realizar essa transformação. Utilizando o terminal integrado do VS Code, criei o banco de dados OLDataBase.db e importei cada tabela individualmente, o que possibilitou um uso muito mais dinâmico para realizar as consultas no SQL.

**Exemplo:**

    sqlite3 OLData_Base.db

    .mode csv

    .import olist_customers_dataset.csv clientes

#### **Core**

O foco das consultas em SQL foi diminuir a quantidade de informações desnecessárias e unir as principais bases de dados. Com isso, formei tabelas reduzidas que seriam utilizadas posteriormente na transformação dos dados dentro do Python.

Para ter um controle total dos JOINS, utilizei o Python para mapear todas as variáveis de cada tabela em um único arquivo de texto *(Variaveis_E_Tabelas.txt)*. Isso me permitiu identificar as chaves primárias e estrangeiras necessárias para os cruzamentos de dados.

Com isso foi criado **4** tabelas

Para a exportação final, utilizei a biblioteca SQLAlchemy, que permitiu rodar as queries diretamente no Python. Essa foi a estratégia mais eficiente que encontrei para gerar os arquivos sem sobrecarregar o processamento da máquina.

No total, foram estruturadas **4** tabelas principais:

* *TBClientes.csv:* Dados dos compradores.

* *TBReviews.csv:* Notas e comentários de satisfação.

* *TBVendedores.csv:* Informações sobre os lojistas.

* *TBVendas_master.csv:* Base consolidada de vendas.


#### **Tratamento da Tabela de Vendas**

Um desafio que surgiu durante a preparação dos dados, foi a duplicidade contida na tabela de vendas original. Algumas váriaveis como "*quantidade de itens*" e "*forma de pagamento*", criavam linhas duplicadas para o mesmo ID do pedido, o que se tornava uma barreira para a realização dos JOINS.

A solução encontrada foi realizar um agrupamento (GROUP BY) pelo ID do pedido, porém por conta disso foi preciso tomar algumas decissões. 

* **Categoria Principal:** Defini que o pedido teria a categoria do primeiro item vendido.

* **Somas do Pedido:** Realizei a soma do preço de venda, do frete e da quantidade de itens por pedido.

* **Vendedor Principal:** Seguindo a mesma logica da categori, encontrei o vendedor principal do pedido

Além disso, os dados foram filtrados para considerar apenas pedidos com o status "delivered" (entregue). 

Com esse tratamento, a tabela passou de **112.650** para **96.478** observações, eliminando **16.172** linhas duplicadas ou irrelevantes para a análise de satisfação.

**Query da tabela TBVendas_master.csv:**

    SELECT
        t1.order_id,
        t1.customer_id,
        t2.seller_id,
        t2.total_price,
        t2.total_freight_value,
        t2.qtd_itens,
        t3.product_category_name as categoria_principal, 
        t1.order_purchase_timestamp,
        t1.order_delivered_customer_date,
        t1.order_delivered_carrier_date,
        t1.order_estimated_delivery_date
    FROM OdersDataset as t1

    LEFT JOIN (
        SELECT 
            order_id, 
            SUM(CAST(price AS DOUBLE)) as total_price,
            SUM(CAST(freight_value AS DOUBLE)) as total_freight_value,
            COUNT(order_item_id) as qtd_itens,
            MAX(CASE WHEN order_item_id = 1 THEN product_id END) as main_product_id,
            MAX(CASE WHEN order_item_id = 1 THEN seller_id END) as seller_id
        FROM OrdemItems
        GROUP BY order_id
    ) as t2 
    ON t1.order_id = t2.order_id


    LEFT JOIN ProductsDS as t3 
    ON t2.main_product_id = t3.product_id

    WHERE t1.order_status = 'delivered'


## Transformação dos Dados (Python & Pandas)

O uso do Python neste projeto foi focado na criação e transformação de variáveis estratégicas para melhorar a análise e a visualização dos dados no PowerBI.

Antes de iniciar os scripts, planejei quais seriam as principais transformações necessárias para responder às perguntas de negócio:

* **Mesmo estado:** Criação de uma váriavel booleana (0 ou 1) que indica se o vendedor e o consumidor residem no mesmo estado.

* **Performance de Entrega:** Cálculo da diferença entre a data de entrega com a data de previsão, categorizando entre "*Adiantado*", "*NoDia*" ou "*Atrasado*".

* **Filtrar Estados por Frete:** Identificação dos estados que contem apenas frete interestadual (utilizado diretamente com integração do PowerBI).

* **Medía do Review Score por Pedido:** Agrupamento das avaliações para obter a nota média por pedido.


**Exemplo da Criação da Coluna "MesmoEstado"**

    import pandas as pd

    # Importar base de dados
    df_vendas = pd.read_csv("../DadosFiltrados/TBVendas_master.csv", sep=";")
    df_clientes = pd.read_csv("../DadosFiltrados/TBClientes.csv", sep=";")
    df_sellers = pd.read_csv("../DadosFiltrados/TBVendedores.csv", sep=";")

    # Juntar tabelas necessarias
    df_vendasMcliente = (df_vendas.merge
            (right=df_clientes,
            how='left',
            on=['customer_id'],
            suffixes=["Vendas","Cliente"],

            )
    )
    df_estados = (df_vendasMcliente.merge
            (right=df_sellers,
            how='left',
            on=["seller_id"],
            suffixes=["Vendas","Vendedores"]
            )
    )

    # Criar coluna MesmoEstado
    df_estados["mesmo_estado"] = (df_estados["customer_state"] == df_estados["seller_state"]).astype(int)


Com a realização de cada transformação individual, o ultimo passo foi consolidar todas as novas váriaveis em uma tabela única ("*Tabela_Analises_Final.csv*"), que serviu como fonte para realização do dashboard.

## Criação do Dashboard (PowerBI)

Para a construção do dashboard, desenvolvi métricas essenciais para o negócio, como o "*Período de Análise*" e o "*Peso do Frete no Preço Final*".

Além disso, conforme a criação e teste dos modelos ia tomando forma, identifiquei a necessidade de variáveis mais profundas para a análise logística. Um exemplo foi a implementação da variável "*Mesmo Estado*", que realizei através da integração de scripts Python diretamente no Power BI.

Essa métrica foi fundamental para cruzar os dados de logística com os custos de frete, permitindo identificar os gargalos logísticos de possuir muitos vendedores concentrados em poucos locais.


### **Estrutura da Análise**

Para garantir uma visão geral da operação, dividi o dashboard em três pilares de análise:

* **Dados Gerais:** Visão macro do faturamento, volume de pedidos e performance de vendas por categoria, entre outras métricas de saúde do negócio.

<p align="center">
  <img src="img\dashboard_geral1.png" width="600px" alt="Print do Dashboard">
</p>

* **Logística & Frete:** Análise sobre prazos de entrega e a diferença de performance entre o frete interestadual e estadual.

<p align="center">
  <img src="img\dashboard_logistica.png" width="600px" alt="Print do Dashboard">
</p>

* **Satisfação dos Compradores:** Estudo do comportamento do consumidor e do "*Review Score*", correlacionando a satisfação com o cumprimento do prazo de entrega e as categorias de produtos.

<p align="center">
  <img src="img\dashboard_satisfacao.png" width="600px" alt="Print do Dashboard">
</p>



## **Análises**

### **Dados Gerais e Contexto Macroeconômico**

Para entender os números deste projeto, é preciso compreender o período analisado (set/2016 a ago/2018), o qual reflete um momento delicado da economia brasileira. De acordo com a Trading Economics, o ano de **2016** registrou um dos menores PIBs per capita (PPC) da história recente, superado apenas pela crise de **2020**. O poder de compra só retornaria aos níveis de **2014** quase uma década depois, em **2023**.

Esse cenário de restrição orçamentária impacta diretamente os indicadores do dashboard:

* **Ticket Médio e Consumo:** O preço médio de venda de **R$ 137,00** e a média de **1,14** itens por pedido reforçam o comportamento de um consumidor cauteloso, que realiza compras focadas e raramente adiciona múltiplos produtos ao carrinho em uma mesma transação.

* **Marketplace:** A proporção de **1** vendedor para cada **32,59** clientes indica uma base de lojistas robusta, mas que exige uma logística extremamente eficiente para atender à demanda.

* **Concentração Geográfica:** Identifiquei uma forte disparidade regional, também causada pela recessão econômica. O Sudeste domina a base com **40,5 mil** clientes em SP, seguido por RJ (12,3k) e MG (11,3k). Somando-se com os **3**  da região Sul que vem logo em seguida, fica evidente que o faturamento da operação está concentrado em regiões onde há maior poder de compra.


Ao analisarmos o ranking de categorias (imagem abaixo), notamos um padrão de consumo resiliente à crise:

* **Cama, Mesa e Banho (9,17 mil itens):** Lidera o volume, indicando que o consumidor priorizou a manutenção e renovação do lar, possivelmente por serem bens de necessidade básica e com grande variedade de preços.

* **Beleza e Saúde (8,61 mil itens):** Ocupa o segundo lugar, confirmando a tese de que o setor de cuidados pessoais é menos elástico à renda (o consumidor mantém esses gastos mesmo em períodos de baixa).

* **Esporte e Lazer (7,49 mil itens):** Surpreende em terceiro lugar, mostrando um nicho de mercado forte focado em estilo de vida e hobbies

<p align="center">
<img src="img\grafico_categoria1.png" width="300px" alt="Quantidade de Itens por Categoria">
</p>


### **Logística e Eficiência de Entrega**

A análise logística revela uma operação com alto nível de confiabilidade no cumprimento de prazos, mas que enfrenta gargalos estruturais em termos de custos regionais.

**Performance de Entrega (SLA)**

A operação apresenta um índice de assertividade altíssimo: **93,2%** das encomendas chegam dentro ou antes do prazo estipulado (90,35% adiantadas e 2,85% no dia previsto), com uma mediana de frete de **10,22** dias, mantendo uma baixa taxa de atrasos.

**A Barreira do Frete Interestadual**

Apesar da forte concentração de compradores e vendedores em São Paulo, **64,03%** dos pedidos são interestaduais. Essa dinâmica gera um impacto direto no bolso do consumidor pelos seguintes fatores:

* **Custo interestadual:** Compras interestaduais custam, em média, **R$ 11,45** a mais em frete do que compras locais.

* **Decisão de Compra:** Em produtos de baixo preço médio, esse valor pode representar uma barreira, onde o frete acaba se tornando uma porcentagem considerável do preço final.

**Disparidades Regionais**

Ao analisarmos o peso do frete sobre o preço total por estado, a desigualdade logística fica evidente:

* **Norte/Nordeste:** Estados como Roraima (28,08%), Maranhão (26,32%), Rondônia (24,70%) e Amazonas (24,51%) possuem os maiores pesos de frete do país. Nesses locais, o custo logístico consome quase 1/3 do valor da transação.

* **O Efeito Proximidade:** O Mato Grosso do Sul (MS) surge como uma exceção positiva fora do eixo Sul-Sudeste; devido à sua facilidade logística com São Paulo, consegue manter custos mais competitivos que seus vizinhos.

* **Oportunidade de Mercado:** O fato de o primeiro estado fora do Norte/Nordeste aparecer apenas na **16ª** posição do ranking de peso de frete sinaliza uma oportunidade clara de expansão. Com uma estratégia voltada para preços mais competitivos, é possível conquistar e fidelizar esse mercado.

### **Satisfação do Cliente**

A análise de satisfação revela que a experiência do cliente no E-Commerce Olist é impulsionada pela qualidade dos produtos e, principalmente, pela gestão das expectativas de entrega.

**Engajamento Orgânico**

Um ponto de destaque é o volume de avaliações, que é quase equivalente ao volume de pedidos. Diferente de outros e-commerces que utilizam sistemas de recompensas ou descontos para incentivar os compradores a realizar avaliações, a base da Olist apresenta um engajamento orgânico altíssimo. Isso indica que o consumidor sente uma necessidade natural de reportar sua experiência, o que torna os dados de Review Score extremamente confiáveis.

**Distribuição de Notas e Qualidade**

A média geral de **4,16** é um indicador sólido de que a operação atende as expectativas.

* **Nota Máxima:** **60,48%** (aprox. 57 mil pedidos) receberam nota **5**, seguidos por **19 mil** pedidos com nota **4**. Indicando que a maioria dos produtos atenderam as expectativas.

* **Nota Miníma:** Apenas cerca de **9 mil** pedidos receberam nota **1**, representando uma parcela pequena diante do volume total de **95.832** pedidos.

**impacto da Logística na Satisfação**

Os dados confirmam que a logística é o principal fator de variação na nota.

Pedidos que chegam adiantados possuem uma nota média **0,20** superior aos que chegam no dia previsto. Isso valida a estratégia de manter prazos estimados maiores para gerar uma surpresa positiva no cliente.

Em contrapartida, pedidos atrasados têm uma média crítica de **2,27**. Isso sugere que a maioria das notas baixas está atrelada à falha no prazo de entrega, e não necessariamente a defeitos no produto.

**Análise de Categorias**

A grande maioria das **73** categorias mantém médias de avaliação superiores a **4**, sendo que apenas **12** delas ficaram abaixo. isso indica que a percepção de qualidade não está restrita a nichos específicos, o que descarta a hipótese de que determinadas categorias ou grupos de vendedores estariam impactando negativamente a performance geral da plataforma por problemas crônicos de produto.

No entanto, identifiquei anomalias causadas pela baixa amostragem em algumas categorias:

* **Viés Negativo:** A categoria Seguros e Serviços apresenta a menor nota média da base de dados (2,5), porém ela é baseada em apenas **2** pedidos. Por isso não possui significância de se avaliar esta categoria.

* **Viés Positivo:** O mesmo ocorre em Fashion Roupa Infanto-Juvenil, com nota **5** baseada em apenas **7** pedidos.


## **Conclusão e Próximos Passos**

Este projeto foi uma oportunidade de aplicar e unir meus conhecimentos em Economia e Análise de Dados em um cenário real de e-commerce, utilizando um pipeline de dados completo.

Ao longo do processo, foquei na utilização prática das seguintes ferramentas:

* **SQL:** Para a extração, limpeza e estruturação inicial dos dados brutos.

* **Python/Pandas:** Para o tratamento e a criação de novas métricas.

* **Power BI:** Para a construção de um dashboard intuitivo, focado em facilitar a tomada de decisão.

A integração dessas ferramentas possibilitou uma análise final sólida, conectando a teoria econômica (como o impacto do poder de compra e custos logísticos) com os desafios práticos de um marketplace.

**Próximos Passos:**

Com o objetivo de evoluir este estudo e a mim mesmo, pretendo explorar o uso de Machine Learning para criar modelos que possibilitem prever o comportamento de entrega e aprofundar a análise de Elasticidade de Preço em relação ao frete, buscando soluções para os gargalos identificados neste projeto.

