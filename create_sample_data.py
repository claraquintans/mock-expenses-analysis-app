"""
Script to create sample Excel file for testing
"""
import pandas as pd

# Create sample transaction data spanning multiple months
data = {
    'date': [
        '2026-01-05', '2026-01-10', '2026-01-15', '2026-01-20', '2026-01-25', '2026-01-30',
        '2026-02-02', '2026-02-05', '2026-02-10', '2026-02-15', '2026-02-20', '2026-02-28',
        '2026-03-01', '2026-03-05', '2026-03-10', '2026-03-15', '2026-03-20', '2026-03-31',
        '2026-04-01', '2026-04-05', '2026-04-10', '2026-04-15', '2026-04-20', '2026-04-30'
    ],
    'description': [
        'Monthly Salary', 'Grocery Store', 'Coffee Shop', 'Electric Bill', 'Gas Station', 'Freelance Payment',
        'Grocery Store', 'Restaurant', 'Monthly Salary', 'Online Shopping', 'Phone Bill', 'Car Repair',
        'Monthly Salary', 'Grocery Store', 'Movie Tickets', 'Insurance Payment', 'Coffee Shop', 'Bonus',
        'Monthly Salary', 'Grocery Store', 'Gym Membership', 'Dining Out', 'Coffee Shop', 'Consultant Fee'
    ],
    'category': [
        'Salary', 'Groceries', 'Dining', 'Utilities', 'Transport', 'Income',
        'Groceries', 'Dining', 'Salary', 'Shopping', 'Utilities', 'Transport',
        'Salary', 'Groceries', 'Entertainment', 'Insurance', 'Dining', 'Income',
        'Salary', 'Groceries', 'Health', 'Dining', 'Dining', 'Income'
    ],
    'value': [
        3000.00, -120.50, -4.50, -85.00, -45.00, 500.00,
        -135.75, -62.30, 3000.00, -89.99, -55.00, -420.00,
        3000.00, -110.20, -25.00, -180.00, -5.50, 800.00,
        3000.00, -125.40, -50.00, -48.75, -6.00, 600.00
    ]
}

df = pd.DataFrame(data)
df.to_excel('data/sample_transactions.xlsx', index=False)
print('Sample Excel file created successfully at: data/sample_transactions.xlsx')
print(f'Total transactions: {len(df)}')
print(f'Date range: {df["date"].min()} to {df["date"].max()}')
