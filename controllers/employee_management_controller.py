from flask import Blueprint
from flask_login import login_required
from services.employee_management_service import EmployeeManagementService

employee_management_app = Blueprint('employee_management_controller', __name__)

employee_management_service = EmployeeManagementService()


@employee_management_app.route('/employeeManagement/allEmployees')
@login_required
def all_employees():
    return employee_management_service.all_employees()


@employee_management_app.route('/employeeManagement/allEmployees/actionEmployee', methods=['POST'])
@login_required
def action_employee():
    return employee_management_service.action_employee()


@employee_management_app.route('/employeeManagement/viewTransactions')
@login_required
def view_transactions():
    return employee_management_service.view_transactions()


@employee_management_app.route('/employeeManagement/saveTransactions', methods=['GET', 'POST'])
@login_required
def save_transactions():
    return employee_management_service.save_transactions()


@employee_management_app.route('/employeeManagement/absence', methods=['GET', 'POST'])
@login_required
def absence_tracker():
    return employee_management_service.absence_tracker()


@employee_management_app.route('/employeeManagement/paySlip', methods=['GET', 'POST'])
@login_required
def pay_slip():
    return employee_management_service.pay_slip()

