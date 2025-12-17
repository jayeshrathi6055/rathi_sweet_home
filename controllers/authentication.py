from flask import request, redirect, current_app, Blueprint, render_template
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from models import *
from utils import set_alert

auth_app = Blueprint('auth_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth_app.login' # Redirect here if not logged in (<app_name>.<method_name>)


@login_manager.user_loader
def load_user(user_email: str) -> UserRole:
    return __get_db().fetch_user_credentials(user_email)

@auth_app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_role: UserRole = __get_db().fetch_user_credentials(email)
        if user_role and check_password_hash(user_role.user_password, password):
            print("Logged in")
            login_user(user_role)  # Starts the session
            return redirect("/")
        else:
            print("Login failed...")
            set_alert("warning", "Invalid credentials.", "Please try again.")

    return render_template("admin_login.html")

@auth_app.route('/admin/logout')
def logout():
    logout_user()
    return redirect("/")

@auth_app.route('/admin/create', methods=['GET', 'POST'])
@login_required
def create_admin():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = generate_password_hash(request.form['password'])
        user_type = UserType.ADMIN
        is_user_present = __get_db().fetch_user_credentials(user_email)
        if not is_user_present:
            user_role = UserRole(user_email, user_password, user_type)
            __get_db().save_user_credentials(user_role)
            return redirect("/admin/login")
        else:
            print("Registration failed...")
            set_alert("warning", "Existing User.", "This user already exists.")

    return render_template("admin_create.html")


def __get_db():
    return current_app.extensions['database']
