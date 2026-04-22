SELECT
    s.seller_id,
    s.seller_state,
    COUNT(o.order_id) AS total_orders,
    SUM(oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE ($1 IS NULL OR o.order_purchase_timestamp >= $1)
  AND ($2 IS NULL OR o.order_purchase_timestamp <= $2)
  AND ($3 IS NULL OR s.seller_state = $3)
GROUP BY s.seller_id, s.seller_state
ORDER BY revenue DESC;