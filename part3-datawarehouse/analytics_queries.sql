-- Analytics Queries on FlexiMart Data Warehouse

-- 1) Total revenue by month (2024)
SELECT
  d.year,
  d.month,
  d.month_name,
  SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 2) Top categories by revenue
SELECT
  p.category,
  SUM(f.sales_amount) AS category_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 3) Top 5 customers by revenue
SELECT
  c.full_name,
  c.city,
  SUM(f.sales_amount) AS total_spent
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.full_name, c.city
ORDER BY total_spent DESC
LIMIT 5;

-- 4) Revenue by order status
SELECT
  s.status,
  SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
JOIN dim_order_status s ON f.order_status_key = s.order_status_key
GROUP BY s.status
ORDER BY total_revenue DESC;
