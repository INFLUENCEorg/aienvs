#!/bin/sh
ENV_FILE=${3:-./debug_configs/factory_floor_cluster.yaml}
AGENT_FILE=${4:-./debug_configs/agent_config_seq.yaml}
DATA_DIR=${1:-data/}
DEPENDENCY=${2:-NONE}

if [ $DEPENDENCY = "NONE" ]; then
    JOBID=$(sbatch --parsable collect_data_batcher.sh $ENV_FILE $AGENT_FILE $DATA_DIR)
else
    JOBID=$(sbatch --parsable --dependency=afterok:$DEPENDENCY collect_data_batcher.sh $ENV_FILE $AGENT_FILE $DATA_DIR)
fi

mkdir -p $DATA_DIR
mkdir $DATA_DIR/$JOBID
cp $ENV_FILE $DATA_DIR/$JOBID/env.yaml
cp $AGENT_FILE $DATA_DIR/$JOBID/agent.yaml

echo $JOBID
