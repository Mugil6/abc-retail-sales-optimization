from sqlalchemy import create_engine, text
import config_snowflake as cfg

def get_engine():
    conn_string = (
        f'snowflake://{cfg.SNOWFLAKE_USER}:{cfg.SNOWFLAKE_PASSWORD}@{cfg.SNOWFLAKE_ACCOUNT}/'
        f'{cfg.SNOWFLAKE_DATABASE}/{cfg.SNOWFLAKE_SCHEMA}?warehouse={cfg.SNOWFLAKE_WAREHOUSE}'
    )
    return create_engine(conn_string)

def run_transformation():
    engine = get_engine()
    with engine.begin() as conn:
        # Drop if exists
        conn.execute(text("DROP TABLE IF EXISTS RETAIL_OPTIMIZATION.RAW_DATA.TRANSFORMED_SALES_DATA"))

        # Create transformed table
        query = """
        CREATE OR REPLACE TABLE RETAIL_OPTIMIZATION.RAW_DATA.TRANSFORMED_SALES_DATA AS
        SELECT *,
            YEAR("Date") AS Year,
            MONTH("Date") AS Month,
            DAY("Date") AS Day,
            WEEKOFYEAR("Date") AS Week,
            CASE WHEN "DayOfWeek" IN (6, 7) THEN 1 ELSE 0 END AS IsWeekend,
            CASE WHEN "Customers" > 0 THEN "Sales" / "Customers" ELSE 0 END AS SalesPerCustomer
        FROM RETAIL_OPTIMIZATION.RAW_DATA.SALES_DATA;
        """
        conn.execute(text(query))
        print("Transformation complete. Table 'TRANSFORMED_SALES_DATA' created.")

if __name__ == "__main__":
    run_transformation()
