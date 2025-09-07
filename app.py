from flask import Flask
from flask_bootstrap import Bootstrap5
from rathi_sweet_home_database import RathiSweetHomeDatabase
from controllers import home_app, employee_management_app, expense_app

# Initialize app
app = Flask(__name__)

# Initialize Bootstrap5 for UI
bootstrap = Bootstrap5(app)

# Register Controllers
app.register_blueprint(home_app)
app.register_blueprint(employee_management_app)
app.register_blueprint(expense_app)

# Add Extensions
app.extensions['database'] = RathiSweetHomeDatabase(app)


if __name__ == '__main__':
    app.run(debug=True)
