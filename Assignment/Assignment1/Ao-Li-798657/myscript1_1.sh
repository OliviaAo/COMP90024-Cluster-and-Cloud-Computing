#!/bin/bash
#SBATCH -p cloud
#SBATCH --output=big1_8mpi.txt
#SBATCH --error=big1_8error.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
module load Python/3.4.3-goolf-2015a
mpirun -np 1 python assignment1.py