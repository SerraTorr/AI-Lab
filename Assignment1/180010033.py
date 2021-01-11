from queue import Queue;
import sys;

class Node:
    loc = []
    def __init__(self, row, col, data):
        self.loc.append(row)
        self.loc.append(col)
        self.data = data
        self.visited = False 
        self.found = False
        self.depth = 10**9 + 7
        self.parent = None

def moveGen(curr, neighbors, graph):
    # DURL being the order
    maybe_nbrs = []
    maybe_nbrs.append((curr[0]+1, curr[1]))
    maybe_nbrs.append((curr[0]-1, curr[1]))
    maybe_nbrs.append((curr[0], curr[1]+1))
    maybe_nbrs.append((curr[0], curr[1]-1))

    #check for empty and undiscovered neighbours and update
    for i in range(4):  
        if maybe_nbrs[i][0] >= 0 and maybe_nbrs[i][1] >= 0:
            #check if visited/found already
            if (graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].visited == True or graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].found == True) and graph[curr[0]][curr[1]].depth + 1 >= graph[maybe_nbrs[i][0]][maybe_nbrs[i][1]].depth:
                continue
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
        if self.mode == 0:
            BFS()
        elif self.mode == 1:
            DFS()
        elif self.mode == 2:
            DFID()
        else :
            print("Enter a valid choice of algorithm\n");

    def getVisited(self):
        states = 0;
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
        print(self.dest)
        q.put(self.curr);
        self.graph[self.curr[0]][self.curr[1]].visited = True;
        while not q.empty():
            if goaltest(self.curr, self.dest) == True:
                break;
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

        print(self.getVisited());

    def reverse(self): 
        length = 1;
        tracker = self.graph[self.dest[0]][self.dest[1]];
        while tracker.parent != None: 
            self.graph[tracker.loc[0]][tracker.loc[1]].data = '0'
            tracker = tracker.parent
            length += 1;

        print(length);

    def display(self):
        for i in range(self.row):
            for j in range(self.cols):
                print(self.graph[i][j].data, end = '')
            print('\n')

                
def main(): 
    M = Maze(sys.argv[1]);
    M.BFS();
    M.reverse();
    M.display();

main();

