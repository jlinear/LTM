
#!/bin/csh
#$ -q debug
#$ -pe smp 12
#$ -M jyang9@nd.edu
#$ -m abe
#$ -N LTM_debug


module load python

python ./code/LTM.py ./data/data_both_CP_rawdb.txt both

