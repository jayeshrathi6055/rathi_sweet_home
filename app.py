from flask import Flask
from flask_bootstrap import Bootstrap5
from rathi_sweet_home_database import RathiSweetHomeDatabase
from controllers import *

# Initialize app
app = Flask(__name__)
app.secret_key = 'rathiSweetHomeSecretKey'  # Needed for session cookies

# Initialize Bootstrap5 for UI
bootstrap = Bootstrap5(app)

# Configure Flask Login
login_manager.init_app(app)

# Register Controllers
app.register_blueprint(home_app)
app.register_blueprint(employee_management_app)
app.register_blueprint(expense_app)
app.register_blueprint(auth_app)

# Global exception handlers
global_exception_handlers(app)

# Add Extensions
app.extensions['database'] = RathiSweetHomeDatabase(app)
database = RathiSweetHomeDatabase(app)


if __name__ == '__main__':
    app.run(debug=True)
