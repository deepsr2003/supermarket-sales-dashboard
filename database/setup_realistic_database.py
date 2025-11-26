import sqlite3
import pandas as pd
import os


def create_realistic_database():
    """Create SQLite database and load realistic data"""

    # Remove existing database
    if os.path.exists("database/supermarket.db"):
        os.remove("database/supermarket.db")

    # Create database connection
    conn = sqlite3.connect("database/supermarket.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE transactions (
            transaction_id TEXT PRIMARY KEY,
            date TEXT,
            time TEXT,
            city TEXT,
            store TEXT,
            customer_id TEXT,
            payment_method TEXT,
            num_items INTEGER,
            subtotal REAL,
            tax REAL,
            gross_income REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE transaction_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            product TEXT,
            category TEXT,
            quantity INTEGER,
            unit_price REAL,
            item_total REAL,
            rating REAL,
            FOREIGN KEY (transaction_id) REFERENCES transactions (transaction_id)
        )
    """)

    # Load realistic data
    transactions_df = pd.read_csv("data/transactions.csv")
    items_df = pd.read_csv("data/transaction_items.csv")

    # Insert data
    transactions_df.to_sql("transactions", conn, if_exists="append", index=False)
    items_df.to_sql("transaction_items", conn, if_exists="append", index=False)

    # Create indexes for better performance
    cursor.execute("CREATE INDEX idx_transactions_date ON transactions(date)")
    cursor.execute("CREATE INDEX idx_transactions_city ON transactions(city)")
    cursor.execute(
        "CREATE INDEX idx_transactions_payment ON transactions(payment_method)"
    )
    cursor.execute("CREATE INDEX idx_items_category ON transaction_items(category)")
    cursor.execute("CREATE INDEX idx_items_rating ON transaction_items(rating)")

    conn.commit()
    conn.close()

    print("Realistic database created successfully!")
    print(f"Transactions: {len(transactions_df)} records")
    print(f"Items: {len(items_df)} records")


def run_realistic_queries():
    """Run sample queries to verify realistic data"""
    conn = sqlite3.connect("database/supermarket.db")

    # Total sales by payment method
    payment_stats = pd.read_sql_query(
        """
        SELECT 
            payment_method,
            COUNT(*) as transaction_count,
            SUM(gross_income) as total_revenue,
            ROUND(SUM(gross_income) * 100.0 / (SELECT SUM(gross_income) FROM transactions), 1) as revenue_percentage
        FROM transactions
        GROUP BY payment_method
        ORDER BY total_revenue DESC
    """,
        conn,
    )

    print("\nPayment Method Analysis:")
    print(payment_stats)

    # Top performing products
    top_products = pd.read_sql_query(
        """
        SELECT 
            product,
            category,
            SUM(quantity) as total_quantity,
            SUM(item_total) as total_revenue,
            AVG(rating) as avg_rating
        FROM transaction_items
        GROUP BY product, category
        ORDER BY total_revenue DESC
        LIMIT 10
    """,
        conn,
    )

    print("\nTop 10 Products by Revenue:")
    print(top_products)

    # Sales by city
    city_stats = pd.read_sql_query(
        """
        SELECT 
            city,
            COUNT(DISTINCT transaction_id) as transaction_count,
            SUM(gross_income) as total_revenue
        FROM transactions
        GROUP BY city
        ORDER BY total_revenue DESC
    """,
        conn,
    )

    print("\nSales by City:")
    print(city_stats)

    conn.close()


if __name__ == "__main__":
    create_realistic_database()
    run_realistic_queries()
