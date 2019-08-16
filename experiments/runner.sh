#!/bin/sh
echo PYTHONPATH: $PYTHONPATH
ENV_FILE=${1:-./debug_configs/factory_floor_cluster.yaml}
AGENT_FILE=${2:-./debug_configs/agent_cluster.yaml}

JOBID=$(sbatch --parsable batcher.sh $ENV_FILE $AGENT_FILE)

mkdir data/$JOBID
cp $ENV_FILE data/$JOBID/env.yaml
cp $AGENT_FILE data/$JOBID/agent.yaml
