import os
import sqlite3
import pandas as pd
import webbrowser


def test_realistic_system():
    """Test the realistic supermarket dashboard system"""

    print("Testing Supermarket Sales Dashboard...")
    print("=" * 50)

    # Test 1: Check files exist
    print("\n1. Checking required files...")
    required_files = [
        "data/transactions.csv",
        "data/transaction_items.csv",
        "database/supermarket.db",
        "dashboard/realistic_supermarket_dashboard.html",
    ]

    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✓ {file_path} ({size:,} bytes)")
        else:
            print(f"   ❌ {file_path} missing")
            all_files_exist = False

    if not all_files_exist:
        print("\nSome files are missing. Run setup first:")
        print("python scripts/generate_realistic_data.py")
        print("python database/setup_realistic_database.py")
        print("python dashboard/create_realistic_dashboard.py")
        return False

    # Test 2: Database connectivity
    print("\n2. Testing database...")
    try:
        conn = sqlite3.connect("database/supermarket.db")

        # Check data counts
        trans_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM transactions", conn
        )
        items_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM transaction_items", conn
        )

        print(f"   ✓ Database connected")
        print(f"   ✓ {trans_count.iloc[0, 0]:,} transactions")
        print(f"   ✓ {items_count.iloc[0, 0]:,} items sold")

        conn.close()
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

    # Test 3: Validate key insights
    print("\n3. Validating business insights...")
    try:
        conn = sqlite3.connect("database/supermarket.db")

        # Payment analysis
        payment_stats = pd.read_sql_query(
            """
            SELECT payment_method, SUM(gross_income) as revenue
            FROM transactions
            GROUP BY payment_method
            ORDER BY revenue DESC
        """,
            conn,
        )

        cash_revenue = 0
        for _, row in payment_stats.iterrows():
            if row["payment_method"] == "Cash":
                cash_revenue = row["revenue"]
                break
        total_revenue = payment_stats["revenue"].sum()
        cash_percentage = (cash_revenue / total_revenue) * 100

        print(f"   ✓ Cash revenue: {cash_percentage:.1f}% of total")

        if cash_percentage >= 50:
            print("   ✓ Cash is primary payment method (as expected)")

        # Product performance
        top_products = pd.read_sql_query(
            """
            SELECT product, SUM(item_total) as revenue
            FROM transaction_items
            GROUP BY product
            ORDER BY revenue DESC
            LIMIT 5
        """,
            conn,
        )

        print(f"   ✓ Top product: {top_products['product'].iloc[0]}")

        conn.close()
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
        return False

    # Test 4: Dashboard accessibility
    print("\n4. Testing dashboard...")
    dashboard_file = "dashboard/realistic_supermarket_dashboard.html"
    if os.path.exists(dashboard_file):
        file_size = os.path.getsize(dashboard_file)
        if file_size > 1000:  # Should be substantial
            print(f"   ✓ Dashboard ready ({file_size:,} bytes)")

            # Try to open in browser
            try:
                dashboard_path = os.path.abspath(dashboard_file)
                webbrowser.open(f"file://{dashboard_path}")
                print(f"   ✓ Dashboard opened in browser")
            except:
                dashboard_path = os.path.abspath(dashboard_file)
                print(f"   ⚠ Could not auto-open dashboard")
                print(f"     Open manually: {dashboard_path}")
        else:
            print(f"   ❌ Dashboard file too small")
            return False
    else:
        print(f"   ❌ Dashboard file missing")
        return False

    # Summary
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("\nThe supermarket dashboard is ready to use.")
    print("\nWhat you can do:")
    print("• View payment trends and patterns")
    print("• Analyze product performance")
    print("• Compare store locations")
    print("• Track sales over time")
    print("\nDashboard should be open in your browser now.")

    return True


if __name__ == "__main__":
    success = test_realistic_system()

    if not success:
        print("\n" + "=" * 50)
        print("❌ SOME TESTS FAILED")
        print("\nTo fix issues, run:")
        print("python scripts/generate_realistic_data.py")
        print("python database/setup_realistic_database.py")
        print("python dashboard/create_realistic_dashboard.py")
        print("python scripts/test_realistic_system.py")
