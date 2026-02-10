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


def create_category_breakdown_chart(breakdown: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart showing monthly spending by category.
    
    Args:
        breakdown (pd.DataFrame): Category breakdown with columns:
            - month (period): Month identifier
            - category (str): Category name
            - spending (float): Expense amount for that month/category
            
    Returns:
        plotly.graph_objects.Figure: Interactive stacked bar chart
        
    Chart Specifications:
        - X-axis: Month (time series)
        - Y-axis: Amount (currency)
        - Bars: Stacked by category
        - Color-coded categories
        - Hover shows category and amount
        
    Example:
        >>> breakdown = pd.DataFrame({
        ...     'month': pd.to_period(['2026-01', '2026-01', '2026-02']),
        ...     'category': ['Groceries', 'Dining', 'Groceries'],
        ...     'spending': [100.0, 50.0, 75.0]
        ... })
        >>> fig = create_category_breakdown_chart(breakdown)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    if breakdown.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No expense data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Convert period to string for plotting
    breakdown_copy = breakdown.copy()
    breakdown_copy['month_str'] = breakdown_copy['month'].astype(str)
    
    # Get unique categories
    categories = breakdown_copy['category'].unique()
    
    # Create figure
    fig = go.Figure()
    
    # Add a bar trace for each category
    for category in categories:
        category_data = breakdown_copy[breakdown_copy['category'] == category]
        
        fig.add_trace(go.Bar(
            x=category_data['month_str'],
            y=category_data['spending'],
            name=category,
            text=category_data['spending'].apply(lambda x: f'${x:.2f}'),
            textposition='auto',
        ))
    
    # Update layout for stacked bars
    fig.update_layout(
        title='Monthly Spending by Category',
        xaxis_title='Month',
        yaxis_title='Spending ($)',
        barmode='stack',
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=50, r=150, t=80, b=50)
    )
    
    return fig


def create_rolling_average_chart(rolling: pd.Series) -> go.Figure:
    """
    Create a line chart showing the 3-month rolling average of expenses.
    
    Args:
        rolling (pd.Series): Rolling average indexed by month
        
    Returns:
        plotly.graph_objects.Figure: Line chart
        
    Chart Specifications:
        - X-axis: Month
        - Y-axis: Average spending (currency)
        - Single line with markers
        - Title: "3-Month Rolling Spending Average"
        
    Example:
        >>> rolling = pd.Series({
        ...     pd.Period('2026-03'): 150.0,
        ...     pd.Period('2026-04'): 160.0,
        ...     pd.Period('2026-05'): 155.0
        ... })
        >>> fig = create_rolling_average_chart(rolling)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    if rolling.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="Insufficient data for rolling average (need at least 3 months)",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Convert period index to string for plotting
    months_str = rolling.index.astype(str)
    
    # Create figure
    fig = go.Figure()
    
    # Add rolling average line
    fig.add_trace(go.Scatter(
        x=months_str,
        y=rolling.values,
        mode='lines+markers',
        name='3-Month Average',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=10),
        text=[f'${val:.2f}' for val in rolling.values],
        textposition='top center'
    ))
    
    # Update layout
    fig.update_layout(
        title='3-Month Rolling Spending Average',
        xaxis_title='Month',
        yaxis_title='Average Spending ($)',
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig
