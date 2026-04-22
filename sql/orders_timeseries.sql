SELECT
    DATE(o.order_purchase_timestamp) AS order_date,
    SUM(oi.price) AS daily_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE(o.order_purchase_timestamp)
ORDER BY order_date;