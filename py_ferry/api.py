import os.path
import json

from flask import request, Response, url_for, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
# from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from py_ferry import app
from .database import session

@app.route('/api/ferry_classes', methods = ['GET'])
@decorators.accept('application/json')
def ferry_classes_get():
    ''' get a list of ferry classes '''
    
    ferry_classes = session.query(models.Ferry_Class)
    ferry_classes = ferry_classes.order_by(models.Ferry_Class.cost)

    data = json.dumps([ferry_class.as_dictionary() for ferry_class in ferry_classes])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/ferries', methods = ['GET'])
@login_required
@decorators.accept('application/json')
def ferries_get():
    ''' get a list player ferries '''
    
    print(current_user)
    
    ferries = session.query(models.Ferry).filter(models.Ferry.owner == current_user)
    # ferry = ferry.order_by(models.Ferry_Class.cost)

    data = json.dumps([ferry.as_dictionary() for ferry in ferries])
    print(data)
    return Response(data, 200, mimetype = 'application/json')