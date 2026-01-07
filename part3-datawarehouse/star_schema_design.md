\# FlexiMart Data Warehouse – Star Schema Design



\## Section 1: Schema Overview (Text Format)



\### FACT TABLE: fact\_sales

\*\*Grain:\*\* One row per product per order line item (one record per order item).  

\*\*Business Process:\*\* Sales transactions (order item level).



\*\*Measures (Numeric Facts):\*\*

\- \*\*quantity\_sold:\*\* Number of units sold (from order\_items.quantity)

\- \*\*unit\_price:\*\* Unit selling price at time of sale (from order\_items.unit\_price)

\- \*\*sales\_amount:\*\* Total sales amount for the line = quantity\_sold × unit\_price

\- \*\*order\_total\_amount:\*\* Order header total amount (from orders.total\_amount) (optional but useful)



\*\*Foreign Keys (Dimensions):\*\*

\- \*\*date\_key → dim\_date\*\*

\- \*\*customer\_key → dim\_customer\*\*

\- \*\*product\_key → dim\_product\*\*

\- \*\*order\_status\_key → dim\_order\_status\*\* (optional dimension for cleaner reporting)



---



\### DIMENSION TABLE: dim\_date

\*\*Purpose:\*\* Enables time-based reporting and aggregation.  

\*\*Type:\*\* Conformed time dimension.



\*\*Attributes:\*\*

\- \*\*date\_key (PK):\*\* Surrogate key in integer format `YYYYMMDD`

\- \*\*full\_date:\*\* Actual date (DATE)

\- \*\*day\_of\_week:\*\* Monday, Tuesday, etc.

\- \*\*month:\*\* 1–12

\- \*\*month\_name:\*\* January, February, etc.

\- \*\*quarter:\*\* Q1, Q2, Q3, Q4

\- \*\*year:\*\* 2023, 2024, etc.

\- \*\*is\_weekend:\*\* Boolean flag



---



\### DIMENSION TABLE: dim\_customer

\*\*Purpose:\*\* Customer profiling and geographic/customer-level analysis.



\*\*Attributes:\*\*

\- \*\*customer\_key (PK):\*\* Surrogate key (auto-increment)

\- \*\*customer\_id\_nk:\*\* Natural key from OLTP (customers.customer\_id)

\- \*\*full\_name:\*\* Customer name

\- \*\*email:\*\* Customer email

\- \*\*phone:\*\* Customer phone

\- \*\*city:\*\* Customer city

\- \*\*registration\_date:\*\* Registration date



---



\### DIMENSION TABLE: dim\_product

\*\*Purpose:\*\* Product-level analysis by category/subcategory and price bands.



\*\*Attributes:\*\*

\- \*\*product\_key (PK):\*\* Surrogate key (auto-increment)

\- \*\*product\_id\_nk:\*\* Natural key from OLTP (products.product\_id)

\- \*\*product\_name:\*\* Product name

\- \*\*category:\*\* Electronics/Fashion/Groceries

\- \*\*price:\*\* Current product price (reference)

\- \*\*stock\_quantity:\*\* Current stock quantity (reference)



---



\### DIMENSION TABLE: dim\_order\_status (Optional but recommended)

\*\*Purpose:\*\* Cleanly analyze sales by order status without text repetition in fact.



\*\*Attributes:\*\*

\- \*\*order\_status\_key (PK):\*\* Surrogate key

\- \*\*status:\*\* Completed / Pending / Cancelled



---



\## Section 2: Why a Star Schema?



A star schema is optimized for analytics workloads. Dimensions store descriptive attributes, while the fact table stores measurable events (sales). This supports:

\- Fast aggregations (SUM, COUNT, AVG) on large fact tables

\- Simple joins from fact to dimensions

\- Easy reporting by time, product category, and customer attributes



---



\## Section 3: Mapping from OLTP to Data Warehouse



\*\*Source (OLTP) → Target (DW):\*\*

\- `orders.order\_date` → `dim\_date.full\_date` and `fact\_sales.date\_key`

\- `customers.\*` → `dim\_customer.\*`

\- `products.\*` → `dim\_product.\*`

\- `orders.status` → `dim\_order\_status.status`

\- `order\_items.quantity, unit\_price, subtotal` → `fact\_sales.quantity\_sold, unit\_price, sales\_amount`



