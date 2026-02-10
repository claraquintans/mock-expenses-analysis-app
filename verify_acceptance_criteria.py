"""
Acceptance Criteria Verification Script

This script verifies that all acceptance criteria from the problem statement are met.
"""

import pandas as pd
import sys
sys.path.insert(0, '/home/runner/work/mock-expenses-analysis-app/mock-expenses-analysis-app')

from src.services.file_parser import validate_file

print("=" * 80)
print("ACCEPTANCE CRITERIA VERIFICATION")
print("=" * 80)

# Acceptance Criteria 1: Single currency handling
print("\n📋 Acceptance Criterion 1:")
print("   GIVEN a user has an expense report with monetary values containing currency symbols")
print("   AND all values use the same currency symbol")
print("   WHEN the user uploads the file")
print("   THEN:")
print("   - Currency symbols should be automatically detected and removed for calculations")
print("   - The detected currency symbol should be stored")
print("   - All numerical analysis should work correctly")

print("\n   Testing with dollar currency file...")
try:
    df = pd.read_excel('data/test_transactions_dollar.xlsx')
    print(f"   ✓ Original values (first 3): {df['value'].head(3).tolist()}")
    
    validated_df, currency = validate_file(df)
    
    # Verify currency detected
    assert currency == '$', f"Expected '$', got {currency}"
    print(f"   ✅ Currency symbol detected: {currency}")
    
    # Verify symbols removed (values are now numeric)
    assert validated_df['value'].dtype == 'float64', "Values should be numeric"
    print(f"   ✅ Currency symbols stripped, values are numeric: {validated_df['value'].dtype}")
    
    # Verify values are correct after stripping
    expected_first_value = 3000.0
    actual_first_value = validated_df['value'].iloc[0]
    assert actual_first_value == expected_first_value, f"Expected {expected_first_value}, got {actual_first_value}"
    print(f"   ✅ Numeric values correct after stripping: {validated_df['value'].head(3).tolist()}")
    
    # Verify calculations work
    total = validated_df['value'].sum()
    print(f"   ✅ Numerical analysis works (total calculated): {total}")
    
    print("\n   ✅ Acceptance Criterion 1: PASSED")
    
except Exception as e:
    print(f"\n   ❌ Acceptance Criterion 1: FAILED - {e}")
    sys.exit(1)

# Acceptance Criteria 2: Multiple currency detection
print("\n📋 Acceptance Criterion 2:")
print("   GIVEN a user has an expense report with multiple different currency symbols")
print("   WHEN the user uploads the file")
print("   THEN:")
print("   - The application should detect the presence of multiple currencies")
print("   - An error message should be displayed")
print("   - The file should not be processed further")

print("\n   Testing with mixed currency file...")
try:
    df = pd.read_excel('data/test_transactions_mixed.xlsx')
    print(f"   ✓ File has mixed currencies: {df['value'].tolist()}")
    
    try:
        validated_df, currency = validate_file(df)
        print(f"\n   ❌ Acceptance Criterion 2: FAILED - File should have been rejected")
        sys.exit(1)
    except ValueError as e:
        error_message = str(e)
        expected_message = "Multiple currencies detected. Please ensure all values use the same currency."
        
        # Verify correct error message
        assert error_message == expected_message, f"Expected '{expected_message}', got '{error_message}'"
        print(f"   ✅ Multiple currencies detected")
        print(f"   ✅ Correct error message: '{error_message}'")
        print(f"   ✅ File processing stopped (exception raised)")
        
    print("\n   ✅ Acceptance Criterion 2: PASSED")
    
except AssertionError as e:
    print(f"\n   ❌ Acceptance Criterion 2: FAILED - {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n   ❌ Acceptance Criterion 2: FAILED - Unexpected error: {e}")
    sys.exit(1)

# Test with different currency types (Euro and Pound)
print("\n📋 Additional Verification:")
print("   Testing with Euro (€) currency...")
try:
    df = pd.read_excel('data/test_transactions_euro.xlsx')
    validated_df, currency = validate_file(df)
    assert currency == '€'
    assert validated_df['value'].dtype == 'float64'
    print(f"   ✅ Euro currency handled correctly: {currency}")
except Exception as e:
    print(f"   ❌ Euro test failed: {e}")
    sys.exit(1)

print("\n   Testing with Pound (£) currency...")
try:
    df = pd.read_excel('data/test_transactions_pound.xlsx')
    validated_df, currency = validate_file(df)
    assert currency == '£'
    assert validated_df['value'].dtype == 'float64'
    print(f"   ✅ Pound currency handled correctly: {currency}")
except Exception as e:
    print(f"   ❌ Pound test failed: {e}")
    sys.exit(1)

print("\n   Testing backward compatibility (no currency symbols)...")
try:
    df = pd.DataFrame({
        'date': ['2026-01-15', '2026-01-30'],
        'description': ['Test1', 'Test2'],
        'category': ['Cat1', 'Cat2'],
        'value': [100.50, -50.25]
    })
    validated_df, currency = validate_file(df)
    assert currency is None
    assert validated_df['value'].dtype == 'float64'
    print(f"   ✅ Files without currency still work (currency={currency})")
except Exception as e:
    print(f"   ❌ Backward compatibility test failed: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ ALL ACCEPTANCE CRITERIA VERIFIED SUCCESSFULLY")
print("=" * 80)
print("\nSummary:")
print("✓ Single currency detection and extraction works")
print("✓ Currency symbols stripped for calculations")
print("✓ Multiple currency detection works with correct error message")
print("✓ Multiple currencies tested ($, €, £)")
print("✓ Backward compatibility maintained (files without currency work)")
print("\n" + "=" * 80)
