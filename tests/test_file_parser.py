"""
Unit tests for file parser service with currency handling.
"""

import pytest
import pandas as pd
from src.services.file_parser import (
    detect_currency_symbol,
    strip_currency_symbols,
    validate_file
)


class TestCurrencyDetection:
    """Test currency symbol detection functionality."""
    
    def test_detect_dollar_sign(self):
        """Test detection of dollar sign currency."""
        values = pd.Series(['$100.50', '$250.75', '$89.99'])
        result = detect_currency_symbol(values)
        assert result == '$'
    
    def test_detect_euro_sign(self):
        """Test detection of euro currency."""
        values = pd.Series(['€100.50', '€250.75', '€89.99'])
        result = detect_currency_symbol(values)
        assert result == '€'
    
    def test_detect_pound_sign(self):
        """Test detection of pound currency."""
        values = pd.Series(['£100.50', '£250.75', '£89.99'])
        result = detect_currency_symbol(values)
        assert result == '£'
    
    def test_no_currency_detected(self):
        """Test when no currency symbols are present."""
        values = pd.Series(['100.50', '250.75', '89.99'])
        result = detect_currency_symbol(values)
        assert result is None
    
    def test_mixed_values_with_currency(self):
        """Test detection when some values have currency and some don't."""
        values = pd.Series(['$100.50', '250.75', '$89.99'])
        result = detect_currency_symbol(values)
        assert result == '$'
    
    def test_multiple_currencies_raises_error(self):
        """Test that multiple currencies raise a ValueError."""
        values = pd.Series(['$100.50', '€75.00', '£50.25'])
        with pytest.raises(ValueError, match="Multiple currencies detected"):
            detect_currency_symbol(values)
    
    def test_negative_values_with_currency(self):
        """Test detection with negative values."""
        values = pd.Series(['-$100.50', '-$250.75', '$89.99'])
        result = detect_currency_symbol(values)
        assert result == '$'


class TestCurrencyStripping:
    """Test currency symbol stripping functionality."""
    
    def test_strip_dollar_signs(self):
        """Test stripping dollar signs."""
        values = pd.Series(['$100.50', '$250.75', '$89.99'])
        result = strip_currency_symbols(values)
        expected = pd.Series(['100.50', '250.75', '89.99'])
        pd.testing.assert_series_equal(result, expected)
    
    def test_strip_euro_signs(self):
        """Test stripping euro signs."""
        values = pd.Series(['€100.50', '€250.75', '€89.99'])
        result = strip_currency_symbols(values)
        expected = pd.Series(['100.50', '250.75', '89.99'])
        pd.testing.assert_series_equal(result, expected)
    
    def test_strip_pound_signs(self):
        """Test stripping pound signs."""
        values = pd.Series(['£100.50', '£250.75', '£89.99'])
        result = strip_currency_symbols(values)
        expected = pd.Series(['100.50', '250.75', '89.99'])
        pd.testing.assert_series_equal(result, expected)
    
    def test_strip_with_spaces(self):
        """Test stripping currency symbols with spaces."""
        values = pd.Series(['$ 100.50', '$ 250.75', '$ 89.99'])
        result = strip_currency_symbols(values)
        expected = pd.Series(['100.50', '250.75', '89.99'])
        pd.testing.assert_series_equal(result, expected)
    
    def test_strip_negative_values(self):
        """Test stripping with negative values."""
        values = pd.Series(['-$100.50', '-$250.75', '$89.99'])
        result = strip_currency_symbols(values)
        expected = pd.Series(['-100.50', '-250.75', '89.99'])
        pd.testing.assert_series_equal(result, expected)
    
    def test_strip_no_currency(self):
        """Test stripping when no currency symbols present."""
        values = pd.Series(['100.50', '250.75', '89.99'])
        result = strip_currency_symbols(values)
        expected = pd.Series(['100.50', '250.75', '89.99'])
        pd.testing.assert_series_equal(result, expected)


class TestValidateFileWithCurrency:
    """Test file validation with currency symbol handling."""
    
    def test_validate_file_with_dollar_currency(self):
        """Test validation of file with dollar currency symbols."""
        df = pd.DataFrame({
            'date': ['2026-01-15', '2026-01-30', '2026-02-03'],
            'description': ['Grocery Store', 'Monthly Salary', 'Coffee Shop'],
            'category': ['Groceries', 'Salary', 'Dining'],
            'value': ['$-120.50', '$3000.00', '$-4.50']
        })
        
        result_df, currency_symbol = validate_file(df)
        
        assert currency_symbol == '$'
        assert len(result_df) == 3
        assert result_df['value'].dtype == 'float64'
        assert result_df['value'].iloc[0] == -120.50
        assert result_df['value'].iloc[1] == 3000.00
        assert result_df['value'].iloc[2] == -4.50
    
    def test_validate_file_with_euro_currency(self):
        """Test validation of file with euro currency symbols."""
        df = pd.DataFrame({
            'date': ['2026-01-15', '2026-01-30', '2026-02-03'],
            'description': ['Grocery Store', 'Monthly Salary', 'Coffee Shop'],
            'category': ['Groceries', 'Salary', 'Dining'],
            'value': ['€-120.50', '€3000.00', '€-4.50']
        })
        
        result_df, currency_symbol = validate_file(df)
        
        assert currency_symbol == '€'
        assert len(result_df) == 3
        assert result_df['value'].dtype == 'float64'
    
    def test_validate_file_with_pound_currency(self):
        """Test validation of file with pound currency symbols."""
        df = pd.DataFrame({
            'date': ['2026-01-15', '2026-01-30', '2026-02-03'],
            'description': ['Grocery Store', 'Monthly Salary', 'Coffee Shop'],
            'category': ['Groceries', 'Salary', 'Dining'],
            'value': ['£-120.50', '£3000.00', '£-4.50']
        })
        
        result_df, currency_symbol = validate_file(df)
        
        assert currency_symbol == '£'
        assert len(result_df) == 3
        assert result_df['value'].dtype == 'float64'
    
    def test_validate_file_without_currency(self):
        """Test validation of file without currency symbols."""
        df = pd.DataFrame({
            'date': ['2026-01-15', '2026-01-30', '2026-02-03'],
            'description': ['Grocery Store', 'Monthly Salary', 'Coffee Shop'],
            'category': ['Groceries', 'Salary', 'Dining'],
            'value': [-120.50, 3000.00, -4.50]
        })
        
        result_df, currency_symbol = validate_file(df)
        
        assert currency_symbol is None
        assert len(result_df) == 3
        assert result_df['value'].dtype == 'float64'
    
    def test_validate_file_multiple_currencies_error(self):
        """Test that multiple currencies in file raises ValueError."""
        df = pd.DataFrame({
            'date': ['2026-01-15', '2026-01-30', '2026-02-03'],
            'description': ['Grocery Store', 'Monthly Salary', 'Coffee Shop'],
            'category': ['Groceries', 'Salary', 'Dining'],
            'value': ['$-120.50', '€3000.00', '£-4.50']
        })
        
        with pytest.raises(ValueError, match="Multiple currencies detected"):
            validate_file(df)
    
    def test_validate_file_preserves_validation_rules(self):
        """Test that currency handling doesn't break existing validation."""
        # Test wrong column count
        df = pd.DataFrame({
            'date': ['2026-01-15'],
            'description': ['Test'],
            'value': ['$100.00']
        })
        
        with pytest.raises(ValueError, match="exactly 4 columns"):
            validate_file(df)
        
        # Test wrong column names
        df = pd.DataFrame({
            'date': ['2026-01-15'],
            'desc': ['Test'],
            'cat': ['Category'],
            'amount': ['$100.00']
        })
        
        with pytest.raises(ValueError, match="Columns must be"):
            validate_file(df)
        
        # Test empty file
        df = pd.DataFrame(columns=['date', 'description', 'category', 'value'])
        
        with pytest.raises(ValueError, match="empty"):
            validate_file(df)
        
        # Test invalid dates
        df = pd.DataFrame({
            'date': ['not-a-date', '2026-01-30'],
            'description': ['Test', 'Test2'],
            'category': ['Cat1', 'Cat2'],
            'value': ['$100.00', '$200.00']
        })
        
        with pytest.raises(ValueError, match="Invalid dates"):
            validate_file(df)
    
    def test_validate_file_invalid_values_after_stripping(self):
        """Test that invalid values still raise error after currency stripping."""
        df = pd.DataFrame({
            'date': ['2026-01-15', '2026-01-30'],
            'description': ['Test', 'Test2'],
            'category': ['Cat1', 'Cat2'],
            'value': ['$100.00', '$invalid']
        })
        
        with pytest.raises(ValueError, match="Invalid numeric values"):
            validate_file(df)
