class Ferry(object):
    '''
    The ferry class is the core of the project
    because that's what this game is all about!
    '''

    def __init__(self, passengers, cars, trucks, speed, burn_rate, price, launched, usable_life):
        self.passengers = passengers
        self.cars = cars
        self.trucks = trucks # commercial vehicles
        self.speed = speed # knots
        self.burn_rate = burn_rate # gals/hr
        self.price = price # millions
        self.launched = launched
        self.usable_life = usable_life

    def depreciated_value(self, year):
        age = year - self.launched
        if(age >= self.usable_life):
            return 0
        return self.price - self.price * age / self.usable_life
