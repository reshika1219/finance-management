# Chirathma Flora — Event Accounts Desktop Application

## 1. Project Objective

Build a simple, minimalistic, professional desktop application for **Chirathma Flora**, an event management and decoration business.

The application is intended for a non-technical user, so simplicity and ease of use are extremely important.

The application will be used to:

1. Record each event/client contract.
2. Record total income from each event.
3. Record event-specific expenditures.
4. Automatically calculate event profit.
5. Record general monthly business expenses.
6. Automatically calculate total monthly income, total monthly expenditure, and monthly profit.
7. Export a clean and professional monthly Excel `.xlsx` report.
8. Generate a combined financial report covering any selected range of months.
9. Generate the combined report either:
   - directly from data stored in the application, or
   - by importing previously exported monthly Excel files.
10. Store all information locally and work fully offline.

The final production environment is **Windows**, but development and testing should also work on **macOS**.

---

# 2. Core Principles

The application must be:

- Simple
- Minimalistic
- Easy for a non-technical user
- Fully offline
- Desktop-based
- Fast to open
- Easy to navigate
- Professional looking
- Reliable
- Difficult for the user to accidentally break
- Free from unnecessary features

Do not turn this into a complex accounting system.

Do not add inventory management, invoicing systems, customer relationship management, employee management, authentication accounts, cloud synchronization, online services, or other unrelated features.

Keep the workflow extremely straightforward.

---

# 3. Recommended Technology

Use:

- **Python 3**
- **PySide6** for the desktop GUI
- **SQLite** for local data storage
- **openpyxl** for Excel generation/import
- **PyInstaller** or an equivalent reliable packaging method for desktop builds

The source project should remain cross-platform enough to run during development on macOS.

The final deployment target is:

- Windows 10/11
- Standalone desktop application
- No browser
- No localhost server
- No terminal required
- No separate Python installation required by the end user

The final Windows version should be packageable into an `.exe` and preferably a proper installer.

---

# 4. Application Name

Default application/business name:

**Chirathma Flora**

This should appear in:

- Application title
- Login/PIN screen
- Dashboard
- Excel reports

The business name should also be editable from Settings in case it changes in the future.

---

# 5. First Launch

On first launch, ask the user to create a **4-digit PIN**.

Requirements:

- Exactly 4 numeric digits
- Ask user to enter the PIN twice for confirmation
- Store the PIN securely rather than as plain text
- Use an appropriate local hash
- No online authentication
- No username
- No email
- No account creation

After setup, every application launch should show a simple PIN screen.

Example:

```text
Chirathma Flora

Enter PIN

[ • • • • ]

[ Unlock ]
```

Also provide a **Change PIN** option under Settings.

Do not unnecessarily complicate PIN recovery.

---

# 6. Main Navigation

Use a simple left sidebar or similarly clean navigation structure.

Recommended sections:

1. Dashboard
2. Events
3. Monthly Summary
4. Reports
5. Backup & Restore
6. Settings

The interface must not feel crowded.

---

# 7. Dashboard

The Dashboard should focus on the currently selected month.

Example:

```text
Chirathma Flora

September 2026

Events
5

Total Income
Rs. 1,250,000.00

Total Expenditure
Rs. 690,000.00

Profit
Rs. 560,000.00

[ Add Event ]

[ Monthly Expenses ]

[ View Monthly Summary ]

[ Export Month ]
```

Also allow month navigation.

Example:

```text
< August 2026     September 2026     October 2026 >
```

The user should be able to browse old months easily.

Do not require manually typing month names.

---

# 8. Currency

Use Sri Lankan Rupees.

Display:

```text
Rs. 125,000.00
```

Use two decimal places.

Store financial values accurately.

Do not use floating-point arithmetic if it can introduce financial rounding errors.

Prefer decimal-safe calculations.

---

# 9. Date Format

Use:

```text
DD/MM/YYYY
```

Example:

```text
21/09/2026
```

Internally, dates may be stored in ISO format if convenient.

---

# 10. Event Concept

An important business rule is:

**One event represents one day.**

Do not create unnecessary transaction dates inside individual event expenses.

The event itself already has a date.

One event contains:

### Basic Event Details

- Event Name
- Event Date
- Client Name
- Location
- Description
- Total Income

Example:

```text
Event Name:
Perera Wedding

Event Date:
21/09/2026

Client Name:
Mr. Perera

Location:
Kandy

Description:
Wedding decoration

Total Income:
Rs. 350,000.00
```

---

# 11. Event Expenses

Each event has exactly five expense categories.

1. Employee Salaries
2. Transportation
3. Food for Employees
4. Supplier Payments
5. Utilities / Others

Each category should contain only **one amount**.

Do NOT create a system with multiple transactions underneath each category.

Example:

```text
Employee Salaries       Rs. 45,000.00
Transportation          Rs. 20,000.00
Food for Employees      Rs. 12,000.00
Supplier Payments       Rs. 125,000.00
Utilities / Others      Rs. 8,000.00
```

Allow one optional simple description/note beside each event expense.

Example:

```text
Transportation
Amount: Rs. 20,000.00
Note: Van hire and fuel
```

Do not request:

- receipt numbers
- invoice numbers
- individual payment dates
- transaction references
- multiple suppliers
- individual employees

Keep it simple.

---

# 12. Empty Expense Fields

If an expense field is left empty, automatically treat it as:

```text
Rs. 0.00
```

Do not force the user to manually enter zero.

---

# 13. Event Calculations

For every event calculate:

```text
Total Event Expenditure =
Employee Salaries
+ Transportation
+ Food for Employees
+ Supplier Payments
+ Utilities / Others
```

Then:

```text
Event Profit =
Total Income - Total Event Expenditure
```

The profit should update instantly while the user edits values.

Example:

```text
Total Income:
Rs. 350,000.00

Total Event Expenditure:
Rs. 210,000.00

Event Profit:
Rs. 140,000.00
```

Negative event profits must be allowed.

Zero income must also be allowed.

---

# 14. Add Event Screen

Keep all event information on one straightforward screen.

Suggested structure:

```text
Add Event

EVENT DETAILS

Event Name
[________________________]

Date
[ 21/09/2026 ]

Client Name
[________________________]

Location
[________________________]

Description
[________________________]


INCOME

Total Income
Rs. [________________]


EVENT EXPENSES

Employee Salaries
Rs. [____________]
Note [________________]

Transportation
Rs. [____________]
Note [________________]

Food for Employees
Rs. [____________]
Note [________________]

Supplier Payments
Rs. [____________]
Note [________________]

Utilities / Others
Rs. [____________]
Note [________________]


SUMMARY

Total Income              Rs. XXX
Total Expenditure         Rs. XXX
Event Profit              Rs. XXX


[ Cancel ]       [ Save Event ]
```

The calculated summary should update automatically.

---

# 15. Events Screen

Display saved events in a clean table.

Recommended columns:

- Date
- Event
- Client
- Location
- Income
- Expenditure
- Profit
- Actions

Actions:

- View
- Edit
- Delete

Allow filtering by month.

Optional simple search can search:

- Event name
- Client name
- Location

Do not add complicated filters.

---

# 16. Editing Events

All previously saved events must remain editable.

If the user changes an event:

- recalculate event totals
- recalculate the month's totals
- update reports accordingly

No month should ever become permanently locked.

---

# 17. Delete Event

Allow event deletion.

Before deleting, display a confirmation dialog.

Example:

```text
Delete Event?

Are you sure you want to delete
"Perera Wedding"?

This action cannot be undone.

[ Cancel ]   [ Delete ]
```

Never delete immediately after one accidental click.

---

# 18. Monthly Business Expenses

Monthly expenses are independent of individual events.

There are exactly five monthly categories:

1. Rent
2. Electricity Bill
3. Water Bill
4. Telephone Bill
5. Others

Each category has one amount for each month.

Example:

```text
September 2026

Rent
Rs. 50,000.00

Electricity Bill
Rs. 12,500.00

Water Bill
Rs. 3,000.00

Telephone Bill
Rs. 4,500.00

Others
Rs. 5,000.00
```

No optional notes are required for these categories.

Empty values should automatically mean `0.00`.

Allow editing these amounts at any time.

---

# 19. Monthly Calculations

For the selected month:

```text
Total Monthly Income =
Sum of income from every event in that month
```

Calculate total event expenditure:

```text
Total Event Expenditure =
Sum of all event expenses in that month
```

Calculate monthly general expenditure:

```text
Monthly General Expenditure =
Rent
+ Electricity
+ Water
+ Telephone
+ Others
```

Then:

```text
Total Monthly Expenditure =
Total Event Expenditure
+ Monthly General Expenditure
```

Finally:

```text
Monthly Profit =
Total Monthly Income
- Total Monthly Expenditure
```

---

# 20. Monthly Summary Screen

Display something similar to:

```text
Chirathma Flora
Monthly Summary

September 2026

Number of Events:
5

EVENT TOTALS

Total Event Income
Rs. 1,250,000.00

Employee Salaries
Rs. 120,000.00

Transportation
Rs. 45,000.00

Food for Employees
Rs. 30,000.00

Supplier Payments
Rs. 400,000.00

Utilities / Others
Rs. 20,000.00


MONTHLY EXPENSES

Rent
Rs. 50,000.00

Electricity
Rs. 12,500.00

Water
Rs. 3,000.00

Telephone
Rs. 4,500.00

Others
Rs. 5,000.00


FINAL SUMMARY

Total Income
Rs. 1,250,000.00

Total Expenditure
Rs. 690,000.00

Net Profit
Rs. 560,000.00


[ Edit Monthly Expenses ]

[ Export Excel ]
```

---

# 21. Monthly Excel Export

Provide a clear button:

```text
Export Monthly Excel
```

Suggested filename:

```text
Chirathma_Flora_September_2026.xlsx
```

The user should be shown a standard Save File dialog.

The `.xlsx` file must be clean, professional and readable.

Do not export CSV.

---

# 22. Monthly Excel Structure

Use two worksheets.

## Sheet 1 — Monthly Summary

Suggested header:

```text
CHIRATHMA FLORA

MONTHLY FINANCIAL SUMMARY

September 2026
```

Then:

| Item | Amount (Rs.) |
|---|---:|
| Total Income | 1,250,000.00 |
| Employee Salaries | 120,000.00 |
| Transportation | 45,000.00 |
| Food for Employees | 30,000.00 |
| Supplier Payments | 400,000.00 |
| Utilities / Others | 20,000.00 |
| Rent | 50,000.00 |
| Electricity Bill | 12,500.00 |
| Water Bill | 3,000.00 |
| Telephone Bill | 4,500.00 |
| Monthly Others | 5,000.00 |
| Total Expenditure | 690,000.00 |
| Net Profit | 560,000.00 |

Make `Total Income`, `Total Expenditure`, and `Net Profit` visually clear.

---

# 23. Monthly Excel — Event Details Sheet

Worksheet name:

```text
Event Details
```

Recommended columns:

| Date | Event | Client | Location | Income | Salaries | Transportation | Food | Suppliers | Utilities/Others | Total Expenditure | Profit |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

Each event occupies one row.

Do not add separate rows for individual expenses.

Each event is one day and one record.

Include a totals row at the bottom.

---

# 24. Excel Styling

Use a professional minimalist design.

Requirements:

- White background
- Clean typography
- Bold titles
- Dark/simple headings
- Subtle borders
- Proper column widths
- Right-aligned numerical values
- Thousands separators
- Two decimal places
- Freeze relevant header rows if useful
- Avoid unnecessary colours
- Avoid decorative graphics
- No charts
- No unnecessary logos
- Print-friendly layout

Do not make the Excel file visually busy.

---

# 25. Reports

Create a section called:

```text
Reports
```

This replaces the concept of a rigid "Annual Report" because reporting periods are flexible.

A reporting period may be:

```text
January 2026 – December 2026
```

or:

```text
March 2026 – March 2027
```

or:

```text
August 2026 – March 2027
```

or any other collection of months.

Do not assume January-to-December.

---

# 26. Generate Report From Saved Data

Provide:

```text
Generate Report from Saved Data
```

The user should select:

- Start month
- Start year
- End month
- End year

Example:

```text
From:
August 2026

To:
March 2027
```

The application should retrieve each month's totals and create a combined report.

---

# 27. Generate Report From Monthly Excel Files

Also provide:

```text
Generate Report from Monthly Excel Files
```

Allow the user to select multiple previously exported monthly `.xlsx` files.

The number of files is variable.

Possible examples:

- 8 monthly files
- 10 monthly files
- 12 monthly files
- 13 monthly files

Do NOT require exactly 12 files.

Do NOT assume the files are January through December.

---

# 28. Excel Import Validation

When monthly Excel files are imported:

1. Confirm the file is a valid Chirathma Flora monthly report.
2. Read its month and year.
3. Read total income.
4. Read total expenditure.
5. Read monthly profit.
6. Sort imported months chronologically.

If two files represent the same month and year, show an error.

Example:

```text
Duplicate Month

September 2026 has been selected more than once.

Please remove the duplicate file and try again.
```

Do not silently combine duplicate files.

---

# 29. Combined Report Format

The combined report should contain only month-level totals.

Do not include individual events.

Do not include expense-category breakdowns.

Recommended table:

| Month | Total Income (Rs.) | Total Expenditure (Rs.) | Profit (Rs.) |
|---|---:|---:|---:|
| August 2026 | 850,000.00 | 610,000.00 | 240,000.00 |
| September 2026 | 1,200,000.00 | 790,000.00 | 410,000.00 |
| October 2026 | 980,000.00 | 600,000.00 | 380,000.00 |
| ... | ... | ... | ... |
| TOTAL | 3,030,000.00 | 2,000,000.00 | 1,030,000.00 |

At the top show:

```text
CHIRATHMA FLORA

FINANCIAL SUMMARY

Reporting Period:
August 2026 – March 2027
```

Calculate:

```text
Total Income =
Sum of all selected monthly income

Total Expenditure =
Sum of all selected monthly expenditure

Total Profit =
Total Income - Total Expenditure
```

Also verify:

```text
Total Profit =
Sum of individual monthly profits
```

These should match.

---

# 30. Combined Report Filename

Suggested filename:

```text
Chirathma_Flora_August_2026_to_March_2027.xlsx
```

If it happens to be a normal calendar year, something like:

```text
Chirathma_Flora_2026.xlsx
```

is also acceptable.

---

# 31. Missing Months

Do not artificially generate empty months.

Only use months that actually exist within the selected saved-data reporting range or imported files.

However, because monthly business expenses exist even without events, the application must support months containing:

```text
Income = Rs. 0.00

Monthly Expenses > Rs. 0.00

Profit = negative value
```

This is valid.

---

# 32. Database

Use SQLite.

The user should never have to interact with the database manually.

Suggested database entities:

## settings

Possible fields:

```text
id
business_name
pin_hash
created_at
updated_at
```

## events

Possible fields:

```text
id
event_name
event_date
client_name
location
description
income
employee_salary
employee_salary_note
transportation
transportation_note
food
food_note
supplier_payments
supplier_note
utilities_others
utilities_others_note
created_at
updated_at
```

Do not unnecessarily store calculated event profit if it can safely be calculated from the source values.

## monthly_expenses

Possible fields:

```text
id
year
month
rent
electricity
water
telephone
others
created_at
updated_at
```

Ensure there is only one monthly-expense record for each year/month combination.

Use appropriate database constraints.

---

# 33. Financial Data Integrity

Financial correctness is extremely important.

Use a safe representation for currency.

Avoid binary floating-point calculation errors.

Round/display to two decimal places.

Validate numerical inputs.

Prevent invalid values such as:

```text
abc
Rs. xyz
```

Negative income or negative expenses should normally not be accepted as manually entered values.

Negative profit is allowed because it is calculated.

---

# 34. Backup

Create a dedicated:

```text
Backup & Restore
```

screen.

Provide:

```text
[ Create Backup ]

[ Restore Backup ]
```

---

# 35. Create Backup

Create a backup containing all application data.

Suggested filename:

```text
Chirathma_Flora_Backup_2026-09-21.db
```

or package the backup using another simple extension if appropriate.

Allow the user to choose where to save it.

The backup should preserve:

- Events
- Monthly expenses
- Business settings
- Application configuration required to restore the data

Avoid unnecessarily exposing sensitive PIN data if there is a safer implementation.

---

# 36. Restore Backup

Allow selecting a valid Chirathma Flora backup.

Before overwriting existing data, show:

```text
Restore Backup?

Restoring this backup will replace the current application data.

Would you like to continue?

[ Cancel ] [ Restore ]
```

Validate the backup before replacing the existing database.

Do not corrupt the current database if the selected backup is invalid.

---

# 37. Settings

Keep Settings minimal.

Include:

### Business Name

Default:

```text
Chirathma Flora
```

Allow editing.

### Change PIN

Require:

- Current PIN
- New 4-digit PIN
- Confirm new PIN

### Data / Application Information

Optionally display:

```text
Database Location
Application Version
```

but do not expose technical information unnecessarily.

---

# 38. User Experience

The target user has very little technical knowledge.

Therefore:

- Use large enough buttons.
- Use clear labels.
- Avoid technical terminology.
- Avoid command-line actions.
- Avoid configuration files.
- Avoid requiring folder management.
- Avoid complicated modal flows.
- Avoid hidden actions.
- Make Save, Edit, Delete and Export obvious.

Use understandable messages.

Bad example:

```text
SQLite IntegrityError: UNIQUE constraint failed
```

Good example:

```text
Monthly expenses for September 2026 already exist.

The existing values have been opened for editing.
```

---

# 39. Validation

Required fields for an event:

- Event Name
- Date
- Client Name
- Total Income

Location and description may remain empty if needed.

Expense amounts may remain empty and default to zero.

Before saving, validate everything cleanly.

---

# 40. Confirmation Messages

After saving:

```text
Event Saved

The event has been saved successfully.
```

After Excel export:

```text
Export Complete

The Excel report was created successfully.
```

Do not overwhelm the user with dialogs for every tiny interaction.

---

# 41. Error Handling

Handle errors gracefully.

Examples:

### Invalid Excel file

```text
Unable to Import File

This does not appear to be a valid Chirathma Flora monthly report.
```

### File currently open in Excel

```text
Unable to Save Report

The Excel file may currently be open in another application.

Please close it and try again.
```

### Invalid backup

```text
Invalid Backup

The selected file could not be restored.
```

Never show raw stack traces to normal users.

Write technical errors to a local log if necessary.

---

# 42. Application Appearance

Aim for a modern but restrained interface.

Suggested visual direction:

- White/light background
- Dark text
- Muted secondary text
- One subtle accent colour
- Rounded cards/buttons if appropriate
- Spacious layout
- Consistent padding
- Simple icons where useful
- Clear typography

Avoid:

- gradients everywhere
- flashy animations
- excessive colours
- glassmorphism
- cluttered dashboards
- oversized graphics
- unnecessary charts

This is business software.

Functionality and clarity are more important than visual novelty.

---

# 43. Responsive Desktop Layout

The application should work comfortably on common Windows laptop displays.

Target at least:

```text
1366 × 768
```

and above.

Make forms scrollable if necessary.

Avoid fixed layouts that break on smaller laptop screens.

---

# 44. Cross-Platform Development

Development is initially being performed on a MacBook.

Therefore:

- The source code should run on macOS for development/testing.
- The SQLite database should work identically.
- Excel generation should work identically.
- Event calculations should work identically.
- Reports should work identically.
- Backup/restore should work identically.

The production target remains Windows.

Do not use Windows-only APIs in core application logic unless absolutely necessary.

---

# 45. Windows Distribution

Prepare the project so it can eventually produce:

```text
ChirathmaFloraSetup.exe
```

or a similarly simple installer.

The final user should not need:

- Python
- pip
- terminal
- VS Code
- Antigravity
- developer tools

The user should simply install the software and open it from the desktop or Start Menu.

---

# 46. Project Structure

Use a clean maintainable structure.

For example:

```text
chirathma-flora/
│
├── main.py
├── requirements.txt
├── README.md
│
├── app/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── ui/
│   ├── utils/
│   └── reports/
│
├── assets/
│
├── tests/
│
├── build/
│
└── docs/
```

The exact structure can vary, but separate:

- database logic
- business calculations
- UI
- Excel handling
- backup handling

Do not put the entire application into one huge Python file.

---

# 47. Business Logic Separation

Financial calculations must not depend directly on GUI widgets.

Create dedicated services/functions for:

```text
calculate_event_expenditure()
calculate_event_profit()
calculate_month_income()
calculate_month_event_expenses()
calculate_month_general_expenses()
calculate_month_total_expenditure()
calculate_month_profit()
calculate_reporting_period_totals()
```

This makes calculations testable.

---

# 48. Automated Tests

Create automated tests for critical calculations.

At minimum test:

### Event

```text
Income = 100,000

Salary = 10,000
Transport = 5,000
Food = 2,500
Supplier = 20,000
Utilities = 2,500

Expected expenditure = 40,000
Expected profit = 60,000
```

### Monthly totals

Test several events plus monthly expenses.

### Negative monthly profit

Ensure negative profit works correctly.

### Decimal currency values

Example:

```text
1234.56
```

must calculate correctly.

### Excel export/import

Export a monthly report and re-import it.

Ensure imported totals match the original totals.

### Duplicate reporting month

Ensure duplicate monthly Excel files are rejected.

### Backup/restore

Verify data remains intact after restore.

---

# 49. Excel Import Reliability

Monthly files generated by this application must contain machine-readable metadata so they can reliably be re-imported.

Do not depend only on visually locating random cells.

For example, create a hidden worksheet named:

```text
_ReportMetadata
```

containing values such as:

```text
report_type = monthly
application = Chirathma Flora
format_version = 1
year = 2026
month = 9
total_income = ...
total_expenditure = ...
profit = ...
```

Hide this worksheet from normal Excel viewing.

Use it when generating combined reports from imported monthly files.

This keeps imports reliable even if the visible spreadsheet formatting changes later.

Still keep all visible information human-readable.

---

# 50. Excel Format Versioning

Include an internal report format version.

Example:

```text
format_version = 1
```

If future versions change, the importer should be able to recognize unsupported report formats and provide a friendly message.

---

# 51. Autosave Philosophy

Do not autosave partially completed event forms.

Only save after the user explicitly presses:

```text
Save Event
```

However, after saving, all changes must immediately persist to SQLite.

---

# 52. Unsaved Changes

If the user edits an event and attempts to leave the screen without saving, show:

```text
Unsaved Changes

You have unsaved changes.

Do you want to discard them?

[ Stay ] [ Discard ]
```

---

# 53. No Month Locking

Do not implement financial-period locking.

The user may edit old events or old monthly expenses at any time.

If they later export the month again, the Excel file should reflect the latest saved information.

---

# 54. Reporting Period Terminology

Prefer:

```text
Financial Report
Reporting Period
Combined Report
```

instead of always calling everything:

```text
Annual Report
```

because the reporting period is not necessarily January–December and may contain fewer or more than 12 months.

---

# 55. Things That Must NOT Be Added

Do not add:

- customer login
- cloud sync
- web backend
- localhost server
- online database
- internet requirement
- email sending
- invoice creation
- receipt management
- inventory management
- payroll system
- employee profiles
- supplier database
- individual supplier transactions
- multiple income payments per event
- multiple expense transactions per category
- graphs unless explicitly requested later
- complicated accounting terminology
- tax-related wording
- tax calculation
- VAT calculation
- calendar integrations
- notifications
- AI functionality
- advertisements
- subscription systems

---

# 56. Important Privacy Requirement

Do not include wording inside the application or exported reports referring to:

- Inland Revenue
- tax submission
- tax department
- government submission

The application should simply function as a general business financial-record and reporting tool.

---

# 57. Example Complete Workflow

### Step 1

User opens Chirathma Flora.

### Step 2

User enters the 4-digit PIN.

### Step 3

Dashboard opens to September 2026.

### Step 4

User clicks:

```text
Add Event
```

### Step 5

User enters:

```text
Event Name:
Perera Wedding

Date:
21/09/2026

Client:
Mr. Perera

Location:
Kandy

Income:
Rs. 350,000

Salary:
Rs. 45,000

Transportation:
Rs. 20,000

Food:
Rs. 12,000

Supplier:
Rs. 125,000

Utilities/Others:
Rs. 8,000
```

The application immediately shows:

```text
Total Expenditure:
Rs. 210,000.00

Profit:
Rs. 140,000.00
```

### Step 6

User clicks Save.

### Step 7

At the end of September, user opens Monthly Expenses.

Enters:

```text
Rent:
50,000

Electricity:
12,500

Water:
3,000

Telephone:
4,500

Others:
5,000
```

### Step 8

Application combines all September events and monthly expenses.

Shows:

```text
Total Income
Rs. 1,250,000.00

Total Expenditure
Rs. 690,000.00

Profit
Rs. 560,000.00
```

### Step 9

User presses:

```text
Export Monthly Excel
```

File produced:

```text
Chirathma_Flora_September_2026.xlsx
```

### Step 10

Several months later, user opens Reports.

Selects:

```text
August 2026
to
March 2027
```

or imports the corresponding monthly `.xlsx` files.

### Step 11

Application generates:

```text
Month             Income          Expenditure        Profit

August 2026       ...
September 2026    ...
October 2026      ...
November 2026     ...
December 2026     ...
January 2027      ...
February 2027     ...
March 2027        ...

TOTAL             ...             ...                ...
```

### Step 12

User exports the combined Excel file.

---

# 58. Development Approach for the AI Agent

Build this incrementally.

Do NOT try to implement everything in a single unstructured pass.

Recommended development order:

### Phase 1 — Foundation

- Create project structure
- Configure PySide6
- Create SQLite database
- Implement settings
- Implement PIN setup/login

### Phase 2 — Events

- Event form
- Event database operations
- Event calculations
- Event list
- Edit
- Delete

### Phase 3 — Monthly Accounting

- Monthly expense form
- Monthly totals
- Dashboard
- Month navigation
- Monthly summary

### Phase 4 — Excel

- Monthly Excel export
- Event detail worksheet
- Hidden metadata
- Styling

### Phase 5 — Reports

- Generate report from database
- Import monthly Excel files
- Validate files
- Detect duplicates
- Sort months
- Generate combined report

### Phase 6 — Backup

- Create backup
- Restore backup
- Validation

### Phase 7 — Testing

- Financial calculation tests
- Database tests
- Excel round-trip tests
- Backup tests

### Phase 8 — Deployment

- macOS development test
- Windows compatibility
- PyInstaller configuration
- Windows executable
- Windows installer instructions

---

# 59. Agent Behaviour During Development

When implementing this project:

1. Read this complete specification before changing the architecture.
2. Do not arbitrarily add features.
3. Prefer the simplest solution that satisfies this specification.
4. Keep the UI understandable for a non-technical person.
5. Preserve financial calculation accuracy.
6. Write maintainable code.
7. Comment complex logic but avoid excessive comments.
8. Handle errors gracefully.
9. Never silently discard financial data.
10. Before destructive operations, require confirmation.
11. Ensure changes to old events automatically affect monthly totals.
12. Test each major feature as it is created.
13. Maintain a clear `README.md` describing how to run the project on macOS and Windows.
14. Maintain `requirements.txt`.
15. Do not replace completed working components unnecessarily.

---

# 60. Definition of Done

The project is complete when a non-technical Windows user can:

1. Install the application.
2. Open it normally.
3. Enter a 4-digit PIN.
4. Add events.
5. Enter one total income per event.
6. Enter the five event expense categories.
7. See event profit automatically.
8. Edit an event.
9. Delete an event with confirmation.
10. Browse previous months.
11. Enter monthly expenses.
12. See monthly income.
13. See monthly expenditure.
14. See monthly profit.
15. Export a professional monthly `.xlsx`.
16. Reopen the software later without losing data.
17. Generate a combined report from saved data.
18. Generate a combined report from previously exported monthly Excel files.
19. Use flexible reporting periods across calendar years.
20. Export the combined financial `.xlsx`.
21. Create a backup.
22. Restore a backup.
23. Change the PIN.
24. Perform all of the above without needing internet access, a browser, terminal commands, Python, or technical knowledge.

The final result should feel like a small polished business application rather than a developer prototype.