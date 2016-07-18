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
    
    ferries = relationship('Ferry', backref = 'owner')

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
        
    def depreciated_value(self, year):
        age = year - self.launched
        if(age >= self.usable_life):
            return 0
        return self.cost - self.cost * age / self.usable_life
    
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True)
    passengers = Column(Integer)
    cars = Column(Integer)
    max_commercial = Column(Integer) # maximum commercial vehicles
    speed = Column(Integer) # knots
    burn_rate = Column(Integer) # fuel consumption per hour
    cost = Column(Integer) # acquisition cost
    usable_life = Column(Integer)
    


class Ferry(Base):
    __tablename__ = 'ferries'
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "ferry_class": self.ferry_class.as_dictionary()
        }
        
    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    launched = Column(Integer) 
    owner_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    ferry_class_id = Column(Integer, ForeignKey('ferry_classes.id'), nullable = False)
    
    ferry_class = relationship('Ferry_Class', uselist = False)
    