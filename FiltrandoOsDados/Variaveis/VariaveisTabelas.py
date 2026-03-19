#%%
import pandas as pd

#%%

df1 = pd.read_csv("../data/olist_customers_dataset.csv", sep=",")
clientesCol = list(df1.columns)
clientes = ", ".join(clientesCol)
clientes
#%%

df2 = pd.read_csv("../data/olist_geolocation_dataset.csv", sep=",")
GeoCol = list(df2.columns)
Geo = ", ".join(GeoCol)
Geo

#%%

df3 = pd.read_csv("../../data\olist_order_items_dataset.csv", sep=",")
OrderItensCol = list(df3.columns)
OrderItens = ", ".join(OrderItensCol)
OrderItens

#%%

df4 = pd.read_csv("../data\olist_order_payments_dataset.csv", sep=",")
OrderPaymenyCol = list(df4.columns)
OrderPayment = ", ".join(OrderPaymenyCol)
OrderPayment

#%%

df5 = pd.read_csv("../data\olist_order_reviews_dataset.csv", sep=",")
OrderReviewsCol = list(df5.columns)
OrderReviews = ", ".join(OrderReviewsCol)
OrderReviews

#%%

df6 = pd.read_csv("../data\olist_orders_dataset.csv", sep=",")
OrderDSCol = list(df6.columns)
OrderDS = ", ".join(OrderDSCol)
OrderDS

#%%

df7 = pd.read_csv("../data\olist_products_dataset.csv", sep=",")
ProductsCol = list(df7.columns)
ProductsDS = ", ".join(ProductsCol)
ProductsDS

#%%

df9 = pd.read_csv("../data\product_category_name_translation.csv", sep=",")
ProductCategoryCol = list(df9.columns)
ProductCategory = ", ".join(ProductCategoryCol)
ProductCategory



#%%

df3.shape