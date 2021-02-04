import copy

class Node:
    def __init__(self, literals, tabu_tenures):
        self.literal_list = literals
        self.tabu_tenure_list = tabu_tenures

    def movGen(self, tt):
        neighbours = []
        for index, val in enumerate(self.literal_list):
            if self.tabu_tenure_list[index] == 0:
                temp_literals = copy.deepcopy(self.literal_list)
                temp_literals[index] = int(not temp_literals[index])
                temp_tt = copy.deepcopy(self.tabu_tenure_list)
                for i, j in enumerate(temp_tt):
                    temp_tt[i] = max(temp_tt[i]-1, 0)

                temp_tt[index] = tt
                neighbours.append(Node(temp_literals, temp_tt))

        return neighbours

    def pretty_print(self):
        print(self.literal_list,self.tabu_tenure_list)

    def get_literals(self):
        return self.literal_list

    def get_tenures(self):
        return self.tabu_tenure_list

def generate_CNF(testcase):
    testcase = testcase
    testcase = testcase.replace("(", "")
    testcase = testcase.replace(")", "")
    clauses = testcase.split("^")
    literals = []
    for i in clauses:
        save = i.split("v")
        real_list = []

        for lit in save:
            if lit=="a":
                real_list.append(0)
            elif lit == "~a":
                real_list.append(1)
            elif lit == "b":
                real_list.append(2)
            elif lit == "~b":
                real_list.append(3)
            elif lit == "c":
                real_list.append(4)
            elif lit == "~c":
                real_list.append(5)
            elif lit == "d":
                real_list.append(6)
            elif lit == "~d":
                real_list.append(7)

        literals.append(real_list)

    return literals

def clause_values(node_,literals_values):
    literals = node_.get_literals()
    literals_values_bool = []
    for i in range(4):
        literals_values_bool.append(literals[i])
        literals_values_bool.append(int(not literals[i]))

    clause_value = literals_values_bool[literals_values[0]]
    for i in literals_values:
        clause_value = clause_value or literals_values_bool[i]

    return clause_value

def goalTest(node_,literals_values):
    return clause_values(node_,literals_values[0]) and clause_values(node_,literals_values[1]) and clause_values(node_,literals_values[2]) and clause_values(node_,literals_values[3]) and clause_values(node_,literals_values[4])

def heuristic_function(node_,literals_values):
    return clause_values(node_,literals_values[0]) + clause_values(node_,literals_values[1]) + clause_values(node_,literals_values[2]) + clause_values(node_,literals_values[3]) + clause_values(node_,literals_values[4])

def tabu(tt, testcase):
    literals_values = generate_CNF(testcase) #encode string 4-SAT for further processing
    node_ = Node([0,0,0,0],[0,0,0,0]) # starting node
    stopping_criteria = 0 #5 MAX NUMBER OF ITERATIONS ALLOWED TO AVOID INFINITE EXECUTION

    while goalTest(node_,literals_values) == 0:
        # print(stopping_criteria, goalTest(node_, literals_values), end=" ")
        # node_.pretty_print()

        stopping_criteria += 1
        if stopping_criteria > 50:
            break
        neighbours = node_.movGen(tt)

        if len(neighbours) == 0:
            return node_, 0, stopping_criteria
            break
        maximum = heuristic_function(neighbours[0],literals_values)
        node_ = neighbours[0]
        for i in neighbours:
            if heuristic_function(i,literals_values) > maximum:
                node_ = i
                maximum = heuristic_function(i,literals_values)

    return node_, 1, stopping_criteria

def process_file(filename):
    file = open(filename, 'r')

    candidate_tabu_tenures = [1,2,3,4,6,8] # candidate tabu tenures

    database_list = []
    for line in file:
        line = line.replace("\n","")
        list_for_string = []
        for tt in candidate_tabu_tenures:
            result,found,sc = tabu(tt,line)
            list_for_string.append(sc)
        database_list.append(list_for_string)

    for i in database_list:
        for j in i:
            print(j,end=" ")
        print()
# process_file("testcases.txt")



result,found,sc = tabu(3,"(~av~bv~cv~d)^(bvav~bvd)^(cv~avbvd)^(avbvcvd)^(avbvcv~d)")
print(sc)
print("SAT solution is : ")
if found :
    result.pretty_print()
else :
    print("Not Found : Try changing Tabu Tenure value.")
