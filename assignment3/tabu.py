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

x = Node([0],[0])
neighbours = x.movGen(4)

for i in neighbours:
    i.pretty_print()
