from utils import preprocess
from aienvs.FactoryFloor.FactoryFloorState import toTuple
import yaml
import sys
import os
from scipy import stats as s
import configargparse

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
    parser = configargparse.ArgParser()
    parser.add('-c', '--my-config', is_config_file=True, help='config file path')
    parser.add('-d', '--dirname', dest="dirname")
    parser.add('-o', '--outputdir', dest="outputdir")
    parser.add('-r', '--robotIds', dest="robotIds", action="append")
    argums = parser.parse_args()
 
    formTabularModels(argums.dirname, argums.outputdir, argums.robotIds)

if __name__ == "__main__":
        main()
	
    
