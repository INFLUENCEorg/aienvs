from utils import preprocess
from aienvs.utils import getParameters
from aienvs.FactoryFloor.FactoryFloorState import toTuple
import yaml
import sys
import os
from scipy import stats as s

def formTabularModels(dirname, outputdir, robotIds):
    os.makedirs(outputdir, exist_ok=True)

    for robotId in robotIds:
        states, actions = preprocess(dirname, [robotId])
    
        actionDict = {}

        idx=0
        while idx < len(states):
            try:
                actionDict[toTuple(states[idx])].append(actions[idx])
            except KeyError:
                actionDict[toTuple(states[idx])]=[actions[idx]]
            idx+=1

        for key in actionDict.keys():
            actionDict[key]=s.mode(actionDict[key])[0][0]
        
        with open(outputdir + "/" + robotId + '.yaml', 'w+') as outfile:
            yaml.dump(actionDict, outfile, default_flow_style=False)


def main():
    if(len(sys.argv) == 3):
        param_filename = str(sys.argv[1])
        parametersDict = getParameters(param_filename)
        dirname = str(sys.argv[2])
        outputdir = parametersDict["outputDir"]
        robotIds = parametersDict["robotIds"]
    else:
        raise "3 arguments needed"

    formTabularModels(dirname, outputdir, robotIds)

if __name__ == "__main__":
        main()
	
    
