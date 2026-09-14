class Transaction:
    transaction_count = 0

    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

        Transaction.transaction_count += 1

    def __str__(self):
        return f"{self.date} | {self.description} | {self.amount:.2f} | {self.category}"

    def is_income(self):
        return self.amount > 0

    def formatted(self):
        return f"{self.date} {self.description} {self.amount:.2f} {self.category}"


class RecurringTransaction(Transaction):
    def __init__(self, date, description, amount, category, frequency):
        super().__init__(date, description, amount, category)
        self.frequency = frequency

    def __str__(self):
        return (
            f"{self.date} | {self.description} | "
            f"{self.amount:.2f} | {self.category} | "
            f"Recurring: {self.frequency}"
        )