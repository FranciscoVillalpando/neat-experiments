
import sys
import xlwt
from parse import *
from parse import compile
from collections import defaultdict


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

def getStatsDict(fileNameList, runsFirst = True, parse_map = parseMap):
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

    # Dictionary organized in the following format : 
    #   [stat][run][gen]
    # where gen is an array
    # Example: statsDict['avg_fitness']['run2'][3]
    statsDict = defaultdict(lambda: defaultdict(list))

    for statFileName in fileNameList:

        with open(statFileName, 'r') as statFile:
            for line in statFile:
                for keyString in parse_map:
                    if parse_map[keyString]['searchString'] in line:   
                        parser = parse_map[keyString]['parser']
                        parsedData = parser.parse(line)

                        # Use failback parser if something goes wrong
                        if parsedData == None:
                            parser = parse_map[keyString]['alt_parser']
                            parsedData = parser.parse(line)
                    
                        clean_name = statFileName.split("/")[-1]

                        #print(clean_name)
                        for statName, statValue in parsedData.named.items():
                            # Add result to dictionary
                            if runsFirst:
                                statsDict[clean_name][statName].append(statValue)
                            else:
                                statsDict[statName][clean_name].append(statValue)
    return statsDict

def collapseByRun(fileNameList):
    ''' Returns a map collapsedStats[stat][aggregation][gen]
        where aggregation may be:
            mean

        TODO: Finish this function
    '''

    statsDict = getStatsDict(fileNameList,False)
    collapsedStats = defaultdict(lambda: defaultdict(list))
    statList = []
    runList = []

    for stat in statsDict:
        statList.append(stat)

    for run in statsDict[statList[0]]:
        runList.append(run)

    #print(statList, runList)

    #collapsedStats[stat] = statsDict[stat]

def generateXLS(filename,fileNameList):

    statsDict = getStatsDict(fileNameList, True)

    #the code for creating the workbook and worksheets
    wb= xlwt.Workbook()
    worksheets = []

    for run in statsDict:
        # Create worksheet for each run
        ws = wb.add_sheet(run[0:31])
        ws.write(0, 0, "Generation")

        for columnIndex, statName in enumerate(statsDict[run]):
            # Save column names to worksheet
            ws.write(0, columnIndex + 1, statName)
            for rowIndex, populationVal in enumerate(statsDict[run][statName]):
                # Save column names to worksheet
                print(rowIndex)
                #ws.write(rowIndex + 1, 0, rowIndex)
                ws.write(rowIndex + 1, columnIndex + 1, populationVal)

    wb.save(filename)
    print("saved xls")

def generateScoreTable(filename, fileNameList):
    ''' Creates a table of state score vs run in a XLS:
                r1  r2  r3
        State1   X   X   X
        State2   X   X   X

        This Score Table takes uses best_genome_fitness (i.e. the best genome of the gen)
        as the score for each  
    '''
    statsDict = getStatsDict(fileNameList, False)
     
    #the code for creating the workbook and worksheets
    wb= xlwt.Workbook()
    ws = wb.add_sheet("Scores")

    stateDict = defaultdict(lambda: defaultdict(float))
    parser = compile("{}.txt")
    # Generate state dict:
    #   dict ["state"][randRun]
    # note that since we dont care the order of the runs it is random in the list
    # i.e. dict["state"][0] may not correspond to the first run
    # ex:
    #   dict["SpringYardZone.Act1.state"][0-4] = someScore
    for logName in statsDict['best_genome_fitness']:

        state = logName.split("_")[0]
        run = parser.parse(logName.split("_")[-1])[0]
        print(state,run)
        stateDict[state][run]  =  max(statsDict['best_genome_fitness'][logName])
        

    print(stateDict)
    # Write XLS based on the contents of the stateDict
    ws.write(0, 0, "State/Run")
    # Get run names
    run_list = []
    for idx, run_id in enumerate((list(stateDict.values())[0])):
        run_list.append(run_id)
        ws.write(0, idx+1, run_id)   

    row = 1
    for state in stateDict :
        ws.write(row, 0, state)
        for col, run_id in enumerate(run_list):
            ws.write(row, col+1, stateDict[state][run_id])

        row += 1

    wb.save(filename)
    print("saved xls")


def generateBenchmarkScoreTable(filename, fileNameList):
    ''' Creates a table of state score vs run in a XLS:
                r1  r2  r3
        State1   X   X   X
        State2   X   X   X

        This Score Table takes uses best_genome_fitness (i.e. the best genome of the gen)
        as the score for each gen and creates an average of all gens
    '''
    statsDict = getStatsDict(fileNameList, False)
     
    #the code for creating the workbook and worksheets
    wb= xlwt.Workbook()
    ws = wb.add_sheet("Scores")

    stateDict = defaultdict(lambda: defaultdict(float))
    # Generate state dict:
    #   dict ["state"][randRun]
    # note that since we dont care the order of the runs it is random in the list
    # i.e. dict["state"][0] may not correspond to the first run
    # ex:
    #   dict["SpringYardZone.Act1.state"][0-4] = someScore
    for logName in statsDict['best_genome_fitness']:
        state = logName.split("_")[0]
        print(state)
        run = parse("{}.{}",logName.split("_")[-1])[0]
        print(state,run)

        data = statsDict['best_genome_fitness'][logName]

        stateDict[state][run] = sum(data)/len(data)
        

    print(stateDict)
    # Write XLS based on the contents of the stateDict
    ws.write(0, 0, "State/Run")
    # Get run names
    run_list = []
    for idx, run_id in enumerate((list(stateDict.values())[0])):
        run_list.append(run_id)
        ws.write(0, idx+1, run_id)   

    row = 1
    for state in stateDict :
        ws.write(row, 0, state)
        for col, run_id in enumerate(run_list):
            ws.write(row, col+1, stateDict[state][run_id])

        row += 1

    wb.save(filename)
    print("saved xls")

def generateBruteScoreTable(filename, fileNameList):
    ''' Creates a table of state score vs run in a XLS:
                r1  r2  r3
        State1   X   X   X
        State2   X   X   X

        This function works by reading fitness_achieved messages instead of end of gen messages
    '''

    # Use reduced map for faster parsing
    trimmed_map = {
        "fitness_achieved": {
            'searchString':'achieved fitness',
            "parser": compile("achieved fitness: {fitness:f} at timestep {timestep:d} time: {}")
        }
    }

    statsDict = getStatsDict(fileNameList, False, trimmed_map)
     
    #the code for creating the workbook and worksheets
    wb= xlwt.Workbook()
    ws = wb.add_sheet("Scores")

    stateDict = defaultdict(lambda: defaultdict(float))
    parser = compile("{}.txt")
    # Generate state dict:
    #   dict ["state"][randRun]
    # note that since we dont care the order of the runs it is random in the list
    # i.e. dict["state"][0] does not correspond to the first run
    # ex:
    #   dict["SpringYardZone.Act1.state"][0-4] = someScore
    print(statsDict)
    for logName in statsDict['fitness']:

        state = logName.split("_")[0]
        run = parser.parse(logName.split("_")[-1])[0]
        print(state,run)
        stateDict[state][run]  =  max(statsDict['fitness'][logName])

    print(stateDict)
    # Write XLS based on the contents of the stateDict
    ws.write(0, 0, "State/Run")
    # Get run names
    run_list = []
    for idx, run_id in enumerate((list(stateDict.values())[0])):
        run_list.append(run_id)
        ws.write(0, idx+1, run_id)   

    row = 1
    for state in stateDict :
        ws.write(row, 0, state)
        for col, run_id in enumerate(run_list):
            ws.write(row, col+1, stateDict[state][run_id])

        row += 1

    wb.save(filename)
    print("saved xls")

def generateAccumulatedScoreByTimestep(fileNameList):
    '''
    Generate learning curve (of best achieved fitnesses) vs timesteps 
    gets a list containing (timestep,score) tuples

    Usage: share the files *for a single run/seed* 
    '''

    # Use reduced map for faster parsing
    trimmed_map = {
        "achieved_fitness": {
            'searchString':'achieved fitness:',
            "parser": compile("achieved fitness: {fitness:f} at timestep {timestep:d} time: {}")
        }  
    }
    stats_dict = getStatsDict(fileNameList, runsFirst = True, parse_map=trimmed_map)
    #print(stats_dict)

    # Array of one million elements (one per timestep) representing fitnes vs timestep
    per_level_curves = {}

    # now we have a [level_run]: fitness: [a,b], timestep:[x,y]
    for level in stats_dict:
        # init level curve for this level
        print(f"level:{level}")
        per_level_curves[level] = [0]* int(1e6)
        #ws.write(0, idx+1, level)
        for idx, fitness in enumerate(stats_dict[level]["fitness"]):
            timestep = stats_dict[level]['timestep'][idx]
            
            print(f"fitness {fitness} timestep:{timestep}")
            per_level_curves[level][timestep] = fitness

    #now we have a pseudo training curve for each level with the correct fitness in specific timesteps
    # but 0 on all other timesteps without data, we need to normalize this by filling in all the data
    # with the last fitness recorded
    for level_name in per_level_curves:
        print(level_name)
        level_curve = per_level_curves[level_name]
        for idx, timestep in enumerate(level_curve):
            if timestep == 0 and idx > 0:
                level_curve[idx] = level_curve[idx-1]

    # Create average of all level curves to have a single one
    average_across_levels = [0] * int(1e6)
    number_of_levels = len(per_level_curves)
    print(number_of_levels)
    for level_name in per_level_curves:
        print(level_name)
        level_curve = per_level_curves[level_name]
        average_across_levels = [x + y for x, y in zip(average_across_levels, level_curve)]

    average_across_levels = list(map((lambda x: x/number_of_levels), average_across_levels))

    # now we have the real learning curve for all 1M timesteps, however this may be hard to plot, should compress

    return average_across_levels

    #the code for creating the workbook and worksheets
    # wb= xlwt.Workbook()
    # ws = wb.add_sheet("learning curve")
    # for idx, fitness in enumerate(average_across_levels):
    #     ws.write(idx, 0, fitness)
    # wb.save(filename)

def printLearningCurveForRuns(fileNameList):
    import matplotlib.pyplot as plt
    runDict = getFileNamesByRun(fileNameList)
    average_of_runs = [0] * int(1e6)
    number_of_runs = len(runDict)

    for run in runDict:
        curve_for_run = generateAccumulatedScoreByTimestep(runDict[run])
        average_of_runs  = [x + y for x, y in zip(average_of_runs, curve_for_run)]
        plt.plot(curve_for_run)

    average_of_runs = list(map((lambda x: x/number_of_runs), average_of_runs))
    plt.ylabel('Average score')
    plt.xlabel('Timestep')
    plt.show()

    plt.figure(2)
    plt.plot(average_of_runs)
    plt.show()

def getFileNamesByRun(fileNameList):

    runDict = {}
    for fileName in fileNameList:
        run = parse("{}.{}",fileName.split("_")[-1])[0]
        print(run)

        if run not in runDict.keys():
            runDict[run] = []

        runDict[run].append(fileName)

    #print(runDict)
    return runDict


if __name__ == "__main__":

    fileNameList = []
    output_file_name = "test.xls"
    # We are able to specify both a set of files or a glob
    if len(sys.argv) > 3:
        output_file_name = sys.argv[1]
        fileNameList = sys.argv[2:]
    else:
        print("Need files to process")
        exit(1)

    print(f"Creating xls with name {output_file_name} using files: {fileNameList}")

    #generateScoreTable(output_file_name, fileNameList)
    #generateBruteScoreTable(output_file_name, fileNameList)
    generateBenchmarkScoreTable(output_file_name, fileNameList)
    #generateLearnCurveTimestep(output_file_name, fileNameList)
    #printLearningCurveForRuns(fileNameList)