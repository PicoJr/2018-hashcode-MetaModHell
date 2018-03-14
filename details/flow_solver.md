# Flow Solver

implementation: [flowsolver.py](../solvers/flowsolver.py)

## Heuristics

similar to [ridesolver.py](../solvers/ridesolver.py) except:

* Each ride has a _flow_ value
* The flow is the number of departures within radius of arrival.
* Flow is computed using KDTree.

flow is used as an additional sort key for rides

## Results

| Input            |  Score     |
|:-----------------|-----------:|
| A-example        | 10         |
| B-should be easy | 176,877    |
| C-no hurry       | 13,275,923 |
| D-metropolis     | 11,386,481 |
| E-high bonus     | 21,465,945 |

Score: 46,305,236
