import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, event
from sqlalchemy.exc import OperationalError
import logging
import sqlite3

# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)

# Database Configuration
DB_DRIVER = os.getenv("DB_DRIVER", "postgres").lower()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "quantivaiq")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "quantivaiq.db")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQLITE_DB_FULL_PATH = PROJECT_ROOT / SQLITE_DB_PATH

if DB_DRIVER == "sqlite":
    DATABASE_URL = f"sqlite:///{SQLITE_DB_FULL_PATH}"
else:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Connection String

def _sqlite_configure(dbapi_con, connection_record):
    if isinstance(dbapi_con, sqlite3.Connection):
        cursor = dbapi_con.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA busy_timeout=30000;")
        cursor.close()


def get_engine(echo=False):
    """Returns a SQLAlchemy engine instance."""
    if DB_DRIVER == "sqlite":
        engine = create_engine(
            DATABASE_URL,
            echo=echo,
            connect_args={"check_same_thread": False, "timeout": 30},
        )
        event.listen(engine, "connect", _sqlite_configure)
        return engine
    return create_engine(DATABASE_URL, echo=echo, pool_pre_ping=True)


def is_sqlite():
    return DB_DRIVER == "sqlite"


def test_db_connection():
    """Check whether the configured database is reachable."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError as exc:
        logger = setup_logging("DBConnectionCheck")
        logger.error("Unable to connect to the configured database. Confirm your .env values are correct.")
        logger.debug(exc)
        return False

# Logging Configuration
def setup_logging(name="QuantivaIQ"):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
    return logger

# Simulation & Scale Constants
SIMULATION_INTERVAL = int(os.getenv("SIMULATION_INTERVAL_SECONDS", 5))
NUM_CUSTOMERS = int(os.getenv("NUM_CUSTOMERS", 5000))
NUM_PRODUCTS = int(os.getenv("NUM_PRODUCTS", 500))
NUM_ORDERS = int(os.getenv("NUM_ORDERS", 50000))
FRAUD_RATE = float(os.getenv("FRAUD_CONTAMINATION_RATE", 0.02))
