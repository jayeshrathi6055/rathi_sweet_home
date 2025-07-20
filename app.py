from flask import Flask, render_template
from employee_transaction_database import EmployeeTransactionDatabase

app = Flask(__name__)
employee_transaction_database = EmployeeTransactionDatabase(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/employeeManagement')
def employee_management():
    return render_template("employee_management/employee_management_dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)

