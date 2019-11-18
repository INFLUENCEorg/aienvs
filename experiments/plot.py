# libraries
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import glob
import yaml
import scipy.stats as st
 
def main():
    if(len(sys.argv) == 2):
        dirname=str(sys.argv[1])
 
    generationCount=0
    rewardMeans = []
    confBoundList = []

    for generationDir in sorted(os.listdir(dirname+"/data")):
        try:
            print(generationDir)
            generationCount += 1
            rewardList = []
            allRewardFiles = glob.glob( dirname + '/data/'+generationDir+ "/**/rewards.yaml" ) 

            for rewardFile in allRewardFiles:
                with open(rewardFile, 'rb') as instream:
                    newRewards = yaml.load(instream)
                    rewardList.extend(newRewards)

            rewardMeans.append(np.mean(rewardList))
            confBound = list(st.t.interval(0.95, len(rewardList)-1, loc=np.mean(rewardList), scale=st.sem(rewardList)))
            confBoundList.append((rewardMeans[-1]-confBound[0]))
            print(rewardMeans[-1])
            print(confBound)
        except:
            pass

    confBoundArray = np.transpose(np.array(confBoundList))

    gens = np.arange(generationCount)
    
    plt.xlabel("Generation")
    plt.ylabel("Mean total reward")
    plt.scatter(gens, rewardMeans, color="m")
    plt.errorbar(gens,rewardMeans, yerr=confBoundList, ecolor="k", ls="none", uplims=True, lolims=True)
    plt.show()

if __name__=="__main__":
    main()
