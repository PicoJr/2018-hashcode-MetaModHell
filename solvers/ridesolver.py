#! /usr/bin/python3

from tqdm import tqdm

from car import Car
from ride import Ride
from score import Score
from solvers.basesolver import BaseSolver


class RideSolver(BaseSolver):
    def __init__(self):
        super().__init__()

    def get_solution(self, rides_list, rows, columns, vehicles, rides, bonus, steps, args):
        cars = [Car() for _ in range(vehicles)]
        score = Score()
        rides_instance_list = [Ride(rid, *data) for rid, data in enumerate(rides_list)]
        rides_earliest_departure = sorted(rides_instance_list, key=lambda ride: ride.step_min)
        rides_earliest_departure = tqdm(rides_earliest_departure) if args.progress else rides_earliest_departure
        for r in rides_earliest_departure:
            candidates = [c for c in cars if c.can_finish_in_time(r, steps)]
            cars_with_bonus = [c for c in candidates if c.can_start_on_time(r)]
            if cars_with_bonus:
                best_car = min(cars_with_bonus, key=lambda c: c.wait_time(r))
                score.bonus_score += bonus
                score.raw_score += r.distance()
                score.wait_time += best_car.wait_time(r)
                score.assigned += 1
                best_car.assign(r)
            elif candidates:
                best_car = min(candidates, key=lambda c: c.distance_to_ride_start(r))
                score.raw_score += r.distance()
                score.assigned += 1
                best_car.assign(r)
            else:
                score.unassigned += 1
        rides_solution = [c.assigned_rides for c in cars]
        return rides_solution, score
