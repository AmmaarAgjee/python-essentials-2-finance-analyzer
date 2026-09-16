# tests.py
# This file contains assertion tests for the Personal Finance Transaction Analyzer.
# The tests check transaction creation, data validation, running balances,
# closures, duplicate detection, income detection, and category totals.


from datetime import date

from models import Transaction
from parser import generate_sample_file, load_transactions
from analytics import (
    running_balance,
    make_flagger,
    find_duplicates,
    category_totals,
)


# Tests that a valid transaction is created with the correct values.
def test_valid_transaction():
    transaction = Transaction(
        date(2026, 8, 1),
        "Salary",
        15000.0,
        "INCOME"
    )

    assert transaction.date == date(2026, 8, 1), "Date was not stored correctly"
    assert transaction.description == "Salary", "Description was not stored correctly"
    assert transaction.amount == 15000.0, "Amount was not stored correctly"
    assert transaction.category == "INCOME", "Category was not stored correctly"


# Tests that dates using "/" are normalized to "-".
def test_date_normalization():
    path = generate_sample_file()
    transactions, rejections = load_transactions(path)

    matching_transactions = [
        transaction
        for transaction in transactions
        if transaction.description == "Transport"
    ]

    assert len(matching_transactions) == 1, "Normalized date transaction was not loaded"
    assert matching_transactions[0].date == date(2026, 8, 3), (
        "Date separator was not normalized correctly"
    )


# Tests that junk and missing-field rows are rejected.
def test_invalid_rows_rejected():
    path = generate_sample_file()
    transactions, rejections = load_transactions(path)

    assert len(rejections) >= 2, "Invalid rows were not rejected"


# Tests that non-numeric amounts are rejected.
def test_invalid_amount_rejected():
    path = generate_sample_file()
    transactions, rejections = load_transactions(path)

    abc_rejection = [
        reason
        for reason in rejections
        if "abc" in reason.lower() or "float" in reason.lower()
    ]

    assert len(abc_rejection) >= 1, "Nonnumeric amount was not rejected"


# Tests the running balance generator with a known sequence.
def test_running_balance():
    transactions = [
        Transaction(date(2026, 8, 1), "Income", 1000.0, "INCOME"),
        Transaction(date(2026, 8, 2), "Food", -200.0, "FOOD"),
        Transaction(date(2026, 8, 3), "Transport", -100.0, "TRANSPORT"),
    ]

    balances = list(running_balance(transactions))

    assert balances == [1000.0, 800.0, 700.0], (
        "Running balance did not produce the expected sequence"
    )


# Tests that the closure flags large transactions.
def test_flagger():
    flagger = make_flagger(1000)

    large_transaction = Transaction(
        date(2026, 8, 1),
        "Large Payment",
        5000.0,
        "OTHER"
    )

    small_transaction = Transaction(
        date(2026, 8, 2),
        "Small Payment",
        50.0,
        "OTHER"
    )

    assert flagger(large_transaction) is True, (
        "Flagger failed to identify a large transaction"
    )

    assert flagger(small_transaction) is False, (
        "Flagger incorrectly identified a small transaction"
    )


# Tests that an exact duplicate transaction is detected.
def test_find_duplicates():
    transaction = Transaction(
        date(2026, 8, 1),
        "Groceries",
        -500.0,
        "FOOD"
    )

    duplicate_transactions = [transaction, transaction]

    duplicates = find_duplicates(duplicate_transactions)

    assert len(duplicates) == 1, "Duplicate transaction was not detected"


# Tests that a clean list does not report duplicates.
def test_no_duplicates():
    transactions = [
        Transaction(date(2026, 8, 1), "Food", -100.0, "FOOD"),
        Transaction(date(2026, 8, 2), "Transport", -200.0, "TRANSPORT"),
    ]

    duplicates = find_duplicates(transactions)

    assert len(duplicates) == 0, "Clean transaction list incorrectly has duplicates"


# Tests the is_income method.
def test_is_income():
    income = Transaction(
        date(2026, 8, 1),
        "Salary",
        15000.0,
        "INCOME"
    )

    expense = Transaction(
        date(2026, 8, 2),
        "Groceries",
        -500.0,
        "FOOD"
    )

    assert income.is_income() is True, "Positive transaction was not identified as income"
    assert expense.is_income() is False, "Negative transaction was incorrectly identified as income"


# Tests category totals.
def test_category_totals():
    transactions = [
        Transaction(date(2026, 8, 1), "Food", -100.0, "FOOD"),
        Transaction(date(2026, 8, 2), "Food", -50.0, "FOOD"),
        Transaction(date(2026, 8, 3), "Salary", 1000.0, "INCOME"),
    ]

    totals = category_totals(transactions)

    assert totals["FOOD"] == -150.0, "Food category total is incorrect"
    assert totals["INCOME"] == 1000.0, "Income category total is incorrect"


# Runs every test and confirms that all tests pass.
if __name__ == "__main__":
    test_valid_transaction()
    test_date_normalization()
    test_invalid_rows_rejected()
    test_invalid_amount_rejected()
    test_running_balance()
    test_flagger()
    test_find_duplicates()
    test_no_duplicates()
    test_is_income()
    test_category_totals()

    print("All tests passed")