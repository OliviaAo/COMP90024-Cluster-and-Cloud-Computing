#!/bin/bash
#SBATCH -p physical
#SBATCH --output=big2_8mpi.txt
#SBATCH --error=big2_8error.txt
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
module load Python/3.4.3-goolf-2015a
mpirun -np 8 python assignment1.py

