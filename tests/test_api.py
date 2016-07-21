import unittest
import os
import sys
import shutil
import json
from datetime import datetime

from werkzeug.security import generate_password_hash

try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse
from io import StringIO, BytesIO

import sys

from py_ferry import app
from py_ferry import database
from py_ferry.database import Base, engine, session

def unix_timestamp(date_time):
    if not date_time:
        return None
    return int(date_time.strftime("%s"))

class TestAPI(unittest.TestCase):
    """ Tests for the py_ferry API """

    def setUp(self):
        """ test setup """
        self.client = app.test_client()

        # set up the tables in the database
        Base.metadata.create_all(engine)
        
        # create an example user
        self.user = database.User(name = 'capnmorgan', email = 'rumshine@gmail.com', 
            password = generate_password_hash('test'))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        ''' test teardown '''
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
        ''' test getting empty ferry class list '''
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
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            max_commercial = ferry_class_props['max_commercial'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
        )
        
        # ferry_class_B is a red herring for testing
        ferry_class_B = database.Ferry_Class()
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
        
    def test_get_empty_terminals(self):
        ''' test getting empty terminal list '''
        response = self.client.get('/api/terminals',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 0)    
        
    def test_get_terminals(self):
        ''' test getting a couple of terminals '''
        
        terminalA = database.Terminal(name = 'Timbuktu', lat = 111.1111, lon = -122.2222)
        terminalB = database.Terminal(name = 'Never Never Land', lat = 33.3333, lon = -160.9999)
        
        session.add_all([terminalA, terminalB])
        session.commit()
        
        response = self.client.get('/api/terminals',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 2)
        
        # we have to switch the indexes because the API returns results sorted by name
        terminalA = data[1]
        terminalB = data[0]
        self.assertEqual(terminalA['name'], 'Timbuktu')
        self.assertEqual(terminalA['lat'], 111.1111)
        self.assertEqual(terminalA['lon'], -122.2222)
        self.assertEqual(terminalB['name'], 'Never Never Land')
        self.assertEqual(terminalB['lat'], 33.3333)
        self.assertEqual(terminalB['lon'], -160.9999)
    
    def test_get_ferries(self):
        ''' get all ferries associated with a player's game '''
        self.simulate_login()
        
        # Bob and George are red herrings for testing
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com')
        george = database.User(name = 'bestsysmgr', email = 'bestsysmgr@gmail.com')
        ferry_class_props = { 'name': 'Jumbo Mark II' }
        ferry_class = database.Ferry_Class(name = ferry_class_props['name'])
        gameA = database.Game(player = self.user)
        gameB = database.Game(player = george)

        ferryA = database.Ferry(name = 'Puget Rider', ferry_class = ferry_class, game = gameA)
        ferryB = database.Ferry(ferry_class = ferry_class, game = gameB)

        session.add_all([bob, george, ferry_class, gameA, gameB, ferryA, ferryB])
        session.commit()
        
        response = self.client.get('/api/games/' + str(gameA.id) + '/ferries',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 1)
        
        ferryA = data[0]
        self.assertEqual(ferryA['ferry_class']['name'], ferry_class_props['name'])
        self.assertEqual(ferryA['name'], 'Puget Rider')
        
    def test_get_new_game(self):
        ''' get a new game for the current user '''
        self.simulate_login()
        
        game = database.Game(player = self.user)
        
        session.add_all([game])
        session.commit()
        
        response = self.client.get('/api/games',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 1)
        
        game = data[0]
        self.assertEqual(game['player']['id'], self.user.id)
        self.assertLessEqual(game['created_date'], unix_timestamp(datetime.now()))
        self.assertEqual(game['cash_available'], 0)
        
    def test_get_empty_routes(self):
        ''' try to get routes for a game where none exist '''
        self.simulate_login()
        
        game = database.Game(player = self.user)
        
        session.add_all([game])
        session.commit()
        
        response = self.client.get('/api/games/' + str(game.id) + '/routes',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 0)
        
    def test_get_routes(self):
        ''' get a new game for the current user '''
        self.simulate_login()
        
        game = database.Game(player = self.user)
        
        seattle = database.Terminal(name = 'Seattle', lat = 47.6025001, lon = -122.33857590000002)
        bainbridge_island = database.Terminal(name = 'Bainbridge Island', lat = 47.623089, lon = -122.511171)
        
        route = database.Route(game = game, first_terminal = seattle, second_terminal = bainbridge_island)
        
        session.add_all([game, seattle, bainbridge_island])
        session.commit()
        
        response = self.client.get('/api/games/' + str(game.id) + '/routes',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 1)
        
        route = data[0]
        print(route)
        self.assertEqual(route['game']['player']['id'], self.user.id)
        self.assertAlmostEqual(route['route_distance'], 7.47, 2)
        # self.assertLessEqual(game['created_date'], unix_timestamp(datetime.now()))
        # self.assertEqual(game['cash_available'], 0)  
        
    def test_game_endturn(self):
        ''' end the current turn, run the simulation cycle, and test the response '''
        self.simulate_login()
        
        # create a new game
        game = database.Game(player = self.user)
        
        # create terminals
        seattle = database.Terminal(name = 'Seattle', lat = 47.6025001, lon = -122.33857590000002)
        bainbridge_island = database.Terminal(name = 'Bainbridge Island', lat = 47.623089, lon = -122.511171)
        
        # create route
        route = database.Route(game = game, first_terminal = seattle, second_terminal = bainbridge_island)
        
        # TODO ferry_class_props should be moved outside of this function as it duplicates an object for another test
        # create a ferry class
        ferry_class_props = { 
            'name': 'Jumbo Mark II',
            'passengers': 2500,
            'cars': 202,
            'max_commercial': 60,
            'speed': 21,
            'burn_rate': 350
        }
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            max_commercial = ferry_class_props['max_commercial'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
        )
        
        ferry = database.Ferry(game = game, ferry_class = ferry_class_A, route = route)
        
        session.add_all([game, seattle, bainbridge_island, route, ferry_class_A, ferry])
        session.commit()
        
        response = self.client.get('/api/games/' + str(game.id) + '/endturn',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['message'], 'success')

        response = self.client.get('/api/games/' + str(game.id),
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        # self.assertEqual(len(data), 1)
        
        self.assertEqual(data['current_week'], 1)
    
    
if __name__ == '__main__':
    unittest.main()