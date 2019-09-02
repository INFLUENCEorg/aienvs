#!/bin/sh
#you can control the resources and scheduling with '#SBATCH' settings
# (see 'man sbatch' for more information on setting these parameters)

# The default partition is the 'general' partition
#SBATCH --partition=influence

# The default Quality of Service is the 'short' QoS (maximum run time: 4 hours)
#SBATCH --qos=long

# The default run (wall-clock) time is 1 minute
#SBATCH --time=2:00:00

# The default number of parallel tasks per job is 1
#SBATCH --ntasks=1

# The default number of CPUs per task is 1, however CPUs are always allocated per 2, so for a single task you should use 2
#SBATCH --cpus-per-task=2

# The default memory per node is 1024 megabytes (1GB)
#SBATCH --mem=8192

# Set mail type to 'END' to receive a mail when the job finishes (with usage statistics)
#SBATCH --mail-type=END

#SBATCH --gres=gpu

# Your job commands go below here

# Uncomment these lines when your job requires this software
echo "PYTHONPATH: "$PYTHONPATH
DIRNAME=$2
echo $DIRNAME
echo $DIRNAME/data$1/

module use /opt/insy/modulefiles
module load cuda/10.0 cudnn/10.0-7.4.2.24
module list

srun python3 preprocessor2.py debug_configs/training.yaml $DIRNAME/data$1/
#cp $DIRNAME/models/robot.h5 $DIRNAME/models/robot_gen$1.h5
