import os
import unittest

import py_ferry
from py_ferry.models import *

# define all of the test classes we're going to use

class Terminal(object):
    def __init__(self, id, passenger_pool, car_pool, truck_pool):
        self.id = id
        self.passenger_pool = passenger_pool
        self.car_pool = car_pool
        self.truck_pool = truck_pool

class Ferry_Class(object):
    def __init__(self, passengers, cars, trucks, burn_rate, speed, turnover_time):
        self.passengers = passengers
        self.cars = cars
        self.trucks = trucks
        self.burn_rate = burn_rate
        self.speed = speed
        self.turnover_time = turnover_time

class Ferry(object):
    def __init__(self, ferry_class, name):
        self.ferry_class = ferry_class
        self.name = name

class Route(object):
    def __init__(self, first_terminal, second_terminal, ferries, passenger_fare, car_fare, truck_fare):
        self.first_terminal = first_terminal
        self.second_terminal = second_terminal
        self.ferries = ferries
        self.passenger_fare = passenger_fare
        self.car_fare = car_fare
        self.truck_fare = truck_fare
    
    def route_distance(self):
        return 7.1
    
class ModelTests(unittest.TestCase):
    def test_fuel_cost(self):
        fuel_cost = Fuel().cost_per_gallon()
        self.assertAlmostEqual(fuel_cost, 10.17, 2)
        
    def test_empty_passenger_demand(self):
        with self.assertRaises(TypeError):
            demand = Passenger().route_passenger_demand()
        
    def test_passenger_demand(self):
        demand = Passenger().route_passenger_demand(30000, 7, 'Tuesday', 3, 2016)
        self.assertEqual(demand, 831)
        
    def test_route_interval(self):
        ferry_class = Ferry_Class(
            passengers = 2500, cars = 200, trucks = 60, burn_rate = 350, 
            speed = 21, turnover_time = 0.2
        )
        ferry = Ferry(ferry_class = ferry_class, name = 'M/V Wenatchee')
        ferries = [ferry]
        first_terminal = Terminal(
            id = 1, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        second_terminal = Terminal(
            id = 2, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        route = Route(
            first_terminal = first_terminal, second_terminal = second_terminal, 
            ferries = ferries, passenger_fare = 8, car_fare = 18, truck_fare = 50
        )
        route_interval = Schedule().route_interval(route, ferry)
        self.assertAlmostEqual(route_interval, 0.54, 2)
        
    def test_build_schedule(self):
        ferry_class = Ferry_Class(
            passengers = 2500, cars = 200, trucks = 60, burn_rate = 350, 
            speed = 21, turnover_time = 0.2
        )
        ferry = Ferry(ferry_class = ferry_class, name = 'M/V Wenatchee')
        ferries = [ferry]
        first_terminal = Terminal(
            id = 1, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        second_terminal = Terminal(
            id = 2, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        route = Route(
            first_terminal = first_terminal, second_terminal = second_terminal, 
            ferries = ferries, passenger_fare = 8, car_fare = 18, truck_fare = 50
        )
        expected_schedule = [{'arrives': second_terminal, 'departs': first_terminal, 'time': 0}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 0.5380952380952381}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 5.3809523809523805}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 5.9190476190476184}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 6.457142857142856}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 6.995238095238094}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 7.533333333333332}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 8.071428571428571}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 8.60952380952381}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 9.147619047619047}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 9.685714285714285}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 10.223809523809523}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 10.761904761904761}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 11.299999999999999}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 11.838095238095237}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 12.376190476190475}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 12.914285714285713}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 13.45238095238095}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 13.990476190476189}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 14.528571428571427}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 15.066666666666665}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 15.604761904761903}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 16.142857142857142}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 16.68095238095238}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 17.21904761904762}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 17.757142857142856}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 18.295238095238094}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 18.833333333333332}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 19.37142857142857}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 19.909523809523808}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 20.447619047619046}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 20.985714285714284}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 21.523809523809522}, {'arrives': first_terminal, 'departs': second_terminal, 'time': 22.06190476190476}, {'arrives': second_terminal, 'departs': first_terminal, 'time': 22.599999999999998}]
        schedule = Schedule().build_schedule(route, ferry, 'Monday')
        self.assertEqual(schedule, expected_schedule)

    def test_daily_crossings(self):
        ferry_class = Ferry_Class(
            passengers = 2500, cars = 200, trucks = 60, burn_rate = 350, 
            speed = 21, turnover_time = 0.2
        )
        ferry = Ferry(ferry_class = ferry_class, name = 'M/V Wenatchee')
        ferries = [ferry]
        first_terminal = Terminal(
            id = 1, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        second_terminal = Terminal(
            id = 2, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        route = Route(first_terminal = first_terminal, second_terminal = second_terminal, 
            ferries = ferries, passenger_fare = 8, car_fare = 18, truck_fare = 50
        )

        daily_results = Sailings().daily_crossings(route, 'Tuesday', 7, 2016)
        self.assertEqual(daily_results[0]['results']['total_passengers'], 8270)
        self.assertEqual(daily_results[0]['results']['total_cars'], 1276)
        self.assertEqual(daily_results[0]['results']['total_trucks'], 190)
        # self.assertEqual(daily_results[0]['results']['total_sailings'], 35)
        # self.assertEqual(daily_results[0]['results']['total_hours'], 20)
        
    def test_weekly_crossings(self):
        ferry_class = Ferry_Class(
            passengers = 2500, cars = 200, trucks = 60, burn_rate = 350, 
            speed = 21, turnover_time = 0.2
        )
        ferry = Ferry(ferry_class = ferry_class, name = 'M/V Wenatchee')
        ferries = [ferry]
        first_terminal = Terminal(
            id = 1, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        second_terminal = Terminal(
            id = 2, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        route = Route(first_terminal = first_terminal, second_terminal = second_terminal, 
            ferries = ferries, passenger_fare = 8, car_fare = 18, truck_fare = 50
        )
        
        weekly_results = Sailings().weekly_crossings(route, 7, 2016)
        self.assertEqual(weekly_results[0]['ferry'], ferry)
        self.assertEqual(weekly_results[0]['results']['total_passengers'], 56750)
        self.assertEqual(weekly_results[0]['results']['total_cars'], 8756)
        self.assertEqual(weekly_results[0]['results']['total_trucks'], 1304)
        self.assertEqual(weekly_results[0]['results']['total_sailings'], 269)
        self.assertEqual(weekly_results[0]['results']['total_hours'], 152)
        
    def test_calc_turn_results_with_two_ferries(self):
        # ferryA will carry passengers, cars, and trucks and ferryB only passengers
        ferry_classA = Ferry_Class(
            passengers = 2500, cars = 200, trucks = 60, burn_rate = 350, 
            speed = 21, turnover_time = 0.2
        )
        ferry_classB = Ferry_Class(
            passengers = 250, cars = 0, trucks = 0, burn_rate = 35, 
            speed = 30, turnover_time = 0.1
        )
        ferryA = Ferry(ferry_class = ferry_classA, name = 'M/V Wenatchee')
        ferryB = Ferry(ferry_class = ferry_classB, name = 'M/V Puyallup')
        ferries = [ferryA, ferryB]
        first_terminal = Terminal(
            id = 1, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        second_terminal = Terminal(
            id = 2, passenger_pool = 13000, car_pool = 2000, truck_pool = 300
        )
        route = Route(first_terminal = first_terminal, second_terminal = second_terminal, 
            ferries = ferries, passenger_fare = 8, car_fare = 18, truck_fare = 50
        )

        weekly_results = Sailings().weekly_crossings(route, 7, 2016)
        self.assertEqual(weekly_results[0]['ferry'], ferryA)
        self.assertEqual(weekly_results[1]['ferry'], ferryB)
        self.assertEqual(weekly_results[0]['results']['total_passengers'], 52368)
        self.assertEqual(weekly_results[1]['results']['total_passengers'], 4382)
        self.assertEqual(weekly_results[0]['results']['total_cars'], 8756)
        self.assertEqual(weekly_results[1]['results']['total_cars'], 0)
        self.assertEqual(weekly_results[0]['results']['total_trucks'], 1304)
        self.assertEqual(weekly_results[1]['results']['total_trucks'], 0)
        self.assertEqual(weekly_results[0]['results']['total_sailings'], 269)
        self.assertEqual(weekly_results[1]['results']['total_sailings'], 435)
        self.assertEqual(weekly_results[0]['results']['fuel_used'], 53200)
        self.assertEqual(weekly_results[1]['results']['fuel_used'], 5320)
        self.assertEqual(weekly_results[0]['ferry'].name, 'M/V Wenatchee')
        self.assertEqual(weekly_results[1]['ferry'].name, 'M/V Puyallup')
        
if __name__ == '__main__':
    unittest.main()