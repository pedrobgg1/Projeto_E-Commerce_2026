#%%
import pandas as pd

df = pd.read_csv("../DadosFiltrados/TBVendas_master.csv", sep=";")


df = (df["categoria_principal"].value_counts().reset_index())

with pd.option_context('display.max_rows', None):
    print(df.sort_values(by=["count"], ascending=True))