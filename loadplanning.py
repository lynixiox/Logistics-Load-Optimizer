import random
import math

# Define the population
def create_population(n_individuals, n_trucks, n_cars, truck_capacity, car_destinations, car_movement_costs):
    population = []
    for i in range(n_individuals):
        individual = [[] for _ in range(n_trucks)]
        for j in range(n_cars):
            truck = random.randint(0, n_trucks - 1)
            individual[truck].append(j)
        population.append(individual)
    return population

# Define the fitness function
def evaluate_fitness(individual, n_trucks, n_cars, car_weights, truck_capacity, car_destinations, car_movement_costs):
    fitness = 0
    for i in range(n_trucks):
        weight = sum([car_weights[car] for car in individual[i]])
        if weight > truck_capacity:
            fitness -= weight - truck_capacity
        # Calculate the total distance and movement cost for the route
        route_distance = 0
        route_movement_cost = 0
        for car in individual[i]:
            route_distance += distance(car_destinations[car])
            route_movement_cost += route_distance * car_movement_costs[car]
        fitness -= route_movement_cost
    return fitness

# Define the selection function
def select_parents(population, n_parents):
    parents = []
    fitness = [evaluate_fitness(individual, n_trucks, n_cars, car_weights, truck_capacity, car_destinations, car_movement_costs) for individual in population]
    for i in range(n_parents):
        chosen = random.choices(population, weights=fitness, k=1)[0]
        parents.append(chosen)
    return parents

# Define the mutation function
def mutate(children, mutation_rate):
    for child in children:
        for i in range(n_trucks):
            if random.random() < mutation_rate:
                car = random.randint(0, n_cars - 1)
                truck = random.randint(0, n_trucks - 1)
                child[i].remove(car)
                child[truck].append(car)
    return children

# Define the genetic algorithm
def genetic_algorithm(n_generations, n_individuals, n_parents, n_children, mutation_rate, n_trucks, n_cars, car_weights, truck_capacity, car_destinations, car_movement_costs):
    population = create_population(n_individuals, n_trucks, n_cars, truck_capacity, car_destinations, car_movement_costs)
    for i in range(n_generations):
        parents = select_parents(population, n_parents)
        children = crossover(parents, n_children)
        children = mutate(children, mutation_rate)
        population += children
        population = sorted(population, key=lambda x: evaluate_fitness(x, n_trucks, n_cars, car_weights, truck_capacity, car_destinations, car_movement_costs), reverse=True)
    return population[0]

# Example usage
n_trucks = 10
n_cars = 100
car_weights = [random.randint(1, 10) for _ in range(n_cars)]
truck_capacity = 50
car_destinations = [random.randint(1, 10) for _ in range(n_cars)]
car_movement_costs = [random.randint(1, 10) for _ in range(n_cars)]

best_solution = genetic_algorithm(100, 100, 20, 80, 0.1, n_trucks, n_cars, car_weights, truck_capacity, car_destinations, car_movement_costs)
print(best_solution)

