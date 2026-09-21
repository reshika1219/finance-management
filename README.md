# Chirathma Flora — Event Accounts Desktop Application

A minimalistic, professional, offline desktop application for **Chirathma Flora** (Event Management and Decoration). Built with **Python 3**, **PySide6**, **SQLite**, and **openpyxl**.

---

## Features

- **First Launch PIN Setup**: Secure 4-digit PIN setup with PBKDF2-HMAC-SHA256 salted hash.
- **Event Accounting**:
  - Record contract details (Event Name, Date, Client Name, Location, Description).
  - Track Total Income and 5 specific event expense categories (Employee Salaries, Transportation, Food for Employees, Supplier Payments, Utilities / Others).
  - Real-time event expenditure & profit calculation.
  - Full CRUD: View, edit, and delete events with confirmation dialogs.
- **Monthly Accounting**:
  - Dashboard with month navigation (`< Month Year >`).
  - Track 5 general monthly business expenses (Rent, Electricity Bill, Water Bill, Telephone Bill, Others).
  - Instant monthly aggregates: Total Monthly Income, Total Monthly Expenditure, Monthly Net Profit.
- **Excel Reports & Metadata Import**:
  - Export clean, professional `.xlsx` monthly reports (Monthly Summary + Event Details).
  - Embeds hidden machine-readable metadata (`_ReportMetadata`) for reliable round-trip importing.
  - Flexible reporting period generator from saved database records or imported monthly Excel files.
  - Automatic duplicate month rejection and chronological sorting.
- **Data Safety & Integrity**:
  - `decimal.Decimal` safe calculations avoiding binary floating-point rounding errors.
  - Local database snapshot Backup & Restore (`.db`).
  - Works 100% offline with zero online/external dependencies.

---

## Setup & Running Locally

### Requirements
- Python 3.10+ (Tested on Python 3.12)

### 1. Installation

```bash
# Clone or navigate to the repository
cd finance-management

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
python main.py
```

---

## Running Automated Tests

Run the full pytest suite:

```bash
pytest -v
```

All calculation logic, decimal handling, database operations, Excel metadata round-trips, duplicate month rejection, and backup/restore procedures are covered by automated unit tests.

---

## Building Executables for Distribution

### Building Desktop Binary with PyInstaller

To compile a standalone executable (`.exe` on Windows or executable on macOS):

```bash
pyinstaller ChirathmaFlora.spec
```

The output standalone binary will be created inside the `dist/` directory.

### Windows Installer Instructions (Inno Setup)

To package `dist/ChirathmaFlora.exe` into a Windows Setup wizard (`ChirathmaFloraSetup.exe`):
1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php).
2. Create an Inno Setup script pointing to `dist/ChirathmaFlora.exe`.
3. Compile the script to generate `ChirathmaFloraSetup.exe`.
