from flask_pymongo import PyMongo
from mappers import *

class EmployeeTransactionDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/employee_transaction_detail")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['User']
        self.__transaction_collection = self.__db['Transaction']

    def fetch_employee(self, filter_args=None):
        if filter_args is None:
            filter_args = {"type": UserType.EMPLOYEE}
        employees = self.__user_collection.find(filter_args)
        sorted_employees = sorted(employees, key=lambda employee: employee.get('created_at', datetime.now()), reverse=True)
        return tuple({**emp, "_id": str(emp["_id"])} for emp in sorted_employees)

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
        limit = int(kwargs.get('transactions_limit', 0))
        user_id = kwargs.get('user_id')
        if not limit:
            limit = 7
        if user_id:
            filter_args["user_id"] = ObjectId(user_id)
        all_transactions = tuple(self.__transaction_collection.find(filter_args).limit(limit))
        sorted_transactions = sorted(all_transactions, key=lambda t: datetime.fromisoformat(t.get("created_at", datetime.now())), reverse=True)
        user_transactions = []
        for i in sorted_transactions:
            i['user_name'] = self.__user_collection.find_one({"_id": ObjectId(i['user_id'])})['name']
            user_transactions.append(i)
        return user_transactions

    def save_transaction(self, employee_transaction:EmployeeTransaction):
        return self.__transaction_collection.insert_one(EmployeeTransactionMapper.for_save_dict(employee_transaction))
