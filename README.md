# FlexiMart Data Architecture Project

# FlexiMart Data Architecture Project

**Student Name:** Vraj Roshan Porob
**Student ID:** BITSoM_BA_25071409
**Email:** vrajporob96@gmail.com
**Date:** 07-01-2026

## Project Overview

This project demonstrates the design and implementation of a complete data architecture for an e-commerce platform named FlexiMart. It covers the full data lifecycle including data ingestion and cleaning using an ETL pipeline, relational database design and querying, NoSQL data modeling using MongoDB, and analytical reporting using a star schema data warehouse. The solution enables efficient operational processing as well as scalable analytical insights for business decision-making.


## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- **Python 3.x** – ETL pipeline implementation  
- **pandas** – Data cleaning and transformation  
- **mysql-connector-python** – Database connectivity  
- **MySQL 8.0** – Relational database and data warehouse  
- **MongoDB 6.0** – NoSQL document database  


## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

Through this project, I gained hands-on experience in designing end-to-end data architectures for real-world business scenarios. I learned how to build robust ETL pipelines to handle data quality issues, design normalized relational schemas, and write complex SQL queries for business reporting. Additionally, I understood when and why NoSQL databases such as MongoDB are suitable for flexible and schema-less data, and how star schemas enable efficient OLAP analytics. This project strengthened my understanding of data modeling, analytics, and system design trade-offs.

## Challenges Faced

1. Handling inconsistent and missing data during ETL:
    This was resolved by applying appropriate cleaning strategies such as deduplication, default values, format standardization, and validation rules using pandas.

2. Designing an analytics-friendly data warehouse schema:
    This was addressed by adopting a star schema with clear granularity, surrogate keys, and well-defined fact and dimension tables to support efficient OLAP queries.
