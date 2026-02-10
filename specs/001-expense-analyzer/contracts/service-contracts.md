# Service Contracts: Expense Analysis Webapp

**Feature**: 001-expense-analyzer  
**Date**: 2026-02-10  
**Type**: Function/Service Interface Definitions

## Overview

Since this is a Streamlit application (not a REST API), contracts are defined as function interfaces that represent the core services. These contracts define the expected inputs, outputs, and behavior of key business logic functions.

## File Processing Contracts

### `validate_file(df: pd.DataFrame) -> pd.DataFrame`

Validates an uploaded Excel file's structure and data.

**Input**:
- `df` (pd.DataFrame): Raw DataFrame loaded from Excel file

**Output**:
- `pd.DataFrame`: Validated and cleaned DataFrame with correct types

**Raises**:
- `ValueError`: If file structure is invalid (wrong columns, missing data, invalid types)

**Validation Rules**:
1. DataFrame must have exactly 4 columns
2. Columns must be named: `['date', 'description', 'category', 'value']`
3. `date` column must contain valid dates (parseable by pandas)
4. `value` column must contain numeric data
5. DataFrame must have at least one data row (beyond header)

**Example**:
```python
# Valid input
df = pd.DataFrame({
    'date': ['2026-01-15', '2026-02-01'],
    'description': ['Groceries', 'Salary'],
    'category': ['Shopping', 'Income'],
    'value': [-100.0, 3000.0]
})

validated_df = validate_file(df)
# Returns DataFrame with:
# - date column as datetime64
# - value column as float64
# - All rows validated

# Invalid input
invalid_df = pd.DataFrame({'col1': [1], 'col2': [2]})
validate_file(invalid_df)  # Raises ValueError: "File must have exactly 4 columns"
```

**Error Messages**:
- `"File must have exactly 4 columns (found {n})"`
- `"Columns must be: date, description, category, value (found: {actual})"`
- `"Invalid dates found in date column"`
- `"Invalid numeric values found in value column"`
- `"File is empty or contains only header row"`

---

### `read_excel_file(uploaded_file: UploadedFile) -> pd.DataFrame`

Reads and parses an uploaded Excel file.

**Input**:
- `uploaded_file` (streamlit.UploadedFile): File object from `st.file_uploader()`

**Output**:
- `pd.DataFrame`: Raw DataFrame with data from Excel file

**Raises**:
- `Exception`: If file cannot be read or is not valid Excel format

**Behavior**:
- Uses `pd.read_excel()` with `header=0` to skip first row
- Reads all columns from the Excel file
- Does not perform validation (validation is separate step)

**Example**:
```python
uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
if uploaded_file:
    df = read_excel_file(uploaded_file)
    # Returns raw DataFrame, validation comes next
```

---

## Calculation Contracts

### `calculate_current_balance(df: pd.DataFrame) -> float`

Calculates the current account balance from all transactions.

**Input**:
- `df` (pd.DataFrame): Validated transactions DataFrame

**Output**:
- `float`: Sum of all transaction values (income - expenses)

**Preconditions**:
- `df` must have a `value` column with numeric data
- `df` must be validated (correct schema)

**Example**:
```python
df = pd.DataFrame({'value': [3000.0, -100.0, -50.0, 500.0]})
balance = calculate_current_balance(df)
# Returns: 3350.0
```

---

### `calculate_monthly_summary(df: pd.DataFrame) -> pd.DataFrame`

Groups transactions by month and calculates income/expense totals.

**Input**:
- `df` (pd.DataFrame): Validated transactions with `date` and `value` columns

**Output**:
- `pd.DataFrame`: Monthly summary with columns:
  - `month` (period): Month identifier (e.g., Period('2026-01'))
  - `total_income` (float): Sum of positive values for the month
  - `total_expenses` (float): Absolute sum of negative values for the month
  - `net_income` (float): total_income - total_expenses

**Preconditions**:
- `df` must have `date` column (datetime type)
- `df` must have `value` column (numeric type)

**Example**:
```python
df = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-15', '2026-01-30', '2026-02-05']),
    'value': [-100.0, 3000.0, -50.0]
})

monthly = calculate_monthly_summary(df)
# Returns DataFrame:
#   month     | total_income | total_expenses | net_income
#   2026-01   | 3000.0       | 100.0          | 2900.0
#   2026-02   | 0.0          | 50.0           | -50.0
```

---

### `calculate_category_breakdown(df: pd.DataFrame) -> pd.DataFrame`

Groups expenses by month and category.

**Input**:
- `df` (pd.DataFrame): Validated transactions with `date`, `category`, and `value` columns

**Output**:
- `pd.DataFrame`: Multi-index DataFrame with:
  - Index: (month, category)
  - Column: `spending` (float) - absolute value of expenses

**Behavior**:
- Filters to expenses only (value < 0)
- Takes absolute value of expenses
- Groups by month and category

**Example**:
```python
df = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-15', '2026-01-20', '2026-02-05']),
    'category': ['Groceries', 'Dining', 'Groceries'],
    'value': [-100.0, -50.0, -75.0]
})

breakdown = calculate_category_breakdown(df)
# Returns:
#   month, category  | spending
#   2026-01, Groceries | 100.0
#   2026-01, Dining    | 50.0
#   2026-02, Groceries | 75.0
```

---

### `calculate_rolling_average(df: pd.DataFrame, window: int = 3) -> pd.Series`

Calculates rolling average of monthly expenses.

**Input**:
- `df` (pd.DataFrame): Validated transactions with `date` and `value` columns
- `window` (int): Number of months for rolling window (default: 3)

**Output**:
- `pd.Series`: Rolling average of expenses indexed by month
  - Only includes months with sufficient history (≥ window size)

**Behavior**:
- Filters to expenses only (value < 0)
- Groups by month and sums expenses (as absolute values)
- Applies rolling window calculation
- Drops NaN values (first window-1 months)

**Example**:
```python
df = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-15', '2026-02-10', '2026-03-05', '2026-04-12']),
    'value': [-100.0, -200.0, -150.0, -180.0]
})

rolling = calculate_rolling_average(df, window=3)
# Returns Series:
#   2026-03 -> 150.0  (avg of 100, 200, 150)
#   2026-04 -> 176.67 (avg of 200, 150, 180)
# First 2 months omitted (insufficient data)
```

---

### `calculate_financial_metrics(df: pd.DataFrame, monthly: pd.DataFrame) -> dict`

Calculates summary metrics across all transactions.

**Input**:
- `df` (pd.DataFrame): All transactions
- `monthly` (pd.DataFrame): Monthly summary from `calculate_monthly_summary()`

**Output**:
- `dict`: Financial metrics with keys:
  - `current_balance` (float): Total balance
  - `average_monthly_savings` (float): Average of monthly net income
  - `best_month` (dict): `{'month': str, 'net_income': float}`
  - `worst_month` (dict): `{'month': str, 'net_income': float}`

**Preconditions**:
- `monthly` DataFrame must have `net_income` column
- At least one month of data must exist

**Example**:
```python
df = pd.DataFrame({'value': [3000.0, -100.0, 500.0, -200.0]})
monthly = pd.DataFrame({
    'month': pd.to_period(['2026-01', '2026-02']),
    'net_income': [2900.0, 300.0]
})

metrics = calculate_financial_metrics(df, monthly)
# Returns:
# {
#   'current_balance': 3200.0,
#   'average_monthly_savings': 1600.0,
#   'best_month': {'month': 'January 2026', 'net_income': 2900.0},
#   'worst_month': {'month': 'February 2026', 'net_income': 300.0}
# }
```

---

## Visualization Contracts

### `create_income_expense_chart(monthly: pd.DataFrame) -> go.Figure`

Creates a line chart showing monthly income vs expenses.

**Input**:
- `monthly` (pd.DataFrame): Monthly summary with `month`, `total_income`, `total_expenses`

**Output**:
- `plotly.graph_objects.Figure`: Interactive line chart

**Chart Specifications**:
- X-axis: Month (time series)
- Y-axis: Amount (currency)
- Two lines: Income (one color) and Expenses (another color)
- Markers at each data point
- Legend showing which line is which
- Title: "Monthly Income vs Expenses"

**Example**:
```python
monthly = pd.DataFrame({
    'month': pd.to_period(['2026-01', '2026-02', '2026-03']),
    'total_income': [3000, 3100, 2900],
    'total_expenses': [1200, 1100, 1300]
})

fig = create_income_expense_chart(monthly)
st.plotly_chart(fig, use_container_width=True)
```

---

### `create_category_breakdown_chart(breakdown: pd.DataFrame) -> go.Figure`

Creates a stacked bar chart showing spending by category per month.

**Input**:
- `breakdown` (pd.DataFrame): Category breakdown with multi-index (month, category)

**Output**:
- `plotly.graph_objects.Figure`: Stacked bar chart

**Chart Specifications**:
- X-axis: Month
- Y-axis: Total spending (currency)
- Stacked bars: Each category is a segment with distinct color
- Legend: Category names
- Title: "Monthly Spending by Category"

**Example**:
```python
breakdown = pd.DataFrame({
    'month': pd.to_period(['2026-01', '2026-01', '2026-02']),
    'category': ['Groceries', 'Dining', 'Groceries'],
    'spending': [100, 50, 75]
})

fig = create_category_breakdown_chart(breakdown)
st.plotly_chart(fig, use_container_width=True)
```

---

### `create_rolling_average_chart(rolling: pd.Series) -> go.Figure`

Creates a line chart showing the 3-month rolling average of expenses.

**Input**:
- `rolling` (pd.Series): Rolling average indexed by month

**Output**:
- `plotly.graph_objects.Figure`: Line chart

**Chart Specifications**:
- X-axis: Month
- Y-axis: Average spending (currency)
- Single line with markers
- Title: "3-Month Rolling Spending Average"
- Note if insufficient data (< 3 months)

**Example**:
```python
rolling = pd.Series({
    pd.Period('2026-03'): 150.0,
    pd.Period('2026-04'): 160.0,
    pd.Period('2026-05'): 155.0
})

fig = create_rolling_average_chart(rolling)
st.plotly_chart(fig, use_container_width=True)
```

---

## UI Component Contracts

### `display_kpi_card(title: str, value: float, format_currency: bool = True) -> None`

Displays a KPI metric card in Streamlit.

**Input**:
- `title` (str): Card title (e.g., "Current Balance")
- `value` (float): Numeric value to display
- `format_currency` (bool): Whether to format as currency (default: True)

**Output**:
- None (renders UI component in Streamlit)

**UI Specifications**:
- Large, prominent value display
- Title above or beside value
- Currency formatting if enabled (e.g., "$3,200.00")
- Color coding: green for positive, red for negative (optional)

**Example**:
```python
display_kpi_card("Current Balance", 3200.50, format_currency=True)
# Renders: "Current Balance: $3,200.50"

display_kpi_card("Average Savings", 1600.25, format_currency=True)
# Renders: "Average Savings: $1,600.25"
```

---

### `display_best_worst_months(best: dict, worst: dict) -> None`

Displays KPI cards for best and worst months.

**Input**:
- `best` (dict): `{'month': str, 'net_income': float}`
- `worst` (dict): `{'month': str, 'net_income': float}`

**Output**:
- None (renders UI components in Streamlit)

**UI Specifications**:
- Two cards side by side
- Best month: Title with month name, value with net income
- Worst month: Title with month name, value with net income
- Color: green for best, red for worst (optional)

**Example**:
```python
best = {'month': 'January 2026', 'net_income': 2900.0}
worst = {'month': 'February 2026', 'net_income': 300.0}

display_best_worst_months(best, worst)
# Renders:
#   [Best Month]          [Worst Month]
#   January 2026          February 2026
#   $2,900.00             $300.00
```

---

## Error Handling Contracts

### `handle_validation_error(error: ValueError) -> None`

Displays a user-friendly error message for validation failures.

**Input**:
- `error` (ValueError): Validation error from `validate_file()`

**Output**:
- None (renders error UI in Streamlit)

**UI Specifications**:
- Use `st.error()` for error message
- Display clear, actionable message
- Optionally show `st.info()` with guidance for fixing the issue

**Example**:
```python
try:
    df = validate_file(uploaded_df)
except ValueError as e:
    handle_validation_error(e)
    # Renders:
    # ❌ File validation failed: Invalid dates found in date column
    # ℹ️ Please ensure dates are in a valid format (YYYY-MM-DD, MM/DD/YYYY, etc.)
```

---

## Contract Testing

Each service function should have corresponding unit tests that verify:

1. **Happy Path**: Valid inputs produce expected outputs
2. **Edge Cases**: Boundary conditions are handled correctly
3. **Error Cases**: Invalid inputs raise appropriate exceptions
4. **Contract Adherence**: Output types and formats match specification

**Example Test Structure**:
```python
# tests/unit/test_calculations.py

def test_calculate_current_balance_positive():
    df = pd.DataFrame({'value': [1000.0, -200.0, 300.0]})
    assert calculate_current_balance(df) == 1100.0

def test_calculate_current_balance_negative():
    df = pd.DataFrame({'value': [-500.0, -300.0, 100.0]})
    assert calculate_current_balance(df) == -700.0

def test_calculate_current_balance_empty():
    df = pd.DataFrame({'value': []})
    assert calculate_current_balance(df) == 0.0
```

---

## Summary

These function contracts define the public interfaces for the expense analysis webapp:

- **File Processing**: Validation and parsing
- **Calculations**: Financial metrics and aggregations
- **Visualizations**: Chart generation
- **UI Components**: Display elements

All functions follow consistent patterns:
- Clear input/output types
- Explicit preconditions
- Well-defined error handling
- Testable interfaces

Implementation should strictly adhere to these contracts to ensure modularity and testability.
