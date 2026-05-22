import pandas as pd
from sqlalchemy import text
from python.config import get_engine, setup_logging

logger = setup_logging("Utils")

def execute_query(query, params=None):
    """Executes a SQL query without returning results (e.g., INSERT, UPDATE, DELETE)."""
    engine = get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(text(query), params or {})
            logger.debug("Query executed successfully.")
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise

def fetch_data(query, params=None):
    """Executes a SQL query and returns results as a pandas DataFrame."""
    engine = get_engine()
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params=params)
            return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise

def bulk_insert(df, table_name, if_exists="append"):
    """Inserts a pandas DataFrame into a PostgreSQL table efficiently."""
    if df.empty:
        logger.warning(f"Empty DataFrame. Skipping insert for table {table_name}.")
        return
        
    engine = get_engine()
    try:
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi', chunksize=1000)
        logger.info(f"Successfully inserted {len(df)} rows into {table_name}.")
    except Exception as e:
        logger.error(f"Error during bulk insert to {table_name}: {e}")
        raise
