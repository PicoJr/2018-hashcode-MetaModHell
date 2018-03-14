# Ride Solver

implementation: [ridesolver.py](../solvers/ridesolver.py)

## Heuristics

On rides

* priority to rides starting early

On cars

* priority to cars able to start on time (granting bonus points)
* priority to car closer to ride start

## Results

| Input            |  Score     |
|:-----------------|-----------:|
| A-example        | 10         |
| B-should be easy | 176,877    |
| C-no hurry       | 13,052,303 |
| D-metropolis     | 11,364,520 |
| E-high bonus     | 21,465,945 |

Score: 46,059,655
