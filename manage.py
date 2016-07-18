import os, json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from py_ferry.database import session, Base
from getpass import getpass
from werkzeug.security import generate_password_hash
from pprint import pprint

from py_ferry import app
from py_ferry.models import User
from py_ferry import models
# might be better to load these dynamically for the importdata function

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host = '0.0.0.0', port = port)
    
@manager.command
def test():
    if not 'CONFIG_PATH' in os.environ:
        os.environ['CONFIG_PATH'] = 'py_ferry.config.TestingConfig'
    os.system('nosetests')

@manager.command
def importdata():
    ''' import data from data.json '''
    with open('data.json') as data_file:
        data = json.load(data_file)
    
    for collection in data:
        model_name = collection['model_name']
        data_records = collection['data']
        count = 0
        for data_record in data_records:
            try:
                model = getattr(models, model_name)
                item = model(**data_record)
                session.add(item)
                session.commit()
            except Exception as e:
                print(type(e), 'for {}'.format(model_name))
            else:
                count += 1
                pass
                
        if count == len(data_records):
            print('Successfully imported all {} records of type {}'.format(count, model_name))
        else:
            print('{} records of {} were imported of type {}'.format(count, len(data_records), model_name))
    
@manager.command
def adduser():
    name = input('Name: ')
    email = input('Email: ')
    if session.query(User).filter_by(email = email).first():
        print('User with that email address already exists.')
        return
    
    password = ''
    password_2 = ''
    while len(password) < 8 or password != password_2:
        password = getpass('Password: ')
        password_2 = getpass('Re-enter password: ')
    user = User(name = name, email = email, password = generate_password_hash(password))
    session.add(user)
    session.commit()
    
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()