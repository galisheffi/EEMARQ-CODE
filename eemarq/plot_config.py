###### MICROBENCHMARK PLOT CONFIG ######

## Points to location of microbenchmark data (should not change)
microbench_dir = './microbench/data'

### "workloads" experiment configuration ###

## Must correspond to one of the rqrates in run_workloads() in ./microbench/experiment_list_generate.sh
workloads_rqrate = 0
## Only change if you know what you are doing. Must correspong to urates in run_workloads() in ./microbench/experiment_list_generate.sh
workloads_urates = [5]

### "rq_size" experiment configuration ###
rqsize=1000

## Must correspond to one of the ksizes in ./microbench/experiment_list_generate.sh
rqsize_max_key = 1000000


### "rq_threads" experiment configuration ###
n_rq_threads = 0

#########################################

###### MACROBENCHMARK PLOT CONFIG ######

# Points to location of macrobenchmark data (should not change)
macrobench_dir = './macrobench/data'

#########################################
