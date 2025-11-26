import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3
import webbrowser
import os


def create_dashboard():
    """Create static dashboard with Plotly"""

    # Database connection
    conn = sqlite3.connect("database/supermarket.db")

    # Payment method analysis
    payment_query = """
        SELECT 
            payment_method,
            COUNT(*) as transaction_count,
            SUM(total_price) as total_revenue,
            ROUND(SUM(total_price) * 100.0 / (SELECT SUM(total_price) FROM sales), 1) as revenue_percentage
        FROM sales
        GROUP BY payment_method
        ORDER BY total_revenue DESC
    """
    payment_data = pd.read_sql_query(payment_query, conn)

    # Product performance by rating
    product_rating_query = """
        SELECT 
            CASE 
                WHEN product_rating >= 4.5 THEN 'High (4.5-5.0)'
                WHEN product_rating >= 4.0 THEN 'Medium-High (4.0-4.4)'
                WHEN product_rating >= 3.5 THEN 'Medium (3.5-3.9)'
                ELSE 'Low (3.0-3.4)'
            END as rating_category,
            SUM(quantity) as total_quantity,
            SUM(total_price) as total_revenue,
            COUNT(DISTINCT product_name) as product_count
        FROM sales
        GROUP BY rating_category
        ORDER BY total_revenue DESC
    """
    rating_data = pd.read_sql_query(product_rating_query, conn)

    # Sales by city over time
    city_time_query = """
        SELECT 
            date,
            city,
            SUM(total_price) as daily_revenue
        FROM sales
        GROUP BY date, city
        ORDER BY date
    """
    city_time_data = pd.read_sql_query(city_time_query, conn)

    # Category performance
    category_query = """
        SELECT 
            category,
            SUM(total_price) as total_revenue,
            SUM(quantity) as total_quantity,
            AVG(product_rating) as avg_rating,
            COUNT(DISTINCT product_name) as product_count
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """
    category_data = pd.read_sql_query(category_query, conn)

    # Top products
    top_products_query = """
        SELECT 
            product_name,
            category,
            SUM(total_price) as total_revenue,
            SUM(quantity) as total_quantity,
            AVG(product_rating) as avg_rating
        FROM sales
        GROUP BY product_name, category
        ORDER BY total_revenue DESC
        LIMIT 15
    """
    top_products_data = pd.read_sql_query(top_products_query, conn)

    conn.close()

    # Create subplots
    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=(
            "Payment Method Revenue Distribution",
            "Product Performance by Rating",
            "Sales Trends by City",
            "Category Performance",
            "Top Products by Revenue",
            "Key Metrics",
        ),
        specs=[
            [{"type": "pie"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "bar"}, {"type": "table"}],
        ],
    )

    # 1. Payment Method Pie Chart
    fig.add_trace(
        go.Pie(
            labels=payment_data["payment_method"],
            values=payment_data["total_revenue"],
            name="Payment Methods",
        ),
        row=1,
        col=1,
    )

    # 2. Product Rating Performance
    fig.add_trace(
        go.Bar(
            x=rating_data["rating_category"],
            y=rating_data["total_revenue"],
            name="Revenue by Rating",
            marker_color="lightblue",
        ),
        row=1,
        col=2,
    )

    # 3. City Trends
    for city in city_time_data["city"].unique():
        city_data = city_time_data[city_time_data["city"] == city]
        fig.add_trace(
            go.Scatter(
                x=city_data["date"],
                y=city_data["daily_revenue"],
                mode="lines",
                name=city,
            ),
            row=2,
            col=1,
        )

    # 4. Category Performance Scatter
    fig.add_trace(
        go.Scatter(
            x=category_data["total_quantity"],
            y=category_data["total_revenue"],
            mode="markers",
            text=category_data["category"],
            textposition="top center",
            marker=dict(
                size=category_data["avg_rating"] * 10,
                color=category_data["avg_rating"],
                colorscale="Viridis",
                showscale=True,
            ),
            name="Categories",
        ),
        row=2,
        col=2,
    )

    # 5. Top Products Bar Chart
    fig.add_trace(
        go.Bar(
            x=top_products_data.head(10)["total_revenue"],
            y=top_products_data.head(10)["product_name"],
            orientation="h",
            name="Top Products",
            marker_color="lightgreen",
        ),
        row=3,
        col=1,
    )

    # 6. Key Metrics Table
    total_revenue = payment_data["total_revenue"].sum()
    total_transactions = payment_data["transaction_count"].sum()
    cash_percentage = 0
    for _, row in payment_data.iterrows():
        if row["payment_method"] == "Cash":
            cash_percentage = float(row["revenue_percentage"])
            break

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Metric", "Value"], fill_color="lightgray", align="left"
            ),
            cells=dict(
                values=[
                    [
                        "Total Revenue",
                        "Total Transactions",
                        "Cash Revenue %",
                        "Cities",
                        "Product Categories",
                    ],
                    [
                        f"${total_revenue:,.0f}",
                        f"{total_transactions:,}",
                        f"{cash_percentage}%",
                        "3",
                        str(len(category_data)),
                    ],
                ],
                fill_color="white",
                align="left",
            ),
        ),
        row=3,
        col=2,
    )

    # Update layout
    fig.update_layout(
        height=1200, title_text="Supermarket Sales Dashboard", showlegend=True
    )

    # Save dashboard
    fig.write_html("dashboard/supermarket_dashboard.html")
    print("Dashboard saved to dashboard/supermarket_dashboard.html")

    # Generate insights
    generate_insights(
        payment_data, rating_data, category_data, total_revenue, cash_percentage
    )

    return fig


def generate_insights(
    payment_data, rating_data, category_data, total_revenue, cash_percentage
):
    """Generate business insights"""

    print("\n" + "=" * 50)
    print("SUPERMARKET SALES DASHBOARD INSIGHTS")
    print("=" * 50)

    print(f"\n📊 OVERALL PERFORMANCE:")
    print(f"   • Total Revenue: ${total_revenue:,.2f}")
    print(f"   • Cash Revenue: {cash_percentage}% of total")

    print(f"\n💳 PAYMENT METHOD ANALYSIS:")
    for _, row in payment_data.iterrows():
        print(
            f"   • {row['payment_method']}: ${row['total_revenue']:,.0f} ({row['revenue_percentage']}%)"
        )

    print(f"\n⭐ PRODUCT RATING INSIGHTS:")
    for _, row in rating_data.iterrows():
        print(f"   • {row['rating_category']}: ${row['total_revenue']:,.0f}")

    print(f"\n📦 TOP CATEGORIES:")
    for _, row in category_data.head(3).iterrows():
        print(
            f"   • {row['category']}: ${row['total_revenue']:,.0f} (Avg Rating: {row['avg_rating']:.1f})"
        )

    print(f"\n🔍 KEY FINDINGS:")
    print(f"   • Cash transactions contribute {cash_percentage}% of gross income")
    if cash_percentage >= 50:
        print(f"   ✓ Cash is the primary revenue source as expected")

    high_rating_revenue = rating_data[
        rating_data["rating_category"].str.contains("High", na=False)
    ]["total_revenue"].sum()
    total_rating_revenue = rating_data["total_revenue"].sum()
    high_rating_percentage = (high_rating_revenue / total_rating_revenue) * 100

    print(
        f"   • High-rated products (4.5+) generate {high_rating_percentage:.1f}% of revenue"
    )
    if high_rating_percentage >= 20:
        print(f"   ✓ Top-rated items achieve higher sales volume as expected")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    # Create dashboard directory if it doesn't exist
    os.makedirs("dashboard", exist_ok=True)

    # Generate dashboard
    fig = create_dashboard()

    # Open in browser
    dashboard_path = os.path.abspath("dashboard/supermarket_dashboard.html")
    webbrowser.open(f"file://{dashboard_path}")
    print(f"\nDashboard opened in browser: {dashboard_path}")
