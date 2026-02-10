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
from src.services.error_handler import display_error
from src.visualizations.kpi_cards import display_kpi_card
from src.visualizations.charts import create_income_expense_chart, create_category_breakdown_chart, create_rolling_average_chart


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
            
            # Calculate and display current balance
            st.subheader("Account Balance")
            balance = calculate_current_balance(df)
            
            # Display KPI card for balance
            col1, col2, col3 = st.columns(3)
            with col1:
                display_kpi_card("Current Balance", balance)
            
            # Calculate monthly summary
            monthly_summary = calculate_monthly_summary(df)
            
            # Display monthly income vs expenses chart (if data available)
            if not monthly_summary.empty:
                st.subheader("Monthly Income vs Expenses")
                
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
                st.subheader("Spending by Category")
                
                # Create and display the stacked bar chart
                fig_category = create_category_breakdown_chart(category_breakdown)
                st.plotly_chart(fig_category, use_container_width=True)
            else:
                st.info("📊 No expense data available for category breakdown. Upload transactions with expenses (negative values) to see category analysis.")
            
            # Calculate and display rolling average (User Story 4: P4)
            st.subheader("Spending Trends")
            
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
