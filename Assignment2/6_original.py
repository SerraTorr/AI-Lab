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
            children = sort_(children, goal)
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

def sort_(children,goal):
    """
    sort the children according to selected heuristic
    """
    sorted_children = []
    for child in children:
        obj = None
        cost = 10000 #make it INT_MAX
        for child in children:
            if(heuristic(2,child,goal) < cost):
                cost = heuristic(2,child,goal)
                obj = child
        sorted_children.append(obj)
        children.remove(obj)

    return sorted_children

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
    Input: design and goalDesign are candidate_state class
    heuristic_number 1 : underestimating
    heuristic_number 2 : Just Perfect
    heuristic_number 3 : Overestimating (manhattan distance)
    """

    temp = deepcopy(design)
    goal = deepcopy(goalDesign)
    cost = 0

    if heuristic_number == 1:
        stacks = deepcopy(temp.design)
        goal_stacks = deepcopy(goal.design)

        for stack,goal_stack in zip(stacks,goal_stacks):
            cost += abs(len(stack) - len(goal_stack))
    elif heuristic_number == 2:
        """
        check for all blocks in goal state--> if corresponding test state doesn't contain same block then add one to the cost
        """
        stacks = deepcopy(temp.design)
        goal_stacks = deepcopy(goal.design)

        stack_no = 0
        elem_no = 0
        for stack in goal_stacks:
            for element in stack:
                if elem_no < len(stacks[stack_no]):
                    if not (stacks[stack_no][elem_no] == element):
                        cost += 1
                else :
                    cost += 1
                elem_no += 1
            stack_no += 1
        cost = cost // 2

    return cost


yo = candidate_design([[3], [2], [1]], None, 0, 0)
yoyo = candidate_design([[1,2,3], [], []], None, 0, 0)
print(heuristic(2,yo,yoyo))

yo.Best_first_search(yoyo, yo)

# state = yoyo
# while state != None:
#     print(state.design)
#     state = state.parent
# print(heuristic(1,yo,yoyo))

# children = movGen(yo)
# for child in children:
#     print(child.design)
