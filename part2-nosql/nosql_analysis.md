\# NoSQL Justification Report – FlexiMart



\## Problem Context



FlexiMart plans to expand its product catalog to include a wide variety of products with highly diverse attributes such as electronics, apparel, groceries, and lifestyle items. The objective of this analysis is to evaluate whether a NoSQL database, specifically MongoDB, is suitable for managing such a dynamic product catalog.



---



\## Section A: Limitations of RDBMS (≈150 words)



Relational databases such as MySQL are well suited for structured and fixed-schema data; however, they face limitations when handling highly diverse product catalogs. In FlexiMart’s case, different product categories require different attributes—for example, laptops require specifications like RAM and processor, while shoes require size and color. Representing such variability in an RDBMS would require many nullable columns or multiple related tables, increasing complexity and reducing efficiency.



Additionally, frequent schema changes are required when introducing new product types or attributes. Each schema change involves ALTER TABLE operations, which can be costly and disruptive in large databases. Furthermore, storing customer reviews as nested data is not natural in a relational model and requires separate tables and complex joins, making read operations slower and queries harder to maintain.



Thus, a traditional RDBMS struggles with flexibility, rapid evolution, and hierarchical data representation in this use case.



---



\## Section B: NoSQL Benefits (≈150 words)



MongoDB addresses the limitations of relational databases through its flexible, document-based data model. Products can be stored as JSON-like documents where each product includes only the attributes relevant to its category. For example, an electronics product can store technical specifications, while a fashion product can store size and color, without affecting other documents.



MongoDB also supports embedded documents, allowing customer reviews to be stored directly within product documents. This improves read performance and simplifies data retrieval by avoiding expensive joins. Additionally, MongoDB is designed for horizontal scalability using sharding, enabling FlexiMart to handle rapid growth in product data and traffic by distributing data across multiple servers.



Overall, MongoDB provides schema flexibility, efficient handling of nested data, and scalability, making it well suited for a rapidly evolving and diverse product catalog.



---



\## Section C: Trade-offs (≈100 words)



Despite its advantages, MongoDB has certain trade-offs compared to MySQL. First, MongoDB does not enforce strong relational constraints such as foreign keys, which means data integrity must be handled at the application level. This increases the responsibility on developers to maintain consistency.



Second, MongoDB is not ideal for complex transactional operations involving multiple entities, as relational databases provide stronger ACID guarantees for such scenarios. Therefore, while MongoDB is suitable for product catalogs, relational databases remain preferable for order processing and financial transactions.



---



