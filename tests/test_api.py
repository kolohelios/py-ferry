import unittest
import os
import sys
import shutil
import json

from werkzeug.security import generate_password_hash

try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse
from io import StringIO, BytesIO

import sys

from py_ferry import app
from py_ferry import models
from py_ferry.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the py_ferry API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)
        
        # create an example user
        self.user = models.User(name = 'capnmorgan', email = 'rumshine@gmail.com', 
            password = generate_password_hash('test'))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        ''' Test teardown '''
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session['user_id'] = str(self.user.id)
            http_session['_fresh'] = True
        
    def test_get_with_unsupported_accept_header(self):
        ''' test getting all ferries with an unsupported accept header '''
        response = self.client.get('/api/ferry_classes',
            headers = [('Accept', 'application/xml')]
        )
        
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['message'],
            'Request must accept application/json data')
            
    def test_get_empty_ferry_classes(self):
        ''' test getting empty ferry classes '''
        response = self.client.get('/api/ferry_classes',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 0)
        
    def test_get_ferry_classes(self):
        ''' get all ferry classes '''
        ferry_class_props = { 
            'name': 'Jumbo Mark II',
            'passengers': 2500,
            'cars': 202,
            'max_commercial': 60,
            'speed': 21,
            'burn_rate': 350
        }
        ferry_class_A = models.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            max_commercial = ferry_class_props['max_commercial'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
        )
        ferry_class_B = models.Ferry_Class()
        session.add_all([ferry_class_A, ferry_class_B])
        session.commit()
        
        response = self.client.get('/api/ferry_classes',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 2)
        
        ferry_class_A = data[0]
        for key, value in ferry_class_props.items():
            self.assertEqual(ferry_class_A[key], value)
        
    def test_get_ferries(self):
        ''' get all ferries '''
        self.simulate_login()
        
        bob = models.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com')
        george = models.User(name = 'bestsysmgr', email = 'bestsysmgr@gmail.com')
        ferry_class_props = { 'name': 'Jumbo Mark II' }
        ferry_class = models.Ferry_Class(name = ferry_class_props['name'])

        ferryA = models.Ferry(name = 'Puget Rider', ferry_class = ferry_class, owner = self.user)
        ferryB = models.Ferry(ferry_class = ferry_class, owner = george)

        session.add_all([bob, george, ferry_class, ferryA, ferryB])
        session.commit()
        
        response = self.client.get('/api/ferries',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 1)
        
        ferryA = data[0]
        print(ferryA)
        self.assertEqual(ferryA['ferry_class']['name'], ferry_class_props['name'])
        self.assertEqual(ferryA['name'], 'Puget Rider')
        
if __name__ == '__main__':
    unittest.main()