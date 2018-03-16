#! /usr/bin/python3

from tqdm import tqdm

from car import Car
from ride import Ride
from score import Score
from solvers.basesolver import BaseSolver

class CarSolver(BaseSolver):
    def __init__(self):
        super().__init__()

    def get_solution(self, rides_list, rows, columns, vehicles, rides, bonus, steps, args):
        cars = [Car() for _ in range(vehicles)]
        score = Score()
        rides_instance_list = [Ride(rid, *data) for rid, data in enumerate(rides_list)]
        cars = tqdm(cars) if args.progress else cars
        rides_unassigned = rides_instance_list
        for car in cars:
            rides_possible = [r for r in rides_unassigned if car.can_finish_in_time(r, steps)]
            while rides_possible:
                print(len(rides_possible))
                ride = min(rides_possible, key=lambda r: car.arrival(r))  # earliest arrival
                if car.can_start_on_time(ride):
                    score.bonus_score += bonus
                score.raw_score += ride.distance()
                score.wait_time += car.wait_time(ride)
                score.assigned += 1
                car.assign(ride)
                rides_unassigned.remove(ride)  # remove ride for other cars
                rides_possible.remove(ride)
                rides_possible = [r for r in rides_possible if car.can_finish_in_time(r, steps)]
        score.unassigned = len(rides_unassigned)
        rides_solution = [c.assigned_rides for c in cars]
        return rides_solution, score

