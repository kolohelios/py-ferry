import os
from flask import send_from_directory, send_file

from py_ferry import app

root_dir = os.path.relpath('..')

@app.route('/')
def serve_index():
    return send_file(os.path.join(root_dir, 'public/index.html'))

@app.route('/<path:filename>')
def serve_static(filename):
    for extension in ['.js', '.css', '.png', '.eot', '.svg', '.ttf', '.woff', '.woff2', '.otf', '.map']:
        if extension in filename:
            return send_from_directory(os.path.join(root_dir, 'public'), filename)
    return send_file(os.path.join(root_dir, 'public/index.html'))
