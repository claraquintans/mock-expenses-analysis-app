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
