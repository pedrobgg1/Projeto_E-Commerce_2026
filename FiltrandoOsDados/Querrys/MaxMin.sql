SELECT 
    MIN(order_purchase_timestamp) AS DataMaisAntiga,
    MAX(order_purchase_timestamp) AS DataMaisRecente
FROM OdersDataset;