"""
Calculation functions for expense analysis.

This module provides core calculation logic for financial metrics,
monthly summaries, and aggregations.
"""

import pandas as pd


def calculate_current_balance(df: pd.DataFrame) -> float:
    """
    Calculate the current account balance from all transactions.
    
    Args:
        df (pd.DataFrame): Validated transactions DataFrame with 'value' column
        
    Returns:
        float: Sum of all transaction values (income - expenses)
        
    Example:
        >>> df = pd.DataFrame({'value': [3000.0, -100.0, -50.0, 500.0]})
        >>> calculate_current_balance(df)
        3350.0
    """
    if df.empty:
        return 0.0
    
    return float(df['value'].sum())


def calculate_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group transactions by month and calculate income/expense totals.
    
    Args:
        df (pd.DataFrame): Validated transactions with 'date' and 'value' columns
        
    Returns:
        pd.DataFrame: Monthly summary with columns:
            - month (period): Month identifier (e.g., Period('2026-01'))
            - total_income (float): Sum of positive values for the month
            - total_expenses (float): Absolute sum of negative values for the month
            - net_income (float): total_income - total_expenses
            
    Example:
        >>> df = pd.DataFrame({
        ...     'date': pd.to_datetime(['2026-01-15', '2026-01-30', '2026-02-05']),
        ...     'value': [-100.0, 3000.0, -50.0]
        ... })
        >>> monthly = calculate_monthly_summary(df)
        # Returns DataFrame:
        #   month     | total_income | total_expenses | net_income
        #   2026-01   | 3000.0       | 100.0          | 2900.0
        #   2026-02   | 0.0          | 50.0           | -50.0
    """
    if df.empty:
        return pd.DataFrame(columns=['month', 'total_income', 'total_expenses', 'net_income'])
    
    # Create a copy to avoid modifying the original
    df_copy = df.copy()
    
    # Extract month from date
    df_copy['month'] = df_copy['date'].dt.to_period('M')
    
    # Group by month and calculate aggregations
    monthly = df_copy.groupby('month').agg(
        total_income=('value', lambda x: x[x > 0].sum()),
        total_expenses=('value', lambda x: abs(x[x < 0].sum())),
        net_income=('value', 'sum')
    ).reset_index()
    
    return monthly


def calculate_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group expenses by month and category.
    
    Args:
        df (pd.DataFrame): Validated transactions with 'date', 'category', and 'value' columns
        
    Returns:
        pd.DataFrame: DataFrame with columns:
            - month (period): Month identifier
            - category (str): Category name
            - spending (float): Absolute value of expenses for that month/category
            
    Example:
        >>> df = pd.DataFrame({
        ...     'date': pd.to_datetime(['2026-01-15', '2026-01-20', '2026-02-05']),
        ...     'category': ['Groceries', 'Dining', 'Groceries'],
        ...     'value': [-100.0, -50.0, -75.0]
        ... })
        >>> breakdown = calculate_category_breakdown(df)
        # Returns:
        #   month, category  | spending
        #   2026-01, Groceries | 100.0
        #   2026-01, Dining    | 50.0
        #   2026-02, Groceries | 75.0
    """
    if df.empty:
        return pd.DataFrame(columns=['month', 'category', 'spending'])
    
    # Filter to expenses only (negative values)
    expenses = df[df['value'] < 0].copy()
    
    if expenses.empty:
        return pd.DataFrame(columns=['month', 'category', 'spending'])
    
    # Extract month from date
    expenses['month'] = expenses['date'].dt.to_period('M')
    
    # Take absolute value of expenses
    expenses['spending'] = expenses['value'].abs()
    
    # Group by month and category
    breakdown = expenses.groupby(['month', 'category']).agg(
        spending=('spending', 'sum')
    ).reset_index()
    
    return breakdown
