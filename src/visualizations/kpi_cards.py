"""
KPI card visualization components.

This module provides functions to display financial metrics
as KPI (Key Performance Indicator) cards in the Streamlit UI.
"""

import streamlit as st


def display_kpi_card(title: str, value: float, format_currency: bool = True, delta_color: str = None) -> None:
    """
    Display a KPI card with a title and value.
    
    Args:
        title (str): The title/label for the KPI card
        value (float): The numeric value to display
        format_currency (bool): Whether to format the value as currency (default: True)
        delta_color (str): Optional color coding - "normal", "inverse", or "off" (default: None)
        
    Example:
        >>> display_kpi_card("Current Balance", 3350.0)
        # Displays a metric card showing "Current Balance: $3,350.00"
        
        >>> display_kpi_card("Total Transactions", 125, format_currency=False)
        # Displays a metric card showing "Total Transactions: 125"
    """
    # Get currency symbol from session state, default to '$'
    currency_symbol = st.session_state.get('currency_symbol', '$')
    
    if format_currency:
        formatted_value = f"{currency_symbol}{value:,.2f}"
    else:
        formatted_value = f"{value:,.0f}"
    
    # Determine delta for color coding (green for positive, red for negative)
    delta = None
    if delta_color and value != 0:
        # Use a small relative change to trigger color coding
        delta = value * 0.0001 if value > 0 else value * 0.0001
        
    st.metric(label=title, value=formatted_value, delta=delta, delta_color=delta_color or "normal")


def display_best_worst_months(best: dict, worst: dict) -> None:
    """
    Display KPI cards for best and worst performing months with color coding.
    
    Args:
        best (dict): Best month data with keys 'month' (str) and 'net_income' (float)
        worst (dict): Worst month data with keys 'month' (str) and 'net_income' (float)
        
    Example:
        >>> best = {'month': 'January 2026', 'net_income': 2900.0}
        >>> worst = {'month': 'February 2026', 'net_income': 300.0}
        >>> display_best_worst_months(best, worst)
        # Displays two metric cards side by side showing best and worst months
    """
    # Get currency symbol from session state, default to '$'
    currency_symbol = st.session_state.get('currency_symbol', '$')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Best month with positive delta for green color
        delta_value = best['net_income'] * 0.0001 if best['net_income'] > 0 else None
        st.metric(
            label=f"🏆 Best Month: {best['month']}",
            value=f"{currency_symbol}{best['net_income']:,.2f}",
            delta=delta_value,
            delta_color="normal"
        )
    
    with col2:
        # Worst month with negative delta for red color if net income is negative
        delta_value = worst['net_income'] * 0.0001 if worst['net_income'] < 0 else None
        st.metric(
            label=f"📉 Worst Month: {worst['month']}",
            value=f"{currency_symbol}{worst['net_income']:,.2f}",
            delta=delta_value,
            delta_color="inverse" if worst['net_income'] < 0 else "normal"
        )
