from dataclasses import asdict
from models import Expense


class ExpenseMapper:
    @staticmethod
    def for_save_dict(expense: Expense):
        expense_dict = asdict(expense)
        expense_dict.pop("_id")
        expense_dict['amount'] = float(expense_dict["amount"])
        return expense_dict
