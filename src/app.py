"""
Expense Analysis Webapp

A Streamlit application for analyzing bank transaction data from Excel files.
Users can upload transaction files and view financial visualizations including
account balance, monthly trends, category breakdowns, and summary metrics.
"""

import streamlit as st
import pandas as pd

from src.services.file_parser import read_excel_file, validate_file
from src.services.calculations import calculate_current_balance, calculate_monthly_summary
from src.services.error_handler import display_error
from src.visualizations.kpi_cards import display_kpi_card
from src.visualizations.charts import create_income_expense_chart


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
