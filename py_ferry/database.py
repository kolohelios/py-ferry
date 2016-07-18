import os.path

from flask import url_for
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from py_ferry import app

engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True)
    email = Column(String(128), unique = True)
    password = Column(String(128))
    created_date = Column(DateTime, default = datetime.now)

    games = relationship('Game', backref = 'player')

class Ferry_Class(Base):
    '''
    The ferry model is the core of the project
    because that's what this game is all about!
    '''
    __tablename__ = 'ferry_classes'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "passengers": self.passengers,
            "cars": self.cars,
            "max_commercial": self.max_commercial,
            "speed": self.speed,
            "burn_rate": self.burn_rate,
        }
    
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True)
    passengers = Column(Integer)
    cars = Column(Integer)
    max_commercial = Column(Integer) # maximum commercial vehicles
    speed = Column(Integer) # knots
    burn_rate = Column(Integer) # fuel consumption per hour
    cost = Column(Integer) # acquisition cost
    residual_value = Column(Integer) # minimum asset value
    usable_life = Column(Integer)
    
    ferry = relationship('Ferry', backref = 'ferry_class')

class Ferry(Base):
    __tablename__ = 'ferries'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "ferry_class": self.ferry_class.as_dictionary()
        }
    
    def depreciated_value(self, year):
        age = year - self.launched
        if(age >= self.ferry_class.usable_life):
            return 0
        return self.ferry_class.residual_value - self.ferry_class.cost * age / self.ferry_class.usable_life
        
    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    launched = Column(DateTime)
    game_id = Column(Integer, ForeignKey('games.id'), nullable = False)
    ferry_class_id = Column(Integer, ForeignKey('ferry_classes.id'), nullable = False)
    
class Game(Base):
    __tablename__ = 'games'
    
    def as_dictionary(self):
        return {
            "id": self.id
        }
    
    id = Column(Integer, primary_key = True)
    created_date = Column(DateTime, default = datetime.now)
    current_week = Column(Integer, default = 0)
    cash_available = Column(Float, default = 0)
    player_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    ferries = relationship('Ferry', backref = 'game')
    routes = relationship('Route', backref = 'game')
    
class Terminal(Base):
    __tablename__ = 'terminals'
    
    def as_dictionary(self):
        return {
            "id": self.id
        }
    
    id = Column(Integer, primary_key = True)

class Base_Route(Base):
    __tablename__ = 'base_routes'
    
    id = Column(Integer, primary_key = True)
    
    routes = relationship('Route', backref = 'base_route')

class Route(Base):
    __tablename__ = 'routes'
    
    id = Column(Integer, primary_key = True)
    first_terminal_id = Column(Integer, ForeignKey('terminals.id'))
    second_terminal_id = Column(Integer, ForeignKey('terminals.id'))
    
    first_terminal = relationship('Terminal', uselist = False, foreign_keys = first_terminal_id)
    second_terminal = relationship('Terminal', uselist = False, foreign_keys = second_terminal_id)
    
    base_route_id = Column(Integer, ForeignKey('base_routes.id'), nullable = False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable = False)
    
Base.metadata.create_all(engine)