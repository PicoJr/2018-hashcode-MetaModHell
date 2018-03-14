class Score(object):
    def __init__(self):
        self.raw_score = 0
        self.bonus_score = 0
        self.assigned = 0
        self.unassigned = 0
        self.wait_time = 0

    def total(self):
        return self.raw_score + self.bonus_score

    def add(self, other):
        self.raw_score += other.raw_score
        self.bonus_score += other.bonus_score
        self.assigned += other.assigned
        self.unassigned += other.unassigned
        self.wait_time += other.wait_time
