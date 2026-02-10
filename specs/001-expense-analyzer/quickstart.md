# Quickstart Guide: Expense Analysis Webapp

**Feature**: 001-expense-analyzer  
**Date**: 2026-02-10  
**For**: Developers setting up and running the application

## Prerequisites

- **Python**: Version 3.10 or higher
- **pip**: Python package manager
- **Excel Files**: Sample .xlsx files for testing (optional)

## Installation

### 1. Clone Repository (if applicable)

```bash
cd /path/to/mock-expenses-analysis-app
```

### 2. Create Virtual Environment (Recommended)

**On Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected dependencies** (see `requirements.txt`):
```
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
plotly>=5.17.0
```

**Development dependencies** (optional):
```bash
pip install pytest pytest-cov black ruff
```

---

## Running the Application

### Start Streamlit App

From the repository root:

```bash
streamlit run src/app.py
```

This will:
1. Start a local web server (typically at `http://localhost:8501`)
2. Automatically open the app in your default browser
3. Display the Expense Analysis webapp interface

### Stop the Application

Press `Ctrl+C` in the terminal where Streamlit is running.

---

## Using the Application

### Step 1: Prepare Excel File

Create or use an Excel file (.xlsx) with this structure:

**Required Format**:
- **4 columns** in this exact order:
  1. `date` - Transaction date (any standard date format)
  2. `description` - Text description of transaction
  3. `category` - Category label (e.g., "Groceries", "Salary")
  4. `value` - Numeric amount (positive = income, negative = expenses)
- **Header row** - First row with column names (any names, will be ignored)
- **Data rows** - Starting from row 2

**Example**:

| date       | description    | category   | value   |
|------------|----------------|------------|---------|
| 2026-01-15 | Grocery Store  | Groceries  | -120.50 |
| 2026-01-30 | Monthly Salary | Salary     | 3000.00 |
| 2026-02-05 | Coffee Shop    | Dining     | -4.50   |
| 2026-02-28 | Freelance Work | Income     | 500.00  |

### Step 2: Upload File

1. Open the webapp in your browser
2. Click "Browse files" or drag-and-drop your Excel file
3. Wait for processing (typically < 5 seconds)

### Step 3: View Visualizations

Once uploaded, you'll see:

1. **KPI Cards** (top section):
   - Current Account Balance
   - Average Monthly Savings
   - Best Month (highest net income)
   - Worst Month (lowest net income)

2. **Charts**:
   - Monthly Income vs Expenses (line chart)
   - Monthly Spending by Category (stacked bar chart)
   - 3-Month Rolling Spending Average (line chart)
     - Note: Requires at least 3 months of data

### Step 4: Upload New File

To analyze different data:
1. Upload a new Excel file
2. All visualizations will update automatically
3. Previous data is cleared (not persisted)

---

## Sample Data for Testing

Create a test file `sample_transactions.xlsx`:

```python
import pandas as pd

# Sample data
data = {
    'date': [
        '2026-01-05', '2026-01-15', '2026-01-30',
        '2026-02-03', '2026-02-14', '2026-02-28',
        '2026-03-05', '2026-03-20', '2026-03-31'
    ],
    'description': [
        'Coffee Shop', 'Grocery Store', 'Monthly Salary',
        'Restaurant', 'Online Shopping', 'Freelance Work',
        'Gas Station', 'Utility Bill', 'Monthly Salary'
    ],
    'category': [
        'Dining', 'Groceries', 'Salary',
        'Dining', 'Shopping', 'Income',
        'Transportation', 'Utilities', 'Salary'
    ],
    'value': [
        -4.50, -120.50, 3000.00,
        -45.00, -85.00, 500.00,
        -60.00, -150.00, 3000.00
    ]
}

df = pd.DataFrame(data)
df.to_excel('sample_transactions.xlsx', index=False)
```

Save this as a Python script and run to generate test data.

---

## Development Workflow

### Project Structure

```
mock-expenses-analysis-app/
├── src/
│   ├── app.py                    # Main Streamlit application
│   ├── models/                   # Data models (optional)
│   ├── services/                 # Business logic
│   │   ├── file_parser.py       # File upload & validation
│   │   ├── calculations.py      # Financial calculations
│   │   └── metrics.py           # Summary metrics
│   └── visualizations/           # Chart generation
│       └── charts.py            # Plotly chart functions
├── tests/
│   ├── unit/                     # Unit tests
│   └── integration/              # Integration tests
├── data/                         # Sample Excel files (gitignored)
├── requirements.txt
└── README.md
```

### Running Tests

**All tests**:
```bash
pytest
```

**With coverage**:
```bash
pytest --cov=src --cov-report=html
```

**Specific test file**:
```bash
pytest tests/unit/test_calculations.py
```

### Code Quality

**Format code with Black**:
```bash
black src/ tests/
```

**Lint with Ruff**:
```bash
ruff check src/ tests/
```

**Type checking** (optional):
```bash
mypy src/
```

---

## Troubleshooting

### Issue: "No module named 'streamlit'"

**Solution**: Ensure you've activated your virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "File validation failed: Invalid dates found"

**Solution**: 
- Check that your date column uses a standard format (YYYY-MM-DD, MM/DD/YYYY, etc.)
- Ensure there are no empty cells or non-date values in the date column

### Issue: "File must have exactly 4 columns"

**Solution**:
- Verify your Excel file has exactly 4 columns
- Remove any extra blank columns
- Ensure column order matches: date, description, category, value

### Issue: "Rolling average not displayed"

**Solution**:
- Rolling average requires at least 3 months of data
- Add more transactions spanning multiple months

### Issue: App runs slowly with large files

**Solution**:
- For mock/testing purposes, use smaller datasets (< 1000 transactions)
- If needed, add caching with `@st.cache_data` decorator in functions

---

## Configuration

### Streamlit Configuration (Optional)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
port = 8501
headless = false
```

### Environment Variables

None required for basic functionality.

---

## Deployment (Optional)

### Streamlit Cloud (Recommended for mock projects)

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository and branch
5. Specify main file: `src/app.py`
6. Deploy

### Local Production Mode

```bash
streamlit run src/app.py --server.headless true
```

---

## Next Steps

1. **Review Documentation**:
   - [specs/001-expense-analyzer/spec.md](spec.md) - Feature requirements
   - [specs/001-expense-analyzer/data-model.md](data-model.md) - Data structures
   - [specs/001-expense-analyzer/contracts/service-contracts.md](contracts/service-contracts.md) - Function interfaces

2. **Implement Core Features**:
   - Start with file validation and parsing
   - Add calculation functions
   - Create visualizations
   - Build Streamlit UI

3. **Write Tests**:
   - Unit tests for calculation functions
   - Integration tests for file processing pipeline

4. **Iterate and Improve**:
   - Test with various Excel files
   - Handle edge cases
   - Improve error messages
   - Enhance visualizations

---

## Helpful Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [pytest Documentation](https://docs.pytest.org)

---

## Support

For questions or issues:
- Review the spec documentation in `specs/001-expense-analyzer/`
- Check code comments and function docstrings
- Run tests to verify expected behavior

**Happy coding!** 🚀
