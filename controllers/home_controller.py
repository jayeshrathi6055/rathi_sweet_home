from flask import Blueprint, render_template

home_app = Blueprint('home_controller', __name__)

@home_app.route('/')
def home():
    return render_template("index.html")
