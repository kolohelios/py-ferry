import os
import unittest

import py_ferry
from py_ferry.models import *

class FilterTests(unittest.TestCase):
    def test_fuel_cost(self):
        fuel_cost = Fuel().cost_per_gallon()
        self.assertAlmostEqual(fuel_cost, 10.17, 2)
        
    def test_passenger_demand(self):
        demand = Passengers().demand('Tuesday', 7, 'October', 2016)
        self.assertEqual(demand, 0.76)

if __name__ == '__main__':
    unittest.main()