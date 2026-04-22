WITH seller_revenue AS (
    SELECT
        s.seller_id,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN sellers s ON oi.seller_id = s.seller_id
    GROUP BY s.seller_id
),
ranked AS (
    SELECT
        seller_id,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) /
        SUM(revenue) OVER () AS cumulative_share
    FROM seller_revenue
)
SELECT
    seller_id,
    revenue,
    CASE
        WHEN cumulative_share <= 0.80 THEN 'A'
        WHEN cumulative_share <= 0.95 THEN 'B'
        ELSE 'C'
    END AS abc_class
FROM ranked;