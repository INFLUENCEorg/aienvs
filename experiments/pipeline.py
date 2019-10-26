import subprocess
import shutil
import os, sys
from time import time
import configargparse

def runDjob(env_file, agent_file, datadir, jobid, batching=False, dependencyList=None):
    commandList = ["python3", "MctsExperiment.py", 
        "-e", env_file,
        "-a", agent_file,
        "-d", datadir]

    if(batching):
        return batchJob("./collect_data_batcher.sh", commandList, datadir, dependencyList)
    else:
        my_env = os.environ.copy()
        my_env["SLURM_JOB_ID"] = str(jobid)
        with open(datadir+"/"+str(jobid)+".out","w+") as f:
            return subprocess.Popen(commandList, env=my_env, stdout=f)

def batchJob(runnerFile, commandList, outputdir, dependencyList=[None]):
    command = ["sbatch", "--parsable"]
    if dependencyList[0] is not None:
        dependencyList = [item.decode("utf-8") for item in dependencyList]
        command.append("--dependency=afterok:"+":".join(dependencyList))
    command.extend([runnerFile, " ".join(commandList)])
    command.append(outputdir)
    return subprocess.Popen(command, stdout=subprocess.PIPE)

def runTjob(datadir, modelDir, dlFile, batching=False, dependencyList=None):
    if os.path.exists(modelDir):
       shutil.rmtree(modelDir)
    os.makedirs(modelDir, exist_ok=False)

    command=["python3", "preprocessorDeep.py", 
        "-c", dlFile,
        "-d", datadir,
        "-o", modelDir]

    if(batching):
        job = batchJob("./train_batcher.sh", command, datadir, dependencyList)
        job.wait()
        slurmJobId, err = job.communicate()
        if(slurmJobId):
            slurmJobId=slurmJobId.rstrip()
        print("Tjob: "+str(slurmJobId))
        return slurmJobId.rstrip()
    else:
       subprocess.call(command)


def main():
    parser = configargparse.ArgParser()
    parser.add("-c", "--configFile", is_config_file=True, help="config file path")
    parser.add("-g", "--ngenerations", dest="ngenerations", type=int)
    parser.add("-a", "--nagents", dest="nagents", type=int)
    parser.add("-d", "--ndjobs", dest="ndjobs", type=int)
    parser.add("-s", "--sbatch", dest="sbatch", action="store_true")
    parser.add("-e", "--expname", dest="expname", default="test"+(str(time()).replace('.','')))
    parser.add("-n", "--envFile", dest="envFile")
    parser.add("-t", "--agentFile", dest="agentFile")
    parser.add("-l", "--dlFile", dest="dlFile")
   
    argums = parser.parse_args()

    experiment="./data/"+argums.expname
    if(os.path.exists(experiment)):
        raise Exception("Path to experiment exists")

    os.makedirs(experiment+"/models")
    models_link="./models"
    if(os.path.exists(models_link)):
        os.unlink(models_link)
    os.symlink(experiment+"/models", models_link)

    tDependency=None
    for gen in range(1,argums.ngenerations+1):
        datadir=experiment+"/data/"+str(gen)
        try: 
            os.makedirs(datadir, exist_ok=True)
        except:
            pass

        processes=[]
        for djobid in range(1,argums.ndjobs+1):
            processes.append( runDjob(argums.envFile, argums.agentFile, datadir, 
                djobid, argums.sbatch, [tDependency]) )
        
        dJobDep = []
        for djob in processes:
            djob.wait()
            slurmJobId, err = djob.communicate()
            #rstrip to remove trailing new line
            if(slurmJobId):
                slurmJobId=slurmJobId.rstrip()
            print("Djob: "+str(slurmJobId))
            dJobDep.append(slurmJobId)

        agentTrained = (gen % argums.nagents) + 1

        modelDir = "./"+experiment+"/models/agent"+str(agentTrained)+"/"
        tDependency = runTjob(datadir, modelDir, argums.dlFile, argums.sbatch, dJobDep)

if __name__=="__main__":
    main()
