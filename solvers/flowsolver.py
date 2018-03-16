#! /usr/bin/python3

from scipy import spatial
from tqdm import tqdm

from car import Car
from ride import Ride
from score import Score
from solvers.basesolver import BaseSolver


class FlowRide(Ride):
    def __init__(self, rid, x1, y1, x2, y2, step_min, step_max):
        super().__init__(rid, x1, y1, x2, y2, step_min, step_max)
        self.flow = 0

    def compute_flow(self, kdtree, radius):
        self.flow = len(kdtree.query_ball_point((self.x2, self.y2), radius))


class FlowSolver(BaseSolver):
    def __init__(self):
        super().__init__()

    def get_solution(self, rides_list, rows, columns, vehicles, rides, bonus, steps, args):
        cars = [Car() for _ in range(vehicles)]
        score = Score()
        rides_instance_list = [FlowRide(rid, *data) for rid, data in enumerate(rides_list)]
        departures = [(r.x1, r.y1) for r in rides_instance_list]
        kdtree = spatial.KDTree(departures)
        flow_bar = tqdm(rides_instance_list) if args.progress else rides_instance_list
        for r in flow_bar:
            r.compute_flow(kdtree, 20)
        rides_sorted = sorted(rides_instance_list, key=lambda ride: (ride.step_min, ride.flow))
        rides_sorted = tqdm(rides_sorted) if args.progress else rides_sorted
        for r in rides_sorted:
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
