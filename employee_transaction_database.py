from flask_pymongo import PyMongo
from dataclasses import asdict
from models import UserType

class EmployeeTransactionDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/employee_transaction_detail")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['User']

    def fetch_employee(self, filter_args=None):
        if filter_args is None:
            filter_args = {"type": UserType.EMPLOYEE}
        return tuple(self.__user_collection.find(filter_args))

    def save_employee(self, employee):
        saved_employee = self.__user_collection.insert_one(asdict(employee))
        return saved_employee
