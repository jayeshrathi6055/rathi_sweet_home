from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from rathi_sweet_home_database import RathiSweetHomeDatabase
from controllers import *

# Initialize app
app = Flask(__name__)

# Initialize Bootstrap5 for UI
bootstrap = Bootstrap5(app)

# Register Controllers
app.register_blueprint(home_app)
app.register_blueprint(employee_management_app)
app.register_blueprint(expense_app)

# Global exception handlers
global_exception_handlers(app)

# Add Extensions
app.extensions['database'] = RathiSweetHomeDatabase(app)

if __name__ == '__main__':
    app.run(debug=True)
