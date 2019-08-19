#!/bin/sh
ENV_FILE=${3:-./debug_configs/factory_floor_cluster.yaml}
AGENT_FILE=${4:-./debug_configs/agent_config.yaml}
DATA_DIR=${1:-data/}
DEPENDENCY=${2:-NONE}


if [ "$DEPENDENCY"="NONE" ]
  then
    JOBID=$(sbatch --parsable batcher.sh $ENV_FILE $AGENT_FILE)
  else
    JOBID=$(sbatch --parsable --afterok:$DEPENDENCY batcher.sh $ENV_FILE $AGENT_FILE)
fi

mkdir $DATA_DIR/$JOBID
cp $ENV_FILE $DATA_DIR/$JOBID/env.yaml
cp $AGENT_FILE $DATA_DIR/$JOBID/agent.yaml

echo $JOBID
