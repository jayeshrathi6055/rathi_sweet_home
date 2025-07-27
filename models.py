from dataclasses import dataclass, asdict
from datetime import date, datetime
from enum import Enum
from bson import ObjectId
from zoneinfo import ZoneInfo


class UserType(str, Enum):
    EMPLOYEE = 'EMPLOYEE'
    ADMIN = 'ADMIN'

@dataclass
class Employee:
    _id: ObjectId = None
    name: str = None
    age: int = None
    street_address: str = None
    city: str = None
    state: str = None
    date_of_birth: date = None
    salary: int = None
    type: str = UserType.EMPLOYEE
    created_at: datetime = datetime.now(ZoneInfo("Asia/Kolkata"))


class EmployeeMapper:
    @staticmethod
    def for_save_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict.pop("_id")
        return emp_dict

    @staticmethod
    def for_update_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict.pop("created_at")
        emp_dict.pop("type")
        return emp_dict

    @staticmethod
    def for_delete_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict.pop("created_at")
        return emp_dict
