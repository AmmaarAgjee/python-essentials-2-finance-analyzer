# reporting.py
# This file creates the financial summary report.
# It records transaction totals, category totals, rejected rows,
# duplicate transactions, unusual transactions, and run information.


from datetime import datetime
import os
import platform

from analytics import category_totals, find_duplicates, find_outliers


# Creates a monthly summary report and saves it to data/report.txt.
def monthly_summary(transactions, rejected_count=0):
    report_folder = "data"
    report_path = os.path.join(report_folder, "report.txt")

    os.makedirs(report_folder, exist_ok=True)

    duplicates = find_duplicates(transactions)
    outliers = find_outliers(transactions)
    totals = category_totals(transactions) 

    income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.is_income()
    )

    expenses = sum(
        transaction.amount
        for transaction in transactions
        if not transaction.is_income()
    )

    balance_change = income + expenses

    with open(report_path, "w", encoding="utf-8") as report:
        report.write("PERSONAL FINANCE TRANSACTION ANALYZER\n")
        report.write("=" * 45 + "\n\n")

        report.write("SUMMARY\n")
        report.write("-" * 45 + "\n")
        report.write(f"Total transactions: {len(transactions)}\n")
        report.write(f"Total income: {income:.2f}\n")
        report.write(f"Total expenses: {expenses:.2f}\n")
        report.write(f"Balance change: {balance_change:.2f}\n")
        report.write(f"Rejected rows: {rejected_count}\n\n")

        report.write("CATEGORY BREAKDOWN\n")
        report.write("-" * 45 + "\n")

        for category, total in sorted(totals.items()):
            report.write(f"{category}: {total:.2f}\n")

        report.write("\nDUPLICATE TRANSACTIONS\n")
        report.write("-" * 45 + "\n")

        if duplicates:
            for transaction in duplicates:
                report.write(f"{transaction.formatted()}\n")
        else:
            report.write("No duplicates found.\n")

        report.write("\nUNUSUAL TRANSACTIONS\n")
        report.write("-" * 45 + "\n")

        if outliers:
            for transaction in outliers:
                report.write(f"{transaction.formatted()}\n")
        else:
            report.write("No unusual transactions found.\n")

        report.write("\nENVIRONMENT INFORMATION\n")
        report.write("-" * 45 + "\n")
        report.write(f"Operating system: {platform.system()}\n")
        report.write(f"Python platform: {platform.platform()}\n")
        report.write(f"Report generated: {datetime.now()}\n")

    log_run(report_folder)

    return report_path


# Adds a timestamped entry to the analyzer run log.
def log_run(folder="data"):
    log_path = os.path.join(folder, "runs.log")

    with open(log_path, "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"Analyzer run: {timestamp}\n")