import numpy as np
import random

def calculate_optimal_route(points_array, pop_size=300, num_generations=1500, return_to_depot=False):
    points = np.array(points_array)
    num_points = len(points)
    
    if num_points <= 2:
        return list(range(num_points))

    def distance(idx_a, idx_b):
        return np.linalg.norm(points[idx_a] - points[idx_b])

    def calculate_cost(chromosome):
        full_path = [0] + chromosome
        cost = 0
        for i in range(len(full_path) - 1):
            cost += distance(full_path[i], full_path[i+1])
        if return_to_depot:
            cost += distance(full_path[-1], 0)
        return cost

    def create_individual():
        ind = list(range(1, num_points))
        random.shuffle(ind)
        return ind

    def crossover(parent1, parent2):
        size = len(parent1)
        a, b = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[a:b] = parent1[a:b]
        fill_elements = [item for item in parent2 if item not in child]
        fill_idx = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = fill_elements[fill_idx]
                fill_idx += 1
        return child

    def mutate(chromosome, mutation_rate=0.2):
        if random.random() < mutation_rate and len(chromosome) > 2:
            # Dùng Inversion Mutation (mạnh hơn cho 20 phòng)
            i, j = sorted(random.sample(range(len(chromosome)), 2))
            chromosome[i:j] = chromosome[i:j][::-1]
        return chromosome

    # Khởi tạo quần thể
    population = [create_individual() for _ in range(pop_size)]

    for generation in range(num_generations):
        population.sort(key=calculate_cost)
        
        # Elitism: 10% tốt nhất
        num_elites = max(1, int(pop_size * 0.1))
        next_generation = population[:num_elites]

        # Selection Pool: 50% tốt nhất
        selection_pool = population[:max(2, int(pop_size * 0.5))]

        while len(next_generation) < pop_size:
            p1, p2 = random.sample(selection_pool, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_generation.append(child)

        population = next_generation

    best_chromosome = min(population, key=calculate_cost)
    return [0] + best_chromosome