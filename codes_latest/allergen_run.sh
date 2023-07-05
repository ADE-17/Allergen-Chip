#!/bin/bash
#SBATCH --clusters=tinygpu
#SBATCH --partition=rtx3080
#SBATCH --gres=gpu:rtx3080:1
#SBATCH --time=24:00:00

cd $HOME
# module load python/3.10-anaconda
source miniconda/bin/activate
srun python auto_ml.py 