# Heuristics Used

same as `solver` except:

* Each ride has a _flow_ value
* The flow is the number of departures within radius of arrival.
* Flow is computed using KDTree.

flow is used as an additional sort key for rides

## Results

`./flow_solver.py res/*.in --score --progress --wait --rides`

```
INFO:root:opening res/a_example.in
100%|███████████████████████████████████████████████| 3/3 [00:00<00:00, 3117.67it/s]
100%|██████████████████████████████████████████████| 3/3 [00:00<00:00, 13039.29it/s]
rides: 3 = 3 (taken) + 0 (left)
wait time: 2
score: 10 = 8 + 2 (bonus)
INFO:root:dumping rides to res/a_example.out
INFO:root:opening res/b_should_be_easy.in
100%|████████████████████████████████████████████| 300/300 [00:00<00:00, 353.50it/s]
100%|████████████████████████████████████████████| 300/300 [00:00<00:00, 870.03it/s]
rides: 300 = 294 (taken) + 6 (left)
wait time: 149,714
score: 176,877 = 169,677 + 7,200 (bonus)
INFO:root:dumping rides to res/b_should_be_easy.out
INFO:root:opening res/c_no_hurry.in
100%|████████████████████████████████████████| 10000/10000 [00:50<00:00, 199.77it/s]
100%|███████████████████████████████████████| 10000/10000 [00:05<00:00, 1792.55it/s]
rides: 10,000 = 7,895 (taken) + 2,105 (left)
wait time: 0
score: 13,275,923 = 13,275,923 + 0 (bonus)
INFO:root:dumping rides to res/c_no_hurry.out
INFO:root:opening res/d_metropolis.in
100%|████████████████████████████████████████| 10000/10000 [00:59<00:00, 168.65it/s]
100%|████████████████████████████████████████| 10000/10000 [00:22<00:00, 451.09it/s]
rides: 10,000 = 7,958 (taken) + 2,042 (left)
wait time: 3,241,930
score: 11,386,481 = 11,381,693 + 4,788 (bonus)
INFO:root:dumping rides to res/d_metropolis.out
INFO:root:opening res/e_high_bonus.in
100%|████████████████████████████████████████| 10000/10000 [00:54<00:00, 182.68it/s]
100%|████████████████████████████████████████| 10000/10000 [00:28<00:00, 353.29it/s]
rides: 10,000 = 9,984 (taken) + 16 (left)
wait time: 2,040,967
score: 21,465,945 = 11,588,945 + 9,877,000 (bonus)
INFO:root:dumping rides to res/e_high_bonus.out
total wait time: 5,432,613
total score: 46,305,236 = 36,416,246 + 9,888,990 (bonus)
```
