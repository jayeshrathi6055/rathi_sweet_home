import calendar
from datetime import datetime, timedelta, date
from decimal import Decimal, ROUND_HALF_UP
from flask import current_app, redirect, render_template, request

from models import Employee, EmployeeAbsence, EmployeeTransaction

class EmployeeManagementService:

    def all_employees(self):
        db = self.__get_db()
        return render_template("employee_management/all_employees.html",
                               employees=db.fetch_active_employee())

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
            data['_id'] = data['name'].split("_")[0]
            db.delete_employee(data['_id'])
        elif request.form.get("_method") == 'PUT':
            data['_id'], data['name'] = data['name'].split("_")
            employee = Employee(**data)
            db.update_employee(employee)
        return redirect('/employeeManagement/allEmployees')

    def view_transactions(self):
        db = self.__get_db()
        filters = request.args.to_dict()
        user_transactions = db.fetch_user_transactions(**filters)
        users = db.fetch_active_employee()
        return render_template("employee_management/view_transactions.html", user_transactions=user_transactions,
                            users=users)

    def save_transactions(self):
        db = self.__get_db()
        if request.method == "POST":
            data = request.form.to_dict()
            employee_transaction = EmployeeTransaction(**data)
            db.save_transaction(employee_transaction)
        return render_template("employee_management/save_transactions.html",
                               employees=db.fetch_active_employee())

    def holidays(self):
        db = self.__get_db()
        if request.method == "POST":
            data = request.form.to_dict()
            start_date, end_date = self.__parse_dates(data.pop('start_date'), data.pop('end_date'))
            while start_date < end_date:
                data['absence_date'] = start_date.isoformat()
                employee_absence = EmployeeAbsence(**data)
                db.save_employee_absence(employee_absence)
                start_date += timedelta(days=1)
        return render_template("employee_management/holidays.html", employees=db.fetch_active_employee())

    def pay_slip(self):
        db = self.__get_db()
        employees = db.fetch_active_employee()
        if request.method == "POST":
            form_data = request.form.to_dict()
            user_id = form_data['user_id']
            start_date, end_date = self.__parse_dates(form_data.get('start_date'), form_data.get('end_date'))

            # Get User details
            user = next((emp for emp in employees if emp['_id'] == user_id), {})

            # Fetch transactions and leaves
            start_iso, end_iso = start_date.isoformat(), end_date.isoformat()
            paid_transactions = db.fetch_transactions_by_id_and_date(user_id, start_iso, end_iso)
            paid_amount = sum(Decimal(str(txn["amount"]))  for txn in paid_transactions)
            leaves = db.fetch_leaves_by_id_and_date(user_id, start_iso, end_iso)

            # Calculate Salary
            working_days, per_day_salary, salary = self.__calculate_salary_days(Decimal(user.get('yearly_salary')), start_date.date(), end_date.date())

            # Prepare report data
            report_data = self.__build_pay_slip_report_data(
                form_data, working_days, per_day_salary, salary, user, paid_transactions, paid_amount, leaves
            )

            return render_template("employee_management/employee_payslip.html",
                                   employees=employees, report_data=report_data)
        return render_template("employee_management/employee_payslip.html", employees=employees)

    def __calculate_salary_days(self, yearly_salary: Decimal, start_date: date, end_date: date):
        year_days = 366 if calendar.isleap(start_date.year) else 365
        per_day_salary = self.decimal_round_half_up(yearly_salary / Decimal(year_days))
        working_days = (end_date - start_date).days
        salary = self.decimal_round_half_up(per_day_salary * working_days)
        return working_days, per_day_salary, salary

    @staticmethod
    def __build_pay_slip_report_data(form_data, working_days, per_day_salary, salary, user, paid_transactions, paid_amount, leaves):
        leave_amount = len(leaves) * per_day_salary
        leave_balance = salary - leave_amount
        paid_balance = leave_balance - paid_amount

        return {
            'start_date': form_data.get('start_date'),
            'end_date': form_data.get('end_date'),
            'working_days': working_days,
            'per_day_salary': per_day_salary,
            'salary': salary,
            'user': user,
            'paid_transactions': paid_transactions,
            'paid_amount': paid_amount,
            'leaves': leaves,
            'leave_amount': leave_amount,
            'leave_balance': leave_balance,
            'paid_balance': paid_balance
        }

    @staticmethod
    def __get_db():
        return current_app.extensions['database']

    @staticmethod
    def decimal_round_half_up(value: Decimal):
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def __parse_dates(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
        return start_date, end_date
