#%%

import pandas as pd

df = pd.read_csv("../data\olist_order_items_dataset.csv", sep=",")


max(df["price"])

#%%

df_vendasmaster = pd.read_csv("../DadosFiltrados\TBVendas_master.csv", sep=";")
max(df_vendasmaster["total_price"])

#%%

df_final = pd.read_csv("../Tabela_Final\Tabela_Analises_Final.csv", sep=";")

max(df_final["total_price"])