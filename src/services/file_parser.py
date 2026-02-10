"""
File Parser Service
Handles Excel file reading and validation for the expense analysis webapp.
"""

import pandas as pd
import re
from typing import Any, Tuple, Optional


def detect_currency_symbol(value_series: pd.Series) -> Optional[str]:
    """
    Detects currency symbols in a pandas Series of values.
    
    Args:
        value_series: pandas Series containing monetary values
        
    Returns:
        Optional[str]: Detected currency symbol (e.g., '$', '€', '£') or None if no symbol found
        
    Raises:
        ValueError: If multiple different currency symbols are detected
    """
    # Common currency symbols to detect
    currency_pattern = r'[\$€£¥₹¢₽₩₪₱฿₴₦₨₡₲₵₸₺₼₾₿]'
    
    detected_currencies = set()
    
    # Convert to string and check each value for currency symbols
    for value in value_series.astype(str):
        matches = re.findall(currency_pattern, value)
        if matches:
            detected_currencies.update(matches)
    
    # If no currencies detected
    if not detected_currencies:
        return None
    
    # If multiple different currencies detected
    if len(detected_currencies) > 1:
        raise ValueError(
            "Multiple currencies detected. Please ensure all values use the same currency."
        )
    
    # Return the single detected currency
    return detected_currencies.pop()


def strip_currency_symbols(value_series: pd.Series) -> pd.Series:
    """
    Strips currency symbols from monetary values.
    
    Args:
        value_series: pandas Series containing monetary values with currency symbols
        
    Returns:
        pd.Series: Series with currency symbols removed
    """
    # Remove common currency symbols and any whitespace
    currency_pattern = r'[\$€£¥₹¢₽₩₪₱฿₴₦₨₡₲₵₸₺₼₾₿\s]'
    return value_series.astype(str).str.replace(currency_pattern, '', regex=True)


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


def validate_file(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Validates an uploaded Excel file's structure and data.
    
    Args:
        df (pd.DataFrame): Raw DataFrame loaded from Excel file
        
    Returns:
        Tuple[pd.DataFrame, Optional[str]]: Validated and cleaned DataFrame with correct types,
                                            and detected currency symbol (or None if no currency)
        
    Raises:
        ValueError: If file structure is invalid (wrong columns, missing data, invalid types, 
                    or multiple currencies detected)
        
    Validation Rules:
        1. DataFrame must have exactly 4 columns
        2. Columns must be named: ['date', 'description', 'category', 'value']
        3. 'date' column must contain valid dates (parseable by pandas)
        4. 'value' column must contain numeric data (after stripping currency symbols)
        5. DataFrame must have at least one data row (beyond header)
        6. Only one currency symbol type allowed per file
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
    
    # Detect currency symbol (before stripping)
    currency_symbol = detect_currency_symbol(df['value'])
    
    # Validate value column (strip currency symbols first if present)
    try:
        if currency_symbol:
            df['value'] = strip_currency_symbols(df['value'])
        df['value'] = pd.to_numeric(df['value'])
    except Exception:
        raise ValueError("Invalid numeric values found in value column")
    
    # Ensure description and category are strings
    df['description'] = df['description'].astype(str)
    df['category'] = df['category'].astype(str)
    
    return df, currency_symbol
