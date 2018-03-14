from util import manhattan


class Ride(object):
    def __init__(self, rid, x1, y1, x2, y2, step_min, step_max):
        self.rid = rid
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.step_min = step_min
        self.step_max = step_max

    def distance(self):
        return manhattan(self.x1, self.y1, self.x2, self.y2)
