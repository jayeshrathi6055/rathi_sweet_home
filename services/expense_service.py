from datetime import datetime
from zoneinfo import ZoneInfo
from flask import current_app, redirect, render_template, request

from models import Expense, ExpenseCategory

class ExpenseService:
    
    def expenses(self):
        db = self.__get_db()
        filters = request.args.to_dict()
        date_of_expenses = filters.get('date', datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat())
        expenses_by_date = db.fetch_expenses(date_of_expenses)
        total_of_expenses = sum([expense['amount'] for expense in expenses_by_date])
        expense_categories = db.fetch_expense_categories()
        return render_template('expenses.html',
                           expense_categories=expense_categories,
                           expenses=expenses_by_date, total_of_expenses=total_of_expenses)
    
    def add_expense(self):
        db = self.__get_db()
        data = request.form.to_dict()
        expense = Expense(**data)
        db.save_expense(expense)
        return redirect('/expenses')
    
    def add_expense_category(self):
        db = self.__get_db()
        data = request.form.to_dict()
        expense_category = ExpenseCategory(**data)
        db.save_expense_category(expense_category)
        return redirect('/expenses')
    
    @staticmethod
    def __get_db():
        return current_app.extensions['database']