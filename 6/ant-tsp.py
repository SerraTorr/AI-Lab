import random
import sys
import numpy as np
from time import time


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

    def ant_algorithm(self, vaporisation_rate, memory):
        # hyperparameters initialisation
        alpha = 3
        beta = 5
        Q = .2
        num_ants = int(self.num_cities)
        best_route = []
        best_cost = self.INT_MAX_()
        last_cost = best_cost

        reset = np.ones((self.num_cities, self.num_cities))
        pheromone = reset

        identical_cost = 0
        last_iter = False
        flag = False

        while True:
            if (time() - start_time) > 299:
                break

            routes = []
            route_costs = []

            for l in range(num_ants):

                ant = Ant(self.num_cities)
                curr_route = ant.movGen(self.distance, pheromone, self.num_cities, alpha, beta)
                curr_cost = self.cost_(curr_route)
                route_costs.append(curr_cost)
                routes.append(curr_route)

                if curr_cost <= best_cost:
                    best_route = curr_route[:]
                    best_cost = curr_cost

            ants = list(range(num_ants))
            sortedAnts = []
            for i,j in sorted(zip(route_costs, ants)):
                sortedAnts.append(j)

            update_pher = np.zeros((self.num_cities, self.num_cities))
            for k in sortedAnts[:((num_ants * memory) // 100)]:
                for city in range(len(routes[k]) - 1):
                    update_pher[routes[k][city]][routes[k][city + 1]] += Q / route_costs[k]

            pheromone = vaporisation_rate * pheromone + (1 - vaporisation_rate) * update_pher

            if last_cost == best_cost:
                identical_cost += 1
                if identical_cost>5:
                    pheromone = reset
                    identical_cost = 0
            else:
                identical_cost = 0

            last_cost = best_cost

            print(*best_route)
            print(best_cost)

        return best_cost


start_time = time()

T = ant_algorithm_optimisation(sys.argv[1])
T.ant_algorithm(0.3, 50)
