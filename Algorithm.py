from Ga import Ga
import matplotlib.pyplot as plt
import time

plt.close()
ga = Ga()

start = time.time()
result = ga.run(int(ga.popsize), float(ga.crossover), float(ga.mutation), int(ga.generations),
                ga.selection, ga.stop_criterion, float(ga.percentage), int(ga.tournament_size), ga.crossover_method,
                int(ga.number_of_colors), ga.mutation_method, ga.graph)
end = time.time()


if ga.stop_criterion == '1':
    if result[2]:
        result[0].__str__(result[1])
    else:
        print("Not possible to reach max fitness")
else:
    result[0].__str__(result[1])
print(end-start)