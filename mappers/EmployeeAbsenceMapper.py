from dataclasses import asdict
from bson.objectid import ObjectId
from models import EmployeeAbsence


class EmployeeAbsenceMapper:
    @staticmethod
    def for_save_dict(employee_absence: EmployeeAbsence):
        employee_absence_dict = asdict(employee_absence)
        employee_absence_dict['user_id'] = ObjectId(employee_absence_dict["user_id"])
        employee_absence_dict.pop("_id")
        return employee_absence_dict
