from MapIndividual import *
import matplotlib.pyplot as plt  # Drawing graphs
import networkx as nx  # Generating of graphs
import numpy as np

class Population:
    def __init__(self, initialGraph, popsize, n_nodes, number_of_colors, adjacency_list, individual_list=[]):

        colors = ['lightcoral', 'maroon', 'pink', 'blue', 'g', 'c', 'm', 'y', 'k', 'w', 'r', 'dimgrey', 'darkgrey', 'crimson', 'plum', 'palegreen']
        self.color_list = colors[:number_of_colors]
        self.number_of_colors = number_of_colors

        if len(individual_list) > 0:
            self.passPopulation(individual_list)
            return


        self.initialGraph = initialGraph
        self.individual_list = self.generate_random_initial_population(popsize, n_nodes, adjacency_list, self.initialGraph)

    def passPopulation(self, individual_list):
        self.individual_list = individual_list

    # Generate random initial population
    def generate_random_initial_population(self, population_size, n_nodes, al, initialGraph):
        input_population = []

        # Generate random initial population
        for k in range(population_size):
            colors = np.random.choice(self.color_list, n_nodes, replace=True)
            color_list = list(colors)
            input_population.append(MapIndividual(color_list, al, initialGraph))

        return input_population


    def createPopulation(self, individual_list):
        self.individual_list = individual_list

    def print_me(self, figure_number=1, figure_title=''):

        self.sort(True)

        node_list = self.individual_list[0].graph_nx.nodes(data=True)
        colors_nodes = [element[1]['color'] for element in node_list]

        plt.figure(figure_number)
        plt.title("Generation " + str(figure_number) + " with fitness = " + str(self.individual_list[0].fitness) + ", " + str(self.individual_list[0].wrong_connections)  +" Wrong Edges")
        nx.draw_networkx(self.individual_list[0].graph_nx, with_labels=True, node_color=colors_nodes)
        plt.draw()
        plt.show()

    def truncationSelection(self, G, p):
        # let's sort the elements in order
        self.sort(True)
        n = len(self.individual_list)
        total_elements_selected = round(n * p)

        # put the best % of elements inside the list
        individual_list = self.individual_list[:total_elements_selected]
        output_list = []

        # fill the remaining list with the elements selected
        k = len(self.individual_list)
        size = 0
        while size < k:
            position = size % total_elements_selected
            output_list.append(individual_list[position])
            size = size + 1
        return Population(G, '', '', self.number_of_colors, '', output_list)

    # didnt understand this method clearly
    # are we deleting the p worst, or keeping them?
    # anyway i decided to remove the p worst, and replicate the list back to size n
    def WorstReplacement(self, G, p):
        # sort worst first
        self.sort(False)
        n = len(self.individual_list)
        total_elements_selected = n - round(n * p)

        individual_list = self.individual_list[:total_elements_selected]
        output_list = []

        k = len(self.individual_list)
        size = 0
        while size < k:
            position = size % total_elements_selected
            output_list.append(individual_list[position])
            size = size + 1
        return Population(G, '', '', self.number_of_colors, '', output_list)

    def tournamentWithReplacement(self, G, s):
        tournament_dudes = []
        winners = []
        a = 0
        b = len(self.individual_list) - 1

        for j in range(len(self.individual_list)):
            for i in range(s):
                r = random.random()
                d1 = a + round(r * b - a)
                tournament_dudes.append(self.individual_list[d1])
            # sort so the top individual stays at position = 0
            tournament_dudes.sort(key=lambda x: x.fitness, reverse=True)
            # lets select the top guy
            winners.append(tournament_dudes[0])
            tournament_dudes.clear()

        return Population(G, '', '', self.number_of_colors, '', winners)

    def randomPermutation(self, individual_list):
        for i in range(len(individual_list)):
            b = len(individual_list)
            r = random.random()
            d = i + round(r * (b - i))

            m = individual_list[i]
            individual_list[i] = individual_list[d]
            individual_list[d] = m

    def tournamentSelectionWithoutReplacement(self, G, s):
        winners = []
        tournament = []

        for individual in self.individual_list:
            tournament.append(individual)

        for i in range(s):
            random.shuffle(tournament)
            for j in range(0, len(self.individual_list), s):
                winner = j
                max_fitness = tournament[j].fitness
                for k in range(j + 1, j + s):
                    if tournament[k].fitness > max_fitness:
                        max_fitness = tournament[k].fitness
                        winner = k
                winners.append(tournament[winner])
        return Population(G, '', '', self.number_of_colors, '', winners)


    def averageFitness(self):
        sum = 0
        n = len(self.individual_list)
        for x in range(n):
            sum += self.individual_list[x].fitness
        return sum / n

    def __str__(self, generations=1):
        self.print_me(generations)

    def findMaxElement(self):
        for i in range(len(self.individual_list)):
            if self.individual_list[i].fitness == self.individual_list[0].n_nodes * 2:
                return True
        return False

    # Override basic sort method
    # btw, sorting in python is weird
    def sort(self, order):
        return self.individual_list.sort(key=lambda x: x.fitness, reverse=order)
