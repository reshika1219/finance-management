"""
QSS Styling for Chirathma Flora desktop application.
Restrained, modern, clean, light-mode palette.
"""

MAIN_STYLE = """
/* Global Application Style */
QWidget {
    background-color: #F8FAFC;
    color: #0F172A;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 14px;
}

/* Windows / Dialogs */
QDialog, QMainWindow {
    background-color: #F8FAFC;
}

/* Sidebar Navigation */
#sidebar {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

#sidebarHeader {
    font-size: 18px;
    font-weight: bold;
    color: #1E293B;
    padding: 16px;
}

QPushButton.nav-btn {
    text-align: left;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    color: #475569;
    background-color: transparent;
}

QPushButton.nav-btn:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}

QPushButton.nav-btn:checked {
    background-color: #0284C7;
    color: #FFFFFF;
    font-weight: 600;
}

/* Cards & Frames */
QFrame.card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px;
}

QLabel.card-title {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
}

QLabel.card-value {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
}

QLabel.card-value-positive {
    font-size: 24px;
    font-weight: 700;
    color: #0D9488;
}

QLabel.card-value-negative {
    font-size: 24px;
    font-weight: 700;
    color: #E11D48;
}

/* Buttons */
QPushButton.primary-btn {
    background-color: #0284C7;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}

QPushButton.primary-btn:hover {
    background-color: #0369A1;
}

QPushButton.primary-btn:pressed {
    background-color: #075985;
}

QPushButton.secondary-btn {
    background-color: #FFFFFF;
    color: #334155;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 14px;
}

QPushButton.secondary-btn:hover {
    background-color: #F1F5F9;
}

QPushButton.danger-btn {
    background-color: #E11D48;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}

QPushButton.danger-btn:hover {
    background-color: #BE123C;
}

/* Inputs & Form Controls */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 8px 12px;
    color: #0F172A;
    font-size: 14px;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QDateEdit:focus {
    border: 2px solid #0284C7;
}

/* Tables */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    gridline-color: #F1F5F9;
    border-radius: 8px;
    selection-background-color: #E0F2FE;
    selection-color: #0369A1;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #475569;
    font-weight: 600;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #E2E8F0;
}

/* Headings */
QLabel.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #0F172A;
}

QLabel.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 5px;
}

QLabel.subtext {
    font-size: 13px;
    color: #64748B;
}
"""
