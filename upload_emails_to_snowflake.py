import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
import pandas as pd

# Snowflake connection parameters (replace with your credentials)
connection_parameters = {
        "account" : "DCFQAFF-QXC41329",
        "user" : "HARO",
        "password" : "T7r7YAKh7ggPcC4",
        "role" : "ACCOUNTADMIN",
        "warehouse" : "COMPUTE_WH",
        "database" : "CODIGO_FACILITO",
        "schema" : "PUBLIC"
    }

csv_path = ".data/emails.csv"
table_name = "EMAILS"

# Create Snowpark session
session = Session.builder.configs(connection_parameters).create()

# Inspect first few rows to infer columns
sample = pd.read_csv(csv_path, nrows=5)
columns = sample.columns.tolist()

# Create table if not exists (all columns as VARCHAR for simplicity)
col_defs = ', '.join([f'{col} VARCHAR' for col in columns])
session.sql(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {col_defs}
    )
""").collect()

# Upload in chunks
chunk_size = 10000
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    session.write_pandas(chunk, table_name, auto_create_table=False)

print("Upload complete.")
session.close()
