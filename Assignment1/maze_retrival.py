import requests
from bs4 import BeautifulSoup
import sys

algorithm_type = sys.argv[3]

cols = sys.argv[1]
rows = sys.argv[2]

parameters = {'cols':cols, 'rows':rows,'type':'text', 'width':'3', 'height':'2'}
r = requests.post("http://www.delorie.com/game-room/mazes/genmaze.cgi", parameters)
soup = BeautifulSoup(r.text, 'lxml')
pre = soup.find_all('pre')[-1]
maze = pre.text.strip()

maze = list(maze)

plus_index = []
for i in range(len(maze) - 1):
    if(maze[i] == '\n' and maze[i+1] == '+'):
        plus_index.append(i+1)

for i in plus_index:
    if(maze[i-2] != '|'):
        dest = i - 2

modified_maze = "".join(maze[:dest]) + '*' + "".join(maze[dest+1:])

print(algorithm_type)
print(modified_maze)
# print(pre.text.strip())
