from dataclasses import asdict
from models import *

class EmployeeMapper:
    @staticmethod
    def for_save_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict.pop("_id")
        emp_dict['age'] = int(emp_dict['age'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict['monthly_salary_left'] = emp_dict['monthly_salary_base']
        return emp_dict

    @staticmethod
    def for_update_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict['age'] = int(emp_dict['age'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict['monthly_salary_left'] = float(emp_dict['monthly_salary_left'])
        emp_dict.pop("created_at")
        emp_dict.pop("type")
        return emp_dict

    @staticmethod
    def for_delete_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict['age'] = int(emp_dict['age'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict['monthly_salary_left'] = float(emp_dict['monthly_salary_left'])
        emp_dict.pop("created_at")
        return emp_dict

class EmployeeTransactionMapper:
    @staticmethod
    def for_save_dict(employee_transaction: EmployeeTransaction):
        emp_trc_dict = asdict(employee_transaction)
        emp_trc_dict["user_id"] = ObjectId(emp_trc_dict["user_id"])
        emp_trc_dict["amount"] = float(emp_trc_dict["amount"])
        emp_trc_dict.pop("_id")
        return emp_trc_dict

class ExpenseMapper:
    @staticmethod
    def for_save_dict(expense: Expense):
        expense_dict = asdict(expense)
        expense_dict.pop("_id")
        expense_dict['amount'] = float(expense_dict["amount"])
        return expense_dict

class ExpenseCategoryMapper:
    @staticmethod
    def for_save_dict(expense_category: ExpenseCategory):
        expense_category_dict = asdict(expense_category)
        expense_category_dict.pop("_id")
        return expense_category_dict
