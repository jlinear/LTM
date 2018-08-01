
#!/bin/csh
#$ -q debug
#$ -pe smp 12
#$ -M jyang9@nd.edu
#$ -m abe
#$ -N LTM


module load python

python ./code/LTM.py ./data/data_text_CP_rawdb.txt
