
#!/bin/csh
#$ -q long
#$ -pe mpi-24 24
#$ -M jyang9@nd.edu
#$ -m abe
#$ -N PGM_both


module load R

Rscript PGMrun.R