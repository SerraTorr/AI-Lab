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
                for j in temp_tt:
                    j = j - 1

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
    testcase = "(~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)"
    testcase = testcase.replace("(", "")
    testcase = testcase.replace(")", "")
    clauses = testcase.split("^")
    literals = []
    for i in clauses:
        literals.append([i.split("v")])

    print(literals)

def f1(node_):
    literals = node_.get_literals()

    a = literals[0]
    b = literals[1]
    c = literals[2]
    d = literals[3]
    # (~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)
    return int(((not d) or (a) or (c)))

def f2(node_):
    literals = node_.get_literals()
    a = literals[0]
    b = literals[1]
    c = literals[2]
    d = literals[3]
    # (~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)
    return int(((not d) or (b) or (not c)))

def f3(node_):
    literals = node_.get_literals()
    a = literals[0]
    b = literals[1]
    c = literals[2]
    d = literals[3]
    # (~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)
    return int(((a) or (c) or (d)))

def f4(node_):
    literals = node_.get_literals()
    a = literals[0]
    b = literals[1]
    c = literals[2]
    d = literals[3]
    # (~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)
    return int(((not c) or (not b) or (a)))

def f5(node_):
    literals = node_.get_literals()
    a = literals[0]
    b = literals[1]
    c = literals[2]
    d = literals[3]
    # (~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)
    return int(((not c) or (not a) or (not d)))

def calc(node_):
    return f1(node_) and f2(node_) and f3(node_) and f4(node_) and f5(node_)

def heuristic_function(node_):
    return f1(node_) + f2(node_) + f3(node_) + f4(node_) + f5(node_)

def tabu(tt):
    node_ = Node([0,0,0,0],[0,0,0,0])
    stopping_criteria = 100

    while calc(node_) != 1:
        neighbours = node_.movGen(tt)
        for i in neighbours:
            if heuristic_function(i) > heuristic_function(node_):
                node_ = i

    node_.pretty_print()
    return node_

# x = Node([0,0,0,0],[0,0,0,0])
# neighbours = x.movGen(4)
#
# for i in neighbours:
#     i.pretty_print()
#
# result = tabu(4)
# print("SAT solution is : ")
# result.pretty_print()
generate_CNF("(~dvavc)^(~dv~bv~c)^(avcvd)^(~cv~av~d)^(~cv~bva)")
