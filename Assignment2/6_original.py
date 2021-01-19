from copy import deepcopy

class candidate_design:
    def __init__(self, design, parent, from_, to_):
        """
        design :
        3 stacks of integers containing blocks (could be empty) from bottom to top : list of stacks
        parent :
        parent design of current design
        from :
        integer indicating stack from which to remove block
        to :
        integer indicating stack into which removed block is to be placed
        """

        self.design = design
        self.parent = parent
        self.from_ = from_
        self.to_ = to_


def goalTest(design_one, design_two):
    if(design_one != None and design_two != None):
        return design_one == design_two
    return False

def movGen(design):

    children = []

    des = deepcopy(design)
    candidate_moves = [[0,1], [1,0], [0,2], [2,0], [1,2], [2,1]]

    for move in candidate_moves:
        temp = deepcopy(des.design)
        if temp[move[0]]:
            block = temp[move[0]].pop()
            temp[move[1]].append(block)
            result = candidate_design(temp, design, move[0], move[1])
            children.append(deepcopy(result))

    return children

#
# yo = candidate_design([[1], [2], [3]], None, 0, 0)
# children = movGen(yo)
# for child in children:
#     print(child.design)