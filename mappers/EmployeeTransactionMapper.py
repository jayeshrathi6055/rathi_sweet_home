from dataclasses import asdict
from bson.objectid import ObjectId
from models import EmployeeTransaction


class EmployeeTransactionMapper:
    @staticmethod
    def for_save_dict(employee_transaction: EmployeeTransaction):
        emp_trc_dict = asdict(employee_transaction)
        emp_trc_dict["user_id"] = ObjectId(emp_trc_dict["user_id"])
        emp_trc_dict["amount"] = float(emp_trc_dict["amount"])
        emp_trc_dict.pop("_id")
        return emp_trc_dict
