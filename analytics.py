# analytics.py
# This file contains the functions used to analyse financial transactions.
# It calculates running balances, flags large transactions, finds duplicates,
# detects unusual transactions, and calculates totals for each category.

from statistics import mean, stdev


# Generates the running balance after each transaction.
def running_balance(transactions, start=0.0):
    balance = start

    for transaction in transactions:
        balance += transaction.amount
        yield balance


# Creates a function that flags transactions above a chosen amount.
def make_flagger(threshold):
    def flag_transaction(transaction):
        return abs(transaction.amount) > threshold

    return flag_transaction


# Finds transactions that appear more than once.
def find_duplicates(transactions):
    seen = set()
    duplicates = []

    for transaction in transactions:
        signature = (
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.category
        )

        if signature in seen:
            duplicates.append(transaction)
        else:
            seen.add(signature)

    return duplicates


# Finds transactions that are unusually far from the average amount.
def find_outliers(transactions):
    if len(transactions) < 2:
        return []

    amounts = [transaction.amount for transaction in transactions]

    average = mean(amounts)
    standard_deviation = stdev(amounts)

    outliers = []

    for transaction in transactions:
        if abs(transaction.amount - average) > 2 * standard_deviation:
            outliers.append(transaction)

    return outliers


# Calculates the total amount for each transaction category.
def category_totals(transactions):
    totals = {}

    for transaction in transactions:
        category = transaction.category

        if category not in totals:
            totals[category] = 0.0

        totals[category] += transaction.amount

    return totals