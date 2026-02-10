"""
Error Handler Service
Provides user-friendly error display utilities for the expense analysis webapp.
"""

import streamlit as st
from typing import Optional


def display_error(message: str, exception: Optional[Exception] = None) -> None:
    """
    Display a user-friendly error message in the Streamlit interface.
    
    Args:
        message (str): The error message to display to the user
        exception (Optional[Exception]): The underlying exception (for debugging)
    
    Example:
        >>> try:
        ...     validate_file(df)
        ... except ValueError as e:
        ...     display_error("Invalid file format", e)
    """
    st.error(f"❌ {message}")
    
    if exception and hasattr(st, 'expander'):
        with st.expander("Technical Details"):
            st.code(str(exception))


def display_warning(message: str) -> None:
    """
    Display a warning message in the Streamlit interface.
    
    Args:
        message (str): The warning message to display
    
    Example:
        >>> display_warning("File contains sparse data with missing months")
    """
    st.warning(f"⚠️ {message}")


def display_info(message: str) -> None:
    """
    Display an informational message in the Streamlit interface.
    
    Args:
        message (str): The info message to display
    
    Example:
        >>> display_info("Upload an Excel file to begin analysis")
    """
    st.info(f"ℹ️ {message}")


def display_success(message: str) -> None:
    """
    Display a success message in the Streamlit interface.
    
    Args:
        message (str): The success message to display
    
    Example:
        >>> display_success("File uploaded and validated successfully!")
    """
    st.success(f"✅ {message}")
