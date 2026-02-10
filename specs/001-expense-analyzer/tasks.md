# Tasks: Expense Analysis Webapp

**Feature**: 001-expense-analyzer  
**Input**: Design documents from `/specs/001-expense-analyzer/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - tests are optional for this mock project

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project structure** per plan.md: `src/`, `tests/` at repository root
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (src/, src/models/, src/services/, src/visualizations/, tests/unit/, tests/integration/, data/)
- [X] T002 Create requirements.txt with dependencies: streamlit>=1.28.0, pandas>=2.0.0, openpyxl>=3.1.0, plotly>=5.17.0
- [X] T003 [P] Update .gitignore file to exclude venv/, data/, __pycache__/, *.pyc
- [X] T004 [P] Create README.md with project overview and quickstart instructions
- [X] T005 [P] Create pytest configuration in pytest.ini (optional for mock project)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement read_excel_file() function in src/services/file_parser.py
- [X] T007 Implement validate_file() function in src/services/file_parser.py with column and type validation
- [X] T008 [P] Create sample Excel file in data/sample_transactions.xlsx for testing
- [X] T009 Setup Streamlit session state management utilities in src/services/session_manager.py
- [X] T010 [P] Implement error handling helper display_error() in src/services/error_handler.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Upload and View Account Balance (Priority: P1) 🎯 MVP

**Goal**: Allow users to upload Excel files and immediately see their current account balance

**Independent Test**: Upload a valid Excel file with transaction data and verify the balance KPI card displays the correct sum of all transaction values

### Implementation for User Story 1

- [X] T011 [US1] Implement calculate_current_balance(df) function in src/services/calculations.py
- [X] T012 [US1] Implement display_kpi_card(title, value) function in src/visualizations/kpi_cards.py
- [X] T013 [US1] Create main Streamlit app structure in src/app.py with file uploader widget
- [X] T014 [US1] Integrate file upload → validation → balance calculation → KPI display in src/app.py
- [X] T015 [US1] Add error handling for invalid file uploads with user-friendly messages in src/app.py
- [X] T016 [US1] Test with sample data to verify balance calculation accuracy

**Checkpoint**: At this point, User Story 1 should be fully functional - users can upload files and see their balance

---

## Phase 4: User Story 2 - Compare Monthly Income vs Expenses (Priority: P2)

**Goal**: Display monthly income and expense trends as a line chart

**Independent Test**: Upload transaction data spanning multiple months and verify the line chart correctly groups by month and shows separate income/expense lines

### Implementation for User Story 2

- [X] T017 [P] [US2] Implement calculate_monthly_summary(df) function in src/services/calculations.py
- [X] T018 [US2] Implement create_income_expense_chart(monthly_df) function in src/visualizations/charts.py using Plotly
- [X] T019 [US2] Add monthly income vs expenses visualization to src/app.py below balance KPI
- [X] T020 [US2] Handle edge case: sparse data with missing months (show zeros or skip gaps)
- [X] T021 [US2] Test with multi-month sample data to verify chart accuracy

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Analyze Spending by Category (Priority: P3)

**Goal**: Display monthly spending breakdown by category as a stacked bar chart

**Independent Test**: Upload categorized transaction data and verify the stacked bar chart shows category breakdown per month with correct totals

### Implementation for User Story 3

- [X] T022 [P] [US3] Implement calculate_category_breakdown(df) function in src/services/calculations.py
- [X] T023 [US3] Implement create_category_breakdown_chart(breakdown_df) function in src/visualizations/charts.py using Plotly stacked bars
- [X] T024 [US3] Add category spending visualization to src/app.py below monthly trends chart
- [X] T025 [US3] Ensure only expenses (negative values) are included in category breakdown
- [X] T026 [US3] Test with categorized sample data to verify stacked bar chart rendering

**Checkpoint**: User Stories 1, 2, and 3 should all work independently

---

## Phase 6: User Story 4 - Track Spending Trends with Rolling Average (Priority: P4)

**Goal**: Display 3-month rolling average of expenses to smooth out monthly fluctuations

**Independent Test**: Upload transaction data spanning at least 3 months and verify the rolling average chart displays correct 3-month averages

### Implementation for User Story 4

- [X] T027 [P] [US4] Implement calculate_rolling_average(df, window=3) function in src/services/calculations.py
- [X] T028 [US4] Implement create_rolling_average_chart(rolling_series) function in src/visualizations/charts.py using Plotly
- [X] T029 [US4] Add rolling average visualization to src/app.py below category breakdown chart
- [X] T030 [US4] Add conditional display: show message if less than 3 months of data available
- [X] T031 [US4] Filter to expenses only (negative values) when calculating rolling average
- [X] T032 [US4] Test with 3+ months of sample data to verify rolling calculation

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - View Financial Summary Metrics (Priority: P5)

**Goal**: Display KPI cards for average savings, best month, and worst month

**Independent Test**: Upload multi-month transaction data and verify KPI cards show correct average savings, best month (highest net income), and worst month (lowest net income)

### Implementation for User Story 5

- [X] T033 [P] [US5] Implement calculate_financial_metrics(df, monthly_df) function in src/services/metrics.py
- [X] T034 [US5] Implement display_best_worst_months(best, worst) function in src/visualizations/kpi_cards.py
- [X] T035 [US5] Add average savings KPI card to src/app.py using existing display_kpi_card()
- [X] T036 [US5] Add best/worst month KPI cards to src/app.py below other metrics
- [X] T037 [US5] Format month names (e.g., "January 2026") and currency values properly
- [X] T038 [US5] Test with multi-month sample data to verify metrics accuracy

**Checkpoint**: All user stories (1-5) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Add application title and description at top of src/app.py
- [ ] T040 [P] Improve visual layout with Streamlit columns for better KPI card arrangement
- [ ] T041 [P] Add chart titles and axis labels to all visualizations
- [ ] T042 Add currency formatting ($) to all monetary values in KPI cards
- [ ] T043 [P] Add color coding to KPI cards (green for positive, red for negative values)
- [ ] T044 [P] Create comprehensive sample data file with edge cases in data/comprehensive_sample.xlsx
- [ ] T045 Test all edge cases: empty columns, invalid dates, single month data, all income/all expenses
- [ ] T046 [P] Add inline documentation/docstrings to all functions per research.md recommendations
- [ ] T047 Verify all success criteria from spec.md are met (5-10 second performance targets)
- [ ] T048 Run through quickstart.md installation and usage steps to validate
- [ ] T049 [P] Optional: Add unit tests in tests/unit/ for calculation functions (mock project - optional)
- [ ] T050 [P] Optional: Configure Black/Ruff for code formatting (mock project - optional)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order: P1 → P2 → P3 → P4 → P5
  - Or work on multiple stories in parallel if team capacity allows
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories ✅ MVP
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - Reuses file parsing from US1, independently testable
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) - Reuses monthly grouping logic, independently testable
- **User Story 4 (P4)**: Depends on Foundational (Phase 2) - Uses similar patterns, independently testable
- **User Story 5 (P5)**: Depends on US2 monthly summary calculation (T017) - Builds on monthly data

### Within Each User Story

- Calculation functions before visualization functions
- Visualization functions before UI integration
- Core implementation before edge case handling
- Story complete and tested before moving to next priority

### Parallel Opportunities Per Story

**Setup Phase:**
- T003, T004, T005 can all run in parallel

**Foundational Phase:**
- T008, T010 can run in parallel after T006-T007 complete

**User Story 2:**
- T017 and T018 can run in parallel (different files)

**User Story 3:**
- T022 and T023 can run in parallel (different files)

**User Story 4:**
- T027 and T028 can run in parallel (different files)

**User Story 5:**
- T033 and T034 can run in parallel (different files)

**Polish Phase:**
- Most tasks (T039, T040, T041, T043, T044, T046, T049, T050) can run in parallel

---

## Parallel Example: User Story 1

If working solo (sequential):
```bash
# Complete in order
Complete T011 (calculation) → T012 (visualization) → T013 (app structure) → T014 (integration) → T015 (errors) → T016 (test)
```

If working with team (parallel where possible):
```bash
# Developer A
T011: Implement calculate_current_balance()

# Developer B (parallel)
T012: Implement display_kpi_card()

# Both merge, then Developer A
T013: Create app structure
T014: Integrate components
T015: Add error handling
T016: Test end-to-end
```

---

## Implementation Strategy

### MVP First (Recommended)

**MVP = User Story 1 only**
- Delivers immediate value: users can see their balance
- Simplest to implement: ~6 tasks
- Foundation for all other stories
- Time to MVP: ~2-4 hours for experienced developer

**Incremental Delivery:**
1. **Week 1**: Phase 1, 2, 3 (Setup + Foundation + US1) - MVP launch ✅
2. **Week 2**: Phase 4 (US2) - Add monthly trends
3. **Week 3**: Phase 5 (US3) - Add category breakdown
4. **Week 4**: Phase 6, 7 (US4, US5) - Add rolling average and summary metrics
5. **Week 5**: Phase 8 - Polish and finalize

### Full Feature Delivery

Complete all phases sequentially:
- Estimated time: 1-2 weeks for solo developer
- Testing: Manual verification with sample Excel files
- Deployment: Streamlit Cloud or local hosting

---

## Task Summary

**Total Tasks**: 50
- **Setup**: 5 tasks
- **Foundational**: 5 tasks
- **User Story 1 (P1)** 🎯: 6 tasks
- **User Story 2 (P2)**: 5 tasks
- **User Story 3 (P3)**: 5 tasks
- **User Story 4 (P4)**: 6 tasks
- **User Story 5 (P5)**: 6 tasks
- **Polish**: 12 tasks

**Parallel Opportunities**: 18 tasks marked [P] can run in parallel with other tasks

**MVP Scope** (Recommended first increment):
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 5 tasks
- Phase 3 (User Story 1): 6 tasks
- **Total MVP**: 16 tasks

---

## Validation Checklist

✅ **Format Compliance**:
- All tasks use checkbox format: `- [ ]`
- All tasks have sequential IDs (T001-T050)
- All user story tasks have [Story] labels ([US1], [US2], etc.)
- Parallel tasks marked with [P]
- All tasks include file paths

✅ **Organization**:
- Tasks grouped by user story
- Each story has independent test criteria
- Clear phase structure
- Dependencies documented

✅ **Completeness**:
- All 5 user stories from spec.md included
- All entities from data-model.md covered
- All contracts from service-contracts.md implemented
- Setup tasks from research.md included
- Polish phase for cross-cutting concerns

✅ **MVP Definition**:
- User Story 1 identified as MVP
- Clear incremental delivery path
- Independent testability per story
