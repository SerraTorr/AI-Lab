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

    def Best_first_search(self, goal_design, start_design):

        goal = deepcopy(goal_design)
        start = deepcopy(start_design)
        queue = []
        visited = []
        queue.append(start)

        while len(queue):
            current = queue.pop()
            visited.append(unique_identifier(current.design))

            if goalTest(current.design, goal.design) == True:
                #traching back to reach initial state
                while current != None:
                    print(current.design)
                    current = current.parent
                return

            children = movGen(current)
            sort_(children)
            for child in children:
                id = unique_identifier(child.design)
                if not (id in visited):
                    child.parent = current
                    queue.append(child)

def unique_identifier(design):
    """
    input: state representation
    output: unique identifier string for state
    """

    string = ""
    for stack in design:
        for element in stack:
            string = ''.join([string,str(element)])
        string = ''.join([string,"|"])
    return string

def sort_(children):
    """
    sort the children according to selected heuristic
    """

    return children

def goalTest(design_one, GoalDesign):
    """
    Function to test if the current state is goal state
    return True if it is False otherwise
    """

    if(design_one != None and GoalDesign != None):
        if(unique_identifier(design_one) == unique_identifier(GoalDesign)):
            return True
        if(design_one == GoalDesign) :
            return True
    return False

def movGen(design):
    """
    constraints: maximum allowed states = 3
    Input: takes state representation as input
    Output: returns list of all neighbouts (possible transitions) from current state
    """

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

def heuristic(heuristic_number, design, goalDesign):
    """
    heuristic_number 1 : underestimating
    heuristic_number 2 : overestimating
    """
    
    temp = deepcopy(design)
    goal = deepcopy(goalDesign)
    cost = 0

    if heuristic_number == 1:
        stacks = deepcopy(temp.design)
        goal_stacks = deepcopy(goal.design)

        for stack,goal_stack in zip(stacks,goal_stacks):
            cost += abs(len(stack) - len(goal_stack))
            print("cost : ",cost)
    return cost
#
# yo = candidate_design([[1], [2], [3]], None, 0, 0)
# yoyo = candidate_design([[3,2], [], [1]], None, 0, 0)
# yo.Best_first_search(yoyo, yo)

# state = yoyo
# while state != None:
#     print(state.design)
#     state = state.parent
# print(heuristic(1,yo,yoyo))

# children = movGen(yo)
# for child in children:
#     print(child.design)
