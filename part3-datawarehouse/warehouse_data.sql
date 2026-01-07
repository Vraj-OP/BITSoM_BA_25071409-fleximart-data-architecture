-- Sample Warehouse Data Inserts

-- dim_date (few sample dates)
INSERT INTO dim_date (date_key, full_date, day_of_week, month, month_name, quarter, year, is_weekend) VALUES
(20240115, '2024-01-15', 'Monday', 1, 'January', 'Q1', 2024, FALSE),
(20240116, '2024-01-16', 'Tuesday', 1, 'January', 'Q1', 2024, FALSE),
(20240201, '2024-02-01', 'Thursday', 2, 'February', 'Q1', 2024, FALSE),
(20240305, '2024-03-05', 'Tuesday', 3, 'March', 'Q1', 2024, FALSE);

-- dim_customer (few sample customers)
INSERT INTO dim_customer (customer_id_nk, full_name, email, phone, city, registration_date) VALUES
(1, 'Rahul Sharma', 'rahul.sharma@gmail.com', '+919876543210', 'Bangalore', '2023-01-15'),
(2, 'Priya Patel', 'priya.patel@yahoo.com', '+919988776655', 'Mumbai', '2023-02-20'),
(3, 'Amit Kumar', 'missing.c003@fleximart.local', '+919765432109', 'Delhi', '2023-03-10');

-- dim_product (few sample products)
INSERT INTO dim_product (product_id_nk, product_name, category, price, stock_quantity) VALUES
(1, 'Samsung Galaxy S21', 'Electronics', 45999.00, 150),
(2, 'Nike Running Shoes', 'Fashion', 3499.00, 80),
(12, 'Dell Monitor 24inch', 'Electronics', 12999.00, 40);

-- dim_order_status
INSERT INTO dim_order_status (status) VALUES
('Completed'), ('Pending'), ('Cancelled');

-- fact_sales (sample rows: one per order item)
-- Lookup keys (assumes auto-increment keys start at 1 and inserts above were first)
-- customer_key: Rahul=1, Priya=2, Amit=3
-- product_key: S21=1, Nike Shoes=2, Dell Monitor=3
-- order_status_key: Completed=1, Pending=2, Cancelled=3

INSERT INTO fact_sales (
  date_key, customer_key, product_key, order_status_key,
  quantity_sold, unit_price, sales_amount, order_id_nk
) VALUES
(20240115, 1, 1, 1, 1, 45999.00, 45999.00, 1),
(20240116, 2, 2, 1, 2, 3499.00, 6998.00, 2),
(20240201, 3, 3, 1, 1, 12999.00, 12999.00, 3),
(20240305, 1, 2, 3, 1, 3499.00, 3499.00, 4);
