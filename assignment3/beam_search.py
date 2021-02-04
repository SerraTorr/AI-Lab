import copy

class Node:
    def __init__(self, literals):
        self.literals = literals

    def movGen(self):
        neighbours = []

        for i in range(len(self.literals)):
            temp = copy.deepcopy(self.literals)
            temp[i] = int(not temp[i])
            neighbours.append(Node(temp))

        return neighbours

    def pretty_print(self):
        print(self.literals)

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

def find_best(bw,neighbours,testcase):
    if len(neighbours) == 0:
        return

    bw_list = []
    for i in range(bw):
        if len(neighbours)==0 :
            return bw_list
        node_ = neighbours[0]
        max_ = calc(node_,testcase)
        for j in neighbours:
            if calc(j,testcase) > max_ :
                max_ = calc(j,testcase)
                node_ = j
        bw_list.append(node_)
        neighbours.remove(node_)

    return bw_list

def beam_search(bw,testcase):
    node_ = Node([0,0,0,0])
    queue = [node_]

    while len(queue)>0 and calc(node_,testcase):

        if goalTest(node_,testcase):
            return node_,1

        neighbours = []
        for i in queue:
            neighbours_i = i.movGen()
            for j in neighbours_i:
                neighbours.append(j)


        best_b = find_best(bw,neighbours,testcase)
        queue = []
        for i in best_b:
            queue.append(i)

        node_ = best_b[0]

    return node_, goalTest(node_,testcase)


# x = Node([1,1,1,1])
# neighbours = x.movGen()
# for i in neighbours:
#     i.pretty_print()

beam_search(2,"(~av~bv~cv~d)^(bv~avcvd)^(cv~av~bvd)^(avbvcvd)^(avbvcv~d)")[0].pretty_print()
