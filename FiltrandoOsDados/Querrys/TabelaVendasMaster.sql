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