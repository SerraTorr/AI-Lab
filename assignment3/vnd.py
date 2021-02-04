import copy
import pdb;

# pdb.set_trace()

class Node:
    def __init__(self, literals):
        self.literals = literals

    def movGen_one(self):
        neighbours = []
        for index, i in enumerate(self.literals):
            temp = copy.deepcopy(self.literals)
            temp[index] = int(not temp[index])
            neighbours.append(Node(temp))

        return neighbours

    def movGen_two(self):
        neighbours = []
        index = [[0,1],[0,2], [0,3], [1,2], [1,3], [2,3]]

        for i in index:
            temp = copy.deepcopy(self.literals)
            for j in i:
                temp[j] = int(not temp[j])
            neighbours.append(Node(temp))

        return neighbours

    def movGen_three(self):
        neighbours = []
        index = [[0,1,2], [1,2,3], [2,3,0], [3,0,1]]

        for i in index:
            temp = copy.deepcopy(self.literals)
            for j in i:
                temp[j] = int(not temp[j])
            neighbours.append(Node(temp))

        return neighbours

    def movGen_four(self):
        neighbours = []
        index = [[0,1,2,3]]

        for i in index:
            temp = copy.deepcopy(self.literals)
            for j in i:
                temp[j] = int(not temp[j])
            neighbours.append(Node(temp))

        return neighbours

    def get_movGen(self, node_, mov):
        if mov == 1:
            return node_.movGen_one()
        elif mov == 2 :
            return node_.movGen_two()
        elif mov == 3:
            return node_.movGen_three()
        elif mov == 4:
            return node_.movGen_four()

    def pretty_print(self):
        print(self.literals)

def find_max(neighbours,testcase):
    node_ = copy.deepcopy(neighbours[0])
    max_ = calc(node_,testcase)
    for i in neighbours:
        if max_ < calc(i,testcase):
            node_ = i
            max_ = calc(i,testcase)

    return node_

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
    literals = node_.literals
    literals_values_bool = []
    for i in range(4):
        literals_values_bool.append(literals[i])
        literals_values_bool.append(int(not literals[i]))

    clause_value = literals_values_bool[literals_values[0]]
    for i in literals_values:
        clause_value = clause_value or literals_values_bool[i]

    return clause_value

def goalTest(node_,testcase):
    CNF = generate_CNF(testcase)
    return clause_values(node_,CNF[0]) and clause_values(node_,CNF[1]) and clause_values(node_,CNF[2]) and clause_values(node_,CNF[3]) and clause_values(node_,CNF[4])

def calc(node_,testcase):
    CNF = generate_CNF(testcase)
    return clause_values(node_,CNF[0]) + clause_values(node_,CNF[1]) + clause_values(node_,CNF[2]) + clause_values(node_,CNF[3]) + clause_values(node_,CNF[4])

def hill_climbing(node_, mov,testcase):

    iterations = 0
    while goalTest(node_,testcase) == 0:
        iterations += 1
        neighbours = node_.get_movGen(node_,mov)
        if calc(find_max(neighbours,testcase),testcase) > calc(node_,testcase):
            node_ = find_max(neighbours,testcase)
            node_.pretty_print()
        else :
            return node_

    print("Iteratiosn :", iterations)
    return node_

def VND(testcase):
    node_ = Node([0,0,0,0])
    print(goalTest(node_,testcase))

    if goalTest(node_,testcase):
        return node_,1
    node_ = hill_climbing(node_,1,testcase)

    if goalTest(node_,testcase):
        return node_,1
    node_ = hill_climbing(node_,2,testcase)

    if goalTest(node_,testcase):
        return node_,1
    node_ = hill_climbing(node_,3,testcase)

    if goalTest(node_,testcase):
        return node_,1
    node_ = hill_climbing(node,4,testcase)

    if goalTest(node_,testcase):
        return node_,1
    else :
        return node_,0
#
# x = Node([0,0,0,0])
#
# x = x.get_movGen(x,3)
# for i in x:
#     i.pretty_print()

VND("(av~bvcvd)^(bv~av~bvd)^(cv~av~bvd)^(avbvcvd)^(~avbvcvd)")[0].pretty_print()
