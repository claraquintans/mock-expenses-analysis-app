"""
Financial Metrics Calculations

This module provides functions for calculating summary financial metrics
across all transactions, including average savings and best/worst performing months.
"""

import pandas as pd


def calculate_financial_metrics(df: pd.DataFrame, monthly: pd.DataFrame) -> dict:
    """
    Calculate summary financial metrics across all transactions.
    
    Args:
        df (pd.DataFrame): All transactions with 'value' column
        monthly (pd.DataFrame): Monthly summary from calculate_monthly_summary()
                              Must have 'net_income' and 'month' columns
    
    Returns:
        dict: Financial metrics containing:
            - current_balance (float): Total balance (sum of all values)
            - average_monthly_savings (float): Average of monthly net income
            - best_month (dict): {'month': str, 'net_income': float}
            - worst_month (dict): {'month': str, 'net_income': float}
    
    Example:
        >>> df = pd.DataFrame({'value': [3000.0, -100.0, 500.0, -200.0]})
        >>> monthly = pd.DataFrame({
        ...     'month': pd.to_period(['2026-01', '2026-02']),
        ...     'net_income': [2900.0, 300.0]
        ... })
        >>> metrics = calculate_financial_metrics(df, monthly)
        >>> metrics['current_balance']
        3200.0
        >>> metrics['average_monthly_savings']
        1600.0
    """
    # Calculate current balance (sum of all transaction values)
    current_balance = df['value'].sum()
    
    # Calculate average monthly savings (average net income across all months)
    average_monthly_savings = monthly['net_income'].mean()
    
    # Find best month (highest net income)
    best_month_idx = monthly['net_income'].idxmax()
    best_month_value = monthly['net_income'].max()
    best_month_period = monthly.loc[best_month_idx, 'month']
    
    # Find worst month (lowest net income)
    worst_month_idx = monthly['net_income'].idxmin()
    worst_month_value = monthly['net_income'].min()
    worst_month_period = monthly.loc[worst_month_idx, 'month']
    
    # Format month names (e.g., "January 2026")
    best_month_name = best_month_period.strftime('%B %Y')
    worst_month_name = worst_month_period.strftime('%B %Y')
    
    return {
        'current_balance': current_balance,
        'average_monthly_savings': average_monthly_savings,
        'best_month': {
            'month': best_month_name,
            'net_income': best_month_value
        },
        'worst_month': {
            'month': worst_month_name,
            'net_income': worst_month_value
        }
    }
