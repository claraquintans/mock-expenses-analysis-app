# Data Model: Expense Analysis Webapp

**Feature**: 001-expense-analyzer  
**Date**: 2026-02-10  
**Status**: Design

## Overview

This document defines the data entities and their relationships for the expense analysis application. Since the application does not persist data (in-memory processing only), these models represent the structure of data as it flows through the system from upload to visualization.

## Core Entities

### 1. Transaction

Represents a single financial transaction from the uploaded Excel file.

**Attributes**:
- `date` (datetime): The date when the transaction occurred
- `description` (str): Textual description of the transaction
- `category` (str): Classification label (e.g., "Groceries", "Salary", "Transport")
- `value` (float): Monetary amount - positive for income, negative for expenses

**Validation Rules**:
- `date`: Must be a valid date parseable by pandas `to_datetime()`
- `description`: String, can be empty but column must exist
- `category`: String, can be empty but column must exist
- `value`: Must be numeric (int or float)
- All four fields are required (columns must exist in Excel file)

**Source**: Directly parsed from Excel file (row 2 onwards, with row 1 as header)

**Data Structure** (pandas DataFrame):
```python
# Column names (header row)
columns = ['date', 'description', 'category', 'value']

# Example rows
# date        | description      | category    | value
# 2026-01-15  | Grocery Store    | Groceries   | -120.50
# 2026-01-30  | Monthly Salary   | Salary      | 3000.00
# 2026-02-03  | Coffee Shop      | Dining      | -4.50
```

**State Transitions**: 
- Uploaded → Validated → Processed → Aggregated → Visualized
- No modifications to original transaction data after validation

---

### 2. MonthlySummary

Represents aggregated financial data for a single calendar month.

**Attributes**:
- `month` (datetime or period): Month identifier (e.g., "2026-01" or Period('2026-01'))
- `total_income` (float): Sum of all positive values for the month
- `total_expenses` (float): Sum of absolute values of all negative values for the month
- `net_income` (float): `total_income - total_expenses` (can be negative if expenses exceed income)
- `category_breakdown` (dict[str, float]): Mapping of category names to total spending amount for that category

**Derivation Logic**:
```python
def calculate_monthly_summary(df):
    df['month'] = df['date'].dt.to_period('M')
    
    monthly = df.groupby('month').agg({
        'value': [
            ('total_income', lambda x: x[x > 0].sum()),
            ('total_expenses', lambda x: abs(x[x < 0].sum())),
            ('net_income', 'sum')
        ]
    })
    
    # Category breakdown (expenses only)
    expenses = df[df['value'] < 0].copy()
    expenses['value'] = expenses['value'].abs()
    category_breakdown = expenses.groupby(['month', 'category'])['value'].sum()
    
    return monthly, category_breakdown
```

**Validation Rules**:
- `total_income` ≥ 0 (sum of positive values)
- `total_expenses` ≥ 0 (absolute sum of negative values)
- `net_income` = `total_income - total_expenses` (can be positive or negative)
- `category_breakdown` contains only expense categories (no income categories)

**Usage**:
- Powers the "Monthly Income vs Expenses" line chart (FR-007)
- Powers the "Monthly Spending by Category" stacked bar chart (FR-008)
- Used to calculate best/worst months (FR-012, FR-013)

---

### 3. FinancialMetrics

Represents calculated summary statistics across all transactions.

**Attributes**:
- `current_balance` (float): Sum of all transaction values (income - expenses)
- `average_monthly_savings` (float): Average of monthly net income across all months
- `best_month` (dict): Contains `month` (str) and `net_income` (float) for the best performing month
- `worst_month` (dict): Contains `month` (str) and `net_income` (float) for the worst performing month

**Derivation Logic**:
```python
def calculate_financial_metrics(df, monthly_summary):
    metrics = {
        'current_balance': df['value'].sum(),
        'average_monthly_savings': monthly_summary['net_income'].mean(),
        'best_month': {
            'month': monthly_summary['net_income'].idxmax().strftime('%B %Y'),
            'net_income': monthly_summary['net_income'].max()
        },
        'worst_month': {
            'month': monthly_summary['net_income'].idxmin().strftime('%B %Y'),
            'net_income': monthly_summary['net_income'].min()
        }
    }
    return metrics
```

**Validation Rules**:
- `current_balance`: Can be any float value (positive, negative, or zero)
- `average_monthly_savings`: Can be any float value
- `best_month.net_income` ≥ `worst_month.net_income`
- Both `best_month` and `worst_month` must exist if there is at least one month of data

**Usage**:
- Displayed in KPI cards (FR-004, FR-011, FR-012, FR-013, FR-014)

---

### 4. RollingAverage

Represents the 3-month rolling average of expenses over time.

**Attributes**:
- `month` (datetime or period): Month identifier
- `rolling_avg_expenses` (float): Average of total expenses for current month and previous 2 months

**Derivation Logic**:
```python
def calculate_rolling_average(df, window=3):
    # Extract expenses only (negative values)
    expenses = df[df['value'] < 0].copy()
    expenses['value'] = expenses['value'].abs()
    
    # Group by month
    expenses['month'] = expenses['date'].dt.to_period('M')
    monthly_expenses = expenses.groupby('month')['value'].sum()
    
    # Calculate rolling average
    rolling_avg = monthly_expenses.rolling(window=window).mean()
    
    # Remove NaN values (first 2 months have insufficient data)
    return rolling_avg.dropna()
```

**Validation Rules**:
- `rolling_avg_expenses` ≥ 0 (average of absolute expense values)
- Requires at least 3 months of data to generate meaningful results
- Each point is the average of 3 consecutive months (current + previous 2)

**Edge Cases**:
- If less than 3 months of data exist, display a message indicating insufficient data (per spec FR-009)
- Sparse data (months with no transactions) should be handled as zero expenses for that month

**Usage**:
- Powers the "3-Month Rolling Spending Average" line chart (FR-010)

---

## Entity Relationships

```
Transaction (raw data)
    ↓ group by month
MonthlySummary
    ↓ aggregate across months
FinancialMetrics

Transaction (expenses only)
    ↓ rolling window
RollingAverage
```

**Flow**:
1. **Upload**: Excel file → DataFrame of Transactions
2. **Validation**: Check columns, types, and required fields
3. **Aggregation**: Transactions → MonthlySummary (grouped by month)
4. **Metrics Calculation**: MonthlySummary → FinancialMetrics
5. **Rolling Calculation**: Transactions → RollingAverage (expenses only)
6. **Visualization**: All entities rendered as charts and KPI cards

---

## Data Validation Schema

### Excel File Structure

**Required Format**:
- **File Type**: .xlsx (Excel 2007+)
- **Columns**: Exactly 4 columns in this order
  1. `date` (column A)
  2. `description` (column B)
  3. `category` (column C)
  4. `value` (column D)
- **Header Row**: First row contains column names (can be any names, ignored during parsing)
- **Data Rows**: Starting from row 2

**Validation Checks** (per FR-015):
1. File must be .xlsx format
2. Must have exactly 4 columns
3. Column order must match specification
4. `date` column must contain valid dates
5. `value` column must contain numeric data
6. File must not be empty (at least one data row beyond header)

**Error Handling**:
- Reject entire file if any validation fails
- Display clear error message indicating the issue
- Examples:
  - "File must have exactly 4 columns (found 3)"
  - "Invalid dates found in column 1"
  - "Column 4 must contain numeric values"
  - "File is empty or contains only header row"

---

## Sample Data

### Example Transactions DataFrame

```python
import pandas as pd

transactions = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-05', '2026-01-15', '2026-01-30', '2026-02-03', '2026-02-28']),
    'description': ['Coffee Shop', 'Grocery Store', 'Monthly Salary', 'Restaurant', 'Freelance Work'],
    'category': ['Dining', 'Groceries', 'Salary', 'Dining', 'Income'],
    'value': [-4.50, -120.50, 3000.00, -45.00, 500.00]
})
```

### Example MonthlySummary

```python
monthly_summary = pd.DataFrame({
    'month': pd.to_period(['2026-01', '2026-02']),
    'total_income': [3000.00, 500.00],
    'total_expenses': [125.00, 45.00],
    'net_income': [2875.00, 455.00]
})

category_breakdown = {
    ('2026-01', 'Dining'): 4.50,
    ('2026-01', 'Groceries'): 120.50,
    ('2026-02', 'Dining'): 45.00
}
```

### Example FinancialMetrics

```python
financial_metrics = {
    'current_balance': 3330.00,
    'average_monthly_savings': 1665.00,
    'best_month': {'month': 'January 2026', 'net_income': 2875.00},
    'worst_month': {'month': 'February 2026', 'net_income': 455.00}
}
```

### Example RollingAverage

```python
# Requires at least 3 months of data
rolling_avg = pd.Series({
    pd.Period('2026-03'): 58.17,  # Average of Jan (125), Feb (45), Mar (25) = 65
    pd.Period('2026-04'): 38.33,  # Average of Feb (45), Mar (25), Apr (35) = 35
    # ... continues for each month with ≥3 months history
})
```

---

## Implementation Notes

### Data Storage in Session

Since data is not persisted:
- Store validated DataFrame in Streamlit session state: `st.session_state['df']`
- Recalculate aggregations on each relevant UI interaction
- Clear session state when new file uploaded

### Performance Considerations

For typical datasets (few thousand rows):
- pandas operations are fast (<100ms)
- No caching needed initially
- If performance becomes an issue, use `@st.cache_data` on calculation functions

### Type Hints (Optional)

```python
from typing import Dict, Tuple
from pandas import DataFrame, Series

def calculate_monthly_summary(df: DataFrame) -> Tuple[DataFrame, Series]:
    """Calculate monthly financial summary."""
    pass

def calculate_financial_metrics(df: DataFrame, monthly: DataFrame) -> Dict[str, any]:
    """Calculate aggregate financial metrics."""
    pass
```

---

## Edge Cases & Handling

### Sparse Data
- **Issue**: Months with no transactions
- **Handling**: Include month in timeline with 0 values for income/expenses

### Single Month Data
- **Issue**: Cannot calculate meaningful rolling average
- **Handling**: Display message "At least 3 months of data required for rolling average"

### All Income or All Expenses
- **Issue**: No variety in transaction types
- **Handling**: Display charts with single line (only income or only expenses)

### Very Large Files
- **Issue**: Thousands of transactions may slow rendering
- **Handling**: pandas handles efficiently; optionally downsample charts if needed

### Invalid Dates
- **Issue**: Non-date values in date column
- **Handling**: Reject file with error "Invalid dates found in date column"

### Mixed Date Formats
- **Issue**: "2026-01-15" and "15/01/2026" in same file
- **Handling**: pandas `to_datetime()` handles most formats automatically; if parsing fails, reject file

---

## Conclusion

This data model provides a clear structure for processing and analyzing bank transaction data:
- **Transaction**: Raw input data from Excel
- **MonthlySummary**: Aggregated monthly financial data
- **FinancialMetrics**: Summary statistics across all transactions
- **RollingAverage**: Time-series smoothing for spending trends

All entities are derived from the uploaded Excel file and exist only in memory during the user's session. The model supports all required visualizations and metrics as specified in the feature requirements.
