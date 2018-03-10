#! /usr/bin/python3

import re
import logging
import argparse


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

    def distance_to_ride_start(self, ride):
        return d(self.x, self.y, ride.x1, ride.y1)

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


def get_solution(rides_list, vehicles, bonus):
    rides = sorted(rides_list, key=lambda r: r.step_min)
    cars = []
    raw_score, bonus_score = 0, 0
    for i in range(vehicles):
        cars.append(Car())
    for ride in rides:
        assigned = False
        cars_by_distance = sorted(cars, key=lambda c: c.distance_to_ride_start(ride))
        # Search 1 : on-time only
        for car in cars_by_distance:
            if car.can_start_on_time(ride):
                car.assign(ride)
                raw_score += ride.distance()
                bonus_score += bonus
                assigned = True
                break  # skip all other cars and go to the next ride
        # Search 2 : technically possible
        if not assigned:
            for car in cars_by_distance:
                if car.can_finish_in_time(ride):
                    car.assign(ride)
                    raw_score += ride.distance()
                    break  # skip all other cars and go to the next ride
    rides_solution = [c.assigned_rides for c in cars]
    return rides_solution, raw_score, bonus_score


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
    parser = argparse.ArgumentParser(description='parse input data set')
    parser.add_argument('file_in', type=str, nargs='+', help='<file basename>.in file input')
    parser.add_argument('--debug', action='store_true', help='for debug purpose')
    args = parser.parse_args()
    set_log_level(args)
    raw_score_total, bonus_score_total = 0, 0
    for file_in in args.file_in:
        (rides_list, rows, columns, vehicles, rides, bonus, steps) = parse_input(file_in)
        solution, raw_score, bonus_score = get_solution(rides_list, vehicles, bonus)
        raw_score_total += raw_score
        bonus_score_total += bonus_score
        logging.info("score: {0:,} = {1:,} + {2:,} (bonus)".format(raw_score + bonus_score, raw_score, bonus_score))
        file_out = get_file_out_name(file_in)
        dump_rides(solution, file_out)
    if len(args.file_in) > 1:
        logging.info("total: {0:,} = {1:,} + {2:,} (bonus)".format(raw_score_total + bonus_score_total, raw_score_total, bonus_score_total))


if __name__ == "__main__":
    main()
