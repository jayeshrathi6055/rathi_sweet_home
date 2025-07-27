from bson import ObjectId
from flask_pymongo import PyMongo
from dataclasses import asdict
from models import UserType
from datetime import datetime

class EmployeeTransactionDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/employee_transaction_detail")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['User']

    def fetch_employee(self, filter_args=None):
        if filter_args is None:
            filter_args = {"type": UserType.EMPLOYEE}
        return tuple(self.__user_collection.find(filter_args).sort("created_at", -1))

    def save_employee(self, employee):
        employee = asdict(employee)
        employee['created_at'] = datetime.now()
        employee.pop("_id")
        saved_employee = self.__user_collection.insert_one(employee)
        return saved_employee

    def update_employee(self, employee):
        employee = asdict(employee)
        employee_id = employee.pop("_id")
        return self.__user_collection.update_one({"_id": ObjectId(employee_id)}, {"$set": employee})

    def delete_employee(self, employee):
        employee = asdict(employee)
        employee.pop("_id")
        return self.__user_collection.delete_one(employee)
