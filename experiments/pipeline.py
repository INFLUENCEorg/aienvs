import subprocess
import os
from experiments.preprocessorTabular import formTabularModels

env_file = "./debug_configs/factory_floor_local.yaml" 
agent_file = "./debug_configs/agent_local.yaml"
slurm_job_id = 0

def runDjob(datadir,jobid):
    my_env = os.environ.copy()
    my_env["SLURM_JOB_ID"] = str(jobid)
    os.makedirs(datadir+"/"+str(jobid))
    return subprocess.call(["python3", "MctsExperiment.py", env_file, agent_file, datadir], env=my_env)

def runTjob(datadir, config):
    outputDir = config["outputDir"]
    os.makedirs(outputDir, exist_ok=True)
    robotIds = config["robotIds"]
    formTabularModels(datadir, outputDir, robotIds)
    
    #return subprocess.call(["python3", "preprocessorTabular.py", training_file, experiment+"/data"+str(gen)+"/"])

experiment="testexp3"
ngenerations=2
nagents=2
ndjobs=3

def main():
    for gen in range(1,ngenerations+1):
        print("\nNEW GENERATION\n")
        tjob=None
        datadir=experiment+"/data/"+str(gen)
        try: 
            os.makedirs(datadir, exist_ok=True)
        except:
            pass
        for djobid in range(1,ndjobs+1):
            print("\nNEW DJOB\n")
            runDjob(datadir, djobid)

        agentTrained = gen
        robotIdsToLearn = list(set(["robot1", "robot2"]) - set(["robot"+str(agentTrained)]))
        tjobConfig = {"outputDir": "./models/agent"+str(agentTrained)+"/", "robotIds": robotIdsToLearn}
        tjob=runTjob(datadir, tjobConfig)

if __name__=="__main__":
    main()
