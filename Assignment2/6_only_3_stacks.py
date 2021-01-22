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
        """
        Best First Search:
        sort the children according to the selected heuristic and perform BFS
        """
        goal = deepcopy(goal_design)
        start = deepcopy(start_design)

        queue = []
        visited = []

        queue.append(start)

        while len(queue):
            current = queue.pop()
            visited.append(unique_identifier(current.design))
            print("current: ", current.design)

            if goalTest(current.design, goal.design) == True:
                #traching back to reach initial state
                while current != None:
                    print(current.design)
                    current = current.parent
                return

            #generate all possible children for current node
            children = movGen(current)
            #sort according to selected heuristic
            # l = len(children)
            # for child in children:
            #     print("child:",child.design,end=" ")
            children = sort_(children, goal)
            # m = len(children)

            # print()
            # for child in children:
            #     print("child:",child.design,end=" ")
            #
            # if l != m:
            #     print("booooooooooo")

            for child in children:
                id = unique_identifier(child.design)
                if not (id in visited):
                    child.parent = current
                    queue.append(child)

    def hill_climbing(self, goal_design, start_design):
        """
        Hill Climbing approach :
        Always chose the best and discard the rest.
        If goal state found return
        else stuck at local maxima

        change heuristic function to try different
        """

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

            #generate all possible children for current node
            children = movGen(current)
            #sort according to selected heuristic
            # children = sort_(children, goal)

            find = maximum_(children,goal)
            print(find.design)
            # for child in children:
            #     print(child.design)
            # if none of the children has less cost then current state stuck at local maxima
            if heuristic(2, current, goal) <= heuristic(2, find, goal):
                print("Stuck at local maxima")
                children = []
                return
            # else chose the best child and discard the rest
            else:
                children = [children[0]]

            for child in children:
                id = unique_identifier(child.design)

                if goalTest(child.design, goal.design) == True:
                    #traching back to reach initial state
                    while child != None:
                        print(child.design)
                        child = child.parent
                    return

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

def maximum_(children,goal):
    deep_cp = deepcopy(children)
    min_ = 1000
    obj = None

    for d_child in deep_cp:
        cost = heuristic(2,d_child,goal)
        if cost < min_:
            min_ = heuristic(2,d_child,goal)
            obj = d_child
    return obj


def sort_(children,goal):
    """
    sort the children according to selected heuristic
    """
    sorted_children = []

    deep_copy = deepcopy(children)

    for child in children:
        obj = None
        cost = 10000 #make it INT_MAX
        for child in deep_copy:
            if(heuristic(2,child,goal) < cost):
                cost = heuristic(2,child,goal)
                obj = child
        sorted_children.append(obj)
        deep_copy.remove(obj)

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
            elem_no = 0
            for element in stack:
                if elem_no < len(stacks[stack_no]):
                    if not (stacks[stack_no][elem_no] == element):
                        cost += 1
                else :
                    cost += 1
                elem_no += 1
                # print("cost",cost)
            if elem_no < len(stacks[stack_no]) :
                cost += len(stacks[stack_no]) - elem_no
            stack_no += 1
        cost = cost // 2

    return cost

yo = candidate_design([[4], [],[3,6,1,2,5]], None, 0, 0)
yoyo = candidate_design([[5,2,4], [3], [1,6]], None, 0, 0)
# print(heuristic(2,yo,yoyo))
eyo = deepcopy(yo)
eyoyo = deepcopy(yoyo)
# # print(heuristic(2,yo,yoyo))
#
# yo.Best_first_search(yoyo, yo)
#
print("hill climbing")
yo.hill_climbing(eyoyo, eyo)
