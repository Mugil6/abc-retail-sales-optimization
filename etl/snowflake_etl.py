import pandas as pd
from sqlalchemy import create_engine
import config_snowflake as cfg

def get_engine():
    conn_string = (
        f'snowflake://{cfg.SNOWFLAKE_USER}:{cfg.SNOWFLAKE_PASSWORD}@{cfg.SNOWFLAKE_ACCOUNT}/'
        f'{cfg.SNOWFLAKE_DATABASE}/{cfg.SNOWFLAKE_SCHEMA}?warehouse={cfg.SNOWFLAKE_WAREHOUSE}'
    )
    return create_engine(conn_string)

def load_to_snowflake(csv_path, table_name):
    df = pd.read_csv(csv_path, parse_dates=['Date'])

    engine = get_engine()
    print(f"Inserting {len(df)} rows to Snowflake...")
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
    print(f"Data loaded into {table_name}.")

if __name__ == "__main__":
    load_to_snowflake("data/train_cleaned.csv", "sales_data")
