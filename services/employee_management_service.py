from datetime import datetime
from flask import current_app, redirect, render_template, request

from models import Employee, EmployeeAbsence, EmployeeTransaction

class EmployeeManagementService:
    
    def all_employees(self):
        db = self.__get_db()
        return render_template("employee_management/all_employees.html",
                           employees=db.fetch_employee())
    
    def action_employee(self):
        db = self.__get_db()
        data = request.form.to_dict()
        data.pop("_method")
        dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        data['date_of_birth'] = datetime.strftime(dob, '%d/%m/%Y')
        if request.form.get("_method") == 'POST':
            employee = Employee(**data)
            db.save_employee(employee)
        elif request.form.get("_method") == 'DELETE':
            data['_id'], data['name'] = data['name'].split("_")
            employee = Employee(**data)
            db.delete_employee(employee)
        elif request.form.get("_method") == 'PUT':
            data['_id'], data['name'] = data['name'].split("_")
            employee = Employee(**data)
            db.update_employee(employee)
        return redirect('/employeeManagement/allEmployees')
    
    def view_transactions(self):
        db = self.__get_db()
        filters = request.args.to_dict()
        user_transactions = db.fetch_user_transactions(**filters)
        users = db.fetch_employee()
        return render_template("employee_management/view_transactions.html", user_transactions=user_transactions,
                            users=users)
        
    def save_transactions(self):
        db = self.__get_db()
        if request.method == "POST":
            data = request.form.to_dict()
            employee_transaction = EmployeeTransaction(**data)
            db.save_transaction(employee_transaction)
        return render_template("employee_management/save_transactions.html",
                            employees=db.fetch_employee())
    
    def holidays(self):
        db = self.__get_db()
        if request.method == "POST":
            data = request.form.to_dict()
            employee_absence = EmployeeAbsence(**data)
            db.save_employee_absence(employee_absence)
        return render_template("employee_management/holidays.html", employees=db.fetch_employee())

    @staticmethod
    def __get_db():
        return current_app.extensions['database']