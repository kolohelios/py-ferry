from datetime import datetime
import random

class Fuel(object):
    ''' properties and methods related to fuel costing '''
    def __init__(self):
        self.fuel_cost = 417.05
        self.gals_in_oil_bbl = 41
    
    def cost_per_gallon(self):
        return self.fuel_cost / self.gals_in_oil_bbl
        
class Passengers(object):
    ''' passengers '''
    def __init__(self):
        self.annual_growth_rate = 1.02
        self.week_demand = {
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
        self.year_demand = {
            'January': 0.7,
            'February': 0.7,
            'March': 0.7,
            'April': 0.75,
            'May': 0.8,
            'June': 0.85,
            'July': 0.95,
            'August': 1,
            'September': 0.95,
            'October': 0.8,
            'November': 0.7,
            'December': 0.7
        }
        self.base_year = 2016
        self.growth_rate = 1.025

    def demand(self, day, hour, month, year):
        base_demand = self.week_demand[day][hour] * self.year_demand[month]
        offset_years = year - self.base_year
        base_demand = base_demand * (self.growth_rate ** offset_years)
        return base_demand
        
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