#! /usr/bin/python3

import argparse
import logging
import re

from solvers.ridesolver import RideSolver
from solvers.flowsolver import FlowSolver

from rides_io import parse_input, dump_rides
from score import Score


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


def get_solver(name):
    if name == 'flow':
        return FlowSolver()
    elif name == 'ride':
        return RideSolver()
    else:
        return RideSolver()


def print_score(score, args):
    if args.rides:
        print(
            "rides: {0:,} = {1:,} (taken) + {2:,} (left)".format(score.assigned + score.unassigned, score.assigned, score.unassigned))
    if args.wait:
        print("wait time: {0:,}".format(score.wait_time))
    if args.score:
        print("score: {0:,} = {1:,} + {2:,} (bonus)".format(score.total(), score.raw_score, score.bonus_score))
    else:
        print("score: {0:,}".format(score.total()))


def main():
    parser = argparse.ArgumentParser(description='assign rides to cars')
    parser.add_argument('file_in', type=str, nargs='+', help='<file basename>.in file input')
    parser.add_argument('--solver', type=str, default='ride', choices=('ride', 'flow'), help='solver')
    parser.add_argument('--debug', action='store_true', help='for debug purpose')
    parser.add_argument('--wait', action='store_true', help='display wait time')
    parser.add_argument('--rides', action='store_true', help='display rides taken and left')
    parser.add_argument('--score', action='store_true', help='display raw score and bonus score')
    parser.add_argument('--progress', action='store_true', help='display progress bar')
    args = parser.parse_args()
    set_log_level(args)
    solver = get_solver(args.solver)
    score_total = Score()
    batch = len(args.file_in) > 1  # several input files
    for file_in in args.file_in:
        (rides_list, rows, columns, vehicles, rides, bonus, steps) = parse_input(file_in)
        solution, score = solver.get_solution(rides_list, rows, columns, vehicles, rides, bonus, steps, args)
        print_score(score, args)
        score_total.add(score)
        file_out = get_file_out_name(file_in)
        dump_rides(solution, file_out)
    if batch:
        print_score(score_total, args)


if __name__ == "__main__":
    main()
