#%%
import pandas as pd


shape1 = pd.read_csv("../data/olist_order_items_dataset.csv", sep=",")

shape1.shape[0]

#%%

shape2 = pd.read_csv("../DadosFiltrados/TBVendas_master.csv", sep=";")
shape2.shape[0]

#%%

shape1.shape[0] - shape2.shape[0]