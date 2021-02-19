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

class TSP(object):
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

    def cost_of_route(self, route):
        cost = 0

        for city in range(self.num_cities - 1):
            cost += self.distance[route[city]][route[city + 1]]

        return cost

    def ant_colony_optimizer(self, alpha, beta, Q, nad, retain):
        # Init hyperparams
        vaporisation_rate = 0.3 # evaporation coefficient
        num_ants = int(self.num_cities // nad)

        # Init pheromone
        rand_f = random.random() / 10
        pheromone = np.ones((self.num_cities, self.num_cities)) * rand_f
        init_pheromone = pheromone

        # Init best route
        best_route, best_cost = [], float('Inf')

        # start algo
        last_cost = float('Inf')
        identical_cost = 0
        broken, last_iter = False, False
        while True:
            if (time() - start_time) > 220:
                last_iter = True

            routes = []
            # print(f"Iter: {curr_iter}", f"Best cost: {best_cost}")

            route_costs = []
            routes = []

            # Simulate all ants
            try:
                for l in range(num_ants):
                    if last_iter is True:
                        if (time() - start_time) > 290:
                            broken = True
                            break
                    ant = Ant(self.num_cities)
                    curr_route = ant.movGen(self.distance, pheromone, self.num_cities, alpha, beta)
                    curr_cost = self.cost_of_route(curr_route)

                    if curr_cost < best_cost:
                        best_cost = curr_cost
                        best_route = curr_route[:]

                    route_costs.append(curr_cost)
                    routes.append(curr_route)
            except TypeError as e:
                # print(num_ants)
                raise e

            if broken is True:
                break

            # Update pheromone of top retain% ants
            assert len(route_costs) == num_ants
            ants = list(range(num_ants))
            sorted_ant_costs = [x for _, x in sorted(zip(route_costs, ants))]
            ants_to_update = (num_ants * retain) // 100

            update_pher = np.zeros((self.num_cities, self.num_cities))
            for k in sorted_ant_costs[:ants_to_update]:
                for city in range(len(routes[k]) - 1):
                    update_pher[routes[k][city]][routes[k][city + 1]] += Q / route_costs[k]

            pheromone = vaporisation_rate * pheromone + (1 - vaporisation_rate) * update_pher

            if last_cost == best_cost:
                identical_cost += 1
            else:
                identical_cost = 0

            last_cost = best_cost

            if identical_cost >= 10:
                if self.num_cities < 200:
                    pheromone = init_pheromone
                    identical_cost = 0

            print(*best_route)
            print(best_cost)


        # print best solution
        # print("Best Cost: ", best_cost)
        # print(best_route)
        print(*best_route)
        print(best_cost)

        return best_cost


start_time = time()

T = TSP(sys.argv[1])
T.ant_colony_optimizer(3, 5, 0.0001 * 1500, 0.75, 50)
