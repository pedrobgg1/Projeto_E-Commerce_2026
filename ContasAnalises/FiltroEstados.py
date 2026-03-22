
#%%
import pandas as pd

df = pd.read_csv("../Tabela_Final\Tabela_Analises_Final.csv", sep=";")

df = df.groupby(by=["customer_state"], as_index=False)[["mesmo_estado"]].sum()

filtro = df["mesmo_estado"] == 0

df_final = df[filtro][["customer_state"]]
df.reset_index(drop=True)