import os.path
import json

from flask import request, Response, url_for, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
# from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import decorators
from py_ferry import app
from py_ferry import database
from py_ferry import models
from .database import session

# def current_user_authorized(record_type, id):
#     return True

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
@login_required
@decorators.accept('application/json')
def ferries_get(game_id):
    ''' get player ferries based on game id '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_user:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
    
    ferries = session.query(database.Ferry).filter(database.Ferry.game == game)
    # ferry = ferry.order_by(models.Ferry_Class.cost)

    data = json.dumps([ferry.as_dictionary() for ferry in ferries])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games', methods = ['GET'])
@login_required
@decorators.accept('application/json')
def games_get():
    ''' get player games '''

    # make sure the game ID belongs to the current user
    games = session.query(database.Game).filter(database.Game.player == current_user)
    # if not game.player == current_user:
    #     data = {'message': 'The game ID for the request does not belong to the current user.'}
    #     return Response(data, 403, mimetype = 'application/json')
    
    # ferries = session.query(database.Ferry).filter(database.Ferry.game == game)
    # ferry = ferry.order_by(models.Ferry_Class.cost)

    data = json.dumps([game.as_dictionary() for game in games])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>', methods = ['GET'])
@login_required
@decorators.accept('application/json')
def games_get_one(game_id):
    ''' get player game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_user:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')

    data = json.dumps(game.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/routes', methods = ['GET'])
@login_required
@decorators.accept('application/json')
def routes_get(game_id):
    ''' get routes for a player's game '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_user:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
    
    routes = session.query(database.Route).filter(database.Route.game == game)

    data = json.dumps([route.as_dictionary() for route in routes])
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/endturn', methods = ['GET'])
@login_required
@decorators.accept('application/json')
def games_endturn(game_id):
    ''' end a player's turn '''

    # make sure the game ID belongs to the current user
    game = session.query(database.Game).get(game_id)
    if not game.player == current_user:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')
    
    routes = session.query(database.Route).filter(game == game)
    
    routes_results = []
    # TODO there's got to be a better way to map an existing record to a new record
    for route in routes:
        weekly_results = models.Sailings().weekly_crossings(
            route, game.current_week, game.current_year
        )
        ferry_results = []
        for weekly_result in weekly_results:
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
    )
    
    session.add(turn_result)
    
    game.current_week += 1
    
    session.commit()

    data = json.dumps({'message': 'success'})
    return Response(data, 200, mimetype = 'application/json')
    
@app.route('/api/games/<int:game_id>/turn-results/<int:week_number>', methods = ['GET'])
@login_required
@decorators.accept('application/json')
def games_get_turn(game_id, week_number):
    ''' get turn results given a game ID and week number '''

    # make sure the game ID belongs to the current user
    # TODO we probably don't have to get the game explicitly, we can probable jsut access the player through the game property
    game = session.query(database.Game).get(game_id)
    if not game.player == current_user:
        data = {'message': 'The game ID for the request does not belong to the current user.'}
        return Response(data, 403, mimetype = 'application/json')

    # TODO we need to refactor the following query if we drop using the explicit game record check
    turn_result = session.query(database.Turn_Result).filter(game == game, week_number == week_number)[0]
    
    route_results = session.query(database.Route_Result).filter(turn_result == turn_result)

    data = json.dumps(turn_result.as_dictionary())
    return Response(data, 200, mimetype = 'application/json')