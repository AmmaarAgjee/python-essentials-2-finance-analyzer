# parser.py
# This file creates a sample bank statement and reads transaction data.
# It cleans the data, validates each row, converts values into the correct
# format, and records rejection reasons for invalid transactions.

from datetime import datetime
from pathlib import Path

from models import Transaction


# Creates a sample bank statement containing valid and invalid transactions.
def generate_sample_file():
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    file_path = data_folder / "statement.txt"

    rows = [
        "2026-08-01,Salary,15000,INCOME",
        "2026-08-02,Groceries,-850.50,FOOD",
        "2026/08/03,Transport,-450,TRANSPORT",
        "2026-08-04,  Coffee Shop  , -75.50 , FOOD",
        "2026-08-05,Rent,-6000,RENT",
        "2026-08-06,Electricity,-950,UTILITIES",
        "2026-08-07,Freelance Work,2500,INCOME",
        "2026-08-08,Groceries,-850.50,FOOD",
        "hello world",
        "2026-08-10,Takeaway,abc,FOOD",
        "2026-08-11,Shopping,-1200",
        "2026-08-12,Wrong Sign,500,EXPENSE",
        "2026-08-13,Netflix,-199,ENTERTAINMENT",
        "2026-08-14,Phone,-399,UTILITIES",
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        for row in rows:
            file.write(row + "\n")

    return str(file_path)


# Loads transactions from a statement file and separates valid and rejected rows.
def load_transactions(path):
    transactions = []
    rejections = []

    try:
        with open(path, "r", encoding="utf-8") as file:

            # Reads the file one transaction at a time.
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                # Skips completely empty lines.
                if not line:
                    continue

                try:
                    # Splits the row into separate fields and removes extra spaces.
                    parts = [part.strip() for part in line.split(",")]

                    # Every valid transaction must contain four fields.
                    if len(parts) != 4:
                        raise ValueError("Expected 4 fields")

                    date_text, description, amount_text, category = parts

                    # Allows dates using "/" to be changed into the required "-".
                    date_text = date_text.replace("/", "-")

                    # Converts the date text into a real date object.
                    date = datetime.strptime(date_text, "%Y-%m-%d").date()

                    # Checks that important text fields are not empty.
                    if not description:
                        raise ValueError("Missing description")

                    if not category:
                        raise ValueError("Missing category")

                    # Converts the transaction amount from text into a float.
                    amount = float(amount_text)

                    # Creates a Transaction object for valid rows.
                    transaction = Transaction(
                        date,
                        description,
                        amount,
                        category.upper()
                    )

                    transactions.append(transaction)

                # Rejects the row without stopping the entire program.
                except (ValueError, TypeError) as error:
                    reason = f"Line {line_number}: {error}"
                    rejections.append(reason)

    # Handles a statement file that does not exist.
    except FileNotFoundError:
        rejections.append(f"File not found: {path}")

    # Handles other problems when trying to read the file.
    except OSError as error:
        rejections.append(f"Could not read file: {error}")

    return transactions, rejections
