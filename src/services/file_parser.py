"""
File Parser Service
Handles Excel file reading and validation for the expense analysis webapp.
"""

import pandas as pd
from typing import Any


def read_excel_file(uploaded_file: Any) -> pd.DataFrame:
    """
    Reads and parses an uploaded Excel file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object from st.file_uploader()
        
    Returns:
        pd.DataFrame: Raw DataFrame with data from Excel file
        
    Raises:
        Exception: If file cannot be read or is not valid Excel format
    """
    try:
        df = pd.read_excel(uploaded_file, header=0)
        return df
    except Exception as e:
        raise Exception(f"Failed to read Excel file: {str(e)}")


def validate_file(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates an uploaded Excel file's structure and data.
    
    Args:
        df (pd.DataFrame): Raw DataFrame loaded from Excel file
        
    Returns:
        pd.DataFrame: Validated and cleaned DataFrame with correct types
        
    Raises:
        ValueError: If file structure is invalid (wrong columns, missing data, invalid types)
        
    Validation Rules:
        1. DataFrame must have exactly 4 columns
        2. Columns must be named: ['date', 'description', 'category', 'value']
        3. 'date' column must contain valid dates (parseable by pandas)
        4. 'value' column must contain numeric data
        5. DataFrame must have at least one data row (beyond header)
    """
    # Check column count
    if len(df.columns) != 4:
        raise ValueError(f"File must have exactly 4 columns (found {len(df.columns)})")
    
    # Check column names
    expected_columns = ['date', 'description', 'category', 'value']
    actual_columns = df.columns.tolist()
    
    if actual_columns != expected_columns:
        raise ValueError(
            f"Columns must be: date, description, category, value (found: {', '.join(actual_columns)})"
        )
    
    # Check for empty file
    if len(df) == 0:
        raise ValueError("File is empty or contains only header row")
    
    # Validate date column
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception:
        raise ValueError("Invalid dates found in date column")
    
    # Validate value column
    try:
        df['value'] = pd.to_numeric(df['value'])
    except Exception:
        raise ValueError("Invalid numeric values found in value column")
    
    # Ensure description and category are strings
    df['description'] = df['description'].astype(str)
    df['category'] = df['category'].astype(str)
    
    return df
