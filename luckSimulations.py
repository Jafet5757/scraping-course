""" 
  Los individuos están constituidos de habilidad y suerte, la suerte ocupa un pequeño porcentaje y puede ser positiva o negativa
  la habilidad ocupa la mayor parte
  ambas se generan de forma aleaatoria
"""

import random

def init_population(size, skillRate=0.95, luckRate=0.05):
    """ 
    Los individuos están compuestos por: [skill, luck] 
    """
    population = []
    for _ in range(size):
        individual = [round(random.uniform(0, skillRate), 2), round(random.uniform(-luckRate, luckRate), 2)]
        population.append(individual)

    return population

def fitness(population):
   for individual in population:
      sum = individual[0] + individual[1]
      individual.append(sum)

def paint_individuals(population):
   c = 0
   for ind in population:
      c += 1
      print(c, ind)

def main():
  size = 1000 * 100
  generations = 100
  best_individuals = []

  for _ in range(generations):
    population = init_population(size, 0.75, 0.25)

    fitness(population)

    population.sort(key = lambda i: i[2])

    pos = random.randint(0,size)

    best_individuals.append([population[-1], population[-2], population[-3], population[pos], pos])

  best_individuals.sort(key = lambda i: i[2])

  paint_individuals(best_individuals)

def one_population():
  size = 1000 * 5
  population = init_population(size, 0.75, 0.25)

  fitness(population)

  population.sort(key = lambda i: i[2])

  paint_individuals(population)
  

one_population()
