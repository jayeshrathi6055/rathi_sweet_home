from flask_pymongo import PyMongo

class EmployeeTransactionDatabase:

    def __init__(self, flask_app):
        self.__mongo = PyMongo(flask_app, uri="mongodb://localhost:27017/employee_transaction_detail")
        self.__db = self.__mongo.db
        self.__user_collection = self.__db['User']

    def fetch_users(self, filter_args=None):
        if filter_args is None:
            filter_args = {}
        return list(self.__user_collection.find(filter_args))
