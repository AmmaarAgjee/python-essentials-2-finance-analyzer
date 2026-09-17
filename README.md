# python-essentials-2-finance-analyzer
A Python-based personal finance transaction analyzer that cleans, validates, categorizes, and analyzes messy bank statement data, including running balances, duplicate detection, outlier detection, and summary reports.
# Personal Finance Transaction Analyzer

## Project Description

The Personal Finance Transaction Analyzer is a Python program that reads
financial transactions from a bank statement file.

The program cleans and validates the transaction data before analysing it.
It can calculate running balances, group transactions by category, find
duplicate transactions, identify unusual transactions, and create a
monthly summary report.

The project was built as part of Python Essentials 2.

## Features

The program can:

1. Generate a messy sample bank statement.
2. Load and validate transactions.
3. Show a running balance.
4. Display a category breakdown.
5. Detect duplicate transactions.
6. Flag unusual transactions.
7. Generate a monthly summary report.
8. Run the project's self-tests.
9. Exit the program.

## Handling Invalid Data

The parser is designed to handle messy transaction data without crashing.

It can:

- Normalize dates using different separators.
- Remove unnecessary whitespace.
- Reject rows with missing fields.
- Reject non-numeric transaction amounts.
- Reject junk or invalid rows.
- Continue processing when one row is invalid.
- Record a reason for each rejected row.

Valid transactions are loaded while invalid rows are recorded separately.

## Project Structure

```text
python-essentials-2-finance-analyzer/
│
├── main.py
├── models.py
├── parser.py
├── analytics.py
├── reporting.py
├── tests.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/