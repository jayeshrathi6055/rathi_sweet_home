from dataclasses import asdict
from bson.objectid import ObjectId
from models import Employee

class EmployeeMapper:
    @staticmethod
    def for_save_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict['mobile_number'] = int(emp_dict['mobile_number'])
        emp_dict.pop("_id")
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        return emp_dict

    @staticmethod
    def for_update_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict['mobile_number'] = int(emp_dict['mobile_number'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict.pop("created_at")
        emp_dict.pop("type")
        return emp_dict
