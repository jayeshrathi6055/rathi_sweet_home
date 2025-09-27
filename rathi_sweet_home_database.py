import pymongo
from flask_pymongo import PyMongo

from mappers import *
from models import *

class RathiSweetHomeDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/rathi_sweet_home")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['users']
        self.__transaction_collection = self.__db['transactions']
        self.__employee_absence_collection = self.__db['employee_absences']
        self.__expense_collection = self.__db['expenses']
        self.__expense_category_collection = self.__db['expense_categories']

    # -----------------------Users table operations--------------------------------

    def fetch_active_employee(self, filter_args=None):
        if filter_args is None:
            filter_args = {"type": UserType.EMPLOYEE, "active": True}
        else:
            filter_args["type"] = UserType.EMPLOYEE
            filter_args["active"] = True
        employees = self.__user_collection.find(filter_args).sort("created_at", -1)
        return tuple({**emp, "_id": str(emp["_id"])} for emp in employees)

    def save_employee(self, employee:Employee):
        return self.__user_collection.insert_one(EmployeeMapper.for_save_dict(employee))

    def update_employee(self, employee:Employee):
        employee_dict = EmployeeMapper.for_update_dict(employee)
        employee_id = employee_dict.pop("_id")
        return self.__user_collection.update_one({"_id": employee_id}, {"$set": employee_dict})

    def delete_employee(self, user_id:str):
        return self.__user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {'active': False}})

    # -----------------------Transactions table operations--------------------------------

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
        return self.__transaction_collection.insert_one(EmployeeTransactionMapper.for_save_dict(employee_transaction))

    def fetch_transactions_by_id_and_date(self, user_id: str, start_date: str, end_date: str):
        user_id = ObjectId(user_id)
        return tuple(self.__transaction_collection.find({
            "user_id": user_id,
            "created_at": {
                "$gte": start_date,
                "$lt": end_date
            }}).sort("created_at", -1))

    # -----------------------Expenses table operations--------------------------------

    def fetch_expenses(self, created_date: str):
        return tuple(self.__expense_collection.find({"created_at": created_date}))

    def save_expense(self, expense : Expense):
        return self.__expense_collection.insert_one(ExpenseMapper.for_save_dict(expense))

    # -----------------------Expense Categories table operations--------------------------------

    def fetch_expense_categories(self, filter_args=None):
        if filter_args is None:
            filter_args = {}
        return self.__expense_category_collection.find(filter_args).sort("category", pymongo.ASCENDING)

    def save_expense_category(self, expense_category : ExpenseCategory):
        return self.__expense_category_collection.insert_one(ExpenseCategoryMapper.for_save_dict(expense_category))

    # -----------------------Employee Absences table operations--------------------------------

    def save_employee_absence(self, employee_absence: EmployeeAbsence):
        employee_absence_dict = EmployeeAbsenceMapper.for_save_dict(employee_absence)

        # Check for existing absence
        check_employee_absence = self.__employee_absence_collection.find_one({
            "user_id": employee_absence_dict["user_id"],
            "absence_type": employee_absence_dict["absence_type"],
            "absence_date": employee_absence_dict["absence_date"]
        })
        if check_employee_absence:
            return check_employee_absence

        return self.__employee_absence_collection.insert_one(employee_absence_dict)

    def fetch_upcoming_leaves(self, filters: dict = None):
        if filters is None:
            filters = {}
        filters['absence_date'] = {"$gte": datetime.now().date().isoformat()}
        return tuple(self.__employee_absence_collection.find(filters).sort("absence_date", 1))

    def fetch_leaves_by_id_and_date(self, user_id: str, start_date: str, end_date: str):
        user_id = ObjectId(user_id)
        return tuple(self.__employee_absence_collection.find({
            "user_id": user_id,
            "absence_type": AbsenceType.LEAVE,
            "absence_date": {
                "$gte": start_date,
                "$lt": end_date
            }}).sort("created_at", -1))
