from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
from rathi_sweet_home_database import RathiSweetHomeDatabase
from models import *
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap5(app)
rathi_sweet_home_database = RathiSweetHomeDatabase(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/employeeManagement')
def employee_management():
    return render_template("employee_management/employee_management_dashboard.html")

@app.route('/employeeManagement/allEmployees')
def all_employees():
    return render_template("employee_management/all_employees.html", employees = rathi_sweet_home_database.fetch_employee())

@app.route('/employeeManagement/allEmployees/actionEmployee', methods=['POST'])
def action_employee():
    data = request.form.to_dict()
    data.pop("_method")
    dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    data['date_of_birth'] = datetime.strftime(dob, '%d/%m/%Y')
    if request.form.get("_method") == 'POST':
        employee = Employee(**data)
        rathi_sweet_home_database.save_employee(employee)
    elif request.form.get("_method") == 'DELETE':
        data['_id'], data['name'] = data['name'].split("_")
        employee = Employee(**data)
        rathi_sweet_home_database.delete_employee(employee)
    elif request.form.get("_method") == 'PUT':
        data['_id'], data['name'] = data['name'].split("_")
        employee = Employee(**data)
        rathi_sweet_home_database.update_employee(employee)
    return redirect('/employeeManagement/allEmployees')


@app.route('/employeeManagement/viewTransactions')
def view_transactions():
    filters = request.args.to_dict()
    user_transactions = rathi_sweet_home_database.fetch_user_transactions(**filters)
    users = rathi_sweet_home_database.fetch_employee()
    return render_template("employee_management/view_transactions.html", user_transactions = user_transactions, users = users)

@app.route('/employeeManagement/saveTransactions', methods=['GET', 'POST'])
def save_transactions():
    if request.method == "POST":
        data = request.form.to_dict()
        employee_transaction = EmployeeTransaction(**data)
        rathi_sweet_home_database.save_transaction(employee_transaction)
    return render_template("employee_management/save_transactions.html", employees = rathi_sweet_home_database.fetch_employee())

@app.route('/expenses')
def expenses():
    expense_categories = rathi_sweet_home_database.fetch_expense_categories()
    expenses_by_date = rathi_sweet_home_database.fetch_expenses(datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat())
    return render_template('expenses.html', expense_categories = expense_categories, expenses = expenses_by_date)

@app.route('/expenses/addExpense', methods=['POST'])
def add_expense():
    data = request.form.to_dict()
    expense = Expense(**data)
    rathi_sweet_home_database.save_expense(expense)
    return redirect('/expenses')

@app.route('/expenses/addExpenseCategory', methods=['POST'])
def add_expense_category():
    data = request.form.to_dict()
    expense_category = ExpenseCategory(**data)
    rathi_sweet_home_database.save_expense_category(expense_category)
    return redirect('/expenses')

if __name__ == '__main__':
    app.run(debug=True)

