#%%

# Importar base de dados

import pandas as pd

df_vendas = pd.read_csv("../DadosFiltrados/TBVendas_master.csv", sep=";")

df_clientes = pd.read_csv("../DadosFiltrados/TBClientes.csv", sep=";")

df_sellers = pd.read_csv("../DadosFiltrados/TBVendedores.csv", sep=";")

#%%
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

# Conferir tipo das colunas

df_estados.dtypes

# Criar coluna MesmoEstado

df_estados["mesmo_estado"] = (df_estados["customer_state"] == df_estados["seller_state"]).astype(int)

df_estados


