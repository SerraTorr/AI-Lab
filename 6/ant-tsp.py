import random
from time import time
import sys
import numpy as np

class Ant(object):
    def __init__(self, totalCities):
        self.route = []
        self.num_cities = totalCities

    def movGen(self, distance, pheromone, num_cities, alpha, beta):
        next_city = random.randint(0, self.num_cities - 1)
        self.route.append(next_city)

        max_iterations = 1000
        while len(self.route) != num_cities:
            curr_city = next_city
            next_city = self.find_next_city(num_cities, alpha, beta, pheromone, distance, curr_city)
            self.route.append(next_city)

        return self.route

    def find_next_city(self, num_cities, alpha, beta, pheromone, distance, curr_city):
        open_ = []
        for i in range(num_cities):
            if i not in self.route:
                open_.append(i)
        p_ij_k = 0
        cum_probs = []
        for j in range(len(open_)):
            p_ij_k = self.probability_function(alpha, beta, pheromone, distance, curr_city, open_[j])
            cum_probs.append(p_ij_k)
            if open_[j] == curr_city:
                print("******************************")

        next_city = random.choices(open_, weights=cum_probs)[0]

        return next_city

    def probability_function(self, alpha, beta, pheromone, distance, i, j):
        return (pheromone[i][j] ** alpha ) * ((1 / distance[i][j]) ** beta)

class ant_algorithm_optimisation(object):
    def __init__(self, filename):
        with open(filename, 'r') as inp_file:
            lines = inp_file.readlines()

        type_ = lines[0] # euclidean or noneuclidean
        self.num_cities = int(lines[1].strip())
        self.coordinates = []

        for point in range(self.num_cities+2):
            self.coordinates.append(lines[point])
        self.distance = self.extract_distances(self.num_cities, lines)

    def extract_distances(self, totalCities, lines):
        distance = []
        for index in range(totalCities+2, len(lines)):
            line = lines[index].strip()
            distance.append(list(map(float, line.split(" "))))
        return distance

    def cost_(self, route):
        c = 0
        for i in range(len(route) - 1):
            # cost += self.distance[route[city+1]][route[city]]
            c += self.distance[route[i]][route[i+1]]
            """
            In case of euclidean distance city and city + 1 could be reversed
            not in case of non-euclidean (non symetric case)
            """

        return c

    def INT_MAX_(self):
        return float('Inf')

    def reset_pheromone(self, Q, routes, r_c, ants, memory):
        """
        r_c is route costs
        ants : range from 0 to total ants
        """
        sortedAnts = []
        for i,j in sorted(zip(r_c, ants)):
            sortedAnts.append(j)
        reset_pheromone = np.zeros((self.num_cities, self.num_cities))

        candidate_ants = sortedAnts[:((len(ants) * memory) // 100)]
        for k in candidate_ants:
            for city in range(len(routes[k]) - 1):
                reset_pheromone[routes[k][city]][routes[k][city + 1]] += Q / r_c[k]

        return reset_pheromone

    def cal_phero(self, pheromone, vaporisation_rate, reset_pheromone):
        new_phero = vaporisation_rate * pheromone + (1 - vaporisation_rate) * reset_pheromone
        return new_phero

    def ant_algorithm(self, vaporisation_rate, memory):
        # hyperparameters initialisation
        alpha = 3
        beta = 5
        Q = .2
        num_ants = int(self.num_cities)
        path = []
        path_length = self.INT_MAX_()
        last_cost = path_length

        reset = np.ones((self.num_cities, self.num_cities))
        pheromone = reset

        identical_cost = 0
        last_iter = False
        flag = False

        max_iterations = 10000
        while True:
            if (time() - tick_) > 299:
                break

            routes = []
            route_costs = []

            for l in range(num_ants):

                ant = Ant(self.num_cities)
                curr_route = ant.movGen(self.distance, pheromone, self.num_cities, alpha, beta)
                curr_cost = self.cost_(curr_route)
                route_costs.append(curr_cost)
                routes.append(curr_route)

                if curr_cost <= path_length:
                    path = curr_route[:]
                    path_length = curr_cost

            pheromone = self.cal_phero(pheromone, vaporisation_rate, self.reset_pheromone(Q, routes, route_costs, list(range(num_ants)), memory))

            if last_cost == path_length:
                identical_cost += 1
                if identical_cost > 5:
                    pheromone = reset
                    identical_cost = 0
            else:
                identical_cost = 0

            last_cost = path_length
            print(*path)
            print(path_length)

        return path_length


tick_ = time()
T = ant_algorithm_optimisation(sys.argv[1])
T.ant_algorithm(0.3, 50)
