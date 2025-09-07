from flask import Blueprint
from services.employee_management_service import EmployeeManagementService

employee_management_app = Blueprint('employee_management_controller', __name__)

employee_management_service = EmployeeManagementService()


@employee_management_app.route('/employeeManagement/allEmployees')
def all_employees():
    return employee_management_service.all_employees()


@employee_management_app.route('/employeeManagement/allEmployees/actionEmployee', methods=['POST'])
def action_employee():
    return employee_management_service.action_employee()


@employee_management_app.route('/employeeManagement/viewTransactions')
def view_transactions():
    return employee_management_service.view_transactions()


@employee_management_app.route('/employeeManagement/saveTransactions', methods=['GET', 'POST'])
def save_transactions():
    return employee_management_service.save_transactions()


@employee_management_app.route('/employeeManagement/holidays', methods=['GET', 'POST'])
def holidays():
    return employee_management_service.holidays()

