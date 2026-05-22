import pandas as pd
from sqlalchemy import text

try:
    from config import get_engine, setup_logging, is_sqlite
except ImportError:
    from .config import get_engine, setup_logging, is_sqlite

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


def refresh_materialized_views():
    """Refresh PostgreSQL materialized views used by Power BI dashboards."""
    if is_sqlite():
        logger.info("SQLite mode detected; skipping materialized view refresh.")
        return

    views = [
        "mv_daily_revenue",
        "mv_customer_kpis",
        "mv_product_performance",
        "mv_fraud_summary",
        "mv_inventory_status",
    ]

    for view in views:
        try:
            execute_query(f"REFRESH MATERIALIZED VIEW {view}")
            logger.info(f"Refreshed materialized view: {view}")
        except Exception as exc:
            logger.warning(f"Could not refresh {view}: {exc}")
