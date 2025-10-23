from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, login_user
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from models import UserRole, UserType
from rathi_sweet_home_database import RathiSweetHomeDatabase
from controllers import *

# Initialize app
app = Flask(__name__)
app.secret_key = 'rathiSweetHomeSecretKey'  # Needed for session cookies

# Initialize Bootstrap5 for UI
bootstrap = Bootstrap5(app)

# Configure Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect here if not logged in

# Register Controllers
app.register_blueprint(home_app)
app.register_blueprint(employee_management_app)
app.register_blueprint(expense_app)

# Global exception handlers
global_exception_handlers(app)

# Add Extensions
app.extensions['database'] = RathiSweetHomeDatabase(app)
database = RathiSweetHomeDatabase(app)

# Handle login
@login_manager.user_loader
def load_user(user_email: str) -> UserRole:
    return database.fetch_user_credentials(user_email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_role: UserRole = database.fetch_user_credentials(email)
        if user_role and check_password_hash(user_role.user_password, password):
            print("Logged in")
            login_user(user_role)  # Starts the session
        else:
            print("Login failed. Signing in...")
            password_hash = generate_password_hash(password)
            new_user_role = UserRole(email, password_hash, UserType.ADMIN)
            database.save_user_credentials(new_user_role)
            login_user(new_user_role)  # Starts the session

        return redirect("/")

    return '''  
        <form method="POST">  
            Email: <input type="text" name="email"><br>  
            Password: <input type="password" name="password"><br>  
            <input type="submit" value="Login">  
        </form>  
    '''

if __name__ == '__main__':
    app.run(debug=True)
