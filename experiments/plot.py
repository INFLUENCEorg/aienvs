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

    for generationDir in os.listdir(dirname+"/data"):
        generationCount += 1
        rewardList = []
        allRewardFiles = glob.glob( dirname + '/data/'+generationDir+ "/**/rewards.yaml" ) 

        for rewardFile in allRewardFiles:
            with open(rewardFile, 'rb') as instream:
                newRewards = yaml.load(instream)
                rewardList.extend(newRewards)

        print(rewardList)
        rewardMeans.append(np.mean(rewardList))
        confBound = list(st.t.interval(0.95, len(rewardList)-1, loc=np.mean(rewardList), scale=st.sem(rewardList)))
        confBoundList.append((rewardMeans-confBound[0])[0])

    confBoundArray = np.transpose(np.array(confBoundList))

    gens = np.arange(generationCount)
    print(gens)
    print(rewardMeans)
    print(confBoundList)
    
    plt.xlabel("Generation")
    plt.ylabel("Mean total reward")
    plt.scatter(gens, rewardMeans, color="m")
    plt.errorbar(gens,rewardMeans, yerr=confBoundList, ecolor="k", ls="none", uplims=True, lolims=True)
    plt.show()

if __name__=="__main__":
    main()
