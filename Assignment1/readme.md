# AI Lab 1 Report

## Libraries Required
matplot  
numpy  
requests  
BeautifulSoup  
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

`bash bash.sh`  
bash.sh could be modified to test for different ranges of width and height.
