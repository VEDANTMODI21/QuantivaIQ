import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from config import NUM_CUSTOMERS, NUM_PRODUCTS, NUM_ORDERS, setup_logging, test_db_connection, is_sqlite
from utils import get_engine, fetch_data, bulk_insert, execute_query, refresh_materialized_views

logger = setup_logging("ETL_Pipeline")
fake = Faker()

def generate_customers(num_customers):
    logger.info(f"Generating {num_customers} customers...")
    data = []
    for _ in range(num_customers):
        data.append({
            "name": fake.name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number()[:20],
            "city": fake.city(),
            "state": fake.state(),
            "country": "USA", # Simplified
            "registration_date": fake.date_time_between(start_date='-2y', end_date='now'),
            "is_active": random.choices([True, False], weights=[0.9, 0.1])[0]
        })
    df = pd.DataFrame(data)
    bulk_insert(df, "customers", if_exists="append")
    logger.info("Customers inserted.")

def generate_categories_and_suppliers():
    logger.info("Generating Categories and Suppliers...")
    categories = [
        {"category_name": "Electronics", "parent_category_id": None},
        {"category_name": "Clothing", "parent_category_id": None},
        {"category_name": "Home & Kitchen", "parent_category_id": None},
        {"category_name": "Sports", "parent_category_id": None},
        {"category_name": "Books", "parent_category_id": None}
    ]
    df_cat = pd.DataFrame(categories)
    bulk_insert(df_cat, "categories", if_exists="append")

    suppliers = []
    for _ in range(30):
        suppliers.append({
            "supplier_name": fake.company(),
            "contact_email": fake.company_email(),
            "country": fake.country(),
            "reliability_score": round(random.uniform(80.0, 100.0), 2)
        })
    df_sup = pd.DataFrame(suppliers)
    bulk_insert(df_sup, "suppliers", if_exists="append")
    logger.info("Categories and Suppliers inserted.")

def generate_products(num_products):
    logger.info(f"Generating {num_products} products...")
    cat_ids = fetch_data("SELECT category_id FROM categories")['category_id'].tolist()
    sup_ids = fetch_data("SELECT supplier_id FROM suppliers")['supplier_id'].tolist()
    
    if not cat_ids or not sup_ids:
        logger.error("No categories or suppliers found. Cannot generate products.")
        return

    data = []
    for _ in range(num_products):
        cost_price = round(random.uniform(5.0, 500.0), 2)
        price = round(cost_price * random.uniform(1.2, 2.5), 2) # 20% to 150% markup
        data.append({
            "product_name": fake.catch_phrase(),
            "category_id": random.choice(cat_ids),
            "supplier_id": random.choice(sup_ids),
            "price": price,
            "cost_price": cost_price,
            "stock_quantity": random.randint(50, 1000),
            "reorder_level": random.randint(10, 50)
        })
    df = pd.DataFrame(data)
    bulk_insert(df, "products", if_exists="append")
    
    # Generate Inventory
    prod_ids = fetch_data("SELECT product_id FROM products")['product_id'].tolist()
    inv_data = []
    for pid in prod_ids:
        inv_data.append({
            "product_id": pid,
            "warehouse_location": fake.city() + " Warehouse",
            "quantity_on_hand": random.randint(50, 1000),
            "quantity_reserved": 0,
            "last_restock_date": datetime.now()
        })
    bulk_insert(pd.DataFrame(inv_data), "inventory", if_exists="append")
    logger.info("Products and Inventory inserted.")

def generate_orders(num_orders):
    logger.info(f"Generating {num_orders} orders...")
    cust_ids = fetch_data("SELECT customer_id FROM customers")['customer_id'].tolist()
    prod_df = fetch_data("SELECT product_id, price FROM products")
    
    if not cust_ids or prod_df.empty:
        logger.error("Missing customers or products.")
        return

    # To optimize memory, we'll batch this
    batch_size = 5000
    for i in range(0, num_orders, batch_size):
        batch_orders = min(batch_size, num_orders - i)
        orders = []
        for _ in range(batch_orders):
            orders.append({
                "customer_id": random.choice(cust_ids),
                "order_date": fake.date_time_between(start_date='-1y', end_date='now'),
                "status": random.choices(['Completed', 'Pending', 'Cancelled'], weights=[0.85, 0.1, 0.05])[0],
                "total_amount": 0.0, # Will be updated by trigger, but we'll insert 0 for now
                "shipping_address": fake.address().replace('\n', ', '),
                "region": random.choice(["North", "South", "East", "West"])
            })
        df_orders = pd.DataFrame(orders)
        
        # Need to insert and then fetch generated order_ids to create items
        engine = get_engine()
        with engine.begin() as conn:
            df_orders.to_sql('orders', conn, if_exists='append', index=False, method='multi')
        
        # Fetch the newly inserted order_ids. We'll use a rough heuristic: get max N order_ids
        recent_order_ids = fetch_data(f"SELECT order_id FROM orders ORDER BY order_id DESC LIMIT {batch_orders}")['order_id'].tolist()
        
        items = []
        payments = []
        refunds = []
        for oid in recent_order_ids:
            num_items = random.randint(1, 5)
            order_total = 0
            for _ in range(num_items):
                p = prod_df.sample(1).iloc[0]
                qty = random.randint(1, 3)
                items.append({
                    "order_id": oid,
                    "product_id": int(p['product_id']),
                    "quantity": qty,
                    "unit_price": float(p['price']),
                    "discount": 0.0
                })
                order_total += qty * float(p['price'])
            
            # Payment
            payment_status = 'Completed'
            payments.append({
                "order_id": oid,
                "payment_method": random.choice(["Credit Card", "Debit Card", "UPI", "Wallet"]),
                "amount": float(order_total),
                "payment_date": datetime.now(),
                "status": payment_status,
                "transaction_ref": fake.uuid4()
            })
            
            # Refund (5% chance)
            if random.random() < 0.05:
                refunds.append({
                    "order_id": oid,
                    "payment_id": None, # Will map later or leave null for simplicity
                    "refund_amount": float(order_total),
                    "reason": random.choice(["Defective", "Not Needed", "Wrong Item"]),
                    "refund_date": datetime.now(),
                    "status": "Processed"
                })

        items_df = pd.DataFrame(items)
        if is_sqlite() and not items_df.empty:
            items_df['line_total'] = items_df['quantity'] * items_df['unit_price'] - items_df['discount']

        bulk_insert(items_df, "order_items", if_exists="append")
        bulk_insert(pd.DataFrame(payments), "payments", if_exists="append")
        if refunds:
            bulk_insert(pd.DataFrame(refunds), "refunds", if_exists="append")

        update_order_totals()
        logger.info(f"Inserted order batch {i} to {i + batch_orders}")

def update_order_totals():
    logger.info("Updating order totals from order_items...")
    execute_query(
        """
        UPDATE orders
        SET total_amount = (
            SELECT COALESCE(SUM(quantity * unit_price - discount), 0)
            FROM order_items oi
            WHERE oi.order_id = orders.order_id
        )
        """
    )


def run_pipeline():
    logger.info("Starting ETL Pipeline...")
    
    if not test_db_connection():
        logger.error("Unable to connect to the configured database. Run db_setup.py and verify your .env settings before retrying.")
        return

    # Check if data already exists
    count = fetch_data("SELECT COUNT(*) FROM customers").iloc[0,0]
    if count > 0:
        logger.info("Data already exists. Skipping ETL generation.")
        return

    generate_customers(NUM_CUSTOMERS)
    generate_categories_and_suppliers()
    generate_products(NUM_PRODUCTS)
    generate_orders(NUM_ORDERS)

    if not is_sqlite():
        refresh_materialized_views()
        logger.info("Power BI materialized views refreshed.")
    
    logger.info("ETL Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
