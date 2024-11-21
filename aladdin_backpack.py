import random


class AladdinBackpack:

    def __init__(
        self,
        num_items,
        weight_range: tuple = (1, 10),
        value_range: tuple = (1, 30),
        fragility_range: tuple = (1, 5),
        generations=10,
        backpack_size=20,
        mutation_probability=0.3,
    ) -> None:
        self.num_items = num_items
        self.weight_range = weight_range
        self.value_range = value_range
        self.fragility_range = fragility_range
        self.generations = generations
        self.backpack_size = backpack_size
        self.mutation_probability = mutation_probability
        self.population = []
        self.fitness_list = []
        self.parents_selected = []
        self.weight_list = []
        self.value_list = []
        self.fragility_list = []

    def initialize(self, population_size):
        """
        Initialize the population
        """
        print("Initializing population...")
        for _ in range(population_size):
            individual = ""
            for _ in range(self.num_items):
                if random.random() < 0.5:
                    individual += "0"
                else:
                    individual += "1"
            self.population.append(individual)
        self.weight_list = [
            random.randint(*self.weight_range) for _ in range(self.num_items)
        ]
        self.value_list = [
            random.randint(*self.value_range) for _ in range(self.num_items)
        ]
        self.fragility_list = [
            random.randint(*self.fragility_range) for _ in range(self.num_items)
        ]
        print(self.population)

    def evaluate(self):
        assert self.population, "Population is empty"

        fitness_list = []
        for person in self.population:
            sum_weight = 0
            sum_value = 0
            sum_fragility = 0
            for i in range(len(person)):
                if person[i] == "1":
                    sum_weight += self.weight_list[i]
                    sum_value += self.value_list[i]
                    sum_fragility += self.fragility_list[i]
            if sum_weight <= self.backpack_size:
                fitness_list.append((person, sum_value - sum_fragility))
            else:
                fitness_list.append((person, 0))

        self.fitness_list = fitness_list

    def selection(self, tournament_size=3):
        assert self.fitness_list, "No fit candidates to select from"
        selected = []
        for _ in range(len(self.fitness_list)):
            tournament = random.sample(self.fitness_list, tournament_size)
            best_individual = max(tournament, key=lambda x: x[1])
            selected.append(best_individual[0])
        self.parents_selected = selected


    def crossover(self):
        assert self.parents_selected, "No parents selected"
        new_population = []
        for i in range(0, len(self.parents_selected), 2):
            parent1 = self.population[i]
            parent2 = self.population[i + 1]
            crossover_point = random.randint(1, self.num_items - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            new_population.extend([child1, child2])

        self.population = new_population

    def mutation(self):
        assert self.population, "Population is empty"

        for i in range(len(self.population)):
            if random.random() < self.mutation_probability:
                mutation_point = random.randint(0, self.num_items - 1)
                person = list(self.population[i])
                person[mutation_point] = "1" if person[mutation_point] == "0" else "0"
                
                self.population[i] = "".join(person)

    def run(self):
        self.initialize(population_size=10)
        for generation in range(self.generations):
            print(f"Generation {generation + 1}")
            self.evaluate()
            self.selection()
            self.crossover()
            self.mutation()
            best_solutions = sorted(self.fitness_list, key=lambda x: x[1], reverse=True)[:3]
            print(f"Top 3 solutions after generation {generation + 1}: {best_solutions}")
        self.evaluate()
        best_solutions = sorted(self.fitness_list, key=lambda x: x[1], reverse=True)[0]
        return best_solutions[0], self.weight_list, self.value_list, self.fragility_list

