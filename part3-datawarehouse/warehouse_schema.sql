-- FlexiMart Data Warehouse Schema (Star Schema)
-- Database suggested: fleximart_dw

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_order_status;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_date;

-- -----------------------
-- Dimension: Date
-- -----------------------
CREATE TABLE dim_date (
  date_key INT PRIMARY KEY,           -- YYYYMMDD
  full_date DATE NOT NULL,
  day_of_week VARCHAR(10) NOT NULL,
  month INT NOT NULL,
  month_name VARCHAR(15) NOT NULL,
  quarter VARCHAR(2) NOT NULL,
  year INT NOT NULL,
  is_weekend BOOLEAN NOT NULL
);

-- -----------------------
-- Dimension: Customer
-- -----------------------
CREATE TABLE dim_customer (
  customer_key INT PRIMARY KEY AUTO_INCREMENT,
  customer_id_nk INT NOT NULL,         -- natural key from OLTP customers.customer_id
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(120),
  phone VARCHAR(25),
  city VARCHAR(60),
  registration_date DATE
);

-- -----------------------
-- Dimension: Product
-- -----------------------
CREATE TABLE dim_product (
  product_key INT PRIMARY KEY AUTO_INCREMENT,
  product_id_nk INT NOT NULL,          -- natural key from OLTP products.product_id
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(60) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock_quantity INT NOT NULL
);

-- -----------------------
-- Dimension: Order Status
-- -----------------------
CREATE TABLE dim_order_status (
  order_status_key INT PRIMARY KEY AUTO_INCREMENT,
  status VARCHAR(20) NOT NULL UNIQUE
);

-- -----------------------
-- Fact: Sales (order item grain)
-- -----------------------
CREATE TABLE fact_sales (
  sales_key BIGINT PRIMARY KEY AUTO_INCREMENT,
  date_key INT NOT NULL,
  customer_key INT NOT NULL,
  product_key INT NOT NULL,
  order_status_key INT NOT NULL,

  quantity_sold INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  sales_amount DECIMAL(12,2) NOT NULL,

  order_id_nk INT NOT NULL,            -- optional: OLTP order_id for traceability

  FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
  FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
  FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
  FOREIGN KEY (order_status_key) REFERENCES dim_order_status(order_status_key)
);
