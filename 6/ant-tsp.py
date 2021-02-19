import random
from time import time
import sys
import numpy as np

class Ant(object):
    """
    Initialize the ant
    and
    movGen function creates the path (starting from and ending at same city and covering all)
    probability function used is defined by f(x) probability_function

    params: totalCities
    """
    def __init__(self, totalCities):
        """
        Constructor
        """
        self.route = []
        self.num_cities = totalCities

    def movGen(self, distance, pheromone, num_cities, alpha, beta):
        """
        Input: distance (matrix containing distances between two cities) symatric in case of euclidean
        Input: pheromone (pheormone in paths at T by ants)
        Input: num_cities (total cities)
        Input: alpha (power of pheromone term)
        Input: beta power of visibility term
        """
        next_city = random.randint(0, self.num_cities - 1) # first city in route
        self.route.append(next_city) # route contains path of the ant

        max_iterations = 1000
        while len(self.route) != num_cities: # builds the route covering all cities starting and ending at same city
            curr_city = next_city
            next_city = self.find_next_city(num_cities, alpha, beta, pheromone, distance, curr_city) # next city is found based on probality genearted using defined f(x)
            self.route.append(next_city)

        return self.route

    def find_next_city(self, num_cities, alpha, beta, pheromone, distance, curr_city):
        """
        Input: alpha beta , power of the terms pheromone and visibility
        Output: returns next city in the path
        """
        open_ = [] # list contains all open cities i.e where can next move be
        for i in range(num_cities):
            if i not in self.route: # if city is not present in route add it to open
                open_.append(i)

        p_ij_k = 0 # probability term
        weights_ = [] # storing weights to randomly choose based on weights probability

        for j in range(len(open_)):
            """
            looping over all open cities to choose best next city to move
            """
            p_ij_k = self.probability_function(alpha, beta, pheromone, distance, curr_city, open_[j])
            weights_.append(p_ij_k)

            if open_[j] == curr_city: # never enter loop
                print("******************************")

        next_city = random.choices(open_, weights=weights_)[0] # this function randomly chooses an element with probability of each equal to weights given

        return next_city # next best move

    def probability_function(self, alpha, beta, pheromone, distance, i, j):
        """
        probility to move from city i to city j for ant k
        could be normalised with sum. No effect in output.
        """
        return (pheromone[i][j] ** alpha ) * ((1 / distance[i][j]) ** beta)

class ant_algorithm_optimisation(object):
    def __init__(self, filename):
        with open(filename, 'r') as inp_file:
            lines = inp_file.readlines()

        type_ = lines[0] # euclidean or noneuclidean
        self.num_cities = int(lines[1].strip())
        self.coordinates = [] # never used

        for point in range(self.num_cities+2):
            self.coordinates.append(lines[point]) # never used

        self.distance = self.extract_distances(self.num_cities, lines) # returns the distance matrix

    def extract_distances(self, totalCities, lines):
        """
        Input: file containg data
        Output: returns the distance matrix
        """

        distance = [] # distance matrix to store the graph
        for index in range(totalCities+2, len(lines)): # skipping the coordinates
            line = lines[index].strip()
            distance.append(list(map(float, line.split(" ")))) # space saperated distances
        return distance # distance matrix

    def cost_(self, route):
        """
        Input: route (containg all cities)
        Output: path length of the route
        """
        c = 0 # stores the cost
        for i in range(len(route) - 1):
            # cost += self.distance[route[city+1]][route[city]]
            c += self.distance[route[i]][route[i+1]] # adding to cost
            """
            In case of euclidean distance city and city + 1 could be reversed
            not in case of non-euclidean (non symetric case)
            """

        return c # returning the cost of the route

    def INT_MAX_(self):
        """
        distances are floats
        thus returns INT_MAX as float
        """
        return float('Inf')

    def reset_pheromone(self, Q, routes, r_c, ants, memory):
        """
        r_c is route costs
        ants : range from 0 to total ants
        """
        sortedAnts = [] # list containg ants in best to worst paht length order
        for i,j in sorted(zip(r_c, ants)): # sorting the ants
            sortedAnts.append(j)
        reset_pheromone = np.zeros((self.num_cities, self.num_cities)) # initialising the pheormone

        candidate_ants = sortedAnts[:((len(ants) * memory) // 100)] # taking best memory % of ants
        for k in candidate_ants: # candidate_ants are memory % best ants from total
            for city in range(len(routes[k]) - 1):
                reset_pheromone[routes[k][city]][routes[k][city + 1]] += Q / r_c[k]

        return reset_pheromone #

    def cal_phero(self, pheromone, vaporisation_rate, reset_pheromone):
        """
        Input: vaporisation rate of pheromone and pheormone values
        Output: pheromone left after vaporisation
        """
        new_phero = vaporisation_rate * pheromone + (1 - vaporisation_rate) * reset_pheromone
        # pheormone left is initial - vaporised thus (1-vaporisation_rate)
        return new_phero

    def ant_algorithm(self, vaporisation_rate, memory):
        # hyperparameters initialisation
        alpha = 2 # power of pheormone term
        beta = 4 # power of visiility term
        Q = .2 # constant
        num_ants = int(self.num_cities)
        path = [] # stores the path
        path_length = self.INT_MAX_() # stores the lenght of the above path
        last_cost = path_length

        reset = np.ones((self.num_cities, self.num_cities)) # initialising pheromone
        pheromone = reset

        identical_cost = 0 # if there has been no change in best path values terminate or re_initialise
        last_iter = False
        flag = False

        max_iterations = 10000
        while True:
            if (time() - tick_) > 280:
                """
                max time allowed 300 seconds
                breaking if more than that
                """
                break

            routes = [] # path
            route_costs = [] # cost of above path

            for l in range(num_ants):
                """
                moving ants one by one, keeping tracks of best path
                """

                ant = Ant(self.num_cities)
                curr_route = ant.movGen(self.distance, pheromone, self.num_cities, alpha, beta)
                curr_cost = self.cost_(curr_route)
                route_costs.append(curr_cost)
                routes.append(curr_route)

                if curr_cost <= path_length: # if current is better than best then best is curr
                    path = curr_route[:]
                    path_length = curr_cost

            # calculating new pheromone
            pheromone = self.cal_phero(pheromone, vaporisation_rate, self.reset_pheromone(Q, routes, route_costs, list(range(num_ants)), memory))

            if last_cost == path_length:
                identical_cost += 1
                if identical_cost > 5: # if no change then re_initialise
                    pheromone = reset
                    identical_cost = 0
            else:
                identical_cost = 0

            last_cost = path_length
            # printing best path after every iterations
            print(*path)
            print(path_length)

        return path_length


tick_ = time() # if time > 300 seconds breaking the programe
T = ant_algorithm_optimisation(sys.argv[1]) # taking file name as argument
T.ant_algorithm(0.3, 50)
