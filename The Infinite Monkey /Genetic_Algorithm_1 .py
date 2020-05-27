import random 
import string 
import math
from termcolor import colored

POPLATION_SIZE = 200
TARGET = "Hello World"
MUTATION_RATE = 0.01
MAX_GEN = 700

class DNA:
    def __init__(self, parents = None):
        self.genes = "" 
        self.character_list = string.ascii_letters + string.digits + string.punctuation + " "
        self.fitness_score = 0
        self.probabilty = 0
        self.length = len(TARGET)
        self.parents = parents 
        self.mutation_rate = MUTATION_RATE

        if parents == None:
            for i in range(self.length):
                    self.genes = self.genes + random.choice(self.character_list)
        else: 
            self.genes = self.mutation(self.crossover())
    
    def crossover(self):
        pivot = random.randrange(self.length)
        return self.parents[0].genes[:pivot] + self.parents[1].genes[pivot:]

    def mutation(self, temp):
        temp = list(temp)
        for i in range(len(temp)): 
            if random.uniform(0,1) <= self.mutation_rate:
                temp[i] = random.choice(self.character_list)  
        return ''.join(temp)  


class Population:
    def __init__(self):
        self.population = []
        self.generation_count = 0
        self.finished = False 
        self.target = TARGET
        self.parents = None
          
    def generate(self):
            self.population = []
            self.probabilty_list = []
            for i in range(POPLATION_SIZE):
                self.population.append(DNA(parents = self.parents))
            self.generation_count = self.generation_count + 1 

    def fitness(self):
        for element in self.population:
            for i,target_letter in enumerate(self.target): 
                if target_letter == element.genes[i]:
                    element.fitness_score = element.fitness_score + 1 
                    element.probabilty = ((element.fitness_score/len(TARGET))**100) #to the power of 100, used to imporve fitness function 
            self.probabilty_list.append(element.probabilty)

    def selection(self):  
        if any(count > 0 for count in self.probabilty_list):
            self.parents = random.choices(self.population,weights=self.probabilty_list, k = 2)

        else: self.parents = None
       
    def isComplete(self):
        for element in self.population:
            if element.genes == self.target:
                print(colored(f"Solution: {element.genes}","green"))
                print(colored(f"Generations: {self.generation_count}","blue"),)
                self.finished = True

        if self.generation_count == MAX_GEN:
            self.finished = True


    def show(self):
        for element in self.population:
            print(colored(element.genes, "red"))
    

def main(): 
    population = Population()
    while not population.finished:
        population.generate()
        population.fitness()
        population.selection()
        population.show()
        population.isComplete()

    
if __name__ == "__main__":
    main()