from datetime import datetime
import random
import math

from py_ferry import database

# TODO these singletons don't seem very pythonic - is something else better
class Fuel(object):
    ''' properties and methods related to fuel costing '''
    def __init__(self):
        self.fuel_cost = 417.05
        self.gals_in_oil_bbl = 41
    
    def cost_per_gallon(self):
        return self.fuel_cost / self.gals_in_oil_bbl
        
class Passenger(object):
    ''' passengers '''
    def __init__(self):
        self.annual_growth_rate = 1.02
        self.day_demand = {
            'Monday':
                [
                    0.1, 0.1, 0, 0, 0, 0.3,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ],
            'Tuesday':
                [
                    0.1, 0.2, 0.3, 0.3, 0.5, 0.6,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ],
            'Wednesday':
                [
                    0.1, 0.2, 0.3, 0.3, 0.5, 0.6,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ],
            'Thursday':
                [
                    0.1, 0.2, 0.3, 0.3, 0.5, 0.6,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ],
            'Friday':
                [
                    0.1, 0.2, 0.3, 0.3, 0.5, 0.6,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ],
            'Saturday':
                [
                    0.1, 0.2, 0.3, 0.3, 0.5, 0.6,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ],
            'Sunday':
                [
                    0.1, 0.2, 0.3, 0.3, 0.5, 0.6,
                    0.8, 0.95, 0.75, 0.5, 0.2, 0.1,
                    0.15, 0.2, 0.4, 0.8, 0.9, 0.95,
                    0.8, 0.5, 0.4, 0.3, 0.2, 0.1
                ]
        }
        self.week_demand = {
            1: 0.7,
            5: 0.7,
            9: 0.7,
            13: 0.75,
            17: 0.8,
            21: 0.85,
            25: 0.95,
            29: 1,
            33: 0.95,
            37: 0.8,
            41: 0.7,
            45: 0.7,
            49: 0.7,
        }
        self.base_year = 2016
        self.growth_rate = 1.025

    def route_passenger_demand(self, passengers, hour, day, week, year):
        week_floor = math.floor(week / 4) * 4 + 1
        base_demand = self.day_demand[day][hour] * self.week_demand[week_floor]
        offset_years = year - self.base_year
        base_demand = base_demand * (self.growth_rate ** offset_years)
        return round(base_demand * passengers / 24)
        
class Schedule(object):
    def __init__(self):
        self.full_staffing = {
            'weekday': 
                {
                    0: True,
                    1: False,
                    2: False,
                    3: False,
                    4: False,
                    5: True,
                    6: True,
                    7: True,
                    8: True,
                    9: True,
                    10: True,
                    11: True,
                    12: True,
                    13: True,
                    14: True,
                    15: True,
                    16: True,
                    17: True,
                    18: True,
                    19: True,
                    20: True,
                    21: True,
                    22: True,
                    23: True
                },
            'weekend':
                {
                    0: True,
                    1: True,
                    2: True,
                    3: True,
                    4: True,
                    5: True,
                    6: True,
                    7: True,
                    8: True,
                    9: True,
                    10: True,
                    11: True,
                    12: True,
                    13: True,
                    14: True,
                    15: True,
                    16: True,
                    17: True,
                    18: True,
                    19: True,
                    20: True,
                    21: True,
                    22: True,
                    23: True
                }
        }
        self.day_mapping = {
            'Monday': 'weekday',
            'Tuesday': 'weekday',
            'Wednesday': 'weekday',
            'Thursday': 'weekday',
            'Friday': 'weekend',
            'Saturday': 'weekend',
            'Sunday': 'weekend'
        }
        
    def route_interval(self, route):
        return route['route_distance'] / route['ferries'][0]['speed'] + route['ferries'][0]['turnover_time']
    
    # consider refactoring first_run and last_run into one loop through the shift
    def first_run(self, shift_mapping):
        for time in range(0, 24):
            if self.full_staffing[shift_mapping][time] == True:
                return time
                
    def last_run(self, shift_mapping):
        for time in range(23, -1, -1):
            if self.full_staffing[shift_mapping][time] == True:
                return time
    
    def hours_of_operations(self, day):
        shift_mapping = self.day_mapping[day]
        hours = 0
        for time in range(0, 24):
            if self.full_staffing[shift_mapping][time] == True:
                hours += 1
        return hours
    
    def build_schedule(self, route, day):
        schedule = []
        shift_mapping = self.day_mapping[day]
        first_shift_hour = self.first_run(shift_mapping)
        last_shift_hour = self.last_run(shift_mapping)
        run_interval = self.route_interval(route)
        
        # TODO change logic so that ferries always start at the first terminal and end at the first terminal (maybe)
        next_crossing = { 'time': first_shift_hour, 'departs': route['first_terminal'], 'arrives': route['second_terminal'] }
        while next_crossing['time'] < last_shift_hour:
            if self.full_staffing[shift_mapping][int(next_crossing['time'])] == True:
                schedule.append(next_crossing)
            next_crossing = { 
                'time': next_crossing['time'] + run_interval, 
                'departs': next_crossing['arrives'],
                'arrives': next_crossing['departs'],
            }
            
        return schedule
    
class Sailings(object):
    def __init__(self):
        pass
    
    def daily_crossings(self, route, day, week, year):
        schedule = Schedule().build_schedule(route, day)
        # TODO all these declarations and the repition of the queue code smells
        first_terminal_passenger_queue = 0
        second_terminal_passenger_queue = 0
        first_terminal_car_queue = 0
        second_terminal_car_queue = 0
        first_terminal_truck_queue = 0
        second_terminal_truck_queue = 0
        total_passengers = 0
        total_cars = 0
        total_trucks = 0
        for time in range(0, 23):
            first_terminal_passenger_queue += Passenger().route_passenger_demand(route['first_terminal']['passenger_pool'], time, day, week, year)
            second_terminal_passenger_queue += Passenger().route_passenger_demand(route['second_terminal']['passenger_pool'], time, day, week, year)
            first_terminal_car_queue += Passenger().route_passenger_demand(route['first_terminal']['car_pool'], time, day, week, year)
            second_terminal_car_queue += Passenger().route_passenger_demand(route['second_terminal']['car_pool'], time, day, week, year)
            first_terminal_truck_queue += Passenger().route_passenger_demand(route['first_terminal']['truck_pool'], time, day, week, year)
            second_terminal_truck_queue += Passenger().route_passenger_demand(route['second_terminal']['truck_pool'], time, day, week, year)
            for sailing in schedule:
                # TODO the if block below can probably be changed to parametric expressions that use route[terminal]
                if int(sailing['time']) == time:
                    if sailing['departs'] == route['first_terminal']:
                        passengers = min(route['ferries'][0]['ferry_class']['passengers'], first_terminal_passenger_queue)
                        cars = min(route['ferries'][0]['ferry_class']['cars'], first_terminal_car_queue)
                        trucks = min(route['ferries'][0]['ferry_class']['trucks'], first_terminal_truck_queue)
                        first_terminal_passenger_queue -= passengers
                        first_terminal_car_queue -= cars
                        first_terminal_truck_queue -= trucks
                        total_passengers += passengers
                        total_cars += cars
                        total_trucks += trucks
                    else:
                        passengers = min(route['ferries'][0]['ferry_class']['passengers'], second_terminal_passenger_queue)
                        cars = min(route['ferries'][0]['ferry_class']['cars'], second_terminal_car_queue)
                        trucks = min(route['ferries'][0]['ferry_class']['trucks'], second_terminal_truck_queue)
                        second_terminal_passenger_queue -= passengers
                        second_terminal_car_queue -= cars
                        second_terminal_truck_queue -= trucks
                        total_passengers += passengers
                        total_cars += cars
                        total_trucks += trucks
        daily_results = {
            'total_passengers': total_passengers,
            'total_cars': total_cars,
            'total_trucks': total_trucks,
            'total_sailings': len(schedule),
            'total_hours': Schedule().hours_of_operations(day),
        }
        return daily_results
   
    def weekly_crossings(self, route, week, year):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        total_passengers = 0
        total_cars = 0
        total_trucks = 0
        total_sailings = 0
        total_hours = 0
        for day in days:
            daily_crossings = self.daily_crossings(route, day, week, year)
            total_passengers += daily_crossings['total_passengers']
            total_cars += daily_crossings['total_cars']
            total_trucks += daily_crossings['total_trucks']
            total_sailings += daily_crossings['total_sailings']
            total_hours += daily_crossings['total_hours']
        weekly_results = {
            'total_passengers': total_passengers,
            'total_cars': total_cars,
            'total_trucks': total_trucks,
            'total_sailings': total_sailings,
            'total_hours': total_hours,
        }
        return weekly_results
    
class Financial_Calc(object):
    def __init__(self):
        pass
    
    def calc_weekly_results_for_route(self, route, week, year):
        sailings_results = Sailings().weekly_crossings(route, week, year)
        fuel_used = route['ferries'][0]['ferry_class']['burn_rate'] * sailings_results['total_hours']
        fuel_cost = Fuel().cost_per_gallon() * fuel_used
        passenger_revenue = sailings_results['total_passengers'] * route['passenger_fare']
        car_revenue = sailings_results['total_cars'] * route['car_fare']
        truck_revenue = sailings_results['total_trucks'] * route['truck_fare']
        
        weekly_results = {
            'passengers': sailings_results['total_passengers'],
            'cars': sailings_results['total_cars'],
            'trucks': sailings_results['total_trucks'],
            'fuel_used': fuel_used,
            'fuel_cost': fuel_cost,
            'passenger_revenue': passenger_revenue,
            'car_revenue': car_revenue,
            'truck_revenue': truck_revenue,
        }
        return weekly_results
    
    