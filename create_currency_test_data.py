"""
Script to create test Excel files with currency symbols for testing
"""
import pandas as pd

# Create sample transaction data with dollar currency symbols
data_dollar = {
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
        '$3000.00', '$-120.50', '$-4.50', '$-85.00', '$-45.00', '$500.00',
        '$-135.75', '$-62.30', '$3000.00', '$-89.99', '$-55.00', '$-420.00',
        '$3000.00', '$-110.20', '$-25.00', '$-180.00', '$-5.50', '$800.00',
        '$3000.00', '$-125.40', '$-50.00', '$-48.75', '$-6.00', '$600.00'
    ]
}

# Create sample transaction data with euro currency symbols
data_euro = {
    'date': [
        '2026-01-05', '2026-01-10', '2026-01-15', '2026-01-20', '2026-01-25', '2026-01-30',
        '2026-02-02', '2026-02-05', '2026-02-10', '2026-02-15', '2026-02-20', '2026-02-28'
    ],
    'description': [
        'Monthly Salary', 'Grocery Store', 'Coffee Shop', 'Electric Bill', 'Gas Station', 'Freelance Payment',
        'Grocery Store', 'Restaurant', 'Monthly Salary', 'Online Shopping', 'Phone Bill', 'Car Repair'
    ],
    'category': [
        'Salary', 'Groceries', 'Dining', 'Utilities', 'Transport', 'Income',
        'Groceries', 'Dining', 'Salary', 'Shopping', 'Utilities', 'Transport'
    ],
    'value': [
        '€2500.00', '€-95.50', '€-3.80', '€-72.00', '€-38.00', '€450.00',
        '€-115.00', '€-52.50', '€2500.00', '€-75.99', '€-48.00', '€-380.00'
    ]
}

# Create sample transaction data with pound currency symbols
data_pound = {
    'date': [
        '2026-01-05', '2026-01-10', '2026-01-15', '2026-01-20', '2026-01-25', '2026-01-30',
        '2026-02-02', '2026-02-05', '2026-02-10', '2026-02-15', '2026-02-20', '2026-02-28'
    ],
    'description': [
        'Monthly Salary', 'Grocery Store', 'Coffee Shop', 'Electric Bill', 'Gas Station', 'Freelance Payment',
        'Grocery Store', 'Restaurant', 'Monthly Salary', 'Online Shopping', 'Phone Bill', 'Car Repair'
    ],
    'category': [
        'Salary', 'Groceries', 'Dining', 'Utilities', 'Transport', 'Income',
        'Groceries', 'Dining', 'Salary', 'Shopping', 'Utilities', 'Transport'
    ],
    'value': [
        '£2200.00', '£-88.50', '£-3.50', '£-65.00', '£-35.00', '£400.00',
        '£-105.00', '£-48.50', '£2200.00', '£-68.99', '£-42.00', '£-350.00'
    ]
}

# Create sample transaction data with multiple currencies (should error)
data_mixed = {
    'date': [
        '2026-01-05', '2026-01-10', '2026-01-15', '2026-01-20'
    ],
    'description': [
        'Monthly Salary', 'Grocery Store', 'Coffee Shop', 'Electric Bill'
    ],
    'category': [
        'Salary', 'Groceries', 'Dining', 'Utilities'
    ],
    'value': [
        '$3000.00', '€-120.50', '£-4.50', '$-85.00'
    ]
}

# Create and save Excel files
df_dollar = pd.DataFrame(data_dollar)
df_dollar.to_excel('data/test_transactions_dollar.xlsx', index=False)
print('✅ Created: data/test_transactions_dollar.xlsx (with $ symbols)')

df_euro = pd.DataFrame(data_euro)
df_euro.to_excel('data/test_transactions_euro.xlsx', index=False)
print('✅ Created: data/test_transactions_euro.xlsx (with € symbols)')

df_pound = pd.DataFrame(data_pound)
df_pound.to_excel('data/test_transactions_pound.xlsx', index=False)
print('✅ Created: data/test_transactions_pound.xlsx (with £ symbols)')

df_mixed = pd.DataFrame(data_mixed)
df_mixed.to_excel('data/test_transactions_mixed.xlsx', index=False)
print('✅ Created: data/test_transactions_mixed.xlsx (with mixed currencies - should error)')

print('\nTest files created successfully!')
