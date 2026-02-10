"""
Script to create enhanced sample Excel file for testing category breakdown analysis
"""
import pandas as pd
import os

# Create sample transaction data with diverse categories
data = {
    'date': [
        # January 2026
        '2026-01-05', '2026-01-08', '2026-01-10', '2026-01-12', '2026-01-15', 
        '2026-01-18', '2026-01-20', '2026-01-22', '2026-01-25', '2026-01-28', '2026-01-30',
        # February 2026
        '2026-02-02', '2026-02-05', '2026-02-08', '2026-02-10', '2026-02-12',
        '2026-02-15', '2026-02-18', '2026-02-20', '2026-02-22', '2026-02-25', '2026-02-28',
        # March 2026
        '2026-03-01', '2026-03-05', '2026-03-08', '2026-03-10', '2026-03-12',
        '2026-03-15', '2026-03-18', '2026-03-20', '2026-03-22', '2026-03-25', '2026-03-28', '2026-03-31',
    ],
    'description': [
        # January - Food (Groceries and Dining)
        'Monthly Salary', 'Walmart Groceries', 'Starbucks Coffee', 'Target Grocery Store', 'Pizza Hut Delivery',
        'Whole Foods Market', 'McDonalds Drive Thru', 'Gas Station Fuel', 'Metro Transit Pass', 'Netflix Subscription', 'Freelance Income',
        # February - Transportation and Hobbies
        'Safeway Supermarket', 'Chipotle Restaurant', 'Monthly Salary', 'Uber Ride',
        'Bus Fare Downtown', 'Spotify Premium', 'LA Fitness Gym', 'Coffee Shop Downtown', 'Amazon Prime Video', 'Lyft Shared Ride', 'Car Insurance Payment',
        # March - More diverse spending
        'Monthly Salary', 'Kroger Grocery Shopping', 'Subway Sandwich Shop', 'Gas Station', 'Train Ticket',
        'Peloton Subscription', 'Disney Plus Subscription', 'Olive Garden Dining', 'Xbox Game Pass', 'Trader Joes Market', 'Coursera Course', 'Freelance Payment'
    ],
    'category': [
        # January
        'Salary', 'Groceries', 'Dining', 'Groceries', 'Dining',
        'Groceries', 'Dining', 'Transport', 'Transport', 'Entertainment', 'Income',
        # February
        'Groceries', 'Dining', 'Salary', 'Transport',
        'Transport', 'Entertainment', 'Entertainment', 'Dining', 'Entertainment', 'Transport', 'Insurance',
        # March
        'Salary', 'Groceries', 'Dining', 'Transport', 'Transport',
        'Entertainment', 'Entertainment', 'Dining', 'Entertainment', 'Groceries', 'Entertainment', 'Income'
    ],
    'value': [
        # January
        3000.00, -125.50, -5.75, -98.30, -28.50,
        -156.20, -12.45, -45.00, -85.00, -15.99, 500.00,
        # February
        -142.80, -45.60, 3000.00, -22.50,
        -3.50, -9.99, -49.00, -6.25, -12.99, -18.75, -180.00,
        # March
        3000.00, -118.90, -11.50, -52.00, -4.25,
        -39.00, -7.99, -58.30, -14.99, -89.40, -49.99, 600.00
    ]
}

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

df = pd.DataFrame(data)
df.to_excel('data/sample_transactions.xlsx', index=False)
print('Enhanced sample Excel file created successfully at: data/sample_transactions.xlsx')
print(f'Total transactions: {len(df)}')
print(f'Date range: {df["date"].min()} to {df["date"].max()}')

# Print summary by category
print('\nCategory Summary:')
expenses = df[df['value'] < 0].copy()
expenses['abs_value'] = expenses['value'].abs()
category_summary = expenses.groupby('category')['abs_value'].sum().sort_values(ascending=False)
for category, amount in category_summary.items():
    print(f'  {category}: ${amount:.2f}')
