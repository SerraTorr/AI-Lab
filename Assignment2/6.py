from copy import deepcopy
import json
import sys
import os

class Design:
    def __init__(self, design, parent = None, move = [], distance = 0):
        # design : structure of the block state
        self.design = design
        self.ui = unique_identifier(design)
        # to iterate back
        self.parent = parent
        self.distance = distance
        self.move = move

    def movGen(self):

        des = self.design
        result = []

        # all candidate moves
        candidate_moves = []
        for d in des:
            if des[d][1] == 'c':
                candidate_moves.append(d)
                """
                moving block:
                all open top blocks are movable
                all open top blocks are available for any other movable block

                additionally all empty table places are open for moving blocks
                """
        for block in candidate_moves:

            for target_block in candidate_moves:
                if block != target_block:
                    temp = deepcopy(des)
                    open_top = temp[block][0]
                    temp[block][0] = target_block
                    temp[target_block][1] = 'u'
                    move = []
                    distance = 0
                    move.append(block)
                    if open_top != '-':
                        temp[open_top][1] = 'c'

                        move.append(open_top)
                    else:
                        move.append('table')

                    move.append(target_block)
                    distance = self.distance + 1

                    result.append(Design(design = temp, parent = self, move = move, distance = distance))

            """
            restriction of three stacks
            """
            count_on_table = 0
            for block_ in des:
                if des[block][0] == '-':
                    count_on_table += 1

            if count_on_table > 2:
                continue

            if des[block][0] != '-':
                temp = deepcopy(des)
                move = []
                distance = 0

                open_top = temp[block][0]

                temp[block][0] = '-'
                temp[open_top][1] = 'c'

                move.append(block)
                move.append(open_top)
                move.append('table')

                distance = self.distance + 1
                result.append(Design(design = temp, parent = self, move = move, distance = distance))

        return result
    def conversion(self):
        design = deepcopy(self.design)
        list = []

        for elem in design:
            if design[elem][0] == '-':
                temp = []
                temp.append(elem)
                list.append(temp)

        for i in list:
            index = 0
            current = i[index]
            while design[current][1] != 'c':
                for elem in design:
                    if design[elem][0] == current:
                        i.append(elem)
                index += 1
                current = i[index]

        while len(list) < 3:
            temp = []
            list.append(temp)

        for i in list:
            print(i)
        print()

        return list


def unique_identifier(design):
    """
    input: state representation
    output: unique identifier string for state
    """

    design_ = list(design.values())
    string = ""
    for stack in design_:
        for element in stack:
            string = ''.join([string,str(element)])
    return string

def wrongly_placed(children, goal_, blocks_keys):

    values = []

    for child in children:
        cost = 0
        for key in blocks_keys:
            if child.design[key] != goal_[key]:
                cost += 1
        values.append(cost)
    result = values.index(min(values))
    return result

def two_heuristic(children, goal_, blocks_keys):

    values = []
    for child in children:
        cost = 0
        for key in blocks_keys:
            #for down
            if child.design[key][0] != goal_[key][0]:
                cost += 1
            # for up
            if child.design[key][1] != goal_[key][1]:
                cost += 1
        values.append(cost)
    result = values.index(min(values))
    return result

def goalTest(design, goal_design):
    """
    GoalTest Function
    """
    return design == goal_design

def read_in(filename):

    with open(filename) as f:
        dictionary_state = {}
        dictionary_goal = {}

        dictionary = dictionary_state

        for line in f:
            if "Initial" in line:
                # print(line)
                yo = 0
            elif "Goal" in line:
                dictionary = dictionary_goal
            elif "\n" == line:
                # print(line)
                t = 0
            else:
                line = json.loads(line)

                last_ele = 0
                for element in line:
                    if last_ele == 0:
                        dictionary[str(element)] = ['-', 'c']
                        last_ele = str(element)
                    else:
                        dictionary[str(element)] = [last_ele, 'c']
                        dictionary[last_ele][1] = 'u'
                        last_ele = str(element)

    return Design(design = dictionary_state), Design(design = dictionary_goal)

def pretty_print(solution, filename):
    # for the walk from init to final (goal)
    current_state = solution
    #for state one : the original goal
    current_state.conversion()
    print()

    result = []

    while True:
        # iterate back till the initial state
        result.append(current_state)
        current_state.conversion()
        current_state = current_state.parent

        if current_state.parent == None:
            result.append(current_state)
            break
    return len(result[1:])

def heuristic_search(current_state, goal_, method):
    """
    change heuristic from here.
    """
    # heuristic_function = wrongly_placed
    heuristic_function = two_heuristic
    # ***********************************************************************

    queue = []
    visited = []

    queue.append(current_state)
    blocks_keys = list(current_state.design.keys())
    visited.append(current_state.ui)

    while len(queue):
        print("states Explored : ", len(visited))
        i = heuristic_function(queue, goal_.design, blocks_keys)
        current = queue.pop(i)

        print(current.conversion())

        if goalTest(current.conversion(), goal_.conversion())==True:
            return current

        #generate all possible children for current node
        children = current.movGen()

        flag = 0 #HHIILL

        # i = heuristic_function(children, goal_.design, blocks_keys)
        # child = children.pop(i)
        # child.parent = current
        # if goalTest(child, goal_)==True:
        #     return child
        # queue.append(child)
        # visited.append(child.ui)

        for child in children:
            if goalTest(child, goal_)==True:
                return child

            if not (child.ui in visited):
                child.parent = current
                queue.append(child)
                visited.append(child.ui)
            #     flag = 1
            # if flag == 1:
            #     break

def main():

    if len(sys.argv) == 4:
        method = sys.argv[1] #hill or best
        in_ = sys.argv[2]
        out = sys.argv[3]

        start_, goal_ = read_in(filename = in_)
        solution = heuristic_search(current_state = start_, goal_ = goal_,method=method)
        print(solution)
        if solution == goal_:
            number_of_moves = pretty_print(solution = solution, filename = out)
            print('total steps:', number_of_moves)
    else:
        print('format is \n python3 filename best/hill inputfile outputfile')

if __name__ == '__main__':
	main()
