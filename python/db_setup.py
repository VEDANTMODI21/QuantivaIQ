import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text
from config import get_engine, setup_logging, test_db_connection

load_dotenv()
logger = setup_logging("DBSetup")

ROOT_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT_DIR / "sql"


def run_sql_file(engine, path: Path):
    logger.info(f"Running SQL script: {path}")
    sql_text = path.read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.exec_driver_sql(sql_text)
    logger.info(f"Completed: {path.name}")


def main():
    if not test_db_connection():
        logger.error("Database connectivity check failed. Start PostgreSQL and verify .env settings before running db_setup.py.")
        return

    engine = get_engine()

    schema_file = SQL_DIR / "schema.sql"
    procedures_file = SQL_DIR / "procedures.sql"

    if not schema_file.exists() or not procedures_file.exists():
        logger.error("SQL schema or procedures file not found. Please check the sql/ directory.")
        return

    run_sql_file(engine, schema_file)
    run_sql_file(engine, procedures_file)
    logger.info("Database schema and stored procedures loaded successfully.")


if __name__ == "__main__":
    main()
