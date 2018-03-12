# Hash Code Qualification Round 2018

Team MetaModHell

## Usage

`./solver.py res/b_should_be_easy.in`

```
INFO:root:opening res/b_should_be_easy.in
score: 176,877
INFO:root:dumping rides to res/b_should_be_easy.out
```

`./solver.py res/b_should_be_easy.in --score --wait --rides`

```
INFO:root:opening res/b_should_be_easy.in
rides: 300 = 294 (taken) + 6 (left)
wait time: 149,714
score: 176,877 = 169,677 + 7,200 (bonus)
INFO:root:dumping rides to res/b_should_be_easy.out
```

`./solver.py res/*.in`

```
INFO:root:opening res/a_example.in
score: 10
INFO:root:dumping rides to res/a_example.out
INFO:root:opening res/b_should_be_easy.in
score: 176,877
INFO:root:dumping rides to res/b_should_be_easy.out
INFO:root:opening res/c_no_hurry.in
score: 13,052,303
INFO:root:dumping rides to res/c_no_hurry.out
INFO:root:opening res/d_metropolis.in
score: 11,364,520
INFO:root:dumping rides to res/d_metropolis.out
INFO:root:opening res/e_high_bonus.in
score: 21,465,945
INFO:root:dumping rides to res/e_high_bonus.out
total score: 46,059,655
```

## Progress Bar

`./solver.py res/c_no_hurry.in res/d_metropolis.in  --progress `

```
INFO:root:opening res/c_no_hurry.in
100%|███████████████████████████████████████| 10000/10000 [00:04<00:00, 2086.68it/s]
score: 13,052,303
INFO:root:dumping rides to res/c_no_hurry.out
INFO:root:opening res/d_metropolis.in
 43%|█████████████████▌                       | 4277/10000 [00:10<00:14, 403.53it/s]
```

progress bars require [tqdm](https://github.com/tqdm/tqdm) module.

## Heuristics

On rides

* priority to rides starting early

On cars

* priority to cars able to start on time (granting bonus points)
* priority to car closer to ride start

Flow

* number of departures within radius of arrival

## Our Team & Qualification Round Score

<https://hashcode.withgoogle.com/hashcode_2018.html>

Team: MetaModHell

Members (listed alphabetically): Karbok, PicoJr

### Qualification Round Submissions

| Input            |  Score     |
|:-----------------|-----------:|
| A-example        | 10         |
| B-should be easy | 176,877    |
| C-no hurry       | 13,052,303 |
| D-metropolis     | 11,353,640 |
| E-high bonus     | 21,465,945 |

Score: 46,048,775

Rank: 628th World, 81st France

## Extended Round Submissions

| Input            |  Score     |
|:-----------------|-----------:|
| A-example        | 10         |
| B-should be easy | 176,877    |
| C-no hurry       | 13,147,624 |
| D-metropolis     | 11,354,814 |
| E-high bonus     | 21,465,945 |

Score: 46,145,270

Rank: 632th World, 90th France

## After Extended Round

| Input            |  Score     |
|:-----------------|-----------:|
| A-example        | 10         |
| B-should be easy | 176,877    |
| C-no hurry       | 13,275,923 |
| D-metropolis     | 11,386,481 |
| E-high bonus     | 21,465,945 |

Score: 46,305,236
