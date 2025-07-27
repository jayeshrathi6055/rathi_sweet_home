from bson import ObjectId
from flask_pymongo import PyMongo
from dataclasses import asdict
from models import UserType, Employee, EmployeeMapper

class EmployeeTransactionDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/employee_transaction_detail")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['User']

    def fetch_employee(self, filter_args=None):
        if filter_args is None:
            filter_args = {"type": UserType.EMPLOYEE}
        return tuple(self.__user_collection.find(filter_args).sort("created_at", -1))

    def save_employee(self, employee:Employee):
        return self.__user_collection.insert_one(EmployeeMapper.for_save_dict(employee))

    def update_employee(self, employee:Employee):
        employee_dict = EmployeeMapper.for_update_dict(employee)
        employee_id = employee_dict.pop("_id")
        return self.__user_collection.update_one({"_id": employee_id}, {"$set": employee_dict})

    def delete_employee(self, employee:Employee):
        return self.__user_collection.delete_one(EmployeeMapper.for_delete_dict(employee))
