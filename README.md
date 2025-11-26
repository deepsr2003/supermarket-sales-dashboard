# Supermarket Sales Dashboard

A practical sales analytics dashboard for tracking supermarket performance across multiple locations. Built with real-world business needs in mind, this project helps store managers understand payment trends, product performance, and customer behavior.

## What This Project Does

I built this dashboard to analyze supermarket sales data and answer practical business questions:

- **Payment Methods**: See how customers prefer to pay (cash vs digital)
- **Product Performance**: Find out which products sell best and why
- **Store Comparison**: Compare performance across different cities
- **Sales Trends**: Track how sales change over time

## Key Findings from the Data

After analyzing 1,200 transactions over 3 months:

### Payment Habits
- **Cash is still king**: 57.2% of revenue comes from cash transactions
- **Credit cards are strong**: 23.7% of customers use credit cards
- **Digital payments growing**: Though still small at 3.6%, this is an emerging trend

### Product Insights
- **Household items lead**: Products like batteries and detergent are top sellers
- **Fresh produce sells well**: Carrots and lettuce are consistently popular
- **Quality matters**: Higher-rated products generate 25.4% of revenue

### Store Performance
- **Chicago**: $57,960 in revenue (best performer)
- **Los Angeles**: $57,485 in revenue  
- **New York**: $55,565 in revenue

## Project Structure

```
supermarket-sales-dashboard/
├── data/                          # Sales data and product info
│   ├── transactions.csv           # Transaction records
│   └── transaction_items.csv       # Individual items sold
├── database/                      # SQLite database
│   └── supermarket.db             # Main database file
├── dashboard/                      # Interactive charts
│   └── realistic_supermarket_dashboard.html  # Main dashboard
├── scripts/                       # Analysis tools
│   ├── generate_realistic_data.py  # Create sample data
│   └── setup_realistic_database.py # Database setup
└── README.md                      # This file
```

## Getting Started

### What You Need
- Python 3.7 or newer
- A web browser (Chrome, Firefox, Safari, etc.)

### Setup Steps

1. **Install Python packages**
   ```bash
   pip install pandas plotly sqlite3
   ```

2. **Generate the data**
   ```bash
   python scripts/generate_realistic_data.py
   ```

3. **Set up the database**
   ```bash
   python database/setup_realistic_database.py
   ```

4. **Create the dashboard**
   ```bash
   python dashboard/create_realistic_dashboard.py
   ```

5. **View the results**
   - Open `dashboard/realistic_supermarket_dashboard.html` in your browser
   - The dashboard will open automatically

### Quick Start (All in One)

```bash
python scripts/generate_realistic_data.py && python database/setup_realistic_database.py && python dashboard/create_realistic_dashboard.py
```

## What the Dashboard Shows

### Main Dashboard View
- **Payment breakdown**: Pie chart showing cash vs card payments
- **Product ratings**: How quality affects sales
- **City trends**: Sales patterns over time by location
- **Category performance**: Which departments are most profitable
- **Top products**: Best-selling items list
- **Key metrics**: At-a-glance numbers

### Interactive Features
- Hover over charts for detailed information
- Click legend items to show/hide data
- Zoom in on time-based charts
- Filter by different categories

## Technical Details

### Data Size
- **1,200 transactions** over 90 days
- **4,739 individual items** sold
- **3 cities**: New York, Los Angeles, Chicago
- **8 product categories**: Dairy, Bakery, Produce, Meat, Beverages, Snacks, Household, Frozen

### Technology Used
- **Database**: SQLite (lightweight and reliable)
- **Analysis**: Python with Pandas for data processing
- **Visualization**: Plotly for interactive charts
- **Frontend**: HTML for easy sharing

## Sample Data

The project uses realistic sample data including:

**Products you'd actually find**:
- Organic Whole Milk, Cheddar Cheese Block
- Whole Wheat Bread, Blueberry Muffins  
- Red Apples, Bananas, Carrots
- Chicken Breast, Ground Beef, Salmon
- AA Batteries, Laundry Detergent

**Realistic pricing**:
- Most items: $2-30 range
- Quality premium: Higher-rated items cost 15% more
- Sales tax: 8.25% (typical US rate)

## Business Questions This Answers

1. **Should we invest more in digital payment systems?**
   - Currently only 3.6% of revenue, but growing

2. **Which products should we stock more of?**
   - Household items and fresh produce are top performers

3. **How do our stores compare?**
   - Chicago slightly outperforms other locations

4. **Does quality affect sales?**
   - Yes, high-rated products generate 25% more revenue

## Running Your Own Analysis

### Adding New Data
1. Export your sales data to CSV format
2. Match the column structure in `data/transactions.csv`
3. Update the database using the setup script

### Custom Queries
The SQLite database supports standard SQL queries:

```sql
-- Find top selling products
SELECT product, SUM(quantity) as total_sold
FROM transaction_items 
GROUP BY product 
ORDER BY total_sold DESC 
LIMIT 10;

-- Compare city performance  
SELECT city, SUM(gross_income) as revenue
FROM transactions
GROUP BY city;
```

## Troubleshooting

**Dashboard won't open?**
- Make sure you ran all setup scripts
- Check that the HTML file exists in the dashboard folder
- Try a different web browser

**Data seems wrong?**
- Regenerate data with: `python scripts/generate_realistic_data.py`
- Rebuild database with: `python database/setup_realistic_database.py`

**Python errors?**
- Install missing packages: `pip install pandas plotly`
- Make sure you're using Python 3.7+

## Future Improvements

Ideas for extending this project:
- Add customer demographic analysis
- Include seasonal trend detection
- Build mobile-friendly views
- Connect to real POS systems
- Add inventory tracking

## Contributing

Want to help improve this project?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test everything works
5. Submit a pull request

## License

This project is open source and available under the MIT License.

---

**Built by a data analyst who understands retail challenges**

**Last updated**: November 2025