#! /usr/bin/python3

import re
import logging
import argparse
import heapq
import numpy as np


def d(x1, y1, x2, y2):
    """Manhattan distance between (x1,y1) and (x2,y2)"""
    return abs(x2 - x1) + abs(y2 - y1)


class Ride:
    def __init__(self, rid, x1, y1, x2, y2, step_min, step_max):
        self.rid = rid
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.step_min = step_min
        self.step_max = step_max

    def distance(self):
        return d(self.x1, self.y1, self.x2, self.y2)


class Car:
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


class Score:
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
        rows, columns, vehicles, rides, bonus, steps = tuple(map(int, first_line.split(' ')))
        logging.debug("{} {} {} {} {} {}".format(rows, columns, vehicles, rides, bonus, steps))
        rides_list = []
        for rid, line in enumerate(f.readlines()):
            logging.debug(line.strip())
            ride = tuple(map(int, line.split(' ')))  # x1, y1, x2, y2, step_start, step_end
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


def bonus_ride(cars, ride, k, score, bonus):
    cars_with_bonus = [c for c in cars if c.can_start_on_time(ride)]
    k_closest_cars_with_bonus = heapq.nsmallest(k, cars_with_bonus, key=lambda c: c.distance_to_ride_start(ride))
    if k_closest_cars_with_bonus:
        car = min(k_closest_cars_with_bonus, key=lambda c: c.wait_time(ride))
        assert car.can_finish_in_time(ride)
        score.raw_score += ride.distance()
        score.bonus_score += bonus
        score.wait_time += car.wait_time(ride)
        car.assign(ride)
        return True
    else:
        return False


def normal_ride(cars, ride, k, score):
    cars_can_finish_in_time = [c for c in cars if c.can_finish_in_time(ride)]
    k_closest_cars = heapq.nsmallest(k, cars_can_finish_in_time, key=lambda c: c.distance_to_ride_start(ride))
    if k_closest_cars:
        car = min(k_closest_cars, key=lambda c: c.step)
        assert car.can_finish_in_time(ride)
        score.raw_score += ride.distance()
        car.assign(ride)
        return True
    else:
        return False


def get_solution(rides_list, vehicles, rides, bonus):
    cars = [Car() for i in range(vehicles)]
    score = Score()
    k1 = 5
    k2 = 5
    rides_early_departure = sorted(rides_list, key=lambda r: r.step_min)
    for ride in rides_early_departure:
        if not bonus_ride(cars, ride, k1, score, bonus):
            assigned = normal_ride(cars, ride, k2, score)
            if not assigned:
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
    parser.add_argument('--target', type=int, default=0, help='only dump result if score above target (one input file only)')
    args = parser.parse_args()
    set_log_level(args)
    score_total = Score()
    batch = len(args.file_in) > 1  # several input files
    for file_in in args.file_in:
        (rides_list, rows, columns, vehicles, rides, bonus, steps) = parse_input(file_in)
        solution, score = get_solution(rides_list, vehicles, rides, bonus)
        score_total.add(score)
        logging.info("rides: {0:,} = {1:,} (taken) + {2:,} (left)".format(rides, rides-score.unassigned, score.unassigned))
        logging.info("score: {0:,} = {1:,} + {2:,} (bonus)".format(score.total(), score.raw_score, score.bonus_score))
        file_out = get_file_out_name(file_in)
        if batch or (args.target and score.total() > args.target):
            dump_rides(solution, file_out)
    if batch:
        logging.info("total: {0:,} = {1:,} + {2:,} (bonus)".format(score_total.total(), score_total.raw_score, score_total.bonus_score))
    logging.info("wait time: {0:,}".format(score_total.wait_time))


if __name__ == "__main__":
    main()
