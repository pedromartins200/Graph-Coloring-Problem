from random import randrange, uniform, shuffle, random, sample
from Section import *
from Population import *



class Roulette:

    def __init__(self, population):
        self.roulette = []
        self.sections = len(population.individual_list)
        self.population = population
        for i in range(0, self.sections):
            min = 0
            if i != 0:
                min = self.roulette[i - 1].getMax()
            max = min + self.population.individual_list[i].fitness
            self.roulette.append(Section(min, max))


    def getRoulette(self):
        return self.roulette

    def spinWithOnePointer(self):
        sum = self.roulette[self.sections - 1].getMax()
        winner = None
        u = random.random()
        for x in range(self.sections):
            if u < (self.roulette[x].getMax() / sum):
                winner = self.population.individual_list[x]
                break
        return winner

    def rouletteSelection(self, G, number_of_colors):
        n = self.sections
        winners = []
        for x in range(n):
            winners.append(self.spinWithOnePointer())
        return Population(G, '', '', number_of_colors, '', winners)

    def SUS_selection(self, G, number_of_colors):
        sum = self.roulette[self.sections - 1].getMax()
        min = self.roulette[self.sections - 1].getMin()
        winners = []
        avg = sum / self.sections
        u = random.random()
        d = min + round(u * (sum - min))
        d = d * (avg / sum)

        for p in range(self.sections):
            for i in range(self.sections):
                if d < self.roulette[i].getMax():
                    winners.append(self.population.individual_list[i])
            d = d + avg

        return Population(G, '', '', number_of_colors, '', winners)

    def SUS(self, G, number_of_colors):  # Stochastic Universal Sampling
        NUMBER_OF_PARENTS = len(self.population.individual_list)
        total_fitness = self.compute_total_fitness()
        point_distance = total_fitness / NUMBER_OF_PARENTS
        start_point = uniform(0, point_distance)
        points = [start_point + i * point_distance for i in range(NUMBER_OF_PARENTS)]

        parents = []
        while len(parents) < NUMBER_OF_PARENTS:
            shuffle(self.population.individual_list)
            i = 0
            while i < len(points) and len(parents) < NUMBER_OF_PARENTS:
                j = 0
                while j < len(self.population.individual_list):
                    if self.get_subset_sum(j) > points[i]:
                        parents.append(self.population.individual_list[j])
                        break
                    j += 1
                i += 1

        return Population(G, '', '', number_of_colors, '', parents)

    def compute_total_fitness(self):
        total_fitness = 0
        for member in self.population.individual_list:
            total_fitness += member.fitness
        return total_fitness

    def get_subset_sum(self, end, start=0):
        subset_sum, i = 0.0, start
        while i <= end:
            subset_sum += self.population.individual_list[i].fitness
            i += 1
        return subset_sum
