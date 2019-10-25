import subprocess
import shutil
import os, sys
import tempfile
from time import time

env_file = "./debug_configs/factory_floor_local.yaml" 
agent_file = "./debug_configs/agent_local.yaml"
slurm_job_id = 0

def runDjob(datadir, jobid, batching=False, dependencyList=None):
    commandList = ["python3", "MctsExperiment.py", 
        "-e", env_file,
        "-a", agent_file,
        "-d", datadir]

    if(batching):
        return batchJob(commandList, dependencyList, "./collect_data_batcher.sh")
    else:
        my_env = os.environ.copy()
        my_env["SLURM_JOB_ID"] = str(jobid)
        os.makedirs(datadir+"/"+str(jobid))
        with open(datadir+"/"+str(jobid)+".out","w+") as f:
            return subprocess.Popen(commandList, env=my_env, stdout=f)

def batchJob(commandList, dependencyList, runnerFile):
    command = ["sbatch", "--parsable", runnerFile]
    if dependencyList is not None:
        command.append("--dependency=afterok"+":".join(dependencyList))
    command.append(" ".join(commandList))
    return subprocess.Popen(command)

def runTjob(datadir, config, batching=False, dependencyList=None):
    outputDir = config["outputDir"]
    if os.path.exists(outputDir):
       shutil.rmtree(outputDir)
    os.makedirs(outputDir, exist_ok=False)

    command=["python3", "preprocessorDeep.py", 
        "-d", datadir,
        "-o", outputDir]

    robotIds = config["robotIds"]
    for robotId in robotIds:
        command.append("-r")
        command.append(robotId)
    print(command)

    if(batching):
        job = batchJob(command, dependencyList, "./train_batcher.sh")
        job.wait()
        slurmJobId, err = batchJob.communicate()
        return slurmJobId
    else:
       subprocess.call(command)



ngenerations=4
nagents=2
ndjobs=3
robotIdsToLearn = ["robot1", "robot2"]
sbatch=True

def main():
    if(len(sys.argv) == 2):
        path=str(sys.argv[1])
    else:
        path="test"+(str(time()).replace('.',''))

    experiment="./data/"+path
    if(os.path.exists(experiment)):
        raise Exception("Path to experiment exists")

    os.makedirs(experiment+"/models")
    models_link="./models"
    if(os.path.exists(models_link)):
        os.unlink(models_link)
    os.symlink(experiment+"/models", models_link)

    tDependency="NONE"
    for gen in range(1,ngenerations+1):
        print("\nNEW GENERATION\n")
        datadir=experiment+"/data/"+str(gen)
        try: 
            os.makedirs(datadir, exist_ok=True)
        except:
            pass

        processes=[]
        for djobid in range(1,ndjobs+1):
            processes.append( runDjob(datadir, djobid, sbatch, [tDependency]) )
        
        dJobDep = []
        for djob in processes:
            djob.wait()
            slurmJobId, err = djob.communicate()
            dJobDep.append(slurmJobId)

        agentTrained = (gen % nagents) + 1

        tjobConfig = {"outputDir": "./"+experiment+"/models/agent"+str(agentTrained)+"/", "robotIds": robotIdsToLearn}
        tDependency = runTjob(datadir, tjobConfig, sbatch, dJobDep)

if __name__=="__main__":
    main()
