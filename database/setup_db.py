import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

from database.models import Base, Customer, Product, Order
from utils.logger import logger

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sales.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
SQLITE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Customer).count() > 0:
        logger.info("Database already seeded. Skipping.")
        db.close()
        return

    logger.info("Seeding database with Sales Data...")
    
    # Customers
    customers = [
        Customer(name="Alice Smith", email="alice@corp.com", company="Corp A"),
        Customer(name="Bob Jones", email="bob@tech.com", company="Tech B"),
        Customer(name="Charlie Brown", email="charlie@web.com", company="Web C"),
    ]
    db.add_all(customers)
    db.commit()

    # Products
    products = [
        Product(name="Enterprise Server", category="Hardware", price=5000.0),
        Product(name="Cloud Storage 1TB", category="Software", price=120.0),
        Product(name="Consulting Hours", category="Service", price=250.0),
    ]
    db.add_all(products)
    db.commit()

    # Orders
    for _ in range(15):
        cust = random.choice(customers)
        prod = random.choice(products)
        qty = random.randint(1, 5)
        # Using a fixed date range
        order_date = datetime.utcnow() - timedelta(days=random.randint(1, 60))
        order = Order(
            customer_id=cust.id,
            product_id=prod.id,
            quantity=qty,
            total_price=prod.price * qty,
            order_date=order_date
        )
        db.add(order)
    
    db.commit()
    db.close()
    logger.info(f"Database seeded at {DB_PATH}")

if __name__ == "__main__":
    seed_database()
