from flask import request, redirect, current_app, Blueprint
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import *

auth_app = Blueprint('auth_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth_app.login' # Redirect here if not logged in


@login_manager.user_loader
def load_user(user_email: str) -> UserRole:
    return __get_db().fetch_user_credentials(user_email)

@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_role: UserRole = __get_db().fetch_user_credentials(email)
        if user_role and check_password_hash(user_role.user_password, password):
            print("Logged in")
            login_user(user_role)  # Starts the session
        else:
            print("Login failed. Signing in...")
            password_hash = generate_password_hash(password)
            new_user_role = UserRole(email, password_hash, UserType.ADMIN)
            __get_db().save_user_credentials(new_user_role)
            login_user(new_user_role)  # Starts the session

        return redirect("/")

    return '''
        <form method="POST">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@auth_app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


def __get_db():
    return current_app.extensions['database']
