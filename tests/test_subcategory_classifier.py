"""
Unit tests for subcategory classification functionality.
"""

import pytest
import pandas as pd
from src.services.subcategory_classifier import (
    classify_food_subcategory,
    classify_transportation_subcategory,
    classify_hobbies_subcategory,
    add_subcategory_column,
    calculate_subcategory_breakdown
)


class TestFoodClassification:
    """Test food expense subcategory classification."""
    
    def test_grocery_classification(self):
        """Test that grocery stores are classified as Groceries."""
        assert classify_food_subcategory("Grocery Store") == "Groceries"
        assert classify_food_subcategory("Supermarket") == "Groceries"
        assert classify_food_subcategory("Food Store") == "Groceries"
        assert classify_food_subcategory("Market") == "Groceries"
    
    def test_dining_classification(self):
        """Test that restaurants are classified as Other Food Sources."""
        assert classify_food_subcategory("Restaurant") == "Other Food Sources"
        assert classify_food_subcategory("Cafe") == "Other Food Sources"
        assert classify_food_subcategory("Coffee Shop") == "Other Food Sources"
        assert classify_food_subcategory("Fast Food") == "Other Food Sources"


class TestTransportationClassification:
    """Test transportation expense subcategory classification."""
    
    def test_public_transport_classification(self):
        """Test that public transport is classified correctly."""
        assert classify_transportation_subcategory("Metro Transit Pass") == "Public Transportation"
        assert classify_transportation_subcategory("Bus Fare") == "Public Transportation"
        assert classify_transportation_subcategory("Train Ticket") == "Public Transportation"
        assert classify_transportation_subcategory("Subway Card") == "Public Transportation"
    
    def test_private_transport_classification(self):
        """Test that private transport is classified correctly."""
        assert classify_transportation_subcategory("Gas Station") == "Private Transportation"
        assert classify_transportation_subcategory("Uber Ride") == "Private Transportation"
        assert classify_transportation_subcategory("Parking Fee") == "Private Transportation"


class TestHobbiesClassification:
    """Test hobbies & subscriptions subcategory classification."""
    
    def test_streaming_classification(self):
        """Test that streaming services are classified correctly."""
        assert classify_hobbies_subcategory("Streaming Service") == "Streaming"
        assert classify_hobbies_subcategory("Music Subscription") == "Streaming"
        assert classify_hobbies_subcategory("Video Subscription") == "Streaming"
    
    def test_fitness_classification(self):
        """Test that fitness services are classified correctly."""
        assert classify_hobbies_subcategory("Gym Membership") == "Fitness"
        assert classify_hobbies_subcategory("Fitness Center") == "Fitness"
        assert classify_hobbies_subcategory("Yoga Studio") == "Fitness"
        assert classify_hobbies_subcategory("Workout Subscription") == "Fitness"
    
    def test_gaming_classification(self):
        """Test that gaming services are classified correctly."""
        assert classify_hobbies_subcategory("Game Pass") == "Gaming"
        assert classify_hobbies_subcategory("Gaming Subscription") == "Gaming"
        assert classify_hobbies_subcategory("Video Game") == "Gaming"
    
    def test_educational_classification(self):
        """Test that educational services are classified correctly."""
        assert classify_hobbies_subcategory("Online Course") == "Educational"
        assert classify_hobbies_subcategory("Learning Platform") == "Educational"
        assert classify_hobbies_subcategory("Education Subscription") == "Educational"
    
    def test_books_classification(self):
        """Test that books and reading services are classified correctly."""
        assert classify_hobbies_subcategory("Book Store") == "Books"
        assert classify_hobbies_subcategory("Audiobook Subscription") == "Books"
        assert classify_hobbies_subcategory("Ebook Purchase") == "Books"
        assert classify_hobbies_subcategory("Reading Subscription") == "Books"


class TestAddSubcategoryColumn:
    """Test adding subcategory column to DataFrame."""
    
    def test_add_subcategory_to_dataframe(self):
        """Test that subcategory column is added correctly."""
        df = pd.DataFrame({
            'description': ['Grocery Store', 'Metro Bus', 'Streaming Service'],
            'category': ['Groceries', 'Transport', 'Entertainment'],
            'value': [-100.0, -5.0, -15.99]
        })
        
        result = add_subcategory_column(df)
        
        assert 'subcategory' in result.columns
        assert len(result) == 3
        assert result.iloc[0]['subcategory'] == 'Groceries'
        assert result.iloc[1]['subcategory'] == 'Public Transportation'
        assert result.iloc[2]['subcategory'] == 'Streaming'
    
    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame(columns=['description', 'category', 'value'])
        
        with pytest.raises(ValueError, match="DataFrame cannot be empty"):
            add_subcategory_column(df)


class TestCalculateSubcategoryBreakdown:
    """Test subcategory breakdown calculations."""
    
    def test_food_category_breakdown(self):
        """Test food category breakdown with Groceries and Dining."""
        df = pd.DataFrame({
            'description': ['Grocery Store', 'Coffee Shop', 'Supermarket', 'Restaurant'],
            'category': ['Groceries', 'Dining', 'Groceries', 'Dining'],
            'value': [-100.0, -10.0, -150.0, -40.0],
            'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04'])
        })
        
        # Add subcategory first
        df = add_subcategory_column(df)
        
        # Calculate breakdown for food category (using 'groceries' to match both Groceries and Dining)
        groceries_breakdown = calculate_subcategory_breakdown(df, 'groceries')
        dining_breakdown = calculate_subcategory_breakdown(df, 'dining')
        
        # Combine
        combined = pd.concat([groceries_breakdown, dining_breakdown])
        combined_grouped = combined.groupby('subcategory').agg({'amount': 'sum'}).reset_index()
        total = combined_grouped['amount'].sum()
        combined_grouped['percentage'] = (combined_grouped['amount'] / total) * 100
        
        assert len(combined_grouped) == 2
        assert 'Groceries' in combined_grouped['subcategory'].values
        assert 'Other Food Sources' in combined_grouped['subcategory'].values
        
        # Check amounts
        groceries_row = combined_grouped[combined_grouped['subcategory'] == 'Groceries']
        other_food_row = combined_grouped[combined_grouped['subcategory'] == 'Other Food Sources']
        
        assert groceries_row['amount'].values[0] == 250.0
        assert other_food_row['amount'].values[0] == 50.0
        
        # Check percentages sum to 100
        assert abs(combined_grouped['percentage'].sum() - 100.0) < 0.01
    
    def test_transport_category_breakdown(self):
        """Test transportation category breakdown."""
        df = pd.DataFrame({
            'description': ['Metro Pass', 'Gas Station', 'Bus Fare', 'Uber'],
            'category': ['Transport', 'Transport', 'Transport', 'Transport'],
            'value': [-50.0, -60.0, -10.0, -30.0],
            'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04'])
        })
        
        df = add_subcategory_column(df)
        breakdown = calculate_subcategory_breakdown(df, 'transport')
        
        assert len(breakdown) == 2
        assert 'Public Transportation' in breakdown['subcategory'].values
        assert 'Private Transportation' in breakdown['subcategory'].values
        
        # Check percentages sum to 100
        assert abs(breakdown['percentage'].sum() - 100.0) < 0.01
    
    def test_empty_category(self):
        """Test handling of empty category."""
        df = pd.DataFrame({
            'description': ['Test'],
            'category': ['Other'],
            'value': [-100.0],
            'date': pd.to_datetime(['2026-01-01'])
        })
        
        df = add_subcategory_column(df)
        breakdown = calculate_subcategory_breakdown(df, 'nonexistent')
        
        assert len(breakdown) == 0
        assert list(breakdown.columns) == ['subcategory', 'amount', 'percentage']
    
    def test_percentages_and_amounts(self):
        """Test that amounts and percentages are calculated correctly."""
        df = pd.DataFrame({
            'description': ['Streaming Service', 'Music Subscription', 'Gym Membership'],
            'category': ['Entertainment', 'Entertainment', 'Entertainment'],
            'value': [-15.99, -9.99, -49.00],
            'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03'])
        })
        
        df = add_subcategory_column(df)
        breakdown = calculate_subcategory_breakdown(df, 'entertainment')
        
        # Check that breakdown has correct columns
        assert 'subcategory' in breakdown.columns
        assert 'amount' in breakdown.columns
        assert 'percentage' in breakdown.columns
        
        # Verify percentages sum to 100
        assert abs(breakdown['percentage'].sum() - 100.0) < 0.01
        
        # Verify total amount
        assert abs(breakdown['amount'].sum() - 74.98) < 0.01
    
    def test_empty_dataframe_error(self):
        """Test that empty DataFrame raises ValueError."""
        df = pd.DataFrame(columns=['description', 'category', 'value', 'date'])
        
        with pytest.raises(ValueError, match="DataFrame cannot be empty"):
            calculate_subcategory_breakdown(df, 'food')
