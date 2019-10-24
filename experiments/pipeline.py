import subprocess
import shutil
import os, sys
import tempfile
from time import time
from experiments.preprocessorTabular import formTabularModels

env_file = "./debug_configs/factory_floor_local.yaml" 
agent_file = "./debug_configs/agent_local.yaml"
slurm_job_id = 0

def runDjob(datadir,jobid):
    my_env = os.environ.copy()
    my_env["SLURM_JOB_ID"] = str(jobid)
    os.makedirs(datadir+"/"+str(jobid))

    f=open(datadir+"/"+str(jobid)+".out","w+")
    return subprocess.Popen(["python3", "MctsExperiment.py", env_file, agent_file, datadir], 
            env=my_env, stdout=f)

def runTjob(datadir, config):
    outputDir = config["outputDir"]
    if os.path.exists(outputDir):
       shutil.rmtree(outputDir)
    os.makedirs(outputDir, exist_ok=False)
    robotIds = config["robotIds"]
    formTabularModels(datadir, outputDir, robotIds)
    
    #return subprocess.call(["python3", "preprocessorTabular.py", training_file, experiment+"/data"+str(gen)+"/"])

ngenerations=3
nagents=2
ndjobs=2
robotIdsToLearn = ["robot1", "robot2"]

def main():
    experiment="./data/test"+(str(time()).replace('.',''))
    os.makedirs(experiment+"/models")
    models_link="./models"
    if(os.path.exists(models_link)):
        os.unlink(models_link)
    os.symlink(experiment+"/models", models_link)

    for gen in range(1,ngenerations+1):
        print("\nNEW GENERATION\n")
        tjob=None
        datadir=experiment+"/data/"+str(gen)
        try: 
            os.makedirs(datadir, exist_ok=True)
        except:
            pass

        processes=[]
        for djobid in range(1,ndjobs+1):
            processes.append( runDjob(datadir, djobid) )

        for p in processes:
            p.wait()

        agentTrained = (gen % nagents) + 1

        tjobConfig = {"outputDir": "./"+experiment+"/models/agent"+str(agentTrained)+"/", "robotIds": robotIdsToLearn}
        tjob=runTjob(datadir, tjobConfig)

if __name__=="__main__":
    main()
