# Takes a list of files and appends a line containing:
# Best fitness: {} - size: {} - species 1 - id 0
# for use with benchmark score extractor

import sys
from parse import *
from parse import compile

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Must contain at least one file to patch as argument")
        exit(1)

    parser = compile("achieved fitness: {score:f} at timestep {timestep:d} time: {timestamp}")


    for file_name in sys.argv[1:]:
        print(f"Patching {file_name}")
        with open(file_name, 'r') as metrics_file:
        
            print(metrics_file.name)
            lines = metrics_file.readlines()
            found = False
            for line in reversed(lines):
                if "achieved fitness" in line:
                    parsedData = parser.parse(line)
                    score = parsedData.named["score"]
                    with open(file_name+".patched", "w") as patched_file:
                        patched_file.writelines(lines)
                        patched_file.write(f"Best fitness: {score} - size: {(0,0)} - species 1 - id {0}")

                    found = True
                    break
            if not found:
                with open(file_name+".patched", "w") as patched_file:
                        patched_file.writelines(lines)
                        patched_file.write(f"Best fitness: {0.0} - size: {(0,0)} - species 1 - id {0}")


            


