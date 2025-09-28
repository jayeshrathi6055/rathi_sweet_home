from flask import render_template

def global_exception_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("index.html"), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        return render_template("error.html", error=str(e)), 500
