from datetime import datetime
import random
import math

# TODO these singletons don't seem very pythonic

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
        week_floor = math.floor(week / 4 + 1)
        base_demand = self.day_demand[day][hour] * self.week_demand[week_floor]
        offset_years = year - self.base_year
        base_demand = base_demand * (self.growth_rate ** offset_years)
        return round(base_demand * passengers / 24)
        
    def week_route_passenger_demand(self, passengers, week, year):
        route_total = 0
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            for hour in range(0, 23):
                route_total += self.route_passenger_demand(passengers, hour, day, week, year)
        return route_total
        
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # for day in days:
    #     print(day)
    #     car_queue = 0
    #     for hour in range(0, 24):
    #         for minute in range (0, 60):
    #             car_queue += round((self.passengers.demand(day, hour, 'August', 2016) * route.riders / 23) / 60)
    #             for time in schedule.times:
    #                 if time == hour + minute / 60:
    #                     print('car_queue', car_queue)
    #                     car_queue -= min(ferry.cars, car_queue)
    #                     print('loading up!', math.trunc(time), ':', str(round(time % 1 * 60)).zfill(2), end = ' ')
    
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
            'Friday': 'weekday',
            'Saturday': 'weekend',
            'Sunday': 'weekend',
        }
        
    def route_interval(self, route):
        return route['route_distance'] / route['ferries'][0]['speed'] + route['ferries'][0]['turnover_time']
    
    def first_run(self, shift_mapping):
        for time in range(0, 23):
            if self.full_staffing[shift_mapping][time] == True:
                return time
                
    def last_run(self, shift_mapping):
        for time in range(23, 0, -1):
            if self.full_staffing[shift_mapping][time] == True:
                return time
    
    def build_schedule(self, route, day):
        schedule = []
        shift_mapping = self.day_mapping[day]
        first_shift_hour = self.first_run(shift_mapping)
        last_shift_hour = self.last_run(shift_mapping)
        run_interval = self.route_interval(route)
        
        next_time = first_shift_hour
        while next_time < last_shift_hour:
            if self.full_staffing[shift_mapping][int(next_time)] == True:
                schedule.append(next_time)
            next_time += run_interval
        
        return schedule
    
