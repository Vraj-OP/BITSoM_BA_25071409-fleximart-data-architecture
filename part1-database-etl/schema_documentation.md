# Database Schema Documentation – FlexiMart

This document describes the relational database schema used for the FlexiMart e-commerce system. The schema is designed to store customer, product, and order-related information in a normalized form and supports transactional as well as analytical queries.

---

## 1. Entity–Relationship Description (Text Format)

### ENTITY: customers

**Purpose:**  
Stores information about customers who place orders on the FlexiMart platform.

**Attributes:**
- **customer_id** (INT, Primary Key): Unique identifier for each customer (auto-incremented)
- **first_name** (VARCHAR): Customer’s first name
- **last_name** (VARCHAR): Customer’s last name
- **email** (VARCHAR): Unique email address of the customer
- **phone** (VARCHAR): Contact phone number
- **city** (VARCHAR): City of residence
- **registration_date** (DATE): Date when the customer registered on the platform

**Relationships:**
- One customer can place **many orders**  
  (1 : M relationship with the `orders` table)

---

### ENTITY: products

**Purpose:**  
Stores details of products available for sale on the FlexiMart platform.

**Attributes:**
- **product_id** (INT, Primary Key): Unique identifier for each product (auto-incremented)
- **product_name** (VARCHAR): Name of the product
- **category** (VARCHAR): Product category (e.g., Electronics, Fashion, Groceries)
- **price** (DECIMAL): Price of the product
- **stock_quantity** (INT): Number of units available in inventory

**Relationships:**
- One product can appear in **many order items**  
  (1 : M relationship with the `order_items` table)

---

### ENTITY: orders

**Purpose:**  
Stores order-level information for purchases made by customers.

**Attributes:**
- **order_id** (INT, Primary Key): Unique identifier for each order (auto-incremented)
- **customer_id** (INT, Foreign Key): References `customers.customer_id`
- **order_date** (DATE): Date on which the order was placed
- **total_amount** (DECIMAL): Total value of the order
- **status** (VARCHAR): Order status (Completed, Pending, Cancelled)

**Relationships:**
- Each order belongs to **one customer**  
  (M : 1 relationship with `customers`)
- One order can contain **many order items**  
  (1 : M relationship with `order_items`)

---

### ENTITY: order_items

**Purpose:**  
Stores line-item level details for each order.

**Attributes:**
- **order_item_id** (INT, Primary Key): Unique identifier for each order item
- **order_id** (INT, Foreign Key): References `orders.order_id`
- **product_id** (INT, Foreign Key): References `products.product_id`
- **quantity** (INT): Quantity of the product ordered
- **unit_price** (DECIMAL): Price per unit at the time of purchase
- **subtotal** (DECIMAL): Calculated as quantity × unit_price

**Relationships:**
- Each order item belongs to **one order**
- Each order item refers to **one product**

---

## 2. Normalization Explanation (Third Normal Form – 3NF)

The FlexiMart database schema is designed to satisfy **Third Normal Form (3NF)** to ensure data integrity and eliminate redundancy.

In this design, each table represents a single entity, and all attributes are fully functionally dependent on the primary key. For example, in the `customers` table, attributes such as first_name, last_name, email, phone, city, and registration_date depend solely on customer_id. There are no attributes that depend on non-key attributes, thereby satisfying 2NF and 3NF.

Similarly, the `products` table stores only product-related information, and attributes like product_name, category, price, and stock_quantity depend entirely on product_id. Order-related data is separated into the `orders` table, which avoids repeating customer information for every order. Line-item details are further separated into the `order_items` table, ensuring that repeating groups of products within orders are properly normalized.

**Functional Dependencies:**
- customer_id → first_name, last_name, email, phone, city, registration_date
- product_id → product_name, category, price, stock_quantity
- order_id → customer_id, order_date, total_amount, status
- order_item_id → order_id, product_id, quantity, unit_price, subtotal

This design avoids:
- **Update anomalies**: Product price changes do not require updating multiple order records.
- **Insert anomalies**: New products and customers can be added independently of orders.
- **Delete anomalies**: Deleting an order does not remove customer or product information.

Thus, the schema conforms to **3NF** and supports reliable transactional processing.

---

## 3. Sample Data Representation

### customers

| customer_id | first_name | last_name | email                     | phone          | city       | registration_date |
|------------|------------|-----------|---------------------------|----------------|------------|-------------------|
| 1          | Rahul      | Sharma    | rahul.sharma@gmail.com    | +919876543210  | Bangalore  | 2023-01-15        |
| 2          | Priya      | Patel     | priya.patel@yahoo.com     | +919988776655  | Mumbai    | 2023-02-20        |

---

### products

| product_id | product_name          | category     | price   | stock_quantity |
|-----------|-----------------------|--------------|---------|----------------|
| 1         | Samsung Galaxy S21    | Electronics  | 45999.0 | 150            |
| 2         | Nike Running Shoes    | Fashion      | 3499.0  | 80             |

---

### orders

| order_id | customer_id | order_date | total_amount | status     |
|---------|-------------|------------|--------------|------------|
| 1       | 1           | 2024-01-15 | 45999.0      | Completed  |
| 2       | 2           | 2024-01-16 | 5998.0       | Completed  |

---

### order_items

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|--------------|----------|------------|----------|------------|----------|
| 1            | 1        | 1          | 1        | 45999.0   | 45999.0 |
| 2            | 2        | 2          | 2        | 2999.0    | 5998.0  |

---
