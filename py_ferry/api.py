import os.path
import json

# TODO consider replacing the use of the json library with jsonify
from flask import request, Response, url_for, send_from_directory
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import check_password_hash, generate_password_hash
from jsonschema import validate, ValidationError

from . import decorators
from py_ferry import app
from py_ferry import database
from py_ferry import models
from .database import session

def authenticate(username, password):
    user = session.query(database.User).filter_by(name = username).first()
    if user and check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return session.query(database.User).get(user_id)

jwt = JWT(app, authenticate, identity)

@app.route('/api/register', methods = ['POST'])
@decorators.require('application/json')
def register():
    json_data = request.json
    
    users = session.query(database.User).filter(database.User.name == json_data['name'])
    if users.count():
        message = 'This username is already being used.'
        data = json.dumps({ 'status': 'Error', 'data': None, 'message': message })
        return Response(data, 409, mimetype = 'application/json')
    users = session.query(database.User).filter(database.User.email == json_data['email'])
    if users.count():
        message = 'This email address is already being used.'
        data = json.dumps({ 'status': 'Error', 'data': None, 'message': message })
        return Response(data, 409, mimetype = 'application/json')
    
    user = database.User(
        email = json_data['email'],
        password = generate_password_hash(json_data['password']),
        name = json_data['name']
    )
    
    session.add(user)
    session.commit()
    message = None
    data = json.dumps({ 'status': 'Success', 'data': None, 'message': message })
    return Response(data, 201, mimetype = 'application/json')
        
@app.route('/api/user')
@jwt_required()
def get_identity_with_token():
    data = json.dumps(current_identity.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    
# TODO someday I'd like to get a refresh token endpoint working
# @app.route('/api/refresh_token')
# @jwt_required()
# def get_refreshed_token():
#     # token = JWT.generate_token(current_identity)
#     # data = json.dumps({ 'access_token': token })
#     payload = jwt.payload_callback(current_identity)
#     new_token = jwt.encode_callback(payload)
#     data = json.dumps({ 'access_token': new_token })
#     return Response(data, 200, mimetype = 'application/json')

@app.route('/api/ferry_classes', methods = ['GET'])
@decorators.accept('application/json')
def ferry_classes_get():
    ''' get a list of ferry classes '''
    
    ferry_classes = session.query(database.Ferry_Class)
    ferry_classes = ferry_classes.order_by(database.Ferry_Class.cost)

    data = json.dumps([ferry_class.as_dictionary() for ferry_class in ferry_classes])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/terminals', methods = ['GET'])
@decorators.accept('application/json')
def terminals_get():
    ''' get terminals '''
    
    terminals = session.query(database.Terminal)
    terminals = terminals.order_by(database.Terminal.name)

    data = json.dumps([terminal.as_dictionary() for terminal in terminals])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/ferries', methods = ['GET'])
@jwt_required()
@decorators.accept('application/json')
def ferries_get(game_id):
    ''' get player ferries based on game id '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
    
    ferries = session.query(database.Ferry).filter(database.Ferry.game == game, database.Ferry.active == True)

    data = json.dumps([ferry.as_dictionary() for ferry in ferries])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/ferries/<int:ferry_id>', methods = ['DELETE'])
@jwt_required()
@decorators.accept('application/json')
def ferries_sell(game_id, ferry_id):
    ''' sell a ferry based on game and ferry IDs '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
        
    ferry = session.query(database.Ferry).get(ferry_id)
    
    if not ferry.game == game:
        data = {'message': 'The ferry being sold does not match the game ID in the request.'}
        return Response(data, 403, mimetype = 'application/json')
    
    ferry.active = False
    # clear the route associated with this ferry to take it out of service
    ferry.route = None
    
    game.cash_available += ferry.depreciated_value(game.current_year)
    
    session.commit()

    data = json.dumps(ferry.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')

@app.route('/api/games/<int:game_id>/ferries', methods = ['POST'])
@jwt_required()
@decorators.accept('application/json')
@decorators.require('application/json')
def ferries_post(game_id):
    ''' buy a ferry for a player's game '''
    
    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = json.dumps({'message': 'The game ID for the request does not belong to the current user.'})
        return Response(data, 403, mimetype = 'application/json')
    
    # make sure the player has enough cash to purchase this ferry
    json_data = request.json
    
    ferry_class = session.query(database.Ferry_Class).get(json_data['classId'])
    if not game.cash_available > ferry_class.cost:
        data = json.dumps({'message': 'Not enough available cash to purchase the class of ferry.'})
        return Response(data, 402, mimetype = 'application/json')
    
    ferry = database.Ferry(
        ferry_class = ferry_class,
        name = json_data['name'],
        game = game,
        launched = game.current_year + (game.current_week / 52)
    )
    
    # reduce cash available by the purchase price
    game.cash_available -= ferry_class.cost
    
    session.add(ferry)
    session.commit()
    
    data = json.dumps(ferry.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games', methods = ['POST'])
@jwt_required()
@decorators.accept('application/json')
# TODO yes, there should be a limit to the number of active games a player can have
def games_new():
    ''' create a new player game '''
    
    game = database.Game(player = current_identity)
    
    session.add(game)
    session.commit()
    
    data = json.dumps(game.as_dictionary())
    return Response(data, 201, mimetype = 'application/json')
    
@app.route('/api/games', methods = ['GET'])
@jwt_required()
@decorators.accept('application/json')
def games_get():
    ''' get player games '''

    # make sure the game ID belongs to the current user
    games = session.query(database.Game).filter(database.Game.player == current_identity, database.Game.active == True)

    data = json.dumps([game.as_dictionary() for game in games])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>', methods = ['GET'])
@jwt_required()
@decorators.accept('application/json')
def games_get_one(game_id):
    ''' get player game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')

    data = json.dumps(game.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>', methods = ['DELETE'])
@jwt_required()
@decorators.accept('application/json')
def games_delete(game_id):
    ''' get player game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')

    game.active = False;
    session.commit();
    # because returning the record when we delete is what we do... (though it's not really deleted)
    data = json.dumps(game.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/routes', methods = ['GET'])
@jwt_required()
@decorators.accept('application/json')
def routes_get(game_id):
    ''' get routes for a player's game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
    
    routes = session.query(database.Route).filter(database.Route.game == game)

    data = json.dumps([route.as_dictionary() for route in routes])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/routes', methods = ['POST'])
@jwt_required()
@decorators.accept('application/json')
@decorators.require('application/json')
def routes_create(game_id):
    ''' create a route for a player's game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = json.dumps({'message': 'The game ID for the request does not belong to the current user.'})
        return Response(data, 403, mimetype = 'application/json')
        
    json_data = request.json
    
    if session.query(database.Route).filter(database.Route.game == game, database.Route.first_terminal_id == json_data['terminal1Id'], database.Route.second_terminal_id == json_data['terminal2Id']).first():
        data = json.dumps({"message": "A route between these two terminals already exists."})
        return Response(data, 400, mimetype = 'application/json')
    if session.query(database.Route).filter(database.Route.game == game, database.Route.first_terminal_id == json_data['terminal2Id'], database.Route.second_terminal_id == json_data['terminal1Id']).first():
        data = json.dumps({"message": "A route between these two terminals already exists."})
        return Response(data, 400, mimetype = 'application/json')
    
    
    first_terminal = session.query(database.Terminal).get(json_data['terminal1Id'])
    second_terminal = session.query(database.Terminal).get(json_data['terminal2Id'])
    
    ferries = []
    for ferry in json_data['ferries']:
        ferry = session.query(database.Ferry).get(ferry)
        # only allow ferries to be added if they aren't already on a route
        if ferry and ferry.route == None:
            ferries.append(ferry)
            
    passenger_fare = json_data.get('passenger_fare', 0)
    car_fare = json_data.get('car_fare', 0)
    truck_fare = json_data.get('truck_fare', 0)
    
    route = database.Route(
        first_terminal = first_terminal, second_terminal = second_terminal, 
        game = game, ferries = ferries, passenger_fare = passenger_fare,
        car_fare = car_fare, truck_fare = truck_fare
    )
    
    # HACK we should add formal JSON validation to replace this try...expect block
    try:
        session.add(route)
        session.commit()
        data = json.dumps(route.as_dictionary())
        return Response(data, 201, mimetype = 'application/json')    
    except:
        session.rollback();
        data = json.dumps({"status": "failure"})
        return Response(data, 400, mimetype = 'application/json')
        
@app.route('/api/games/<int:game_id>/routes/<int:route_id>', methods = ['PUT'])
@jwt_required()
@decorators.accept('application/json')
@decorators.require('application/json')
def routes_update(game_id, route_id):
    ''' update a route for a player's game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
        
    json_data = request.json
    
    route = session.query(database.Route).get(route_id)
    
    if not route.game.id == game_id:
        data = {'message': 'The route in the request does not belong to the game associated with the game ID in the request.'}
        return Response(data, 403, mimetype = 'application/json')
    
    first_terminal = session.query(database.Terminal).get(json_data['terminal1Id'])
    second_terminal = session.query(database.Terminal).get(json_data['terminal2Id'])
    
    ferries = []
    print(json_data['ferries'])
    for ferry in json_data['ferries']:
        ferry = session.query(database.Ferry).get(int(ferry))
        # only allow ferries to be added if they aren't already on a route or are already on this route
        if not ferry.route or (ferry.route and ferry.route == route):
            ferries.append(ferry)
    
    route.first_terminal = first_terminal
    route.second_terminal = second_terminal
    route.ferries = ferries
    route.passenger_fare = json_data.get('passenger_fare', 0)
    route.car_fare = json_data.get('car_fare', 0)
    route.truck_fare = json_data.get('truck_fare', 0)
    
    # HACK we should add formal JSON validation to replace this try...expect block
    try:
        session.commit()
        data = json.dumps(route.as_dictionary())
        return Response(data, 200, mimetype = 'application/json')    
    except:
        session.rollback();
        data = json.dumps({"status": "failure"})
        return Response(data, 400, mimetype = 'application/json')

@app.route('/api/games/<int:game_id>/endturn', methods = ['GET'])
@app.route('/api/games/<int:game_id>/endturn/<int:turn_count>', methods = ['GET'])
@jwt_required()
@decorators.accept('application/json')
def games_endturn(game_id, turn_count = 1):
    ''' end a player's turn '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
    
    routes = session.query(database.Route).filter(game == game)
    
    for i in range(0, turn_count):
        routes_results = []
        # TODO there's got to be a better way to map an existing record to a new record
        
        total_fuel = 0
        total_revenue = 0
        
        for route in routes:
            weekly_results = models.Sailings().weekly_crossings(
                route, game.current_week, game.current_year
            )
            ferry_results = []
            for weekly_result in weekly_results:
                total_fuel += weekly_result['results']['fuel_used']
                total_revenue += weekly_result['results']['total_passengers'] * route.passenger_fare
                total_revenue += weekly_result['results']['total_cars'] * route.car_fare
                total_revenue += weekly_result['results']['total_trucks'] * route.truck_fare
                ferry_result = database.Ferry_Result(
                    fuel_used = weekly_result['results']['fuel_used'],
                    total_passengers = weekly_result['results']['total_passengers'],
                    total_cars = weekly_result['results']['total_cars'],
                    total_trucks = weekly_result['results']['total_trucks'],
                    ferry = weekly_result['ferry']
                )
                ferry_results.append(ferry_result)
                session.add(ferry_result)
            route_result = database.Route_Result(
                first_terminal = route.first_terminal,
                second_terminal = route.second_terminal,
                passenger_fare = route.passenger_fare,
                car_fare = route.car_fare,
                truck_fare = route.truck_fare,
                ferry_results = ferry_results
            )
            session.add(route_result)
            routes_results.append(route_result)
        
        turn_result = database.Turn_Result(
            game = game,
            week = game.current_week,
            year = game.current_year,
            route_results = routes_results,
            fuel_cost = models.Fuel().cost_per_gallon(),
        )
        
        session.add(turn_result)
        
        if(game.current_week >= 52):
            game.current_week = 1
            game.current_year += 1
        else:
            game.current_week += 1
        game.cash_available += total_revenue - total_fuel * models.Fuel().cost_per_gallon()
        
    session.commit()

    data = json.dumps(game.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/turn_results/<int:year>/week/<int:week>', methods = ['GET'])
@jwt_required()
@decorators.accept('application/json')
def games_get_turn(game_id, year, week):
    ''' get turn results given a game ID and year and week number '''

    # make sure the game ID belongs to the current user
    # TODO we probably don't have to get the game explicitly, we can probably just access the player through the game property
    game = session.query(database.Game).get(game_id)
    if not game.player == current_identity:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')

    # TODO we need to refactor the following query if we drop using the explicit game record check
    turn_result = session.query(database.Turn_Result).filter(game == game, database.Turn_Result.year == year, database.Turn_Result.week == week).first()
    
    if not turn_result:
        data = {'message': 'There were no results found matching the request.'}
        return Response(data, 400, mimetype = 'application/json')

    data = json.dumps(turn_result.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    