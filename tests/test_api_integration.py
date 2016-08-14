import unittest
import os
import sys
import shutil
import json
from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_jwt import JWT

try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse
from io import StringIO, BytesIO

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
        
    def get_jwt(self, name, password):
        data = {
            "name": name,
            "password": password
        }
            
        response = self.client.post(app.config['JWT_AUTH_URL_RULE'],
            data = json.dumps(data),
            content_type = 'application/json',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        token = data['access_token']
        
        return token
    
    # def simulate_login(self):
    #     with self.client.session_transaction() as http_session:
    #         http_session['user_id'] = str(self.user.id)
    #         http_session['_fresh'] = True
        
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
            
    def test_register(self):
        ''' test the user registration endpoint of the API '''
        data = {
            "email": "joe@joeshome.com",
            "password": "notsecret",
            "name": "BestBureaucrat"
        }
        
        response = self.client.post('/api/register',
            data = json.dumps(data),
            content_type = 'application/json',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['status'], 'Success')
        self.assertEqual(data['data'], None)
        self.assertEqual(data['message'], None)
        
    def test_register_already_exists_email(self):
        ''' test the user registration endpoint of the API where the user
            already exists '''
        user = database.User(
            email = 'joe@joeshome.com', 
            password = 'notsecret',
            name = 'BestBureaucrat'
        )
        session.add(user)
        session.commit()
        
        data = {
            "email": "joe@joeshome.com",
            "password": "notsecret",
            "name": "Second Account"
        }
        
        response = self.client.post('/api/register',
            data = json.dumps(data),
            content_type = 'application/json',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['status'], 'Error')
        self.assertEqual(data['data'], None)
        self.assertEqual(data['message'], 'This email address is already being used.')
        
    def test_register_already_exists_name(self):
        ''' test the user registration endpoint of the API where the user
            already exists '''
        user = database.User(
            email = 'joe@joeshome.com', 
            password = 'notsecret',
            name = 'BestBureaucrat'
        )
        session.add(user)
        session.commit()
        
        data = {
            "email": "bob@msbob.com",
            "password": "notsecret",
            "name": "BestBureaucrat"
        }
        
        response = self.client.post('/api/register',
            data = json.dumps(data),
            content_type = 'application/json',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['status'], 'Error')
        self.assertEqual(data['data'], None)
        self.assertEqual(data['message'], 'This username is already being used.')
        
    def test_login(self):
        ''' test a successful login '''
        user = database.User(
            email = 'joe@joeshome.com', 
            password = generate_password_hash('notsecret'),
            name = 'BestBureaucrat'
        )
        session.add(user)
        session.commit()
        
        data = {
            "name": "BestBureaucrat",
            "password": "notsecret"
        }
        
        response = self.client.post(app.config['JWT_AUTH_URL_RULE'],
            data = json.dumps(data),
            content_type = 'application/json',
            headers = [('Accept', 'application/json')]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        token = data['access_token']
        
        response = self.client.get('/api/user',
            data = json.dumps(data),
            content_type = 'application/json',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['id'], 2)
        self.assertEqual(data['name'], 'BestBureaucrat')
        
    # TODO use this test, or something similar, when I figure out how to add a refresh token endpoint
    # def test_refresh_token(self):
    #     ''' test refreshing a token '''
        
    #     pw = 'notsecret'
    #     bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
    #     session.add(bob)
    #     session.commit()
        
    #     token = self.get_jwt(bob.name, pw)
        
    #     response = self.client.get('/api/refresh_token',
    #         headers = [
    #             ('Accept', 'application/json'),
    #             ('Authorization', 'JWT ' + token)    
    #         ]
    #     )
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.mimetype, 'application/json')
        
    #     data = json.loads(response.data.decode('ascii'))
    #     print(data)
    #     self.assertEqual(len(data), 0)
        
        
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
            'trucks': 60,
            'speed': 21,
            'burn_rate': 350
        }
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            trucks = ferry_class_props['trucks'],
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
        
        # George is a red herring for testing
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        george = database.User(name = 'bestsysmgr', email = 'bestsysmgr@gmail.com', password = generate_password_hash(pw))
        ferry_class_props = { 'name': 'Jumbo Mark II', 'usable_life': 60, 'residual_value': 1000000, 'cost': 1000000 }
        ferry_class = database.Ferry_Class(
            name = ferry_class_props['name'], usable_life = ferry_class_props['usable_life'], 
            residual_value = ferry_class_props['residual_value'], cost = ferry_class_props['cost']
        )
        gameA = database.Game(player = bob)
        gameB = database.Game(player = george)

        ferryA = database.Ferry(name = 'Puget Rider', ferry_class = ferry_class, game = gameA, launched = 2000)
        ferryB = database.Ferry(ferry_class = ferry_class, game = gameB, launched = 2000)

        session.add_all([bob, george, ferry_class, gameA, gameB, ferryA, ferryB])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.get('/api/games/' + str(gameA.id) + '/ferries',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 1)
        
        ferryA = data[0]
        self.assertEqual(ferryA['ferry_class']['name'], ferry_class_props['name'])
        self.assertEqual(ferryA['name'], 'Puget Rider')
        
    def test_get_new_game(self):
        ''' get a new game for a user '''
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        session.add(bob)
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.post('/api/games',
             headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 8)
        
        self.assertEqual(data['player']['id'], bob.id)
        self.assertLessEqual(data['created_date'], unix_timestamp(datetime.now()))
        self.assertEqual(data['cash_available'], 1000000)
        self.assertEqual(data['current_week'], 1)
        self.assertEqual(data['current_year'], 2000)
        
    def test_delete_game(self):
        ''' delete a game for a user '''
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        game = database.Game(player = bob)
        
        session.add_all([bob, game])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.delete('/api/games/' + str(game.id),
             headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 8)
        
        self.assertEqual(data['player']['id'], bob.id)
        self.assertLessEqual(data['created_date'], unix_timestamp(datetime.now()))
        self.assertEqual(data['cash_available'], 1000000)
        self.assertEqual(data['current_week'], 1)
        self.assertEqual(data['current_year'], 2000)
        
        # now, make sure that there are precisely zero games
        response = self.client.get('/api/games',
             headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 0)
        
    def test_delete_game_failure(self):
        ''' try to delete someone else's game '''
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        george = database.User(name = 'bestsysmgr', email = 'bestsysmgr@gmail.com', password = generate_password_hash(pw))
        
        game = database.Game(player = bob)
        
        session.add_all([bob, george, game])
        session.commit()
        
        token = self.get_jwt(george.name, pw)
        
        response = self.client.delete('/api/games/' + str(game.id),
             headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.mimetype, 'application/json')
        
        # and now make sure that Bob still has his game
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.get('/api/games/' + str(game.id),
             headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 8)
    
    def test_ferry_post(self):
        ''' test the purchasing of a ferry '''
        
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        ferry_class_props = { 
            'name': 'Jumbo Mark II',
            'passengers': 2500,
            'cars': 202,
            'trucks': 60,
            'speed': 21,
            'burn_rate': 350,
            'turnover_time': 0.2,
            'cost': 50000,
            'residual_value': 4000,
            'usable_life': 60
        }
        
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            trucks = ferry_class_props['trucks'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
            turnover_time = ferry_class_props['turnover_time'],
            cost = ferry_class_props['cost'],
            residual_value = ferry_class_props['residual_value'],
            usable_life = ferry_class_props['usable_life']
        )
        
        game = database.Game(player = bob)
        
        session.add_all([bob, game, ferry_class_A])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        data = {
            "classId": ferry_class_A.id,
            "name": "M/V Wenatchee"
        }
        
        response = self.client.post('/api/games/' + str(game.id) + '/ferries',
            data = json.dumps(data),
            # TODO all PUT and POST requests should have content_type
            content_type = 'application/json',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ],
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 7)
        
    def test_ferry_post_insufficient_funds(self):
        ''' test the purchasing of a ferry when player doesn't have enough available cash '''
        
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        ferry_class_props = { 
            'name': 'Jumbo Mark II',
            'passengers': 2500,
            'cars': 202,
            'trucks': 60,
            'speed': 21,
            'burn_rate': 350,
            'turnover_time': 0.2,
            'cost': 50000000
        }
        
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            trucks = ferry_class_props['trucks'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
            turnover_time = ferry_class_props['turnover_time'],
            cost = ferry_class_props['cost'],
        )
        
        game = database.Game(player = bob)
        
        session.add_all([bob, game, ferry_class_A])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        data = {
            "classId": ferry_class_A.id,
            "name": "M/V Wenatchee"
        }
        
        response = self.client.post('/api/games/' + str(game.id) + '/ferries',
            data = json.dumps(data),
            # TODO all PUT and POST requests should have content_type
            content_type = 'application/json',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ],
        )
        
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        
        self.assertEqual(data['message'], 'Not enough available cash to purchase the class of ferry.')
        
        
    def test_get_empty_routes(self):
        ''' try to get routes for a game where none exist '''
        
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        game = database.Game(player = bob)
        
        session.add_all([bob, game])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.get('/api/games/' + str(game.id) + '/routes',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 0)
        
    def test_post_route(self):
        ''' create a new route for the current game '''
        
        # create terminals
        seattle = database.Terminal(name = 'Seattle', lat = 47.6025001, lon = -122.33857590000002, passenger_pool = 13000, car_pool = 2000, truck_pool = 300)
        bainbridge_island = database.Terminal(name = 'Bainbridge Island', lat = 47.623089, lon = -122.511171, passenger_pool = 13000, car_pool = 2000, truck_pool = 300)
        
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        ferry_class_props = { 
            'name': 'Jumbo Mark II',
            'passengers': 2500,
            'cars': 202,
            'trucks': 60,
            'speed': 21,
            'burn_rate': 350,
            'turnover_time': 0.2,
            'cost': 50000000
        }
        
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            trucks = ferry_class_props['trucks'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
            turnover_time = ferry_class_props['turnover_time'],
            cost = ferry_class_props['cost'],
        )
        
        game = database.Game(player = bob)
        
        ferry = database.Ferry(
            ferry_class = ferry_class_A,
            game = game,
            name = 'M/V Minnow',
            launched = 2000,
        )
        
        session.add_all([seattle, bainbridge_island, bob, game, ferry_class_A, ferry])
        session.commit()
        
        data = {
            "terminal1Id": seattle.id,
            "terminal2Id": bainbridge_island.id,
            "passenger_fare": 8.50,
            "car_fare": 18,
            "truck_fare": 48,
            "ferries": [
                ferry.id
            ]
        }
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.post('/api/games/' + str(game.id) + '/routes',
        data = json.dumps(data),
            content_type = 'application/json',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 7)
        
    def test_get_routes(self):
        ''' get all the routes for a player's game '''
        
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        game = database.Game(player = bob)
        
        seattle = database.Terminal(name = 'Seattle', lat = 47.6025001, lon = -122.33857590000002)
        bainbridge_island = database.Terminal(name = 'Bainbridge Island', lat = 47.623089, lon = -122.511171)
        
        route = database.Route(game = game, first_terminal = seattle, second_terminal = bainbridge_island)
        
        session.add_all([bob, game, seattle, bainbridge_island])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.get('/api/games/' + str(game.id) + '/routes',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 1)
        
        route = data[0]
        print(route)
        # self.assertEqual(route['game']['player']['id'], bob.id)
        self.assertAlmostEqual(route['route_distance'], 7.47, 2)
        # self.assertLessEqual(game['created_date'], unix_timestamp(datetime.now()))
        # self.assertEqual(game['cash_available'], 0)  
        
    def test_game_endturn(self):
        ''' end the current turn, run the simulation cycle, and test the response '''
        pw = 'notsecret'
        bob = database.User(name = 'ferrycapn', email = 'capnonthebridge@gmail.com', password = generate_password_hash(pw))
        
        # create a new game
        game = database.Game(player = bob)
        
        # create terminals
        seattle = database.Terminal(name = 'Seattle', lat = 47.6025001, lon = -122.33857590000002, passenger_pool = 13000, car_pool = 2000, truck_pool = 300)
        bainbridge_island = database.Terminal(name = 'Bainbridge Island', lat = 47.623089, lon = -122.511171, passenger_pool = 13000, car_pool = 2000, truck_pool = 300)
        
        # create route
        route = database.Route(
            game = game, first_terminal = seattle, second_terminal = bainbridge_island,
            passenger_fare = 8, car_fare = 18, truck_fare = 50
        )
        
        # TODO ferry_class_props should be moved outside of this function as it duplicates an object for another test
        # create a ferry class
        ferry_class_props = { 
            'name': 'Jumbo Mark II',
            'passengers': 2500,
            'cars': 202,
            'trucks': 60,
            'speed': 21,
            'burn_rate': 350,
            'turnover_time': 0.2,
            'cost': 50000,
            'residual_value': 10000,
            'usable_life': 60
        }
        ferry_class_A = database.Ferry_Class(
            name = ferry_class_props['name'],
            passengers = ferry_class_props['passengers'],
            cars = ferry_class_props['cars'],
            trucks = ferry_class_props['trucks'],
            speed = ferry_class_props['speed'],
            burn_rate = ferry_class_props['burn_rate'],
            turnover_time = ferry_class_props['turnover_time'],
            cost = ferry_class_props['cost'],
            residual_value = ferry_class_props['residual_value'],
            usable_life = ferry_class_props['usable_life'],
        )
        
        ferry = database.Ferry(
            game = game, ferry_class = ferry_class_A, route = route, 
            name = 'M/V Wenatchee',
            launched = 2000
        )
        
        session.add_all([bob, game, seattle, bainbridge_island, route, ferry_class_A, ferry])
        session.commit()
        
        token = self.get_jwt(bob.name, pw)
        
        response = self.client.get('/api/games/' + str(game.id) + '/endturn',
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 8)
        
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['current_week'], 2)
        self.assertEqual(data['current_year'], 2000)

        response = self.client.get('/api/games/' + str(game.id),
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        # self.assertEqual(len(data), 1)
        
        self.assertEqual(data['current_week'], 2)
        
        response = self.client.get('/api/games/' + str(game.id) + '/turn_results/' + str(game.current_year) + '/week/' + str(game.current_week - 1), 
            headers = [
                ('Accept', 'application/json'),
                ('Authorization', 'JWT ' + token)
            ]
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        
        data = json.loads(response.data.decode('ascii'))
        
        self.assertEqual(data['week'], 1)
        self.assertEqual(data['year'], 2000)
        self.assertEqual(data['route_results'][0]['id'], 1)
        self.assertEqual(data['route_results'][0]['ferry_results'][0]['ferry']['name'], 'M/V Wenatchee')
        
if __name__ == '__main__':
    unittest.main()