#%%

# Passo 1: Importar base de dados

import pandas as pd

df_vendas = pd.read_csv("../DadosFiltrados/TBVendas_master.csv", sep=";")

df_clientes = pd.read_csv("../DadosFiltrados/TBClientes.csv", sep=";")

df_sellers = pd.read_csv("../DadosFiltrados/TBVendedores.csv", sep=";")

df_reviews = pd.read_csv("../DadosFiltrados\TBReviews.csv", sep=";")

# %%

# Passo 2: Juntar tabelas necessarias

# Group By em reviews

df_reviews = (df_reviews
                .groupby(by=["order_id"], 
                as_index=False)
                [["review_score"]].mean()
)

# Merge Clientes

df_vendas = (df_vendas.merge
        (right=df_clientes,
         how='left',
         on=['customer_id'],
         suffixes=["Vendas","Cliente"],

         )
)

# Merge Sellers

df_vendas = (df_vendas.merge
        (right=df_sellers,
        how='left',
        on=["seller_id"],
        suffixes=["Vendas","Vendedores"]
        )
)


# Merge reviews

df_vendas = df_vendas.merge(right=df_reviews,
                how="left",
                on="order_id",
                suffixes=["Vendas","Reviews"]
)


#%%

# Passo 3: Criar variaveis de analise

# Mesmos Estados

df_vendas["mesmo_estado"] = (df_vendas["customer_state"] == df_vendas["seller_state"]).astype(int)

#%%

# Analises de datas

# Transaformar em data/hora 

df_vendas["order_purchase_timestamp"] = pd.to_datetime(df_vendas["order_purchase_timestamp"])

df_vendas["order_delivered_customer_date"] = pd.to_datetime(df_vendas["order_delivered_customer_date"])

df_vendas["order_estimated_delivery_date"] = pd.to_datetime(df_vendas["order_estimated_delivery_date"])

df_vendas["order_delivered_carrier_date"] = pd.to_datetime(df_vendas["order_delivered_carrier_date"])


# Descobrir o gap entre pedido e entrega

df_vendas["gap_pedido_entrega_em_dias"]  = ((df_vendas["order_purchase_timestamp"] - 
                                          df_vendas["order_delivered_customer_date"])
                                          /pd.Timedelta(days=1)
                                          )*-1

# Descobrir o gap entre Entrega e previsao

df_vendas["gap_entrega_previsao_em_dias"] = ((df_vendas["order_delivered_customer_date"].dt.normalize() - 
                                           df_vendas["order_estimated_delivery_date"].dt.normalize())
                                           /pd.Timedelta(days=1)
                                           )*-1

# Encontrar os imites de atraso

minimo_atraso = min(df_vendas["gap_entrega_previsao_em_dias"])
maximo_atraso = max(df_vendas["gap_entrega_previsao_em_dias"])

# Criar coluna acerto_previsao e descobrir se o pedido:
# foi atrasado 
# chegou no dia 
# foi adiantado

df_vendas["acerto_previsao"] = (pd.cut(
                                    df_vendas["gap_entrega_previsao_em_dias"],
                                    bins=[minimo_atraso, -1, 1, maximo_atraso],
                                    labels=["Atrasado", "No dia", "Adiantado"]
                                        )
                                )

df_vendas.head()


# %%


# Tranformar em uma unica tabela CSV

df_vendas.to_csv("Tabela_Analises_Final.csv",sep=";",index=False)

# %%
