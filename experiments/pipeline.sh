#!/bin/bash
for (( GEN = 1; GEN <= 5; GEN++ ))      ### Outer for loop ###
do
    TJOB=NONE
    DATADIR = DATA$GEN
    mkdir $DATADIR
    DJOBS=()
    for (( djob = 1 ; djob <= 15; djob++ )) ### Inner for loop ###
    do
        DJOBS+=$(./runner.sh $DATADIR $TJOB)
        DJOBS+=:
    done
    DJOBS+=$(./runner.sh $DATADIR $TJOB) # one last one
    
    ln -sfn $DATADIR data
    mv models/robot.h5 models/robot_gen$GEN.h5
    TJOB=$(sbatch --afterok:$DJOBS --parsable train_batcher.sh)
done
