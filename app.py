from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
from employee_transaction_database import EmployeeTransactionDatabase
from models import *
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap5(app)
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
        data['_id'], data['name'] = data['name'].split("_")
        employee = Employee(**data)
        employee_transaction_database.delete_employee(employee)
    elif request.form.get("_method") == 'PUT':
        data['_id'], data['name'] = data['name'].split("_")
        employee = Employee(**data)
        employee_transaction_database.update_employee(employee)
    return redirect('/employeeManagement/allEmployees')


@app.route('/employeeManagement/viewTransactions')
def view_transactions():
    filters = request.args.to_dict()
    user_transactions = employee_transaction_database.fetch_user_transactions(**filters)
    users = employee_transaction_database.fetch_employee()
    return render_template("employee_management/view_transactions.html", user_transactions = user_transactions, users = users)

@app.route('/employeeManagement/saveTransactions', methods=['GET', 'POST'])
def save_transactions():
    if request.method == "POST":
        data = request.form.to_dict()
        employee_transaction = EmployeeTransaction(**data)
        employee_transaction_database.save_transaction(employee_transaction)
    return render_template("employee_management/save_transactions.html", employees = employee_transaction_database.fetch_employee())

if __name__ == '__main__':
    app.run(debug=True)

