"""
Chart generation functions for expense analysis visualizations.

This module provides Plotly chart creation functions for displaying
financial data in interactive visualizations.
"""

import pandas as pd
import plotly.graph_objects as go


def create_income_expense_chart(monthly: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing monthly income vs expenses.
    
    Args:
        monthly (pd.DataFrame): Monthly summary with columns:
            - month (period): Month identifier
            - total_income (float): Monthly income totals
            - total_expenses (float): Monthly expense totals
            
    Returns:
        plotly.graph_objects.Figure: Interactive line chart
        
    Chart Specifications:
        - X-axis: Month (time series)
        - Y-axis: Amount (currency)
        - Two lines: Income and Expenses
        - Markers at each data point
        - Legend showing line identification
        
    Example:
        >>> monthly = pd.DataFrame({
        ...     'month': pd.to_period(['2026-01', '2026-02', '2026-03']),
        ...     'total_income': [3000, 3100, 2900],
        ...     'total_expenses': [1200, 1100, 1300]
        ... })
        >>> fig = create_income_expense_chart(monthly)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    # Convert period to string for plotting
    monthly_copy = monthly.copy()
    monthly_copy['month_str'] = monthly_copy['month'].astype(str)
    
    # Create figure
    fig = go.Figure()
    
    # Add income line
    fig.add_trace(go.Scatter(
        x=monthly_copy['month_str'],
        y=monthly_copy['total_income'],
        mode='lines+markers',
        name='Income',
        line=dict(color='#10b981', width=2),
        marker=dict(size=8)
    ))
    
    # Add expenses line
    fig.add_trace(go.Scatter(
        x=monthly_copy['month_str'],
        y=monthly_copy['total_expenses'],
        mode='lines+markers',
        name='Expenses',
        line=dict(color='#ef4444', width=2),
        marker=dict(size=8)
    ))
    
    # Update layout
    fig.update_layout(
        title='Monthly Income vs Expenses',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig
