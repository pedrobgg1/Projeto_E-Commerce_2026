SELECT  
    COUNT(CASE WHEN order_purchase_timestamp LIKE '2016%' THEN 1 END) AS Qnt2016,
    COUNT(CASE WHEN order_purchase_timestamp LIKE '2017%' THEN 1 END) AS Qnt2017,
    COUNT(CASE WHEN order_purchase_timestamp LIKE '2018%' THEN 1 END) AS Qnt2018
FROM OdersDataset;
