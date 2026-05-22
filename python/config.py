import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging

# Load environment variables
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "quantivaiq")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# SQLAlchemy Connection String
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    """Returns a SQLAlchemy engine instance."""
    return create_engine(DATABASE_URL)

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
