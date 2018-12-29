from flask_app import app
from flask import render_template


@app.errorhandler(401)
def error_401(e):
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404