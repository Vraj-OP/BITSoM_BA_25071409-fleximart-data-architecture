\# FlexiMart Data Warehouse – Star Schema Design



\## Section 1: Schema Overview 



\### FACT TABLE: fact\_sales

\*\*Grain:\*\* One row per product per order line item  

\*\*Business Process:\*\* Sales transactions



\*\*Measures (Numeric Facts):\*\*

\- \*\*quantity\_sold:\*\* Number of units sold

\- \*\*unit\_price:\*\* Price per unit at the time of sale

\- \*\*sales\_amount:\*\* Final sales amount (quantity\_sold × unit\_price)

\- \*\*order\_id\_nk:\*\* Natural key from OLTP for traceability



\*\*Foreign Keys:\*\*

\- \*\*date\_key → dim\_date\*\*

\- \*\*product\_key → dim\_product\*\*

\- \*\*customer\_key → dim\_customer\*\*

\- \*\*order\_status\_key → dim\_order\_status\*\*



---



\### DIMENSION TABLE: dim\_date

\*\*Purpose:\*\* Enables time-based analysis such as daily, monthly, quarterly, and yearly trends  

\*\*Type:\*\* Conformed time dimension



\*\*Attributes:\*\*

\- \*\*date\_key (PK):\*\* Surrogate key in YYYYMMDD format

\- \*\*full\_date:\*\* Actual calendar date

\- \*\*day\_of\_week:\*\* Monday, Tuesday, etc.

\- \*\*month:\*\* Numeric month (1–12)

\- \*\*month\_name:\*\* January, February, etc.

\- \*\*quarter:\*\* Q1, Q2, Q3, Q4

\- \*\*year:\*\* Calendar year

\- \*\*is\_weekend:\*\* Boolean flag



---



\### DIMENSION TABLE: dim\_product

\*\*Purpose:\*\* Supports product and category-level analysis



\*\*Attributes:\*\*

\- \*\*product\_key (PK):\*\* Surrogate key

\- \*\*product\_id\_nk:\*\* Natural product ID from OLTP system

\- \*\*product\_name:\*\* Name of the product

\- \*\*category:\*\* Product category (Electronics, Fashion, etc.)

\- \*\*price:\*\* Reference price

\- \*\*stock\_quantity:\*\* Current stock quantity



---



\### DIMENSION TABLE: dim\_customer

\*\*Purpose:\*\* Enables customer-level and geographic analysis



\*\*Attributes:\*\*

\- \*\*customer\_key (PK):\*\* Surrogate key

\- \*\*customer\_id\_nk:\*\* Natural customer ID from OLTP system

\- \*\*full\_name:\*\* Customer full name

\- \*\*email:\*\* Customer email

\- \*\*phone:\*\* Customer phone number

\- \*\*city:\*\* Customer city

\- \*\*registration\_date:\*\* Date of registration



---



\### DIMENSION TABLE: dim\_order\_status

\*\*Purpose:\*\* Allows clean analysis by order status



\*\*Attributes:\*\*

\- \*\*order\_status\_key (PK):\*\* Surrogate key

\- \*\*status:\*\* Order status (Completed, Pending, Cancelled)



---



\## Section 2: Design Decisions 



The star schema is designed at the transaction line-item level, where each row in the fact table represents a single product sold within an order. This granularity was chosen to provide maximum analytical flexibility. It allows detailed analysis such as product-wise sales, quantity sold per product, and customer purchase behavior, while also supporting aggregated reporting at daily, monthly, or yearly levels.



Surrogate keys are used instead of natural keys to improve query performance and simplify joins between fact and dimension tables. Natural keys from the OLTP system may change or be reused over time, whereas surrogate keys remain stable and ensure historical consistency in analytical reporting.



This design supports drill-down and roll-up operations effectively. Users can roll up data from day to month or year using the date dimension, or drill down from category-level sales to individual products or customers through the respective dimension attributes.



---



\## Section 3: Sample Data Flow (3 marks)



\### Source Transaction (OLTP System)



Order ID: 101  

Customer Name: John Doe  

City: Mumbai  

Product: Laptop  

Category: Electronics  

Quantity: 2  

Unit Price: 50,000  

Order Date: 2024-01-15  



---



\### Representation in Data Warehouse



\*\*fact\_sales\*\*



date\_key : 20240115

customer\_key : 12

product\_key : 5

order\_status\_key : 1

quantity\_sold : 2

unit\_price : 50000

sales\_amount : 100000

order\_id\_nk : 101





\*\*dim\_date\*\*



date\_key : 20240115

full\_date : 2024-01-15

month : 1

month\_name : January

quarter : Q1

year : 2024



\*\*dim\_product\*\*



product\_key : 5

product\_name : Laptop

category : Electronics

price : 50000



\*\*dim\_customer\*\*



customer\_key : 12

full\_name : John Doe

city : Mumbai



