#! /usr/bin/python3

import argparse
import logging
import re
from tqdm import tqdm
from scipy import spatial

def d(x1, y1, x2, y2):
    """Manhattan distance between (x1,y1) and (x2,y2)"""
    return abs(x2 - x1) + abs(y2 - y1)


class Ride(object):
    def __init__(self, rid, x1, y1, x2, y2, step_min, step_max):
        self.rid = rid
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.step_min = step_min
        self.step_max = step_max
        self.flow = 0

    def distance(self):
        return d(self.x1, self.y1, self.x2, self.y2)

    def compute_flow(self, kdtree, radius):
        self.flow = len(kdtree.query_ball_point((self.x2,self.y2), radius))


class Car(object):
    def __init__(self):
        self.assigned_rides = []
        self.step = 0
        self.x = 0
        self.y = 0

    def distance_to(self, x, y):
        return d(self.x, self.y, x, y)

    def distance_to_ride_start(self, ride):
        return d(self.x, self.y, ride.x1, ride.y1)

    def wait_time(self, ride):
        return max(0, ride.step_min - (self.step + self.distance_to_ride_start(ride)))

    def can_start_on_time(self, ride):
        return self.step + self.distance_to_ride_start(ride) <= ride.step_min

    def can_finish_in_time(self, ride):
        can_finish = self.step + self.distance_to_ride_start(ride) + ride.distance() <= ride.step_max
        return can_finish

    def assign(self, ride):
        self.assigned_rides.append(ride.rid)
        step_departure = max(ride.step_min, self.step + self.distance_to_ride_start(ride))
        self.step = step_departure + ride.distance()
        self.x = ride.x2
        self.y = ride.y2


class Score(object):
    def __init__(self):
        self.raw_score = 0
        self.bonus_score = 0
        self.unassigned = 0
        self.wait_time = 0

    def total(self):
        return self.raw_score + self.bonus_score

    def add(self, other):
        self.raw_score += other.raw_score
        self.bonus_score += other.bonus_score
        self.unassigned += other.unassigned
        self.wait_time += other.wait_time


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: rides_list, rows, columns, vehicles, rides, bonus, steps
    """
    logging.info("opening {}".format(file_in))
    with open(file_in, 'r') as f:
        first_line = f.readline()
        rows, columns, vehicles, rides, bonus, steps = tuple([int(x) for x in first_line.split(' ')])
        logging.debug("{} {} {} {} {} {}".format(rows, columns, vehicles, rides, bonus, steps))
        rides_list = []
        for rid, line in enumerate(f.readlines()):
            ride = tuple([int(x) for x in line.split(' ')])  # x1, y1, x2, y2, step_start, step_end
            rides_list.append(Ride(rid, *ride))
    logging.debug("parsing rides done")
    return rides_list, rows, columns, vehicles, rides, bonus, steps


def dump_rides(rides, output):
    """
    Dump rides to output file.
    :param rides: rides assigned to vehicles, i.e. rides[i] = ride ids assigned to vehicle i
    :param output: output file name
    :return: None
    """
    logging.info("dumping rides to {}".format(output))
    data = ""
    for rids in rides:
        data += str(len(rids))
        if rids:
            data += ' '
            data += ' '.join([str(r) for r in rids])
        data += '\n'
    with open(output, 'w+') as f:
        f.write(data)  # only one write statement -> much quicker
    logging.debug("dumping rides: done")


def get_solution(rides_list, vehicles, bonus, progress):
    cars = [Car() for _ in range(vehicles)]
    score = Score()
    data = [(r.x1, r.y1) for r in rides_list]
    kdtree = spatial.KDTree(data)
    flow_bar = tqdm(rides_list) if progress else rides_list
    for r in flow_bar:
        r.compute_flow(kdtree, 20)
    rides_sorted = sorted(rides_list, key=lambda ride: (ride.step_min, ride.flow))
    rides_sorted = tqdm(rides_sorted) if progress else rides_sorted
    for r in rides_sorted:
        candidates = [c for c in cars if c.can_finish_in_time(r)]
        cars_with_bonus = [c for c in candidates if c.can_start_on_time(r)]
        if cars_with_bonus:
            best_car = min(cars_with_bonus, key=lambda c: c.wait_time(r))
            score.bonus_score += bonus
            score.raw_score += r.distance()
            score.wait_time += best_car.wait_time(r)
            best_car.assign(r)
        elif candidates:
            best_car = min(candidates, key=lambda c: c.distance_to_ride_start(r))
            score.raw_score += r.distance()
            best_car.assign(r)
        else:
            score.unassigned += 1
    rides_solution = [c.assigned_rides for c in cars]
    return rides_solution, score


def set_log_level(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def get_file_out_name(file_in_name):
    basename_search = re.search("(.*)\.in", file_in_name)
    if basename_search:
        return basename_search.group(1) + '.out'
    else:
        return 'default.out'


def main():
    parser = argparse.ArgumentParser(description='assign rides to cars')
    parser.add_argument('file_in', type=str, nargs='+', help='<file basename>.in file input')
    parser.add_argument('--debug', action='store_true', help='for debug purpose')
    parser.add_argument('--wait', action='store_true', help='display wait time')
    parser.add_argument('--rides', action='store_true', help='display rides taken and left')
    parser.add_argument('--score', action='store_true', help='display raw score and bonus score')
    parser.add_argument('--progress', action='store_true', help='display progress bar')
    args = parser.parse_args()
    set_log_level(args)
    score_total = Score()
    batch = len(args.file_in) > 1  # several input files
    for file_in in args.file_in:
        (rides_list, rows, columns, vehicles, rides, bonus, steps) = parse_input(file_in)
        solution, score = get_solution(rides_list, vehicles, bonus, args.progress)
        score_total.add(score)
        if args.rides:
            print(
                "rides: {0:,} = {1:,} (taken) + {2:,} (left)".format(rides, rides - score.unassigned, score.unassigned))
        if args.wait:
            print("wait time: {0:,}".format(score.wait_time))
        if args.score:
            print("score: {0:,} = {1:,} + {2:,} (bonus)".format(score.total(), score.raw_score, score.bonus_score))
        else:
            print("score: {0:,}".format(score.total()))
        file_out = get_file_out_name(file_in)
        dump_rides(solution, file_out)
    if batch:
        if args.wait:
            print("total wait time: {0:,}".format(score_total.wait_time))
        if args.score:
            print("total score: {0:,} = {1:,} + {2:,} (bonus)".format(score_total.total(), score_total.raw_score,
                                                                      score_total.bonus_score))
        else:
            print("total score: {0:,}".format(score_total.total()))


if __name__ == "__main__":
    main()
