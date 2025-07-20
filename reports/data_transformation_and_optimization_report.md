Sprint 3 Report Contents
1. Overview of Data Transformation
What was transformed from the raw sales_data

New columns added (Year, Month, Week, IsWeekend, SalesPerCustomer, etc.)

Tools used: SQLAlchemy, Python scripts (snowflake_transform.py)

2. Final Transformed Tables
Table name: TRANSFORMED_SALES_DATA

Columns in the table (with descriptions)

Number of records and basic stats (e.g., number of unique stores/products)

3. Schema Design
Simple ERD or Star Schema

Fact Table: TRANSFORMED_SALES_DATA

Dimensions (if created): stores, products, calendar, etc.

Description of keys and relationships

4. Performance Optimization
Any indexing, clustering keys, or partitioning considered/applied in Snowflake

Query performance tuning (e.g., caching, column ordering)

Justification of schema choice and optimization methods

5. Sample Queries
Aggregations like total weekly sales, sales per store, etc.

Demonstration of how the transformed data can be efficiently queried

6. Challenges & Learnings
Any challenges faced in schema design or transformation

How you validated data quality and correctness