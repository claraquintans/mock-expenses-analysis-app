# Feature Specification: Expense Analysis Webapp

**Feature Branch**: `001-expense-analyzer`  
**Created**: February 10, 2026  
**Status**: Draft  
**Input**: User description: "Create a simple webapp to analyse bank transactions. 1. The app should use streamlit and python. 2. Users upload an excel file with fixed columns: date, description, category, and value. 3. App shows the following analysis: 1. KPI Card: Current account balance 2. Line chart: monthly income vs expenses 3. Stacked bar chart: monthly spend by category 4. Line chart: rolling 3-month spending average 5. KPI cards: average savings, best/worst month"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload and View Account Balance (Priority: P1)

A user wants to quickly check their current account balance by uploading their bank transaction data and immediately seeing their financial position.

**Why this priority**: This is the most fundamental feature - users need to know their current financial state. It provides immediate value with minimal complexity and serves as the foundation for all other analysis.

**Independent Test**: Can be fully tested by uploading a valid Excel file with transaction data and verifying that the current account balance KPI card displays the correct sum of all transaction values.

**Acceptance Scenarios**:

1. **Given** a user has an Excel file with transaction data, **When** they upload the file to the webapp, **Then** the system displays a KPI card showing the current account balance (sum of all transaction values)
2. **Given** a user uploads a file with both income (positive values) and expenses (negative values), **When** the balance is calculated, **Then** the balance reflects the net total (income minus expenses)
3. **Given** a user uploads a file, **When** the file is successfully processed, **Then** the balance KPI card appears prominently on the dashboard

---

### User Story 2 - Compare Monthly Income vs Expenses (Priority: P2)

A user wants to understand their monthly financial trends by viewing income and expenses over time to identify patterns and make informed decisions.

**Why this priority**: Understanding monthly trends is crucial for financial planning. This provides insight into whether the user is living within their means each month.

**Independent Test**: Can be fully tested by uploading transaction data spanning multiple months and verifying that the line chart correctly groups transactions by month, separates income from expenses, and displays both trends on the same chart.

**Acceptance Scenarios**:

1. **Given** a user has uploaded transaction data spanning multiple months, **When** they view the monthly analysis, **Then** they see a line chart with two lines: one for monthly income and one for monthly expenses
2. **Given** transaction data with dates in different months, **When** the chart is generated, **Then** transactions are correctly grouped by month (based on the date column)
3. **Given** transactions with positive values (income) and negative values (expenses), **When** displayed on the chart, **Then** income and expenses are shown as separate, clearly labeled lines
4. **Given** sparse data with some months having no transactions, **When** the chart is displayed, **Then** those months show zero or are appropriately handled

---

### User Story 3 - Analyze Spending by Category (Priority: P3)

A user wants to see how their spending is distributed across different categories each month to identify areas where they can reduce costs.

**Why this priority**: Category breakdown helps users identify spending patterns and make targeted improvements. It builds on the monthly expense data but provides deeper insight.

**Independent Test**: Can be fully tested by uploading categorized transaction data and verifying that the stacked bar chart groups expenses by month and shows the breakdown of categories for each month.

**Acceptance Scenarios**:

1. **Given** a user has uploaded transaction data with category labels, **When** they view the category analysis, **Then** they see a stacked bar chart showing monthly spending broken down by category
2. **Given** transactions with multiple categories (e.g., "Groceries", "Transport", "Entertainment"), **When** the chart is generated, **Then** each category is represented as a distinct color/segment in the stacked bars
3. **Given** expense transactions (negative values), **When** displayed in the chart, **Then** only expenses are included in the category breakdown (income is excluded)
4. **Given** a month with spending across multiple categories, **When** viewing the chart, **Then** the total bar height represents total monthly spending and segments show individual category contributions

---

### User Story 4 - Track Spending Trends with Rolling Average (Priority: P4)

A user wants to see their spending trend smoothed out over time to identify long-term patterns and avoid being misled by monthly fluctuations.

**Why this priority**: Rolling averages help users see the bigger picture beyond monthly volatility. This is valuable for users already familiar with their basic spending patterns.

**Independent Test**: Can be fully tested by uploading transaction data spanning at least 3 months and verifying that the line chart displays a 3-month rolling average of total spending.

**Acceptance Scenarios**:

1. **Given** a user has uploaded transaction data spanning at least 3 months, **When** they view the rolling average analysis, **Then** they see a line chart showing the 3-month rolling average of expenses (negative values only)
2. **Given** transaction data, **When** calculating the rolling average, **Then** each point represents the average total expenses over the current month and the previous 2 months
3. **Given** insufficient data (less than 3 months), **When** attempting to display the rolling average, **Then** the system either shows available data with a note or displays a message indicating more data is needed

---

### User Story 5 - View Financial Summary Metrics (Priority: P5)

A user wants to see key financial metrics at a glance, including average savings rate and best/worst performing months, to evaluate their overall financial health.

**Why this priority**: Summary metrics provide quick insights and motivation. They're valuable but depend on having sufficient historical data for meaningful analysis.

**Independent Test**: Can be fully tested by uploading transaction data spanning multiple months and verifying that KPI cards correctly display average savings, best month (highest net income), and worst month (lowest net income or highest net expense).

**Acceptance Scenarios**:

1. **Given** a user has uploaded multi-month transaction data, **When** summary metrics are calculated, **Then** a KPI card displays the average monthly savings (average of monthly income minus expenses)
2. **Given** transaction data spanning multiple months, **When** identifying the best month, **Then** a KPI card shows the month with the highest net income (total income minus total expenses for that month)
3. **Given** transaction data spanning multiple months, **When** identifying the worst month, **Then** a KPI card shows the month with the lowest net income or highest net loss
4. **Given** a user views the best/worst month KPI cards, **When** displayed, **Then** the month name and net amount are clearly shown

---

### Edge Cases

- What happens when a user uploads an Excel file with missing or empty columns (date, description, category, or value)?
- What happens when a user uploads an Excel file with incorrect column names or column order different from expected?
- What happens when transaction values are all positive or all negative (no income or no expenses)?
- What happens when the uploaded file contains only one month of data?
- What happens when date values are in different formats or invalid?
- What happens when category names contain special characters or are very long?
- What happens when numeric values in the value column are formatted as text?
- What happens when the Excel file is empty or contains only headers (no transaction data rows)?
- What happens when a user uploads a very large file (e.g., 10 years of daily transactions)?
- What happens when transaction dates are not in chronological order?

## Clarifications

### Session 2026-02-10

- Q: The spec mentions "exactly four columns: date, description, category, and value" but doesn't clarify whether column order matters or if the system should detect them by name. → A: Column order must match specification (date, description, category, value)
- Q: When the system encounters edge cases (missing columns, invalid dates, empty files, etc.), should it reject the entire file or attempt partial processing? → A: Reject entire file with clear error message
- Q: For the "rolling 3-month spending average", should this calculation include only expenses (negative values) or both income and expenses (net spending)? → A: Only expenses (negative values)
- Q: Should the Excel file include a header row with column names, or should the first row of data be treated as the first transaction? → A: File must include header row (first row ignored)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept Excel file uploads from users
- **FR-002**: System MUST validate that uploaded files contain exactly four columns in this order: date (column 1), description (column 2), category (column 3), and value (column 4)
- **FR-003**: System MUST skip the first row (header row) and parse transaction data starting from the second row, extracting date, description, category, and value information
- **FR-004**: System MUST calculate and display the current account balance as the sum of all transaction values
- **FR-005**: System MUST group transactions by month based on the date column
- **FR-006**: System MUST distinguish between income (positive values) and expenses (negative values) in the value column
- **FR-007**: System MUST generate a line chart showing monthly income and monthly expenses as two separate lines
- **FR-008**: System MUST generate a stacked bar chart showing monthly spending broken down by category
- **FR-009**: System MUST calculate a 3-month rolling average of total expenses (negative values only, excluding income) when at least 3 months of data are available
- **FR-010**: System MUST generate a line chart displaying the 3-month rolling spending average over time
- **FR-011**: System MUST calculate average monthly savings as the average of (monthly income minus monthly expenses)
- **FR-012**: System MUST identify the best month as the month with the highest net income
- **FR-013**: System MUST identify the worst month as the month with the lowest net income
- **FR-014**: System MUST display KPI cards for: current account balance, average savings, best month, and worst month
- **FR-015**: System MUST reject the entire file upload and display a clear error message when any validation fails (missing columns, invalid data types, empty file, incorrect column order, or malformed data)
- **FR-016**: System MUST allow users to upload new files and update all visualizations accordingly

### Key Entities

- **Transaction**: Represents a single financial transaction with attributes: date (when the transaction occurred), description (textual details about the transaction), category (classification such as "Groceries", "Transport", "Salary"), and value (monetary amount - positive for income, negative for expenses)
- **Monthly Summary**: Represents aggregated financial data for a single month with attributes: month identifier, total income (sum of positive values), total expenses (sum of absolute values of negative transactions), net income (income minus expenses), and category breakdown (spending totals per category)
- **Financial Metrics**: Represents calculated summary statistics with attributes: current balance (sum of all transaction values), average monthly savings (average net income across all months), best month (month with highest net income), and worst month (month with lowest net income)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can upload an Excel file and see their current account balance displayed within 5 seconds
- **SC-002**: 95% of valid Excel files (with correct columns and data format) are successfully processed without errors
- **SC-003**: All visualizations (KPI cards, line charts, bar charts) update and display within 10 seconds of file upload
- **SC-004**: Users can interpret their monthly income vs expense trends by viewing a single line chart without needing additional explanations
- **SC-005**: Users can identify their top spending categories for any month by viewing the stacked bar chart
- **SC-006**: The system correctly calculates financial metrics (balance, averages, best/worst months) with 100% accuracy for valid input data
- **SC-007**: Users receive clear, actionable error messages when uploading invalid files, enabling them to correct issues independently

## Assumptions

- Excel files will use standard date formats recognizable by common spreadsheet applications (e.g., "YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY")
- Transaction values will be numeric (integers or decimals) and use negative numbers to represent expenses
- Category names are pre-assigned by the user before upload (the system does not auto-categorize transactions)
- Users will have basic familiarity with common chart types (line charts, bar charts) and KPI displays
- The webapp will be used by individual users analyzing their personal finances, not for multi-user or enterprise scenarios
- File sizes will typically be modest (up to a few thousand transactions representing a few years of monthly data)
- The system does not need to persist data between sessions - each upload is treated as a new analysis session
