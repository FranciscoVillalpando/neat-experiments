
import sys
import glob
from parse import *
from parse import compile
from collections import defaultdict
'''
    Extracts stats from multiple files

    Take as input the list of files on which to extract NEAT stats.
    Generally this will be the runX.txt files.

    We assume that each generation produces an output with this format:

    Population's average fitness: 326.78333 stdev: 376.21975
    Best fitness: 1881.00000 - size: (12, 3) - species 2 - id 332
    Average adjusted fitness: 0.087
    Mean genetic distance 2.119, standard deviation 0.406
    Population of 60 members in 3 species:
    ID   age  size  fitness  adj fit  stag
    ====  ===  ====  =======  =======  ====
        1    5    11    765.0    0.046     3
        2    1    46   1881.0    0.215     0
        3    1     3     80.0    0.000     0
    Total extinctions: 0
    Generation time: 13.428 sec (12.978 average)

'''

fileNameList = []

# If we don't provide the specific file names,
# then search the current folder for runX.txt files
if len(sys.argv) > 1:
    fileNameList = sys.argv[1:]
else:
    fileNameList = glob.glob("./run*.txt")

print(fileNameList)

# Dictionary organized in the following format : 
# 
# 
#   [stat][run][gen]
# where gen is an array
# Example: statsDict['avg_fitness']['run2'][3]
statsDict = defaultdict(lambda: defaultdict(list))

# key is What lines to search for 
#   parse string
#
parseMap = {
    "avg_fitness": {  # this name does not really matter
        'searchString':'average fitness',  # String that will be used to search for the stat
        'parser':compile("Population's average fitness: {avg_fitness:f} stdev: {stdev:f}") # String used to parse data in the searched line
    },
    "best_genome": {
        'searchString':'Best fitness',
        "parser": compile("Best fitness: {best_genome_fitness:f} - size: {best_genome_size} - species {best_genome_species:d} - id {best_genome_id:d}")
    },
    "gen_time": {
        'searchString':'Generation time',
        "parser": compile("Generation time: {gen_time:f} sec ({avg_time:f} average)"),
        "alt_parser": compile("Generation time: {gen_time:f} sec") # Failback parser
    } 
}

#print(parseMap)

for statFileName in fileNameList:

    with open(statFileName, 'r') as statFile:
        for line in statFile:
            for keyString in parseMap:
                if parseMap[keyString]['searchString'] in line:   
                    parser = parseMap[keyString]['parser']
                    parsedData = parser.parse(line)

                    # Use failback parser if something goes wrong
                    if parsedData == None:
                        parser = parseMap[keyString]['alt_parser']
                        parsedData = parser.parse(line)
                
                    for statName, statValue in parsedData.named.items():
                        # Add result to dictionary
                        statsDict[statName][statFileName].append(statValue)
                        #print(statName)

#print(statsDict)

print(statsDict['avg_fitness']['./run2.txt'])
print(statsDict['best_genome_fitness']['./run5.txt'])
print(statsDict['gen_time']['./run4.txt'])
print(statsDict['gen_time']['./run4.txt'][10])

def collapseByRun(statsDict):
    ''' Returns a map collapsedStats[stat][aggregation][gen]
        where aggregation may be:
            mean
    '''

    collapsedStats = defaultdict(lambda: defaultdict(list))
    statList = []
    runList = []

    for stat in statsDict:
        statList.append(stat)

    for run in statsDict[statList[0]]:
        runList.append(run)

    print(statList, runList)



    #collapsedStats[stat] = statsDict[stat]

collapseByRun(statsDict)