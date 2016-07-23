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
    
    def test_week_passenger_demand(self):
        demand = Passenger().week_route_passenger_demand(30000, 3, 2016)
        self.assertEqual(demand, 65454)
        
    def test_build_schedule(self):
        route = {
            'route_distance': 7.1,
            'ferries': [
                    {
                        'speed': 18,
                        'turnover_time': 0.2
                    }
                ]
        }
        expected_schedule = [0, 0.5944444444444444, 5.35, 5.944444444444444, 6.538888888888888, 7.133333333333332, 7.727777777777776, 8.322222222222221, 8.916666666666666, 9.511111111111111, 10.105555555555556, 10.700000000000001, 11.294444444444446, 11.888888888888891, 12.483333333333336, 13.077777777777781, 13.672222222222226, 14.266666666666671, 14.861111111111116, 15.455555555555561, 16.050000000000004, 16.64444444444445, 17.238888888888894, 17.83333333333334, 18.427777777777784, 19.02222222222223, 19.616666666666674, 20.21111111111112, 20.805555555555564, 21.40000000000001, 21.994444444444454, 22.5888888888889]
        schedule = Schedule().build_schedule(route, 'Monday')
        self.assertEqual(schedule, expected_schedule)

if __name__ == '__main__':
    unittest.main()