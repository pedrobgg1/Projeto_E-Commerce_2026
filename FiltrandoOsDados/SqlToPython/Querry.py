#%%
import pandas as pd
import sqlalchemy as sql
#%% 
engine = sql.create_engine("sqlite:///../../OLDataBase.db")


#%%

query1 = """
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

"""

#%%

df_vendas = pd.read_sql_query(query1, con=engine)
df_vendas

#%%

df_vendas.to_csv("TBVendas_master.csv", index=False, sep=";")


#%%


query2 = """
SELECT customer_id,
        customer_unique_id,
        customer_state

FROM clientes

"""


df_clientes = pd.read_sql_query(query2, con=engine)

df_clientes.to_csv("TBClientes.csv", index=False, sep=";")

df_clientes


#%%


query3 = """

SELECT  seller_id, 
        seller_state

FROM SellersDS

"""


df_vendedores = pd.read_sql_query(query3, con=engine)

df_vendedores.to_csv("TBVendedores.csv", index=False, sep=";")

df_vendedores



#%%


query4 = """

SELECT order_id,
        review_id,
        review_score,
        review_creation_date

FROM OrderReviews

"""
df_reviews = pd.read_sql_query(query4, con=engine)

df_reviews.to_csv("TBReviews.csv", index=False, sep=";")

df_reviews

