import os.path

from flask import url_for
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, String, Float, DateTime, Sequence, ForeignKey
from sqlalchemy.orm import relationship
# from flask_login import UserMixin
from geopy.distance import vincenty

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from py_ferry import app

engine = create_engine(app.config['DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

def unix_timestamp(date_time):
    if not date_time:
        return None
    return int(date_time.strftime('%s'))

class Public:
    private = ()

    def as_dictionary(self):
        dic = {}
        for col in self.__table__.columns:
            name = col.name
            if name in self.private: continue
            if type(getattr(self, name)) == datetime:
                dic[name] = getattr(self, name).timestamp()
            else:
                dic[name] = getattr(self, name)
        return dic

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__,
            ", ".join(
                "%s=%r" % (col.name, getattr(self, col.name))
                for col in self.__table__.columns
                if col.name not in self.private
            )
        )

class User(Base, Public):
    # TODO add a verify password method here and refactor where it is being done a point of use
    __tablename__ = 'users'
    private = ('email', 'password', 'created_date')
    
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True, nullable = False)
    email = Column(String(128), unique = True, nullable = False)
    password = Column(String(128), nullable = False)
    created_date = Column(DateTime, default = datetime.now)

    games = relationship('Game', backref = 'player')

class Ferry_Class(Base, Public):
    '''
    The ferry class model contains the ferry classes that form the basis for
    ferries that users buy and sell.
    '''
    __tablename__ = 'ferry_classes'
    

    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True)
    passengers = Column(Integer)
    cars = Column(Integer)
    trucks = Column(Integer) # maximum tall vehicle spaces
    speed = Column(Integer) # knots
    burn_rate = Column(Integer) # fuel consumption per hour
    cost = Column(Integer) # acquisition cost
    residual_value = Column(Integer) # minimum asset value
    usable_life = Column(Integer)
    turnover_time = Column(Integer)
    
    ferry = relationship('Ferry', backref = 'ferry_class')

class Ferry(Base):
    __tablename__ = 'ferries'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "ferry_class": self.ferry_class.as_dictionary(),
            "depreciated_value": self.depreciated_value(self.game.current_year),
            "launched": self.launched,
            "route": self.route.as_dictionary() if self.route != None else {},
            "active": self.active,
        }
    
    def depreciated_value(self, year):
        age = year - self.launched
        return max(self.ferry_class.residual_value, (self.ferry_class.cost * 0.8) - self.ferry_class.cost * age / self.ferry_class.usable_life)
        
    id = Column(Integer, primary_key = True)
    active = Column(Boolean, default = True)
    name = Column(String(64))
    launched = Column(Integer, nullable = False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable = False)
    ferry_class_id = Column(Integer, ForeignKey('ferry_classes.id'), nullable = False)
    ferry_result = relationship('Ferry_Result', backref = 'ferry')
    route_id = Column(Integer, ForeignKey('routes.id'))
    
class Game(Base):
    __tablename__ = 'games'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "player": self.player.as_dictionary(),
            "created_date": unix_timestamp(self.created_date),
            "cash_available": self.cash_available,
            "current_week": self.current_week,
            "current_year": self.current_year,
            "ferries": [ferry.as_dictionary() for ferry in self.ferries if ferry.active == True],
            "routes": [route.as_dictionary() for route in self.routes],
        }
    
    id = Column(Integer, primary_key = True)
    active = Column(Boolean, default = True)
    created_date = Column(DateTime, default = datetime.now)
    current_week = Column(Integer, default = 1)
    current_year = Column(Integer, default = 2000)
    cash_available = Column(Integer, default = 1000000)
    player_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    ferries = relationship('Ferry', backref = 'game')
    routes = relationship('Route', backref = 'game')
    turn_results = relationship('Turn_Result', backref = 'game')
    
class Terminal(Base):
    __tablename__ = 'terminals'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "passenger_pool": self.passenger_pool,
            "car_pool": self.car_pool,
            "truck_pool": self.truck_pool,
        }
    
    id = Column(Integer, primary_key = True)
    name = Column(String, unique = True)
    lat = Column(Float)
    lon = Column(Float)
    passenger_pool = Column(Integer)
    car_pool = Column(Integer)
    truck_pool = Column(Integer)

class Route(Base):
    __tablename__ = 'routes'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "first_terminal": self.first_terminal.as_dictionary(),
            "second_terminal": self.second_terminal.as_dictionary(),
            "route_distance": self.route_distance(),
            "passenger_fare": self.passenger_fare,
            "car_fare": self.car_fare,
            "truck_fare": self.truck_fare,
            "active": self.active,
        }
    
    # TODO we probably should not be calculating this each time it is requested and instead calculate it once upon creation of the route
    def route_distance(self):
        # TODO this isn't accurate because it's point-to-point... so... someday, someone will have to do something about it beyond the ROUTE_ARC_MULTIPLER
        ROUTE_ARC_MULTIPLER = 1.05
        place_A = (self.first_terminal.lat, self.first_terminal.lon)
        place_B = (self.second_terminal.lat, self.second_terminal.lon)
        return vincenty(place_A, place_B).nm * ROUTE_ARC_MULTIPLER # in nautical miles
    
    id = Column(Integer, primary_key = True)
    passenger_fare = Column(Float, default = 0)
    car_fare = Column(Float, default = 0)
    truck_fare = Column(Float, default = 0)
    
    first_terminal_id = Column(Integer, ForeignKey('terminals.id'))
    second_terminal_id = Column(Integer, ForeignKey('terminals.id'))
    active = Column(Boolean, default = True)
    first_terminal = relationship('Terminal', uselist = False, foreign_keys = first_terminal_id)
    second_terminal = relationship('Terminal', uselist = False, foreign_keys = second_terminal_id)

    # base_route_id = Column(Integer, ForeignKey('base_routes.id'), nullable = False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable = False)
    ferries = relationship('Ferry', backref = 'route')
    
class Ferry_Result(Base):
    __tablename__ = 'ferry_results'
    
    def as_dictionary(self):
        return {
            "ferry": self.ferry.as_dictionary(),
            "total_passengers": self.total_passengers,
            "total_cars": self.total_cars,
            "total_trucks": self.total_trucks,
            "fuel_used": self.fuel_used,
            "sailings": self.sailings,
        }
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    total_passengers = Column(Integer)
    total_cars = Column(Integer)
    total_trucks = Column(Integer)
    fuel_used = Column(Float)
    sailings = Column(Integer)
    
    ferry_id = Column(Integer, ForeignKey('ferries.id'), nullable = False)
    
    route_result_id = Column(Integer, ForeignKey('route_results.id'))

class Route_Result(Base):
    __tablename__ = 'route_results'

    def as_dictionary(self):
        return {
            "id": self.id,
            "first_terminal": self.first_terminal.as_dictionary(),
            "second_terminal": self.second_terminal.as_dictionary(),
            "passenger_fare": self.passenger_fare,
            "car_fare": self.car_fare,
            "truck_fare": self.truck_fare,
            "ferry_results": [ferry_result.as_dictionary() for ferry_result in self.ferry_results] 
        }
        
    id = Column(Integer, primary_key = True)
    passenger_fare = Column(Float)
    car_fare = Column(Float)
    truck_fare = Column(Float)
    
    first_terminal_id = Column(Integer, ForeignKey('terminals.id'))
    second_terminal_id = Column(Integer, ForeignKey('terminals.id'))
    first_terminal = relationship('Terminal', uselist = False, foreign_keys = first_terminal_id)
    second_terminal = relationship('Terminal', uselist = False, foreign_keys = second_terminal_id)
    
    ferry_results = relationship('Ferry_Result', backref = 'route_results')
    
    turn_result_id = Column(Integer, ForeignKey('turn_results.id'))
    
class Turn_Result(Base):
    __tablename__ = 'turn_results'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "week": self.week,
            "year": self.year,
            "fuel_cost": self.fuel_cost,
            "route_results": [route_result.as_dictionary() for route_result in self.route_results],
        }
        
    id = Column(Integer, primary_key = True)
    week = Column(Integer, nullable = False)
    year = Column(Integer, nullable = False)
    fuel_cost = Column(Float)
    game_id = Column(Integer, ForeignKey('games.id'), nullable = False)
    
    route_results = relationship('Route_Result', backref = 'turn_result')
    
Base.metadata.create_all(engine)