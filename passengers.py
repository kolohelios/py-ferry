from datetime import datetime
import random


class Passengers(object):
    ANNUAL_GROWTH_RATE = 1.02
    WEEK_DEMAND = {
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
    YEAR_DEMAND = {
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
    BASE_YEAR = 2016
    GROWTH_RATE = 1.025

    def __init__(self):
        pass

    def demand(self, day, hour, month, year):
        base_demand = self.WEEK_DEMAND[day][hour] * self.YEAR_DEMAND[month]
        offset_years = year - self.BASE_YEAR
        base_demand = base_demand * (self.GROWTH_RATE ** offset_years)
        return base_demand
