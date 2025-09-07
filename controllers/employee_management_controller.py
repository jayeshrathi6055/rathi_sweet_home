from datetime import datetime
from flask import Blueprint, render_template, request, current_app, redirect

from models import Employee, EmployeeAbsence, EmployeeTransaction

employee_management_app = Blueprint('employee_management_controller', __name__)

def get_database():
    return current_app.extensions['database']

@employee_management_app.route('/employeeManagement/allEmployees')
def all_employees():
    db = get_database()
    return render_template("employee_management/all_employees.html",
                           employees=db.fetch_employee())


@employee_management_app.route('/employeeManagement/allEmployees/actionEmployee', methods=['POST'])
def action_employee():
    db = get_database()
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


@employee_management_app.route('/employeeManagement/viewTransactions')
def view_transactions():
    db = get_database()
    filters = request.args.to_dict()
    user_transactions = db.fetch_user_transactions(**filters)
    users = db.fetch_employee()
    return render_template("employee_management/view_transactions.html", user_transactions=user_transactions,
                           users=users)


@employee_management_app.route('/employeeManagement/saveTransactions', methods=['GET', 'POST'])
def save_transactions():
    db = get_database()
    if request.method == "POST":
        data = request.form.to_dict()
        employee_transaction = EmployeeTransaction(**data)
        db.save_transaction(employee_transaction)
    return render_template("employee_management/save_transactions.html",
                           employees=db.fetch_employee())


@employee_management_app.route('/employeeManagement/holidays', methods=['GET', 'POST'])
def holidays():
    db = get_database()
    if request.method == "POST":
        data = request.form.to_dict()
        employee_absence = EmployeeAbsence(**data)
        db.save_employee_absence(employee_absence)
    return render_template("employee_management/holidays.html", employees=db.fetch_employee())

