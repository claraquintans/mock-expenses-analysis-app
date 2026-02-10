"""
Subcategory Classification Service

Classifies transactions into subcategories based on category and description.
Supports Food, Transportation, and Hobbies & Subscriptions categories.
"""

import pandas as pd
from typing import Dict


def classify_food_subcategory(description: str) -> str:
    """
    Classify food expenses into Groceries or Other Food Sources.
    
    Args:
        description (str): Transaction description
        
    Returns:
        str: 'Groceries' or 'Other Food Sources'
    """
    # Remove punctuation and special characters, convert to lowercase
    import re
    description_lower = re.sub(r'[^\w\s]', ' ', description.lower())
    
    # Keywords for groceries
    grocery_keywords = [
        'grocery', 'groceries', 'supermarket', 'market', 'store',
        'food store'
    ]
    
    # Check if description matches grocery keywords
    for keyword in grocery_keywords:
        if keyword in description_lower:
            return 'Groceries'
    
    # Default to Other Food Sources
    return 'Other Food Sources'


def classify_transportation_subcategory(description: str) -> str:
    """
    Classify transportation expenses into Public or Private Transportation.
    
    Args:
        description (str): Transaction description
        
    Returns:
        str: 'Public Transportation' or 'Private Transportation'
    """
    # Remove punctuation and special characters, convert to lowercase
    import re
    description_lower = re.sub(r'[^\w\s]', ' ', description.lower())
    
    # Keywords for public transportation
    public_transport_keywords = [
        'bus', 'metro', 'subway', 'train', 'tram', 'transit',
        'rail', 'metro card', 'transit pass', 'public transport',
        'rail pass'
    ]
    
    # Check if description matches public transport keywords
    for keyword in public_transport_keywords:
        if keyword in description_lower:
            return 'Public Transportation'
    
    # Default to Private Transportation
    return 'Private Transportation'


def classify_hobbies_subcategory(description: str) -> str:
    """
    Classify hobbies & subscriptions into recognizable types.
    
    Args:
        description (str): Transaction description
        
    Returns:
        str: Subscription type (streaming, fitness, gaming, educational, books, etc.)
    """
    # Remove punctuation and special characters, convert to lowercase
    import re
    description_lower = re.sub(r'[^\w\s]', ' ', description.lower())
    
    # Define subcategories with keywords
    subcategory_keywords = {
        'Streaming': [
            'streaming', 'music subscription', 'video subscription'
        ],
        'Fitness': [
            'gym', 'fitness', 'yoga', 'pilates', 'crossfit',
            'workout', 'health club', 'sports club'
        ],
        'Gaming': [
            'game pass', 'gaming', 'game subscription', 'video game'
        ],
        'Educational': [
            'online course', 'learning', 'education', 'course'
        ],
        'Books': [
            'book', 'books', 'reading', 'audiobook', 'ebook', 'magazine'
        ],
        'News & Media': [
            'news', 'newspaper', 'publication'
        ],
        'Professional': [
            'creative cloud', 'workspace', 'cloud storage', 'productivity'
        ]
    }
    
    # Check for matching subcategory
    for subcategory, keywords in subcategory_keywords.items():
        for keyword in keywords:
            if keyword in description_lower:
                return subcategory
    
    # Default to 'Other Subscriptions'
    return 'Other Subscriptions'


def add_subcategory_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a subcategory column to the transactions DataFrame.
    
    Args:
        df (pd.DataFrame): Transactions DataFrame with 'category' and 'description' columns
        
    Returns:
        pd.DataFrame: DataFrame with added 'subcategory' column
        
    Raises:
        ValueError: If DataFrame is empty
    """
    if df.empty:
        raise ValueError("DataFrame cannot be empty")
    
    df_copy = df.copy()
    
    # Define category patterns to check
    food_patterns = ['food', 'groceries', 'dining']
    transport_patterns = ['transport']
    hobbies_patterns = ['hobbies', 'subscription', 'entertainment']
    
    def classify_row(row):
        category = row['category']
        description = row['description']
        
        # Handle variations in category names (case-insensitive)
        category_lower = category.lower()
        
        # Check if category matches food patterns
        if any(pattern in category_lower for pattern in food_patterns):
            return classify_food_subcategory(description)
        # Check if category matches transport patterns
        elif any(pattern in category_lower for pattern in transport_patterns):
            return classify_transportation_subcategory(description)
        # Check if category matches hobbies patterns
        elif any(pattern in category_lower for pattern in hobbies_patterns):
            return classify_hobbies_subcategory(description)
        else:
            # For other categories, use the category name as subcategory
            return category
    
    df_copy['subcategory'] = df_copy.apply(classify_row, axis=1)
    
    return df_copy


def calculate_subcategory_breakdown(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Calculate subcategory breakdown for a specific category.
    
    Args:
        df (pd.DataFrame): Transactions DataFrame with 'category', 'value', and 'subcategory' columns
        category (str): Category to analyze (case-insensitive)
        
    Returns:
        pd.DataFrame: DataFrame with columns:
            - subcategory (str): Subcategory name
            - amount (float): Absolute total spending
            - percentage (float): Percentage of category total (0-100)
            
    Raises:
        ValueError: If DataFrame is empty
    """
    if df.empty:
        raise ValueError("DataFrame cannot be empty")
    
    # Add subcategory if not present
    if 'subcategory' not in df.columns:
        df = add_subcategory_column(df)
    
    # Filter to expenses only (negative values) for the specified category
    # Case-insensitive category matching
    category_mask = df['category'].str.lower().str.contains(category.lower(), na=False)
    expenses = df[(df['value'] < 0) & category_mask].copy()
    
    if expenses.empty:
        return pd.DataFrame(columns=['subcategory', 'amount', 'percentage'])
    
    # Calculate absolute spending by subcategory
    expenses['abs_value'] = expenses['value'].abs()
    subcategory_totals = expenses.groupby('subcategory')['abs_value'].sum().reset_index()
    subcategory_totals.columns = ['subcategory', 'amount']
    
    # Calculate total for the category
    category_total = subcategory_totals['amount'].sum()
    
    # Calculate percentages
    if category_total > 0:
        subcategory_totals['percentage'] = (subcategory_totals['amount'] / category_total) * 100
    else:
        subcategory_totals['percentage'] = 0.0
    
    # Sort by amount descending
    subcategory_totals = subcategory_totals.sort_values('amount', ascending=False)
    
    return subcategory_totals


def get_all_category_breakdowns(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Get subcategory breakdowns for all categories in the DataFrame.
    
    Args:
        df (pd.DataFrame): Transactions DataFrame
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping category names to their subcategory breakdowns
        
    Raises:
        ValueError: If DataFrame is empty
    """
    if df.empty:
        raise ValueError("DataFrame cannot be empty")
    
    # Add subcategory column
    df_with_subcategory = add_subcategory_column(df)
    
    # Get all unique categories from the dataframe (expenses only)
    expenses = df_with_subcategory[df_with_subcategory['value'] < 0]
    unique_categories = expenses['category'].unique()
    
    breakdowns = {}
    
    for category in unique_categories:
        breakdown = calculate_subcategory_breakdown(df_with_subcategory, category)
        if not breakdown.empty:
            breakdowns[category] = breakdown
    
    return breakdowns
