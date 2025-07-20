\# Retail Sales Optimization Project for ABC Retail Corp



> \*\*Tech Stack:\*\* Python, Pandas, Snowflake, RandomForestRegressor, Streamlit, Matplotlib  



\## 📌 Project Overview



This project aims to optimize retail sales forecasting for ABC Retail Corp using historical sales data. We built an end-to-end data engineering and ML pipeline covering:

\- Data ingestion and transformation

\- Forecasting next month's sales for all stores

\- Interactive visualizations and dashboards

\- Deployment-ready Streamlit application



---



\## 🧱 Components



\### 1. \*\*Data Collection and Cleaning\*\*

\- Source: `train.csv`

\- Processed missing values, parsed dates, and extracted temporal features.



\### 2. \*\*Data Ingestion\*\*

\- Loaded cleaned data into \*\*Snowflake\*\* using Python connectors.

\- Schema: Store-wise sales records with date, inventory, and promo info.



\### 3. \*\*Sales Forecasting\*\*

\- Model: `Random Forest Regressor`

\- Forecast: Total store sales for the upcoming month

\- Evaluation: RMSE and MAE on validation set

\- Output: `next\_month\_forecast\_all\_stores.csv`



\### 4. \*\*Dashboard and Visualization\*\*

\- Framework: \*\*Streamlit\*\*

\- Features:

&nbsp; - Store-level sales trends

&nbsp; - Inventory heatmaps

&nbsp; - Forecast visualizations

&nbsp; - Sidebar filters (store, year, month)



---







