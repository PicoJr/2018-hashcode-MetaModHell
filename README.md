# Hash Code Qualification Round 2018

Team MetaModHell

## Usage

`./solver.py res/b_should_be_easy.in`

```
INFO:root:opening res/b_should_be_easy.in
INFO:root:rides: 300 = 294 (taken) + 6 (left)
INFO:root:score: 176,877 = 169,677 + 7,200 (bonus)
INFO:root:dumping rides to res/b_should_be_easy.out
```

`./solver.py res/*.in`

```
INFO:root:opening res/a_example.in
INFO:root:rides: 3 = 3 (taken) + 0 (left)
INFO:root:score: 10 = 8 + 2 (bonus)
INFO:root:dumping rides to res/a_example.out
INFO:root:opening res/b_should_be_easy.in
INFO:root:rides: 300 = 294 (taken) + 6 (left)
INFO:root:score: 176,877 = 169,677 + 7,200 (bonus)
INFO:root:dumping rides to res/b_should_be_easy.out
INFO:root:opening res/c_no_hurry.in
INFO:root:rides: 10,000 = 7,805 (taken) + 2,195 (left)
INFO:root:score: 13,052,303 = 13,052,303 + 0 (bonus)
INFO:root:dumping rides to res/c_no_hurry.out
INFO:root:opening res/d_metropolis.in
INFO:root:rides: 10,000 = 7,881 (taken) + 2,119 (left)
INFO:root:score: 11,323,822 = 11,319,124 + 4,698 (bonus)
INFO:root:dumping rides to res/d_metropolis.out
INFO:root:opening res/e_high_bonus.in
INFO:root:rides: 10,000 = 9,984 (taken) + 16 (left)
INFO:root:score: 21,465,945 = 11,588,945 + 9,877,000 (bonus)
INFO:root:dumping rides to res/e_high_bonus.out
INFO:root:total: 46,018,957 = 36,130,057 + 9,888,900 (bonus)
```

## Heuristics

On rides

* priority to rides starting early

On cars

* priority to cars able to start on time (granting bonus points)
* priority to car closer to ride start

## Our Team & Qualification Round Score

<https://hashcode.withgoogle.com/hashcode_2018.html>

Team: MetaModHell

Members (listed alphabetically): Karbok, PicoJr

Score: 46,048,775

Rank: 628th World, 81st France

### Submissions

| Input            |  Score     |
|:-----------------|-----------:|
| A-example        | 10         |
| B-should be easy | 176,877    |
| C-no hurry       | 13,052,303 |
| D-metropolis     | 11,353,640 |
| E-high bonus     | 21,465,945 |
