#%%

# Importar base de dados

import pandas as pd

df_reviews = pd.read_csv("../DadosFiltrados\TBReviews.csv", sep=";")

df_vendas = pd.read_csv("../DadosFiltrados/TBVendas_master.csv", sep=";")

#%%

# Descobrir se há reviews repitidas 

print((df_reviews["order_id"].count()) - (df_reviews["order_id"].nunique()))

# resultado: 551

# agrupar por order_id com media da nota

df_reviews = (df_reviews
                .groupby(by=["order_id"], 
                as_index=False)
                [["review_score"]].mean()
)

#%%

# Fazer o Merge com a tabela de vendas

df_vendas = df_vendas.merge(right=df_reviews,
                how="left",
                on="order_id",
                suffixes=["Vendas","Reviews"]
)

df_vendas
