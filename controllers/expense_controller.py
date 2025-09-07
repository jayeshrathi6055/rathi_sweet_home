from datetime import datetime
from zoneinfo import ZoneInfo
from flask import render_template, request, redirect, Blueprint, current_app

from models import Expense, ExpenseCategory

expense_app = Blueprint('expense_controller', __name__)

def get_database():
    return current_app.extensions['database']

@expense_app.route('/expenses')
def expenses():
    db = get_database()
    filters = request.args.to_dict()
    date_of_expenses = filters.get('date', datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat())
    expenses_by_date = db.fetch_expenses(date_of_expenses)
    total_of_expenses = sum([expense['amount'] for expense in expenses_by_date])
    expense_categories = db.fetch_expense_categories()
    return render_template('expenses.html',
                           expense_categories=expense_categories,
                           expenses=expenses_by_date, total_of_expenses=total_of_expenses)


@expense_app.route('/expenses/addExpense', methods=['POST'])
def add_expense():
    db = get_database()
    data = request.form.to_dict()
    expense = Expense(**data)
    db.save_expense(expense)
    return redirect('/expenses')


@expense_app.route('/expenses/addExpenseCategory', methods=['POST'])
def add_expense_category():
    db = get_database()
    data = request.form.to_dict()
    expense_category = ExpenseCategory(**data)
    db.save_expense_category(expense_category)
    return redirect('/expenses')