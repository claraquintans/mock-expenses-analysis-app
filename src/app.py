"""
Expense Analysis Webapp

A Streamlit application for analyzing bank transaction data from Excel files.
Users can upload transaction files and view financial visualizations including
account balance, monthly trends, category breakdowns, and summary metrics.
"""

import streamlit as st
import pandas as pd

from src.services.file_parser import read_excel_file, validate_file
from src.services.calculations import calculate_current_balance, calculate_monthly_summary, calculate_category_breakdown, calculate_rolling_average
from src.services.metrics import calculate_financial_metrics
from src.services.error_handler import display_error
from src.services.subcategory_classifier import calculate_subcategory_breakdown, add_subcategory_column
from src.visualizations.kpi_cards import display_kpi_card, display_best_worst_months
from src.visualizations.charts import create_income_expense_chart, create_category_breakdown_chart, create_rolling_average_chart, create_subcategory_breakdown_chart


def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="Expense Analysis",
        page_icon="💰",
        layout="wide"
    )
    
    # Application title and description
    st.title("💰 Expense Analysis Webapp")
    st.markdown("""
    Upload your bank transaction Excel file to analyze your spending patterns,
    track income vs expenses, and gain insights into your financial health.
    """)
    
    # File uploader widget
    st.subheader("Upload Transaction Data")
    uploaded_file = st.file_uploader(
        "Choose an Excel file (.xlsx)",
        type=['xlsx'],
        help="File must contain 4 columns: date, description, category, value"
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = read_excel_file(uploaded_file)
            
            # Validate file structure
            df = validate_file(df)
            
            # Display success message
            st.success(f"✅ File uploaded successfully! {len(df)} transactions loaded.")
            
            # Calculate metrics upfront
            balance = calculate_current_balance(df)
            monthly_summary = calculate_monthly_summary(df)
            
            # Display overview KPI cards in a better layout
            st.subheader("📊 Financial Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                # Current balance with color coding
                delta_color = "normal" if balance >= 0 else "inverse"
                display_kpi_card("Current Balance", balance, delta_color=delta_color)
            with col2:
                if not monthly_summary.empty:
                    avg_income = monthly_summary['total_income'].mean()
                    display_kpi_card("Avg Monthly Income", avg_income)
            with col3:
                if not monthly_summary.empty:
                    avg_expenses = monthly_summary['total_expenses'].mean()
                    display_kpi_card("Avg Monthly Expenses", avg_expenses)
            
            # Display monthly income vs expenses chart (if data available)
            if not monthly_summary.empty:
                st.markdown("---")
                st.subheader("📈 Monthly Income vs Expenses")
                
                # Handle edge case: sparse data with missing months
                # The chart will show actual data points; gaps indicate missing months
                if len(monthly_summary) == 1:
                    st.info("📊 Only one month of data available. Upload more transactions to see trends over time.")
                
                # Create and display the chart
                fig = create_income_expense_chart(monthly_summary)
                st.plotly_chart(fig, use_container_width=True)
            
            # Calculate and display category breakdown
            category_breakdown = calculate_category_breakdown(df)
            
            if not category_breakdown.empty:
                st.markdown("---")
                st.subheader("🏷️ Spending by Category")
                
                # Create and display the stacked bar chart
                fig_category = create_category_breakdown_chart(category_breakdown)
                st.plotly_chart(fig_category, use_container_width=True)
            else:
                st.info("📊 No expense data available for category breakdown. Upload transactions with expenses (negative values) to see category analysis.")
            
            # Calculate and display rolling average (User Story 4: P4)
            st.markdown("---")
            st.subheader("📉 Spending Trends")
            
            # Calculate rolling average (filters to expenses only, window=3)
            rolling_avg = calculate_rolling_average(df, window=3)
            
            # Check if we have sufficient data (at least 3 months)
            if not rolling_avg.empty:
                # Create and display the rolling average chart
                fig_rolling = create_rolling_average_chart(rolling_avg)
                st.plotly_chart(fig_rolling, use_container_width=True)
            else:
                # Show message if less than 3 months of data available
                st.info("📊 Insufficient data for rolling average trend. Upload at least 3 months of expense transactions to see the 3-month rolling average.")
            
            # Calculate and display financial summary metrics (User Story 5: P5)
            if not monthly_summary.empty:
                st.markdown("---")
                st.subheader("💰 Financial Summary Metrics")
                
                # Calculate financial metrics
                metrics = calculate_financial_metrics(df, monthly_summary)
                
                # Display financial summary KPI cards in improved layout
                col1, col2 = st.columns(2)
                with col1:
                    # Average monthly savings with color coding
                    savings_delta = "normal" if metrics['average_monthly_savings'] >= 0 else "inverse"
                    display_kpi_card("Average Monthly Savings", metrics['average_monthly_savings'], delta_color=savings_delta)
                with col2:
                    # Total transactions count
                    display_kpi_card("Total Transactions", len(df), format_currency=False)
                
                # Display best/worst month KPI cards
                st.markdown("####")
                display_best_worst_months(metrics['best_month'], metrics['worst_month'])
            
            # Category Breakdown Analysis Section
            st.markdown("---")
            st.subheader("📂 Category Breakdown Analysis")
            
            # Add subcategory column to the dataframe
            df_with_subcategory = add_subcategory_column(df)
            
            # Define categories to analyze
            categories_to_analyze = [
                ('Food', ['food', 'groceries', 'dining']),
                ('Transportation', ['transport']),
                ('Hobbies & Subscriptions', ['hobbies', 'subscription', 'entertainment'])
            ]
            
            # Create tabs for each category
            tabs = st.tabs([cat[0] for cat in categories_to_analyze])
            
            for idx, (category_name, category_keywords) in enumerate(categories_to_analyze):
                with tabs[idx]:
                    # Calculate subcategory breakdown for this category
                    breakdown = None
                    for keyword in category_keywords:
                        temp_breakdown = calculate_subcategory_breakdown(df_with_subcategory, keyword)
                        if not temp_breakdown.empty:
                            if breakdown is None:
                                breakdown = temp_breakdown
                            else:
                                # Merge if multiple keywords match
                                breakdown = pd.concat([breakdown, temp_breakdown]).groupby('subcategory').agg({
                                    'amount': 'sum'
                                }).reset_index()
                    
                    if breakdown is not None and not breakdown.empty:
                        # Calculate percentages after merging
                        total = breakdown['amount'].sum()
                        breakdown['percentage'] = (breakdown['amount'] / total) * 100
                        breakdown = breakdown.sort_values('amount', ascending=False)
                        
                        # Display summary metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Spending", f"${breakdown['amount'].sum():.2f}")
                        with col2:
                            st.metric("Number of Subcategories", len(breakdown))
                        
                        # Display breakdown chart
                        st.markdown("###")
                        fig = create_subcategory_breakdown_chart(breakdown, category_name)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display detailed breakdown table
                        st.markdown("#### Detailed Breakdown")
                        breakdown_display = breakdown.copy()
                        breakdown_display['amount'] = breakdown_display['amount'].apply(lambda x: f"${x:.2f}")
                        breakdown_display['percentage'] = breakdown_display['percentage'].apply(lambda x: f"{x:.1f}%")
                        breakdown_display.columns = ['Subcategory', 'Amount', 'Percentage']
                        st.dataframe(breakdown_display, use_container_width=True, hide_index=True)
                    else:
                        st.info("No data available for this category")
            
        except Exception as e:
            # Display error message if file processing fails
            display_error(str(e))
    
    else:
        # Show instructions when no file is uploaded
        st.info("👆 Upload an Excel file to get started")
        
        st.markdown("""
        ### File Format Requirements
        
        Your Excel file must contain the following columns:
        - **date**: Transaction date (YYYY-MM-DD format)
        - **description**: Transaction description
        - **category**: Category label (e.g., Groceries, Salary, Transport)
        - **value**: Transaction amount (positive for income, negative for expenses)
        
        ### Example Data
        
        | date       | description    | category   | value   |
        |------------|----------------|------------|---------|
        | 2026-01-15 | Grocery Store  | Groceries  | -120.50 |
        | 2026-01-30 | Monthly Salary | Salary     | 3000.00 |
        | 2026-02-03 | Coffee Shop    | Dining     | -4.50   |
        """)


if __name__ == "__main__":
    main()
