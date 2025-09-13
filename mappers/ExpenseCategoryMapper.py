from dataclasses import asdict
from models import ExpenseCategory


class ExpenseCategoryMapper:
    @staticmethod
    def for_save_dict(expense_category: ExpenseCategory):
        expense_category_dict = asdict(expense_category)
        expense_category_dict.pop("_id")
        return expense_category_dict
