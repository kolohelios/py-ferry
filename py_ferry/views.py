from flask import render_template

from py_ferry import app

@app.route("/")
def index():
    return app.send_static_file("index.html")
