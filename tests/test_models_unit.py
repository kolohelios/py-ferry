import os
import unittest

import py_ferry
from py_ferry.models import *

class FilterTests(unittest.TestCase):
    def test_fuel_cost(self):
        fuel_cost = Fuel().cost_per_gallon()
        self.assertAlmostEqual(fuel_cost, 10.17, 2)
        
    def test_empty_passenger_demand(self):
        with self.assertRaises(TypeError):
            demand = Passenger().route_passenger_demand()
        
    def test_passenger_demand(self):
        demand = Passenger().route_passenger_demand(30000, 7, 'Tuesday', 3, 2016)
        self.assertEqual(demand, 831)
    
    # this is unnecessary because we'll get deamnd for each crossing
    # def test_week_passenger_demand(self):
    #     demand = Passenger().week_route_passenger_demand(30000, 3, 2016)
    #     self.assertEqual(demand, 65454)
        
    def test_build_schedule(self):
        route = {
            'route_distance': 7.1,
            'first_terminal': {
                'id': 1
            },
            'second_terminal': {
                'id': 2
            },
            'ferries': [
                    {
                        'speed': 18,
                        'turnover_time': 0.2
                    }
                ]
        }
        expected_schedule = [{'arrives': {'id': 2}, 'time': 0, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 0.5944444444444444, 'departs': {'id': 2}}, {'arrives': {'id': 1}, 'time': 5.35, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 5.944444444444444, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 6.538888888888888, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 7.133333333333332, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 7.727777777777776, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 8.322222222222221, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 8.916666666666666, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 9.511111111111111, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 10.105555555555556, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 10.700000000000001, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 11.294444444444446, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 11.888888888888891, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 12.483333333333336, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 13.077777777777781, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 13.672222222222226, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 14.266666666666671, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 14.861111111111116, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 15.455555555555561, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 16.050000000000004, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 16.64444444444445, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 17.238888888888894, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 17.83333333333334, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 18.427777777777784, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 19.02222222222223, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 19.616666666666674, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 20.21111111111112, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 20.805555555555564, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 21.40000000000001, 'departs': {'id': 1}}, {'arrives': {'id': 1}, 'time': 21.994444444444454, 'departs': {'id': 2}}, {'arrives': {'id': 2}, 'time': 22.5888888888889, 'departs': {'id': 1}}]
        schedule = Schedule().build_schedule(route, 'Monday')
        self.assertEqual(schedule, expected_schedule)

    def test_daily_crossings(self):
        route = {
            'route_distance': 7.1,
            'first_terminal': {
                'id': 1,
                'passenger_pool': 30000,
            },
            'second_terminal': {
                'id': 2,
                'passenger_pool': 30000,
            },
            'ferries': [
                    {
                        'speed': 18,
                        'turnover_time': 0.2,
                        'ferry_class': {
                            'passengers': 2500
                        }
                        
                    }
                ]
        }
        passengers = Sailings().daily_crossings(route, 'Tuesday', 7, 2016)
        self.assertEqual(passengers, 19076)
        
    def test_weekly_crossings(self):
        route = {
            'route_distance': 7.1,
            'first_terminal': {
                'id': 1,
                'passenger_pool': 30000,
            },
            'second_terminal': {
                'id': 2,
                'passenger_pool': 30000,
            },
            'ferries': [
                    {
                        'speed': 18,
                        'turnover_time': 0.2,
                        'ferry_class': {
                            'passengers': 2500
                        }
                        
                    }
                ]
        }
        passengers = Sailings().weekly_crossings(route, 7, 2016)
        self.assertEqual(passengers, 130908)

if __name__ == '__main__':
    unittest.main()