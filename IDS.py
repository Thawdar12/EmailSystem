# Name: Thawdar Swe Zin
# UOWID: 8039276
# CSCI262 Assignment 3  

import sys
import re
import scipy.stats as stats
import math 

# initialization of global variables
myEvents = []
myStats = []
mySecStats = []
days = 0
totalEvents = 0
baselineMean = []
baselineStd = []

# checking inconsistencies
def checkInconsistence(eventsTxt, statsTxt):
    print("0. Check inconsistencies \n ")
    inconsistent = False
    eventsNum = open(eventsTxt, 'r').readline().strip()
    statsNum = open(statsTxt, 'r').readline().strip()

    # check if number of events in both files are the same
    if(int(eventsNum) != int(statsNum)):
        print("!!! Inconsistency in number of events in both files !!!\n")
        inconsistent = True

    file1 = open(eventsTxt, 'r')
    file2 = open(statsTxt, 'r')

    eventsFile = file1.readlines()
    statsFile = file2.readlines()

    # check if number of events and number of lines are consistent
    num1 = 0
    for line in eventsFile:
        if(line == ""):
            continue
        num1 += 1

    num2 = 0
    for line in statsFile:
        if(line == ""):
            continue
        num2 += 1

    num1 -= 1
    num2 -= 1

    if((num1 != int(eventsNum)) or (num2 != int(statsNum))):
        print(num1, eventsNum)
        print(num2, statsNum)
        print("!!! Inconsistencies found in number of events and number of lines !!!")
        inconsistent = True

    print("< Done checking inconsistencies >\n")     
    return inconsistent

# initial input process
def initialInput(eventsTxt, statsTxt):
    print("1. Initial Input\n")
    # using global variables
    global myEvents
    global myStats
    global mySecStats
    global totalEvents
    global baselineMean
    global baselineSD

    inconsistent = False
    # all the values are resetted
    myEvents = []
    myStats = []
    mySecStats = []
    totalEvents = 0

    file1 = open(eventsTxt, 'r')
    file2 = open(statsTxt, 'r')
    eventsFile = file1.readlines()
    statsFile = file2.readlines()

    ctr = 0
    totalEvents = 0

    print("[ Reading ", eventsTxt," ] \n")
    # reading line by line for events file
    for line in eventsFile: 
        myLine = line.strip()
        print(myLine)
        if(myLine == ""):
            continue
        # first line that stores the number of total events
        if(ctr == 0):
            totalEvents = int(myLine)
            ctr += 1
            continue
        delimiter = re.finditer(pattern=":", string = myLine)
        # find all the indexes that are separated by ':'
        indexes = [index.start() for index in delimiter]
 
        eventName = myLine[0:indexes[0]]
        cd = myLine[indexes[0] + 1 : indexes[1]]
        min = myLine[indexes[1] + 1 : indexes[2]]
        max = myLine[indexes[2] + 1 : indexes[3]]
        weight = int(myLine[indexes[3] + 1 : indexes[4]])
        
        # if event is discrete event
        if(cd == "D"):
            min = int(min)
            max = int(max)
        # if event is continuous event
        elif(cd == "C"):
            min = float(min)
            max = float(max)
        event = [eventName, cd, min, max, weight]
        myEvents.append(event)
        ctr += 1

    ctr = 0

    print("\n[ Reading ", statsTxt, " ]\n")
    # read line by line for stats file
    for line in statsFile: 
        myLine = line.strip()
        print(myLine)
        if(ctr == 0):
            ctr += 1
            continue
        delimiter = re.finditer(pattern=":", string = myLine)
        # find all the indexes that are separated by ':'
        indexes = [index.start() for index in delimiter]

        eventName = myLine[0:indexes[0]]
        mean = float(myLine[indexes[0] + 1:indexes[1]])
        sd = float(myLine[indexes[1] + 1:indexes[2]])

        event = [eventName, mean, sd]
        myStats.append(event)
        ctr += 1

    print("\n" , eventsTxt, " is successfully stored as follows:\n")
    print(myEvents, "\n")
    print("\n", statsTxt, " is successfully stored as follows:\n")
    print(myStats, "\n")

    # check for inconsistency whether the mean is outside the range
    for i in range(0, totalEvents):
        if(myStats[i][1] > myEvents[i][3]):
            inconsistent = True

        if(myStats[i][1] < myEvents[i][2]):
            inconsistent = True
    
    return inconsistent

# Activity Simulation Engine and the Logs
def simulationEngine(first):
    print("2. Activity Simulation Engine and the Logs\n")
    global days
    
    # check if this is the first time of the program or user chooses another file to process
    if(first == True):
        days = int(sys.argv[3])
    elif(first == False):
        days = int(input("  Enter number of days: "))

    # days = int(input(">> Enter number of days: "))

    # first set of the data
    firstSet = []
    print("...Generating random events for each day...\n")
    # generating random numbers for the first set of events based on the days
    for i in range(0, totalEvents):
        min = myEvents[i][2] 
        max = myEvents[i][3]
        mean = myStats[i][1]
        sd = myStats[i][2]
        ranges = stats.truncnorm((min - mean) / sd,(max - mean) / sd,loc=mean, scale = sd)
        randNums = ranges.rvs(days)
        myRandom = []
        # converting to integer number for discrete events
        if(myEvents[i][1] == "D"):
            for j in range (0, len(randNums)):
                myRandom.append(int(randNums[j]))
        else:
            for j in range (0, len(randNums)):
                myRandom.append(float(round(randNums[j],2)))
        firstSet.append(myRandom)
        print("< Done generating random numbers for event: ", myEvents[i][0], " >")

    # creating log file of first set of stats
    firstLog = open('FirstSet.txt', 'w')
    for idx in range(0, days):
        firstLog.write("Day " + str(idx + 1) +  ":\n")
        for oneEvent in range(0, totalEvents):
            firstLog.write(myEvents[oneEvent][0] + ": " + str(firstSet[oneEvent][idx]))
            firstLog.write("\n")
        firstLog.write("\n")
    firstLog.close()
    print("\n< Done writing the first log file: 'FirstSet.txt' >\n")
    return firstSet

# Analysis Engine process
def analysisEngine(firstSet):
    global days
    global baselineMean
    global baselineSD

    print("3. Analysis Engine\n")
    # set the arrays to default
    baselineMean = []
    baselineSD = []

    print("...Measuring the baseline data...\n")
    for i in range(0, totalEvents):
        mean = 0
        sd = 0
        # looping inside all the values for each event
        # calculating mean
        for j in range(0, days):
            mean += firstSet[i][j]
        mean = mean / days

        # calculating standard deviation
        for k in range (0, days):
            sd += pow((firstSet[i][k] - mean),2)

        sd  = math.sqrt(sd / days)

        baselineMean.append(mean)
        baselineSD.append(sd)

    # creating log file for baseline
    baselineTxt = open('Baseline.txt', 'w')
    baselineTxt.write("Total Events: "+ str(totalEvents) + "\n\n")
    baselineTxt.write("The data format below will be -> Event Name : Mean : Standard Deviation : \n\n")
    
    print("Total Events: "+ str(totalEvents) + "\n")
    print("The data format below will be -> Event Name : Mean : Standard Deviation : \n")
    for oneEvent in range(0, totalEvents):
        mean = str(round(baselineMean[oneEvent], 2))
        sd = str(round(baselineSD[oneEvent], 2))
        baselineTxt.write(myEvents[oneEvent][0] + " : " + mean)
        baselineTxt.write(" : " + sd + " : ")
        baselineTxt.write("\n")
        print(myEvents[oneEvent][0] + " : " + mean, end="")
        print(" : " + sd + " : ", end="")
        print()
    baselineTxt.close()
    print("\n< Done writing Baseline.txt >\n")


# Alert Engine process
def alertEngine():
    print("4. Alert Engine")
    global baselineMean
    global baselineSD
    global myEvents
    # second stats file
    stats1Txt = input(">> Enter filename of second Stats.txt: ")
    # number of days to be generated based on second stats file
    days2 = int(input(">> Enter number of days of second stats file: "))

    secondSet = []

    file3 = open(stats1Txt, 'r')
    statsFile1 = file3.readlines()
    # Stats1.txt
    ctr1 = 0
    # Strips the newline character
    for line in statsFile1: 
        myLine = line.strip()
        if(ctr1 == 0):
            ctr1 += 1
            continue
        delimiter = re.finditer(pattern=":", string = myLine)
        indexes = [index.start() for index in delimiter]

        eventName = myLine[0:indexes[0]]
        mean = float(myLine[indexes[0] + 1:indexes[1]])
        sd = float(myLine[indexes[1] + 1:indexes[2]])

        event = [eventName, mean, sd]
        mySecStats.append(event)
        ctr1 += 1

    for i in range(0, totalEvents):
        min = myEvents[i][2] 
        max = myEvents[i][3]
        mean = mySecStats[i][1]
        sd = mySecStats[i][2]
        ranges = stats.truncnorm((min - mean) / sd,(max - mean) / sd,loc=mean, scale = sd)
        randNums = ranges.rvs(days2)
        myRandom = []
        # converting to integer number for discrete events
        if(myEvents[i][1] == "D"):
            for j in range (0, len(randNums)):
                myRandom.append(int(randNums[j]))
        else:
            for j in range (0, len(randNums)):
                myRandom.append(float(round(randNums[j],2)))
        secondSet.append(myRandom)

    # creating log file of second set of stats
    secondLog = open('SecondSet.txt', 'w')
    for idx in range(0, days2):
        secondLog.write("Day " + str(idx + 1) +  ":\n")
        for oneEvent in range(0, totalEvents):
            secondLog.write(myEvents[oneEvent][0] + ": " + str(secondSet[oneEvent][idx]))
            secondLog.write("\n")
        secondLog.write("\n")
    secondLog.close()
    print("< Done writing second log file: 'SecondSet.txt' >\n")

    # array to store anomaly status of each day
    abnormalStatus  = []
    ac = 0

    # calculating total weight
    totalWeight = 0
    for i in range(0, totalEvents):
        totalWeight += myEvents[i][4]

    print("================Anomaly Analysis================\n")
    print("Threshold is: ", totalWeight * 2, "\n")
    print("Anomaly counter for each day:\n")

    # writing to anomaly log file: 'Anomaly.txt'
    anomalyTxt = open('Anomaly.txt', 'w')
    anomalyTxt.write("Threshold is: " + str(totalWeight * 2) + "\n")
    anomalyTxt.write("Anomaly counter for each day:\n")

    # calculate the anomaly counter for each day
    for i in range(0, days2):
        ac = 0
        abnormal = False
        for j in range(0, totalEvents):
            ac += abs(((secondSet[j][i] - baselineMean[j]) / baselineSD[j] )* myEvents[j][4])

        # compare anomaly counter with threshold
        if( ac >= totalWeight * 2):
            abnormal = True
        elif (ac < totalWeight * 2):
            abnormal = False

        abnormalStatus.append(abnormal)

        anomalyTxt.write("Day " + str(i+1) + ": " + str(round(ac,2)))
        
        print("Day " + str(i+1) + ": " + str(round(ac,2)), end=" ")
        if(abnormal == True):
            print("(Anomaly)\n")
            anomalyTxt.write(" (Anomaly)\n\n")
        elif(abnormal == False):
            print("(OK)\n")
            anomalyTxt.write(" (OK)\n\n")

    anomalyTxt.close()
    print("< Done writing to Anomaly.txt. >\n")
    print("== All the processes are done. ==\n")


def dataProcessing(eventsTxt, statsTxt, first):
    inconsistent = initialInput(eventsTxt, statsTxt)
    if(inconsistent == False):
        firstData = simulationEngine(first)
        analysisEngine(firstData)
        alertEngine()
    else:
        print("!!! Inconsistencies found in the data !!!\n")

def mainMenu():
    print("==============================")
    print("1. Process new files")
    print("2. Quit the program")

def main():
    print(" Name: Thawdar Swe Zin \n UOWID: 8039276 \n CSCI262 Assignment 3")
    print("\n----- Welcome -----")
    quitProgram = False

    # taking the filename based on the file execution
    eventsTxt = sys.argv[1]
    statsTxt = sys.argv[2]

    # eventsTxt = "Events.txt"
    # statsTxt = "Stats.txt"

    # checking inconsistencies 
    if(checkInconsistence(eventsTxt, statsTxt)) == True:
        quitProgram = True
    else:
        dataProcessing(eventsTxt, statsTxt, True)

    # loop until user wants to quit the program
    while(quitProgram == False):
        mainMenu()
        option = "3"

        # keep looping until user enters either 1 or 2
        while(option != "1") or (option != "2"):
            option = input("\n>> Choose 1 or 2: ")
            if(option == "1") or (option == "2"):
                break
        
        if(option == "2"):
            quitProgram = True
            break
        elif (option == "1"):
            eventsTxt = input(">> Enter the new events filename: ") 
            statsTxt = input(">> Enter the new stats filename: ") 

        if(checkInconsistence(eventsTxt, statsTxt)) == True:
            quitProgram = True
        else:
            dataProcessing(eventsTxt, statsTxt, False)
        
    print("\n~ Thank you for using the system! ~")

if __name__ == '__main__':
    main()