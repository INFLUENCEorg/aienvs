#!/bin/bash
unlink data

for (( GEN = 1; GEN <= 5; GEN++ ))      ### Outer for loop ###
do
  TJOB=(NONE)
  DATADIR=DATA$GEN
  mkdir $DATADIR
  echo $DATADIR
  exit 1

  DJOBS=()
  for (( djob = 1 ; djob <= 15; djob++ )) ### Inner for loop ###
  do
      DJOBS+=$(./runner.sh $DATADIR $TJOB)
      DJOBS+=:
  done
  DJOBS+=$(./runner.sh $DATADIR $TJOB) # one last one
  
  ln -sfn $DATADIR data
  mv models/robot.h5 models/robot_gen$GEN.h5
  TJOB=$(sbatch --dependency=afterok:$DJOBS --parsable train_batcher.sh)
done
