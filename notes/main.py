import math, random, csv, sys

import ferries
import finance
import routes
import schedules
import fuel
import passengers

if __name__ == '__main__':
    ferry = ferries.Ferry(2500, 160, 20, 18, 240, 80, 1980, 50)
    route = routes.Route(8.6, 8.10, 2507, 'Seattle', 'Bainbridge Island')
    route2 = routes.Route(8.6, 8.10, 2507, 'Bainbridge Island', 'Seattle')
    schedule = schedules.Schedule(ferry, route, [12 + 55 / 60, 4.75, 5 + 20 / 60, 6 + 20 / 60, 7 + 5 / 60, 7 + 55 / 60, 8.75, 9 + 40 / 60, 10 + 25 / 60, 11.5, 12 + 20/60, 13 + 10 / 60, 14 + 5 / 60, 14 + 55 / 60, 15 + 50 / 60, 16 + 35 / 60, 17.5, 18.5, 19 + 10 / 60, 20 + 10 / 60, 20 + 55 / 60, 21.75, 23 + 35 / 60])
    time_to_cross = schedule.time_to_cross()
    print('Time to cross is {} minutes.'.format(time_to_cross * 60))
    gallons_burned = time_to_cross * ferry.burn_rate
    print('The ferry will burn {} gallons of fuel.'.format(gallons_burned))
    print('The fuel cost is ${}'.format(gallons_burned * fuel.cost_per_gallon()))
    passengers = passengers.Passengers()
    # print(passengers.demand('Monday', 1, 'February', 2016) * route.riders / 12)
    # print(passengers.demand('Monday', 6, 'February', 2016) * route.riders / 12)
    # print(passengers.demand('Monday', 6, 'July', 2016) * route.riders / 12)
    print('${} million'.format(ferry.depreciated_value(1981)))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        print(day)
        car_queue = 0
        for hour in range(0, 24):
            for minute in range (0, 60):
                car_queue += round((passengers.demand(day, hour, 'August', 2016) * route.riders / 23) / 60)
                for time in schedule.times:
                    if time == hour + minute / 60:
                        print('car_queue', car_queue)
                        car_queue -= min(ferry.cars, car_queue)
                        print('loading up!', math.trunc(time), ':', str(round(time % 1 * 60)).zfill(2), end = ' ')
    passenger_queue = []
    # first = open('CSV_Database_of_First_Names.csv', 'r')
    # last = open('CSV_Database_of_Last_Names.csv', 'r')
    # passengers = 25000
    # try:
    #     reader_first = list(csv.reader(first))
    #     reader_last = list(csv.reader(last))
    #     # passenger = {'name': 'Rebecca Stevens', 'age': 35, 'student': True}
    #     passenger = {}
    #     for i in range(1, passengers):
    #
    #         passenger['name'] = random.choice(reader_first)[0] + ' ' + random.choice(reader_last)[0]
    #         passenger_queue.append(passenger)
    #         print(passenger)
    # finally:
    #     first.close()
    #     last.close()
    # while True:
    #     menu_selection = ''
    #     print('(Q)uit')
    #     menu_selection = input('Select an option: ').lower()
    #     if menu_selection == 'q':
    #         exit()
