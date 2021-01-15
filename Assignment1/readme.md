# AI Lab 1 Report

## Libraries Required
BeautifulSoup  
matplot  
numpy  
requests  
SciPy  
mpl_toolkits  

## Running

#### To Test for Single Maze
- Write input in the file test1.txt (0: BFS, 1:DFS, 2:DFID)
e.g   
2  
+--+--+--+--+--+--+--+--+--+--+--+--+--+  
   |                 |     |     |     |  
+  +  +--+--+--+  +  +--+  +  +  +  +  +  
|  |  |  |        |           |  |  |  |  
+  +  +  +  +--+--+--+--+  +--+--+  +  +  
|  |     |     |     |     |     |  |  |  
+  +--+--+--+  +--+  +  +--+  +  +  +--+  
|     |        |     |  |     |  |     |  
+--+  +  +  +--+  +--+--+  +--+  +--+  +  
|  |     |  |     |     |  |  |     |  |  
+  +  +--+  +  +--+  +  +  +  +--+  +  +  
|  |     |        |  |  |  |  |     |  |  
+  +--+  +--+  +  +  +  +  +  +  +--+  +  
|     |  |     |  |  |  |  |  |     |  |  
+--+  +  +  +--+  +  +  +  +  +  +  +  +  
|  |     |  |     |  |  |  |  |  |     |  
+  +--+--+  +  +--+  +  +  +  +  +--+  +  
|           |        |     |     |     *  
+--+--+--+--+--+--+--+--+--+--+--+--+--+  

- Below command will print required path found using required algorithm
`python 180010033.py test1.txt`

#### To test for multiple maze

`bash bash.sh > table.txt`
Values in the table.txt are in the format algorithm used", "rows", "cols", "states_explored for order down up right left", "path length for order down up right left", "states explored for order left right up down", "path length for order left right up down"  
   
bash.sh could be modified to test for different ranges of width and height.
