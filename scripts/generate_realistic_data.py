import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


def generate_realistic_sales_data(num_transactions=1200):
    """Generate realistic supermarket sales data"""

    np.random.seed(42)
    random.seed(42)

    # Store locations
    stores = {
        "NY": ["NY-Downtown", "NY-Uptown", "NY-Brooklyn"],
        "LA": ["LA-Santa Monica", "LA-Beverly Hills", "LA-Downtown"],
        "CH": ["CH-Loop", "CH-Lincoln Park", "CH-Wicker Park"],
    }

    # Realistic product catalog
    products = {
        "Dairy": [
            "Organic Whole Milk",
            "Cheddar Cheese Block",
            "Greek Yogurt",
            "Butter Stick",
            "Vanilla Ice Cream",
        ],
        "Bakery": [
            "Whole Wheat Bread",
            "Bagels (6-pack)",
            "Croissants",
            "Blueberry Muffins",
            "Chocolate Chip Cookies",
        ],
        "Produce": ["Red Apples", "Bananas", "Tomatoes", "Romaine Lettuce", "Carrots"],
        "Meat": [
            "Chicken Breast",
            "Ground Beef",
            "Pork Chops",
            "Salmon Fillet",
            "Bacon",
        ],
        "Beverages": [
            "Orange Juice",
            "Cola Soda",
            "Spring Water",
            "Coffee Beans",
            "Green Tea",
        ],
        "Snacks": [
            "Potato Chips",
            "Mixed Nuts",
            "Crackers",
            "Popcorn",
            "Chocolate Bar",
        ],
        "Household": [
            "Paper Towels",
            "Hand Soap",
            "Laundry Detergent",
            "AA Batteries",
            "Trash Bags",
        ],
        "Frozen": [
            "Frozen Pizza",
            "Ice Cream",
            "Frozen Vegetables",
            "Frozen Dinners",
            "Frozen Desserts",
        ],
    }

    # Payment distribution based on retail patterns
    payment_methods = ["Cash", "Credit Card", "Debit Card", "Digital", "Gift Card"]
    payment_dist = [0.55, 0.25, 0.15, 0.03, 0.02]

    # Generate transactions
    transactions = []
    items = []

    start_date = datetime.now() - timedelta(days=90)

    for i in range(num_transactions):
        # Transaction details
        trans_date = start_date + timedelta(
            days=random.randint(0, 89),
            hours=random.randint(6, 22),
            minutes=random.randint(0, 59),
        )

        city = random.choice(list(stores.keys()))
        store = random.choice(stores[city])
        payment = random.choices(payment_methods, weights=payment_dist)[0]

        # Generate basket
        basket_size = random.randint(1, 7)
        trans_items = []
        subtotal = 0

        for _ in range(basket_size):
            category = random.choice(list(products.keys()))
            product = random.choice(products[category])

            # Realistic pricing
            base_price = round(random.uniform(1.99, 29.99), 2)
            quantity = random.randint(1, 3)

            # Quality premium
            rating = round(random.uniform(3.2, 4.8), 1)
            if rating >= 4.5:
                price_multiplier = 1.15
            elif rating >= 4.0:
                price_multiplier = 1.05
            else:
                price_multiplier = 1.0

            unit_price = round(base_price * price_multiplier, 2)
            item_total = round(unit_price * quantity, 2)

            subtotal += item_total

            trans_items.append(
                {
                    "transaction_id": f"TXN{10000 + i}",
                    "product": product,
                    "category": category,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "item_total": item_total,
                    "rating": rating,
                }
            )

        # Calculate totals
        tax = round(subtotal * 0.0825, 2)
        total = round(subtotal + tax, 2)

        # Transaction record
        transactions.append(
            {
                "transaction_id": f"TXN{10000 + i}",
                "date": trans_date.strftime("%Y-%m-%d"),
                "time": trans_date.strftime("%H:%M:%S"),
                "city": city,
                "store": store,
                "customer_id": f"C{random.randint(1000, 9999)}",
                "payment_method": payment,
                "num_items": basket_size,
                "subtotal": subtotal,
                "tax": tax,
                "gross_income": total,
            }
        )

        # Add items
        items.extend(trans_items)

    return transactions, items


def save_data(transactions, items):
    """Save generated data to CSV files"""
    os.makedirs("data", exist_ok=True)

    # Save transactions
    pd.DataFrame(transactions).to_csv("data/transactions.csv", index=False)

    # Save items
    pd.DataFrame(items).to_csv("data/transaction_items.csv", index=False)

    # Summary stats
    df = pd.DataFrame(transactions)
    summary = {
        "total_transactions": len(df),
        "total_revenue": df["gross_income"].sum(),
        "cash_revenue": df[df["payment_method"] == "Cash"]["gross_income"].sum(),
        "cash_percentage": (
            df[df["payment_method"] == "Cash"]["gross_income"].sum()
            / df["gross_income"].sum()
            * 100
        ),
    }

    pd.DataFrame([summary]).to_csv("data/summary.csv", index=False)

    print(f"Generated {len(transactions)} transactions")
    print(f"Total revenue: ${summary['total_revenue']:,.2f}")
    print(f"Cash percentage: {summary['cash_percentage']:.1f}%")


if __name__ == "__main__":
    transactions, items = generate_realistic_sales_data()
    save_data(transactions, items)
