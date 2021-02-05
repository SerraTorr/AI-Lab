# Generating Inputs
- There are 3 files to generate testcases.
1. testcase_generator.py
2. testcase_generator_4cnf.py
3. 8_variables_testcases_generator.py

#### NOTE: You need to give input to test generator files how many testcases to generate. (generated testcases could be directed to files using ">")

- Run testcase_generator.py to generate testcases with 5 clauses each with three literals randomly drawn from 8 candidates ("a", "~a", "b", "~b", "c", "~c", "d", "~d")
e.g (~bv~av~d)^(cvav~d)^(~bvdv~a)^(~dvbva)^(~av~cv~d) here v is disjunction and ^ is conjunction.

- Run testcase_generator_4cnf.py to generate testcases with 5 clauses each containing 4 literals randomly drawn from 8 candidates ("a", "~a", "b", "~b", "c", "~c", "d", "~d")
e.g (~avbvcv~d)^(~av~bvcvd)^(avbvcvd)^(~avbvcvd)^(~av~bvcv~d)

- Run 8_variables_testcase_generator.py to generate testcases with 5 clauses each containing 4 literals randomly drawn from 14 CANDIDATES ("a", "~a", "b", "~b", "c", "~c", "d", "~d", "e", "~e", "f", "~f", "g", "~g")
e.g (~ev~fv~ev~e)^(~evbv~av~c)^(~dv~gvdvb)^(gvfv~cva)^(av~dvbv~g)

- In file 8_variables_testcases_generator, uncomment line 4 and 24 and comment lines 3 and 23 to generate testcases with 5 clauses each containing 4 literals randomly drawn from ("a", "b", "c", "d", "e", "f", "g")
e.g (cvavbvg)^(dvgvdva)^(evdvbvc)^(avfvdvc)^(evcvdvf)

### Sample outputs generated are stored in files
- testcases.txt
- testcase_4cnf.txt
- 8_variables_testcases.txt
for three testfiles mentioned above.  

# Algorithms Implementation
1. tabu.py (Tabu Search Algorithm)
2. vnd.py (Variable Neighbourhood Descent Algorithm)
3. beam_search.py (Beam search Algorithm)

Run algorithm files using commands below.
- `$python tabu.py`
- `$python vnd.py`
- `$python beam_search.py`

- LINE 139 IN tabu.py TAKES TEST FILE NAME AS ARGUMENT AND GENERATES PRINTS GOAL NODE AND TABU TENURE LIST IN THE FORMATE [-,-,-,-] [-,-,-,-] IS EXPRESSION CONTAINS FOUR VARIABLES.
- Change the filename accordingly to run the algorithm on different testfiles.
##### NOTE: Change the line 79 if test file contains less or more variables than 4

- Line 177 in vnd.py calls the function vnd which executes algorithm on the input string given as argument to it and returns the result (Goal) node.

- Line 123 in beam_search.py calls the function beam_search which executes algorithm on the input string with given beam width as argument to it and returns the result (Goal) node.
