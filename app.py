from flask import Flask, render_template
from employee_transaction_database import EmployeeTransactionDatabase

app = Flask(__name__)
employee_transaction_database = EmployeeTransactionDatabase(app)

@app.route('/')
def home():
    users = employee_transaction_database.fetch_users()
    return render_template("index.html", users=users)

if __name__ == '__main__':
    app.run(debug=True)

