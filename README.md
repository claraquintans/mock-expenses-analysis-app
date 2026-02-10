# Expense Analysis Webapp

[![Board Status](https://dev.azure.com/cegid/bd3d2d9d-e39c-439d-8022-9b889701bed7/f91a9e37-cfc0-4d64-9218-8c31726ebec7/_apis/work/boardbadge/cb7e4f5c-4a1e-4b3e-bde5-d7b84290a467)](https://dev.azure.com/cegid/bd3d2d9d-e39c-439d-8022-9b889701bed7/_boards/board/t/f91a9e37-cfc0-4d64-9218-8c31726ebec7/Backlog%20items/)

A Python/Streamlit web application for analyzing personal bank transactions from Excel files. Upload your transaction data and get instant visualizations of your financial health including account balance, monthly trends, category breakdowns, and rolling averages.

## Features

- 📊 **Account Balance**: View current total balance across all transactions
- 📈 **Monthly Trends**: Compare income vs expenses over time with line charts
- 🏷️ **Category Breakdown**: Analyze spending by category with stacked bar charts
- 📉 **Rolling Averages**: Track 3-month rolling average of expenses
- 💰 **Financial Metrics**: See average savings, best month, and worst month KPIs

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Create virtual environment** (recommended):

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run src/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

### Using the App

1. **Prepare your Excel file** with these columns:
   - `date` - Transaction date
   - `description` - Transaction description
   - `category` - Category name (e.g., Groceries, Salary)
   - `value` - Amount (positive for income, negative for expenses)

2. **Upload** your Excel file using the file uploader

3. **View** your financial analysis instantly

## Sample Data

A sample Excel file is provided in `data/sample_transactions.xlsx` for testing.

## Project Structure

```
src/
├── models/              # Data models
├── services/            # Business logic (file parsing, calculations)
├── visualizations/      # Chart generation
└── app.py              # Main Streamlit application

tests/
├── unit/               # Unit tests
└── integration/        # Integration tests

data/                   # Sample data files (gitignored)
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Run linter
ruff check src/

# Format code
black src/
```

## Technical Stack

- **Framework**: Streamlit
- **Data Processing**: pandas
- **Excel Support**: openpyxl
- **Visualizations**: Plotly
- **Testing**: pytest

## Notes

This is a mock/research project for learning purposes. Data is processed in-memory and not persisted between sessions.
