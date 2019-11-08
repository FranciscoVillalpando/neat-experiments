Same as experiment1 but eliminating the time limit for each genome

usage: 

parallel_test_invoker.sh <run_id> <run_path>

example:

parallel_test_invoker.sh 1563887612 ../../train-levels/common_ancestor/last_gen_genomes/1563887612/ 


./parallel_test_invoker.sh 1564712467 ../../train-levels/sequential_parallel/last_gen_genomes/1564712467/ && ./parallel_test_invoker.sh 1564881282 ../../train-levels/sequential_parallel/last_gen_genomes/1564881282/ && ./parallel_test_invoker.sh 1565063864 ../../train-levels/sequential_parallel/last_gen_genomes/1565063864/

./parallel_test_invoker.sh 1560993029 ../../train-levels/experiment1/last_gen_genomes/1560993029/ && ./parallel_test_invoker.sh 1560994547 ../../train-levels/experiment1/last_gen_genomes/1560994547/ && ./parallel_test_invoker.sh 1561003155 ../../train-levels/experiment1/last_gen_genomes/1561003155/