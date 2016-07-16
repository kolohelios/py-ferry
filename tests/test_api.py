import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse
from io import StringIO, BytesIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "py_ferry.config.TestingConfig"

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

    def tearDown(self):
        ''' Test teardown '''
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
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
            'cars': 200,
            'trucks': 60,
            'speed': 21,
            'burn_rate': 350
        }
        ferry_class_A = models.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            trucks = ferry_class_props['trucks'],
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
        ferry_class_props = { 'name': 'Jumbo Mark II' }
        ferry_class = models.Ferry_Class(name = ferry_class_props['name'])

        ferry = models.Ferry(ferry_class = ferry_class)

        session.add_all([ferry_class, ferry])
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
        
if __name__ == '__main__':
    unittest.main()