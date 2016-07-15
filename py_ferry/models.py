import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from py_ferry import app
from .database import Base, engine

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(128))
    email = Column(String(128), unique = True)
    password = Column(String(128))

class Ferry(Base):
    '''
    The ferry model is the core of the project
    because that's what this game is all about!
    '''
    __tablename__ = 'ferries'
    
    def depreciated_value(self, year):
        age = year - self.launched
        if(age >= self.usable_life):
            return 0
        return self.price - self.price * age / self.usable_life
    
    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    passengers = Column(Integer)
    cars = Column(Integer)
    trucks = Column(Integer)
    speed = Column(Integer)
    burn_rate = Column(Integer)
    price = Column(Integer)
    launched = Column(Integer)
    usable_life = Column(Integer)

    # def __init__(self, passengers, cars, trucks, speed, burn_rate, price, launched, usable_life):
    #     self.passengers = passengers
    #     self.cars = cars
    #     self.trucks = trucks # commercial vehicles
    #     self.speed = speed # knots
    #     self.burn_rate = burn_rate # gals/hr
    #     self.price = price # millions
    #     self.launched = launched # year launched
    #     self.usable_life = usable_life

    