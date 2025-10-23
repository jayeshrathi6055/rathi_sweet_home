from flask import Blueprint
from flask_login import login_required
from services.expense_service import ExpenseService

expense_app = Blueprint('expense_controller', __name__)

expense_service = ExpenseService()

@expense_app.route('/expenses')
@login_required
def expenses():
    return expense_service.expenses()


@expense_app.route('/expenses/addExpense', methods=['POST'])
@login_required
def add_expense():
    return expense_service.add_expense()


@expense_app.route('/expenses/addExpenseCategory', methods=['POST'])
@login_required
def add_expense_category():
    return expense_service.add_expense_category()
