from dataclasses import asdict
from bson.objectid import ObjectId
from models import Employee

class EmployeeMapper:
    @staticmethod
    def for_save_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict.pop("_id")
        emp_dict['age'] = int(emp_dict['age'])
        emp_dict['leaves'] = int(emp_dict['leaves'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict['monthly_salary_left'] = emp_dict['monthly_salary_base']
        return emp_dict

    @staticmethod
    def for_update_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict['age'] = int(emp_dict['age'])
        emp_dict['leaves'] = int(emp_dict['leaves'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict['monthly_salary_left'] = float(emp_dict['monthly_salary_left'])
        emp_dict.pop("created_at")
        emp_dict.pop("type")
        return emp_dict

    @staticmethod
    def for_delete_dict(employee: Employee):
        emp_dict = asdict(employee)
        emp_dict["_id"] = ObjectId(emp_dict["_id"])
        emp_dict['age'] = int(emp_dict['age'])
        emp_dict['leaves'] = int(emp_dict['leaves'])
        emp_dict['monthly_salary_base'] = float(emp_dict['monthly_salary_base'])
        emp_dict['monthly_salary_left'] = float(emp_dict['monthly_salary_left'])
        emp_dict.pop("created_at")
        return emp_dict
