class Schedule(object):
    def __init__(self, ferry, route, times):
        self.ferry = ferry
        self.route = route
        self.times = times

    def time_to_cross(self):
        KNOTS_TO_MPG = 1.152
        print(self.times[0])
        return self.route.distance / self.ferry.speed * KNOTS_TO_MPG
