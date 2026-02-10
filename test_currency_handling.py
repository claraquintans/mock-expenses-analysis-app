"""
Script to manually test currency handling functionality
"""
import pandas as pd
import sys
sys.path.insert(0, '/home/runner/work/mock-expenses-analysis-app/mock-expenses-analysis-app')

from src.services.file_parser import read_excel_file, validate_file

print("=" * 80)
print("TESTING CURRENCY SYMBOL HANDLING")
print("=" * 80)

# Test 1: File with dollar symbols
print("\n1. Testing file with DOLLAR currency symbols...")
try:
    df = pd.read_excel('data/test_transactions_dollar.xlsx')
    validated_df, currency = validate_file(df)
    print(f"   ✅ SUCCESS: Detected currency: {currency}")
    print(f"   ✅ First 3 values: {validated_df['value'].head(3).tolist()}")
    print(f"   ✅ Data types: {validated_df['value'].dtype}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 2: File with euro symbols
print("\n2. Testing file with EURO currency symbols...")
try:
    df = pd.read_excel('data/test_transactions_euro.xlsx')
    validated_df, currency = validate_file(df)
    print(f"   ✅ SUCCESS: Detected currency: {currency}")
    print(f"   ✅ First 3 values: {validated_df['value'].head(3).tolist()}")
    print(f"   ✅ Data types: {validated_df['value'].dtype}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 3: File with pound symbols
print("\n3. Testing file with POUND currency symbols...")
try:
    df = pd.read_excel('data/test_transactions_pound.xlsx')
    validated_df, currency = validate_file(df)
    print(f"   ✅ SUCCESS: Detected currency: {currency}")
    print(f"   ✅ First 3 values: {validated_df['value'].head(3).tolist()}")
    print(f"   ✅ Data types: {validated_df['value'].dtype}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 4: File with mixed currencies (should fail)
print("\n4. Testing file with MIXED currencies (should error)...")
try:
    df = pd.read_excel('data/test_transactions_mixed.xlsx')
    validated_df, currency = validate_file(df)
    print(f"   ❌ UNEXPECTED SUCCESS: This should have failed!")
except ValueError as e:
    if "Multiple currencies detected" in str(e):
        print(f"   ✅ SUCCESS: Correctly rejected with error: {e}")
    else:
        print(f"   ⚠️  PARTIAL: Got ValueError but wrong message: {e}")
except Exception as e:
    print(f"   ❌ FAILED with unexpected error: {e}")

# Test 5: File without currency symbols (original sample)
print("\n5. Testing original file WITHOUT currency symbols...")
try:
    # Create a simple test file without currency
    df = pd.DataFrame({
        'date': ['2026-01-15', '2026-01-30'],
        'description': ['Test1', 'Test2'],
        'category': ['Cat1', 'Cat2'],
        'value': [100.50, -50.25]
    })
    validated_df, currency = validate_file(df)
    print(f"   ✅ SUCCESS: Detected currency: {currency} (None expected)")
    print(f"   ✅ First 2 values: {validated_df['value'].tolist()}")
    print(f"   ✅ Data types: {validated_df['value'].dtype}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

print("\n" + "=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
