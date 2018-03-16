from util import manhattan


class Car(object):
    def __init__(self):
        self.assigned_rides = []
        self.step = 0
        self.x = 0
        self.y = 0

    def distance_to(self, x, y):
        return manhattan(self.x, self.y, x, y)

    def distance_to_ride_start(self, ride):
        return manhattan(self.x, self.y, ride.x1, ride.y1)

    def wait_time(self, ride):
        return max(0, ride.step_min - (self.step + self.distance_to_ride_start(ride)))
    def arrival(self, ride):
        return self.step + self.distance_to_ride_start(ride) + self.wait_time(ride) + ride.distance()

    def can_start_on_time(self, ride):
        return self.step + self.distance_to_ride_start(ride) <= ride.step_min

    def can_finish_in_time(self, ride, steps):
        can_finish = self.arrival(ride) <= min(ride.step_max, steps)
        return can_finish

    def assign(self, ride):
        self.assigned_rides.append(ride.rid)
        step_departure = max(ride.step_min, self.step + self.distance_to_ride_start(ride))
        self.step = step_departure + ride.distance()
        self.x = ride.x2
        self.y = ride.y2
