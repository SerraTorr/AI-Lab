from queue import Queue;
import sys;

class Node:
    def __init__(self, row, col, data):
        self.loc = []
        self.loc.append(row)
        self.loc.append(col)
        self.data = data
        self.visited = False
        self.found = False
        self.depth = 10**9 + 7
        self.parent = None

def moveGen(curr, neighbors, graph):
    # Left Right Up Down
    maybe_nbrs = []

    maybe_nbrs.append([curr[0], curr[1]-1])
    maybe_nbrs.append([curr[0], curr[1]+1])
    maybe_nbrs.append([curr[0]-1, curr[1]])
    maybe_nbrs.append([curr[0]+1, curr[1]])

    #check for empty and undiscovered neighbours and update
    for i in range(4):
        if maybe_nbrs[i][0] >= 0 and maybe_nbrs[i][1] >= 0:
            #check if visited/found already
            # print("maybe printing : ", maybe_nbrs[i][0], maybe_nbrs[i][1])
            if (graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].visited == True or graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].found == True) and graph[curr[0]][curr[1]].depth + 1 >= graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].depth:
                continue
            # print("moving")
            #move only if free or goal
            curr_char = graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].data
            if curr_char == ' ' or curr_char == '*':
                neighbors[i] = maybe_nbrs[i]

def goaltest(curr, dest):
    return curr == dest;

class Maze:
    def __init__(self, filename):
        self.graph = []
        self.curr = []
        self.dest = []
        self.row = 0
        first = True

        file = open(filename, 'r')

        for line in file:
            if first:
                self.mode = line[0];
                first = False
                continue;

            self.cols = len(line)

            nodes = []
            for col in range(self.cols):
                nodes.append(Node(self.row, col, line[col]));
            self.graph.append(nodes);

            found = line.find('*')

            if found != -1 :
                self.dest = [self.row, found];

            self.row += 1;
        self.curr = [0,0]
        self.graph[0][0].data = '0';

    def search(self):
        if self.mode == '0':
            self.BFS()
        elif self.mode == '1':
            self.DFS()
        elif self.mode == '2':
            self.DFID()
        else :
            print("Enter a valid choice of algorithm\n");

    def getVisited(self):
        states = 0;
        # print(graph.visited);
        for i in range(self.row):
            for j in range(self.cols):
                if self.graph[i][j].visited == True:
                    states += 1;

        return states;

    def reset(self):
        self.curr = [0,0]
        for i in range(self.row):
            for j in range(self.cols):
                self.graph[i][j].depth = 10**9+7;
                self.graph[i][j].found = False;
                self.graph[i][j].parent = None;
                self.graph[i][j].visited = False;

        self.graph[0][0].depth = 0;
        self.graph[0][0].found = True;

    def BFS(self):
        q = Queue();
        q.put(self.curr);
        self.graph[self.curr[0]][self.curr[1]].visited = True;
        while not q.empty():
            # print("current",self.curr[0],self.curr[1])
            if goaltest(self.curr, self.dest):
                break
            else :
                self.curr = q.get();
                self.graph[self.curr[0]][self.curr[1]].visited = True;
                # self.graph[self.curr[0]][self.curr[1]].depth = self.graph[self.curr[0]][self.curr[1]].parent.depth + 1;

                nbrs = [];
                for i in range(4) :
                    nbrs.append([-1,-1]);

                moveGen(self.curr, nbrs, self.graph);

                for i in range(4):

                    if(nbrs[i][0] != -1 and nbrs[i][1] != -1):
                        q.put(nbrs[i])
                        self.graph[nbrs[i][0]][nbrs[i][1]].found = True;
                        self.graph[nbrs[i][0]][nbrs[i][1]].parent = self.graph[self.curr[0]][self.curr[1]]

        print(self.getVisited(), end=" ")

    def DFS(self):

        stack = [];
        stack.append(self.curr);
        self.graph[self.curr[0]][self.curr[1]].visited = True
        self.graph[self.curr[0]][self.curr[1]].depth = 0;


        while len(stack) > 0:
            if goaltest(self.curr, self.dest) :
                break;
            else :
                self.curr = stack.pop();
                self.graph[self.curr[0]][self.curr[1]].visited = True

                nbrs = []
                for i in range(4):
                    nbrs.append([-1,-1])

                moveGen(self.curr, nbrs, self.graph)
                for i in range(4):
                    if(nbrs[i][0] != -1 and nbrs[i][1] != -1):
                        stack.append(nbrs[i]);
                        self.graph[nbrs[i][0]][nbrs[i][1]].found = True
                        self.graph[nbrs[i][0]][nbrs[i][1]].depth = self.graph[self.curr[0]][self.curr[1]].depth+1;
                        self.graph[nbrs[i][0]][nbrs[i][1]].parent = self.graph[self.curr[0]][self.curr[1]]
        print(self.getVisited(), end=" ")

    def dfs_dfid(self, max_depth, node):
        self.curr = [node.loc[0], node.loc[1]]
        if goaltest(self.curr, self.dest):
            return self.getVisited();

        nbrs = [];
        for i in range(4):
            nbrs.append([-1,-1]);
        node.visited = True;
        self.states_dfid+=1;
        moveGen(self.curr, nbrs, self.graph)
        for i in range(4):
            if(nbrs[i][0] != -1 and nbrs[i][1] != -1) and node.depth+1 <= max_depth:
                self.graph[nbrs[i][0]][nbrs[i][1]].found = True
                self.graph[nbrs[i][0]][nbrs[i][1]].depth = node.depth+1;
                self.graph[nbrs[i][0]][nbrs[i][1]].parent = node
                self.dfs_dfid(max_depth, self.graph[nbrs[i][0]][nbrs[i][1]]);
                if goaltest(self.curr, self.dest):
                    return self.getVisited();

    def DFID(self):
        max_depth = 0;
        self.states_dfid = 0;
        while not goaltest(self.curr, self.dest):
            self.reset();
            temp = self.dfs_dfid(max_depth, self.graph[self.curr[0]][self.curr[1]]);
            # print()
            max_depth+=1;


        print(self.states_dfid, end=" ");

    def reverse(self):
        length = 1;
        tracker = self.graph[self.dest[0]][self.dest[1]];
        while tracker.parent != None:
            self.graph[tracker.loc[0]][tracker.loc[1]].data = '0'
            tracker = tracker.parent
            length += 1;

        print(length, end=" ");

    def display(self):
        for i in range(self.row):
            for j in range(self.cols):
                print(self.graph[i][j].data, end = '')
            print("\n", end = '')


def main():
    M = Maze(sys.argv[1]);

    # print(" ", end="")
    M.search();
    M.reverse();
    print()
    M.display();
    M.reset();

main();
