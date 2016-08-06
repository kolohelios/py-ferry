import os
from flask import send_from_directory

from py_ferry import app

root_dir = os.path.relpath('..')

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(root_dir, 'public'), 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(root_dir, 'public'), filename)
