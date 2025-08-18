import pymongo
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from mappers import *

class RathiSweetHomeDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/rathi_sweet_home")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['users']
        self.__transaction_collection = self.__db['transactions']
        self.__employee_absence_collection = self.__db['employee_absences']
        self.__expense_collection = self.__db['expenses']
        self.__expense_category_collection = self.__db['expense_categories']

    def fetch_employee(self, filter_args=None):
        if filter_args is None:
            filter_args = {"type": UserType.EMPLOYEE}
        else:
            filter_args["type"] = UserType.EMPLOYEE
        employees = self.__user_collection.find(filter_args).sort("created_at", -1)
        return tuple({**emp, "_id": str(emp["_id"])} for emp in employees)

    def save_employee(self, employee:Employee):
        return self.__user_collection.insert_one(EmployeeMapper.for_save_dict(employee))

    def update_employee(self, employee:Employee):
        employee_dict = EmployeeMapper.for_update_dict(employee)
        employee_id = employee_dict.pop("_id")
        return self.__user_collection.update_one({"_id": employee_id}, {"$set": employee_dict})

    def delete_employee(self, employee:Employee):
        return self.__user_collection.delete_one(EmployeeMapper.for_delete_dict(employee))

    def fetch_user_transactions(self, **kwargs):
        filter_args = {}
        limit = int(kwargs.get('transactions_limit', 7))
        user_id = kwargs.get('user_id')
        if user_id:
            filter_args["user_id"] = ObjectId(user_id)

        all_transactions = tuple(
            self.__transaction_collection
            .find(filter_args)
            .sort("created_at", -1)
            .limit(limit)
        )

        user_transactions = []
        for i in all_transactions:
            i['user_name'] = self.__user_collection.find_one({"_id": ObjectId(i['user_id'])})['name']
            user_transactions.append(i)

        return all_transactions

    def save_transaction(self, employee_transaction: EmployeeTransaction):
        # Convert transaction to dictionary format
        transaction_dict = EmployeeTransactionMapper.for_save_dict(employee_transaction)

        # Save transaction to the database
        transaction_saved = self.__transaction_collection.insert_one(transaction_dict)

        # Update user's monthly salary left
        user_id = transaction_dict['user_id']
        amount = int(employee_transaction.amount)

        self.__user_collection.update_one(
            {"_id": user_id},
            {"$inc": {"monthly_salary_left": -amount}}
        )

        return transaction_saved

    def fetch_expenses(self, created_date: str):
        return tuple(self.__expense_collection.find({"created_at": created_date}))

    def save_expense(self, expense : Expense):
        return self.__expense_collection.insert_one(ExpenseMapper.for_save_dict(expense))

    def fetch_expense_categories(self, filter_args=None):
        if filter_args is None:
            filter_args = {}
        return self.__expense_category_collection.find(filter_args).sort("category", pymongo.ASCENDING)

    def save_expense_category(self, expense_category : ExpenseCategory):
        return self.__expense_category_collection.insert_one(ExpenseCategoryMapper.for_save_dict(expense_category))

    def save_employee_absence(self, employee_absence: EmployeeAbsence):
        employee_absence_dict = EmployeeAbsenceMapper.for_save_dict(employee_absence)
        check_employee_absence = self.__employee_absence_collection.find_one(employee_absence_dict)

        if check_employee_absence:
            return check_employee_absence

        employee_absence_saved = self.__employee_absence_collection.insert_one(employee_absence_dict)

        user_id = employee_absence_dict['user_id']
        leaves = (date.fromisoformat(employee_absence_dict['end_date']) - date.fromisoformat(employee_absence_dict['start_date'])).days
        saved_employee = self.__user_collection.find_one({"_id": user_id})
        current_employee_leaves = saved_employee["leaves"]
        updated_leaves = current_employee_leaves - leaves

        if current_employee_leaves > 0 and updated_leaves >= 0:
            self.__user_collection.update_one(
                {"_id": user_id},
                {"$inc": {"leaves": -leaves}}
            )
            return employee_absence_saved

        today = datetime.now(ZoneInfo("Asia/Kolkata"))
        no_of_day_in_month = ((today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)).day
        salary_per_day = saved_employee['monthly_salary_base'] / no_of_day_in_month

        if current_employee_leaves <= 0:
            self.__user_collection.update_one(
                {"_id": user_id},
                {"$inc": {"monthly_salary_left": -salary_per_day*leaves, "leaves": -leaves}}
            )
        elif current_employee_leaves > 0 > updated_leaves:
            self.__user_collection.update_one(
                {"_id": user_id},
                {"$inc": {"monthly_salary_left": salary_per_day * updated_leaves, "leaves": -leaves}}
            )

        return employee_absence_saved

