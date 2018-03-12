# Heuristics Used

On rides

* priority to rides starting early

On cars

* priority to cars able to start on time (granting bonus points)
* priority to car closer to ride start

## Results

`./solver.py res/*.in --score --progress --wait --rides`

```
INFO:root:opening res/a_example.in
100%|██████████████████████████████████████████████| 3/3 [00:00<00:00, 10866.07it/s]
rides: 3 = 3 (taken) + 0 (left)
wait time: 2
score: 10 = 8 + 2 (bonus)
INFO:root:dumping rides to res/a_example.out
INFO:root:opening res/b_should_be_easy.in
100%|███████████████████████████████████████████| 300/300 [00:00<00:00, 1128.55it/s]
rides: 300 = 294 (taken) + 6 (left)
wait time: 149,714
score: 176,877 = 169,677 + 7,200 (bonus)
INFO:root:dumping rides to res/b_should_be_easy.out
INFO:root:opening res/c_no_hurry.in
100%|███████████████████████████████████████| 10000/10000 [00:04<00:00, 2021.35it/s]
rides: 10,000 = 7,805 (taken) + 2,195 (left)
wait time: 0
score: 13,052,303 = 13,052,303 + 0 (bonus)
INFO:root:dumping rides to res/c_no_hurry.out
INFO:root:opening res/d_metropolis.in
100%|████████████████████████████████████████| 10000/10000 [00:21<00:00, 456.84it/s]
rides: 10,000 = 7,935 (taken) + 2,065 (left)
wait time: 3,273,198
score: 11,364,520 = 11,359,818 + 4,702 (bonus)
INFO:root:dumping rides to res/d_metropolis.out
INFO:root:opening res/e_high_bonus.in
100%|████████████████████████████████████████| 10000/10000 [00:29<00:00, 334.28it/s]
rides: 10,000 = 9,984 (taken) + 16 (left)
wait time: 2,032,526
score: 21,465,945 = 11,588,945 + 9,877,000 (bonus)
INFO:root:dumping rides to res/e_high_bonus.out
total wait time: 5,455,440
total score: 46,059,655 = 36,170,751 + 9,888,904 (bonus)
```
