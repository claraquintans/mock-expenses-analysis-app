# Research: Expense Analysis Webapp

**Feature**: 001-expense-analyzer  
**Date**: 2026-02-10  
**Purpose**: Document technology choices and research findings for Python/Streamlit expense analysis application

## Technology Stack Decisions

### 1. Web Framework: Streamlit

**Decision**: Use Streamlit for the web application framework

**Rationale**:
- Designed specifically for data applications and analytics dashboards
- Minimal boilerplate - rapid prototyping with pure Python
- Built-in support for file uploads (`st.file_uploader`)
- Native integration with pandas DataFrames
- Automatic reactive UI updates when data changes
- No need for separate frontend/backend architecture
- Perfect fit for single-page data visualization apps
- Excellent for mock/research projects with fast iteration

**Alternatives Considered**:
- **Flask/FastAPI + React**: More complex, requires separate frontend/backend, overkill for this use case
- **Dash (Plotly)**: Similar to Streamlit but more verbose, steeper learning curve
- **Django**: Too heavy for a simple analytics dashboard without persistence

### 2. Data Processing: pandas

**Decision**: Use pandas for data manipulation and analysis

**Rationale**:
- Industry standard for tabular data in Python
- Excellent Excel file reading capabilities via `read_excel()`
- Powerful grouping and aggregation functions (`groupby`, `resample`)
- Built-in date parsing and time series operations
- Rolling window calculations (`rolling()`) for 3-month averages
- Natural integration with Streamlit (displays DataFrames beautifully)
- Large ecosystem and extensive documentation

**Alternatives Considered**:
- **Polars**: Faster but less mature ecosystem, unnecessary for mock project scale
- **Plain Python with csv/openpyxl**: Too low-level, reinventing the wheel
- **NumPy**: Lower-level, requires more manual work for data wrangling

### 3. Excel File Reading: openpyxl (via pandas)

**Decision**: Use pandas `read_excel()` with openpyxl engine

**Rationale**:
- pandas abstracts Excel reading complexity
- openpyxl is the default engine for .xlsx files in pandas
- Handles column selection and header row skipping automatically
- Robust date parsing with `parse_dates` parameter
- No need to directly interact with openpyxl API

**Alternatives Considered**:
- **xlrd**: Deprecated for .xlsx, only supports legacy .xls format
- **Direct openpyxl**: More control but unnecessary complexity
- **CSV conversion**: Requires user to convert files, poor UX

### 4. Visualization: Plotly

**Decision**: Use Plotly for interactive charts

**Rationale**:
- Native Streamlit support via `st.plotly_chart()`
- Interactive charts (hover, zoom, pan) out of the box
- Professional-looking visualizations with minimal code
- Excellent support for required chart types:
  - Line charts: `plotly.graph_objects.Scatter` for income/expenses and rolling average
  - Stacked bar charts: `plotly.graph_objects.Bar` with `barmode='stack'`
- Works well with pandas DataFrames
- Good documentation and examples

**Alternatives Considered**:
- **Matplotlib/Seaborn**: Static charts, less interactive, require more styling code
- **Altair**: More declarative but less feature-rich, smaller community
- **Streamlit native charts**: Limited customization, basic functionality only

### 5. File Validation Strategy

**Decision**: Fail-fast validation with clear error messages

**Rationale**:
- Per spec requirement FR-015: reject entire file on validation failure
- Check column count and order immediately after upload
- Validate data types before processing
- Use pandas built-in validation (e.g., `pd.to_datetime()` with `errors='coerce'`)
- Display errors using Streamlit's `st.error()` widget
- Simple approach suitable for mock project

**Implementation Approach**:
```python
def validate_file(df):
    # Check column count
    if len(df.columns) != 4:
        raise ValueError("File must have exactly 4 columns")
    
    # Check for required columns (assuming header row)
    expected = ["date", "description", "category", "value"]
    if list(df.columns) != expected:
        raise ValueError(f"Columns must be: {', '.join(expected)}")
    
    # Validate data types
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isna().any():
        raise ValueError("Invalid dates found")
    
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    if df['value'].isna().any():
        raise ValueError("Invalid numeric values found")
    
    return df
```

**Alternatives Considered**:
- **Pydantic models**: Overkill for simple DataFrame validation
- **Partial processing**: Violates spec requirement to reject entire file
- **Custom validation framework**: Unnecessary complexity

### 6. Testing Strategy

**Decision**: pytest with focused unit and integration tests

**Rationale**:
- pytest is the standard for Python testing
- Focus on critical business logic:
  - File validation
  - Balance calculation
  - Monthly aggregation
  - Rolling average computation
  - Best/worst month identification
- Use fixtures for sample DataFrames
- Mock file uploads for integration tests
- No need for extensive coverage in mock project (per constitution)

**Test Structure**:
```
tests/
├── unit/
│   ├── test_validation.py      # File validation logic
│   ├── test_calculations.py    # Balance, averages, best/worst month
│   └── test_aggregations.py    # Monthly grouping, rolling windows
└── integration/
    └── test_file_processing.py # End-to-end file upload to results
```

**Alternatives Considered**:
- **unittest**: More verbose, pytest is more pythonic
- **Integration tests with Selenium**: Overkill for Streamlit app in mock project
- **No tests**: Not recommended even for mock projects; basic tests aid development

### 7. Session State Management

**Decision**: Use Streamlit's session state for uploaded data

**Rationale**:
- Data is not persisted per spec assumption
- Each upload is a new analysis session
- Streamlit re-runs script on every interaction
- Need to store uploaded DataFrame in `st.session_state` to avoid re-processing
- Simple key-value storage: `st.session_state['df']`

**Implementation Pattern**:
```python
if uploaded_file is not None:
    if 'df' not in st.session_state or st.session_state.get('file_id') != uploaded_file.file_id:
        df = pd.read_excel(uploaded_file)
        df = validate_file(df)
        st.session_state['df'] = df
        st.session_state['file_id'] = uploaded_file.file_id
else:
    st.session_state.clear()
```

**Alternatives Considered**:
- **Database storage**: Not needed, violates spec (no persistence)
- **File system caching**: Unnecessary complexity
- **No state management**: Would cause performance issues with re-processing

## Best Practices & Patterns

### Data Flow Architecture

```
User Upload → Validation → DataFrame → Calculations → Visualizations
                ↓                           ↓              ↓
            st.error()              Session State    st.plotly_chart()
```

1. **Upload**: `st.file_uploader()` accepts .xlsx files
2. **Validation**: Check columns, parse dates, validate numeric values
3. **Processing**: Store validated DataFrame in session state
4. **Calculations**: Extract metrics (balance, monthly summaries, rolling avg)
5. **Display**: Render KPI cards and charts

### Code Organization

**Separation of Concerns**:
- `models/`: Data classes for Transaction, MonthlySummary, FinancialMetrics (optional, could use DataFrames directly)
- `services/file_parser.py`: File upload and validation logic
- `services/calculations.py`: Business logic for balance, aggregations, rolling averages
- `services/metrics.py`: Best/worst month, average savings calculations
- `visualizations/charts.py`: Plotly chart generation functions
- `app.py`: Main Streamlit UI orchestration

**Functional Style**:
- Pure functions where possible (input DataFrame → output result)
- Avoid global state except Streamlit session state
- Make functions testable in isolation

### Error Handling Patterns

**User-Friendly Errors**:
```python
try:
    df = validate_file(uploaded_df)
    st.session_state['df'] = df
    st.success("File uploaded successfully!")
except ValueError as e:
    st.error(f"❌ File validation failed: {str(e)}")
    st.info("Please ensure your Excel file has columns: date, description, category, value")
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")
```

### Performance Considerations

**For Typical Datasets** (few thousand transactions):
- pandas operations are fast enough (<1 second)
- No need for optimization in mock project
- Plotly rendering handles datasets well

**If Needed** (optional optimizations):
- Use `@st.cache_data` to cache calculation results
- Downsample very large datasets before charting
- Use `plotly` `scattergl` for large scatter plots

## Integration Patterns

### Streamlit + pandas Pattern

```python
import streamlit as st
import pandas as pd

st.title("Expense Analysis")

uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # Process...
    st.dataframe(df.head())
```

### Plotly Chart Generation

```python
import plotly.graph_objects as go

def create_monthly_income_expense_chart(monthly_df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['income'],
        name='Income',
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['expenses'],
        name='Expenses',
        mode='lines+markers'
    ))
    
    fig.update_layout(title='Monthly Income vs Expenses')
    return fig

# In Streamlit app
st.plotly_chart(fig, use_container_width=True)
```

### Rolling Average Calculation

```python
def calculate_rolling_average(df, window=3):
    # Group by month and sum expenses
    monthly = df[df['value'] < 0].groupby(
        pd.Grouper(key='date', freq='M')
    )['value'].sum().abs()
    
    # Calculate rolling average
    rolling_avg = monthly.rolling(window=window).mean()
    
    return rolling_avg.dropna()  # Remove NaN for first 2 months
```

## Open Questions Resolved

### Q1: Column Detection - By Name or Position?
**Resolution**: By position (per clarification in spec)
- Columns must be in exact order: date, description, category, value
- First row is header (skipped)
- Validation checks column count and order

### Q2: File Rejection Strategy?
**Resolution**: Reject entire file (per spec FR-015)
- No partial processing
- Display clear error message
- Allow user to upload corrected file

### Q3: Rolling Average - Expenses Only or Net?
**Resolution**: Expenses only (per clarification in spec)
- Use only negative values from value column
- Exclude income from calculation
- Take absolute value for display

### Q4: Header Row Handling?
**Resolution**: First row is header (per clarification in spec)
- Use `header=0` in `pd.read_excel()`
- Validate column names match expected
- Start data parsing from row 2

## Dependencies Summary

**Core Dependencies**:
```txt
streamlit>=1.28.0      # Web framework
pandas>=2.0.0          # Data processing
openpyxl>=3.1.0        # Excel file support
plotly>=5.17.0         # Interactive charts
```

**Development Dependencies**:
```txt
pytest>=7.4.0          # Testing framework
pytest-cov>=4.1.0      # Coverage reporting (optional)
black>=23.0.0          # Code formatting (optional)
ruff>=0.1.0            # Linting (optional)
```

**Python Version**: Python 3.10+ (for modern type hints and features)

## Deployment Considerations

**Local Development**:
```bash
streamlit run src/app.py
```

**Cloud Deployment** (optional for mock project):
- Streamlit Cloud (streamlit.io/cloud): Free tier, automatic from GitHub
- Heroku: Requires Procfile
- AWS/GCP/Azure: Containerize with Docker

**Environment Variables**: None required (no secrets, no persistence)

## Conclusion

This technology stack is well-suited for a Python/Streamlit expense analysis webapp:
- **Rapid development**: Streamlit enables quick prototyping
- **Robust data handling**: pandas provides powerful data manipulation
- **Interactive visualizations**: Plotly creates professional charts
- **Minimal complexity**: Single-page app with no persistence keeps it simple
- **Testable**: Clear separation of concerns enables effective testing
- **Appropriate for mock project**: Tools are proven, documentation is excellent

All technology choices align with the spec requirements and constitution guidance for mock/research projects.
