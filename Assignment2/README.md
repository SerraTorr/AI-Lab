The folder contains two files:
1. 6.py --> movGen function implemented specific for 3 stacks input problems
2. 6_only_3_stacks.py ---> movGen funciton implemented for any general blocks formation which could be restricted to max_number_of_stacks

### Directions to Run 6.py
$ python 6.py best <input_file_name> <output_file_name>  
Here, sample input file name is "in".  

When the final state is found, all the moves taken will be written to specified output file.

- line 220 and 221 declares heuristic functions used for while running, comment the required line to get the results for particular heuristics function.  

### Hill Climbing

- line 246 to 252 (currently commented) should be uncommented to get the results for hill climbing and commend the loop below it.
