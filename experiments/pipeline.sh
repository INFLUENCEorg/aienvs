#!/bin/bash
unlink data

for (( GEN = 1; GEN <= 5; GEN++ ))      ### Outer for loop ###
do
  TJOB=(NONE)
  DATADIR=data$GEN

  DJOBS=()
  for (( djob = 1 ; djob <= 15; djob++ )) ### Inner for loop ###
  do
      DJOBS+=$(./runner.sh $DATADIR $TJOB)
      DJOBS+=:
  done
  DJOBS+=$(./runner.sh $DATADIR $TJOB) # one last one
  
  TJOB=$(sbatch --dependency=afterok:$DJOBS --parsable train_batcher.sh $GEN)
done
