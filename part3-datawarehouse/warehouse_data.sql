-- ==============================
-- FlexiMart DW - Warehouse Data
-- Meets minimum requirements:
-- dim_date: 30 dates (Jan-Feb 2024)
-- dim_product: 15 products across 3 categories
-- dim_customer: 12 customers across 4 cities
-- fact_sales: 40 sales transactions
-- ==============================

-- ------------------------------
-- 1) dim_date (30 dates: Jan 20 to Feb 18, 2024)
-- ------------------------------
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,TRUE),
(20240121,'2024-01-21','Sunday',21,1,'January','Q1',2024,TRUE),
(20240122,'2024-01-22','Monday',22,1,'January','Q1',2024,FALSE),
(20240123,'2024-01-23','Tuesday',23,1,'January','Q1',2024,FALSE),
(20240124,'2024-01-24','Wednesday',24,1,'January','Q1',2024,FALSE),
(20240125,'2024-01-25','Thursday',25,1,'January','Q1',2024,FALSE),
(20240126,'2024-01-26','Friday',26,1,'January','Q1',2024,FALSE),
(20240127,'2024-01-27','Saturday',27,1,'January','Q1',2024,TRUE),
(20240128,'2024-01-28','Sunday',28,1,'January','Q1',2024,TRUE),
(20240129,'2024-01-29','Monday',29,1,'January','Q1',2024,FALSE),
(20240130,'2024-01-30','Tuesday',30,1,'January','Q1',2024,FALSE),
(20240131,'2024-01-31','Wednesday',31,1,'January','Q1',2024,FALSE),
(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,FALSE),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,FALSE),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,TRUE),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,TRUE),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,FALSE),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,FALSE),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,FALSE),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,FALSE),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,FALSE),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,TRUE),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,TRUE),
(20240212,'2024-02-12','Monday',12,2,'February','Q1',2024,FALSE),
(20240213,'2024-02-13','Tuesday',13,2,'February','Q1',2024,FALSE),
(20240214,'2024-02-14','Wednesday',14,2,'February','Q1',2024,FALSE),
(20240215,'2024-02-15','Thursday',15,2,'February','Q1',2024,FALSE),
(20240216,'2024-02-16','Friday',16,2,'February','Q1',2024,FALSE),
(20240217,'2024-02-17','Saturday',17,2,'February','Q1',2024,TRUE),
(20240218,'2024-02-18','Sunday',18,2,'February','Q1',2024,TRUE);

-- ------------------------------
-- 2) dim_product (15 products, 3 categories, varied prices)
-- NOTE: inserting product_key explicitly for predictable FK references
-- ------------------------------
INSERT INTO dim_product (product_key, product_id, product_name, category, subcategory, unit_price) VALUES
(1,'ELEC001','Samsung Galaxy S21 Ultra','Electronics','Smartphones',79999.00),
(2,'ELEC002','Apple MacBook Pro 14-inch','Electronics','Laptops',189999.00),
(3,'ELEC003','Sony WH-1000XM5 Headphones','Electronics','Audio',29990.00),
(4,'ELEC004','Dell 27-inch 4K Monitor','Electronics','Monitors',32999.00),
(5,'ELEC005','OnePlus Nord CE 3','Electronics','Smartphones',26999.00),
(6,'ELEC006','Samsung 55-inch QLED TV','Electronics','Televisions',64999.00),

(7,'FASH001','Levis 511 Slim Fit Jeans','Fashion','Clothing',3499.00),
(8,'FASH002','Nike Air Max 270 Sneakers','Fashion','Footwear',12995.00),
(9,'FASH003','Adidas Originals T-Shirt','Fashion','Clothing',1499.00),
(10,'FASH004','Puma RS-X Sneakers','Fashion','Footwear',8999.00),
(11,'FASH005','H&M Slim Fit Formal Shirt','Fashion','Clothing',1999.00),

(12,'GROC001','Basmati Rice 5kg','Groceries','Staples',650.00),
(13,'GROC002','Organic Almonds 500g','Groceries','Dry Fruits',899.00),
(14,'GROC003','Organic Honey 500g','Groceries','Health Foods',450.00),
(15,'GROC004','Masoor Dal 1kg','Groceries','Pulses',120.00);

-- ------------------------------
-- 3) dim_customer (12 customers across 4 cities)
-- NOTE: inserting customer_key explicitly for predictable FK references
-- ------------------------------
INSERT INTO dim_customer (customer_key, customer_id, customer_name, city, state, customer_segment) VALUES
(1,'C001','Rahul Sharma','Mumbai','Maharashtra','Consumer'),
(2,'C002','Priya Patel','Mumbai','Maharashtra','Corporate'),
(3,'C003','Amit Kumar','Bangalore','Karnataka','Consumer'),
(4,'C004','Sneha Reddy','Bangalore','Karnataka','Home Office'),
(5,'C005','Vikram Singh','Delhi','Delhi','Corporate'),
(6,'C006','Anjali Mehta','Delhi','Delhi','Consumer'),
(7,'C007','Ravi Verma','Kolkata','West Bengal','Consumer'),
(8,'C008','Pooja Iyer','Kolkata','West Bengal','Home Office'),
(9,'C009','Karthik Nair','Mumbai','Maharashtra','Consumer'),
(10,'C010','Deepa Gupta','Bangalore','Karnataka','Corporate'),
(11,'C011','Arjun Rao','Delhi','Delhi','Home Office'),
(12,'C012','Lakshmi Krishnan','Kolkata','West Bengal','Consumer');

-- ------------------------------
-- 4) fact_sales (40 transactions)
-- Realistic patterns: higher quantities on weekends + discounts sometimes
-- total_amount = (quantity_sold * unit_price) - discount_amount
-- ------------------------------
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- Weekend spike (Jan 20-21)
(20240120, 12, 1, 6, 650.00, 0.00, 3900.00),
(20240120, 8, 2, 2, 12995.00, 500.00, 25490.00),
(20240120, 3, 3, 1, 29990.00, 1000.00, 28990.00),
(20240121, 15, 4, 10, 120.00, 0.00, 1200.00),
(20240121, 7, 5, 2, 3499.00, 0.00, 6998.00),

-- Weekdays (Jan 22-26)
(20240122, 9, 6, 3, 1499.00, 0.00, 4497.00),
(20240122, 13, 7, 2, 899.00, 0.00, 1798.00),
(20240123, 1, 8, 1, 79999.00, 2000.00, 77999.00),
(20240123, 11, 9, 2, 1999.00, 0.00, 3998.00),
(20240124, 14, 10, 4, 450.00, 0.00, 1800.00),
(20240124, 5, 11, 1, 26999.00, 1500.00, 25499.00),
(20240125, 10, 12, 1, 8999.00, 0.00, 8999.00),
(20240125, 12, 2, 5, 650.00, 0.00, 3250.00),
(20240126, 6, 3, 1, 64999.00, 3000.00, 61999.00),
(20240126, 15, 4, 8, 120.00, 0.00, 960.00),

-- Weekend spike (Jan 27-28)
(20240127, 2, 5, 1, 189999.00, 5000.00, 184999.00),
(20240127, 8, 6, 2, 12995.00, 0.00, 25990.00),
(20240127, 13, 7, 3, 899.00, 0.00, 2697.00),
(20240128, 4, 8, 1, 32999.00, 1000.00, 31999.00),
(20240128, 7, 9, 3, 3499.00, 0.00, 10497.00),

-- End of Jan (Jan 29-31)
(20240129, 3, 10, 1, 29990.00, 0.00, 29990.00),
(20240129, 14, 11, 2, 450.00, 0.00, 900.00),
(20240130, 1, 12, 1, 79999.00, 2500.00, 77499.00),
(20240130, 9, 1, 2, 1499.00, 0.00, 2998.00),
(20240131, 5, 2, 1, 26999.00, 0.00, 26999.00),

-- Feb weekdays (Feb 1-2)
(20240201, 12, 3, 4, 650.00, 0.00, 2600.00),
(20240201, 11, 4, 1, 1999.00, 0.00, 1999.00),
(20240202, 6, 5, 1, 64999.00, 2000.00, 62999.00),
(20240202, 13, 6, 2, 899.00, 0.00, 1798.00),

-- Weekend spike (Feb 3-4)
(20240203, 2, 7, 1, 189999.00, 7000.00, 182999.00),
(20240203, 8, 8, 2, 12995.00, 500.00, 25490.00),
(20240204, 1, 9, 1, 79999.00, 1000.00, 78999.00),
(20240204, 15, 10, 12, 120.00, 0.00, 1440.00),

-- Feb weekdays (Feb 5-9)
(20240205, 7, 11, 1, 3499.00, 0.00, 3499.00),
(20240205, 14, 12, 3, 450.00, 0.00, 1350.00),
(20240206, 4, 1, 1, 32999.00, 0.00, 32999.00),
(20240207, 3, 2, 1, 29990.00, 1000.00, 28990.00),
(20240208, 10, 3, 1, 8999.00, 0.00, 8999.00),
(20240209, 5, 4, 1, 26999.00, 500.00, 26499.00),

-- Weekend spike (Feb 10-11)
(20240210, 12, 5, 6, 650.00, 0.00, 3900.00),
(20240210, 8, 6, 1, 12995.00, 0.00, 12995.00),
(20240211, 6, 7, 1, 64999.00, 3000.00, 61999.00),
(20240211, 9, 8, 4, 1499.00, 0.00, 5996.00),

-- Feb weekdays (Feb 12-18)
(20240212, 11, 9, 2, 1999.00, 0.00, 3998.00),
(20240213, 13, 10, 2, 899.00, 0.00, 1798.00),
(20240214, 1, 11, 1, 79999.00, 2000.00, 77999.00),
(20240215, 4, 12, 1, 32999.00, 1000.00, 31999.00),
(20240216, 5, 1, 1, 26999.00, 0.00, 26999.00),
(20240217, 2, 2, 1, 189999.00, 6000.00, 183999.00),
(20240218, 6, 3, 1, 64999.00, 2000.00, 62999.00);
