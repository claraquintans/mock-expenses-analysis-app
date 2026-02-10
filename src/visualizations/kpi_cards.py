"""
KPI card visualization components.

This module provides functions to display financial metrics
as KPI (Key Performance Indicator) cards in the Streamlit UI.
"""

import streamlit as st


def display_kpi_card(title: str, value: float, format_currency: bool = True) -> None:
    """
    Display a KPI card with a title and value.
    
    Args:
        title (str): The title/label for the KPI card
        value (float): The numeric value to display
        format_currency (bool): Whether to format the value as currency (default: True)
        
    Example:
        >>> display_kpi_card("Current Balance", 3350.0)
        # Displays a metric card showing "Current Balance: $3,350.00"
        
        >>> display_kpi_card("Total Transactions", 125, format_currency=False)
        # Displays a metric card showing "Total Transactions: 125"
    """
    if format_currency:
        formatted_value = f"${value:,.2f}"
    else:
        formatted_value = f"{value:,.0f}"
    
    st.metric(label=title, value=formatted_value)
