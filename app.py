from flask import Flask, render_template, request, redirect
from employee_transaction_database import EmployeeTransactionDatabase
from models import Employee
from datetime import datetime

app = Flask(__name__)
employee_transaction_database = EmployeeTransactionDatabase(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/employeeManagement')
def employee_management():
    return render_template("employee_management/employee_management_dashboard.html")

@app.route('/employeeManagement/allEmployees')
def all_employees():
    return render_template("employee_management/all_employees.html", employees = employee_transaction_database.fetch_employee())

@app.route('/employeeManagement/allEmployees/actionEmployee', methods=['POST'])
def action_employee():
    data = request.form.to_dict()
    data.pop("_method")
    dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    data['date_of_birth'] = datetime.strftime(dob, '%d/%m/%Y')
    if request.form.get("_method") == 'POST':
        employee = Employee(**data)
        employee_transaction_database.save_employee(employee)
    elif request.form.get("_method") == 'DELETE':
        data['name'] = data['name'].split("_")[1]
        employee = Employee(**data)
        employee_transaction_database.delete_employee(employee)
    elif request.form.get("_method") == 'PUT':
        data['_id'], data['name'] = data['name'].split("_")
        employee = Employee(**data)
        employee_transaction_database.update_employee(employee)
    return redirect('/employeeManagement/allEmployees')

if __name__ == '__main__':
    app.run(debug=True)

