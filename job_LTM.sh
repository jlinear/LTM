
#!/bin/csh
#$ -q long
#$ -pe smp 12
#$ -M jyang9@nd.edu
#$ -m abe
#$ -N LTM


module load python

python ./code/LTM.py ./data/data_text_CP_rawdb.txt text

python ./code/LTM.py ./data/data_post_CP_rawdb.txt post

python ./code/LTM.py ./data/data_both_CP_rawdb.txt both

