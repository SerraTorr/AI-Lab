import csv
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_list(filename,algorithm):
    X = []
    Y = []
    path_length_ud = []
    states_explored_ud = []
    path_length_du = []
    states_explored_du = []

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        line_count = 0
        index = 0
        for row in csv_reader:
            if int(row[0]) != algorithm:
                continue
            X.append(int(row[1]))
            Y.append(int(row[2]))
            path_length_ud.append(int(row[3]))
            states_explored_ud.append(int(row[4]))
            path_length_du.append(int(row[5]))
            states_explored_du.append(int(row[6]))
            index += 1

    return X,Y,path_length_ud,states_explored_ud,path_length_du,states_explored_du

def plot_graph(X,Y,Z):
    plotx,ploty, = np.meshgrid(np.linspace(np.min(X),np.max(X),10),\
                               np.linspace(np.min(Y),np.max(Y),10))
    plotz = interp.griddata((X,Y),Z,(plotx,ploty),method='linear')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(plotx,ploty,plotz,cstride=1,rstride=1,cmap='viridis')  # or 'hot'
    plt.show()

# //BFS
X,Y,path_length_ud,states_explored_ud,path_length_du,states_explored_du = get_list('table1.txt',0)
plot_graph(X,Y,path_length_ud)
plot_graph(X,Y,states_explored_ud)
plot_graph(X,Y,path_length_du)
plot_graph(X,Y,states_explored_du)

# //DFS
X,Y,path_length_ud,states_explored_ud,path_length_du,states_explored_du = get_list('table1.txt',1)
plot_graph(X,Y,path_length_ud)
plot_graph(X,Y,states_explored_ud)
plot_graph(X,Y,path_length_du)
plot_graph(X,Y,states_explored_du)

# //DFID
X,Y,path_length_ud,states_explored_ud,path_length_du,states_explored_du = get_list('table1.txt',2)
plot_graph(X,Y,path_length_ud)
plot_graph(X,Y,states_explored_ud)
plot_graph(X,Y,path_length_du)
plot_graph(X,Y,states_explored_du)
