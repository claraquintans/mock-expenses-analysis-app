"""
Session Manager Service
Handles Streamlit session state management for the expense analysis webapp.
"""

import streamlit as st
from typing import Any, Optional


def init_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    
    Sets up the following session state keys:
    - 'uploaded_file': Stores the uploaded Excel file
    - 'df': Stores the validated DataFrame
    - 'file_processed': Boolean flag indicating if file has been processed
    """
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False


def get_session_value(key: str, default: Any = None) -> Any:
    """
    Safely retrieve a value from session state.
    
    Args:
        key (str): Session state key to retrieve
        default (Any): Default value if key doesn't exist
        
    Returns:
        Any: Value from session state or default value
    """
    return st.session_state.get(key, default)


def set_session_value(key: str, value: Any) -> None:
    """
    Set a value in session state.
    
    Args:
        key (str): Session state key to set
        value (Any): Value to store
    """
    st.session_state[key] = value


def clear_session() -> None:
    """
    Clear all session state data.
    
    Resets the application to its initial state by clearing all session variables.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Reinitialize default session state
    init_session_state()


def has_data() -> bool:
    """
    Check if there is processed data in session state.
    
    Returns:
        bool: True if DataFrame is loaded and processed, False otherwise
    """
    return (
        st.session_state.get('file_processed', False) and 
        st.session_state.get('df') is not None
    )
