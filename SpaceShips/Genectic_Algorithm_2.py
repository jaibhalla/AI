import pygame 
import math 
import random
from termcolor import colored 
from operator import add

pygame.init() 

POP_SIZE = 100
size = [600,600]
screen = pygame.display.set_mode(size)
MAX_AGE = 2000

class DNA:
    def __init__(self, pos, parent, max_age):
        self.age = 0 
        self.pos = pos
        self.vel = [0,0] 
        self.acc = [0,0] 
        self.max_age = max_age 
        self.locations = []
        self.parent = parent
        self.mutation_rate = 5
        if self.parent == None: 
            for i in range(self.max_age):    
                self.acc = [random.uniform(-0.5,0.5) + random.uniform(-0.5,0.5) ,random.uniform(-0.5,0.5) + random.uniform(-0.5,0.5)]
                self.vel = list(map(add,self.vel,self.acc))
                self.pos = list(map(add,self.pos,self.vel))
                self.acc = [0,0]
                self.locations.append(self.pos)
        else: 
            self.locations = self.mutate(self.parent)
    
    def mutate(self, parent):        
        if random.randrange(0,100) <= self.mutation_rate:

            mutate_index = random.randint(0,(round(self.max_age)/4))
            self.locations = parent.DNA.locations[:mutate_index]
            for i in range(mutate_index,self.max_age):    
                self.acc = [random.uniform(-0.5,0.5) + random.uniform(-0.5,0.5) ,random.uniform(-0.5,0.5) + random.uniform(-0.5,0.5)]
                self.vel = list(map(add,self.vel,self.acc))
                self.pos = list(map(add,self.pos,self.vel))
                self.acc = [0,0]
                self.locations.append(self.pos)
            return self.locations
        else: 
            return parent.DNA.locations 

class Population: 
    def __init__(self, start_pos, goal_pos,goal_radius,pop_size = POP_SIZE):
        self.population = []
        self.dead_pop = []
        self.goal_pos = goal_pos
        self.probability_list = [] 
        self.start_pos = start_pos
        self.parent = None
        self.generation_count  = 0
        self.solution = None
        self.goal_radius = goal_radius 
    
    def generate(self):
        print(f" Generation Count:{self.generation_count}")
        self.generation_count = self.generation_count + 1 
        for i in range(POP_SIZE):
            self.population.append(Dot(self.start_pos,self.goal_pos,self.goal_radius, self.parent))

    def live(self):
        for dot in self.population:
            dot.show()
            dot.check()

    def all_dead(self):
        if len(self.population) == 0 and len(self.dead_pop) == POP_SIZE:
            return True 
        else: 
            for dot in self.population:
                if not dot.alive and len(self.dead_pop) < POP_SIZE:
                    self.dead_pop.append(dot)
                    self.population.remove(dot)
            return False 
    
    def calc_fitness(self):
        for dot in self.dead_pop:
            closest = 5000000
            for location in dot.DNA.locations: 
                distance = abs(location[0] - self.goal_pos[0]) + abs(location[1] - self.goal_pos[1])
                if distance<closest:
                    closest = distance 
            closest = round(closest**2)        
            dot.fitness = 1/(closest**100)
            self.probability_list.append(dot.fitness)
   
    def select_parent(self):
        self.choice = random.choices(self.dead_pop, weights=self.probability_list,k=1)
        self.parent = self.choice[0]

        self.probability_list = []
        self.dead_pop = []
    
    def is_reached(self):
        for dot in self.population:
            if dot.goal_reached:
                return True 
        else:
            return False 

class Dot: 
    def __init__(self, start_pos, goal_pos, goal_radius, parent):
        self.radius = 5
        self.color = (0,0,0)
        self.DNA = DNA(start_pos, parent, MAX_AGE)
        self.center = []
        self.alive = True
        self.fitness = 0.0  
        self.goal_pos = goal_pos
        self.goal_reached = False 
        self.goal_radius = goal_radius

    def check(self):
        if self.center[0] < 0 or self.center[1] < 0 or self.center[0] > size[0] or self.center[1] > size[1]:
            self.alive = False 
        
        elif self.DNA.age > MAX_AGE:
            self.alive = False 

        # for obstacle in obstacles:
        #     for coord_x in obstacle.boundary_x:
        #         if self.center[0] == coord_x:
        #             for coord_y in obstacle.boundary_y:
        #                 if self.center[1] == coord_y:
        #                     self.alive = False 

        if self.center[0] > (self.goal_pos[0]- self.goal_radius) and self.center[0] < (self.goal_pos[0] + self.goal_radius):
            if self.center[1] > (self.goal_pos[1]-self.goal_radius) and self.center[1] < (self.goal_pos[1] + self.goal_radius):
                self.goal_reached = True
        
        
    def show(self):
        if self.alive:
            self.center = self.DNA.locations[self.DNA.age]
            self.center = list(map(round,self.center))
            self.DNA.age = self.DNA.age + 1 
            pygame.draw.circle(screen,self.color,self.center,self.radius,0)
        else:
            return

# class Obstacle: 
#     def __init__(self,pos,width,height):
#         self.pos = pos 
#         self.width = width 
#         self.height = height 
#         self.boundary_x = []
#         self.boundary_y = []

#         for i in range(self.width):
#             self.boundary_x.append(self.pos[0] +i)
        
#         for j in range(self.height):
#             self.boundary_y.append(self.pos[1] + j)    
    # def show(self):
    #     pygame.draw.rect(screen, (200,200,200), (self.pos[0],self.pos[1], self.width, self.height))

class Start:
    def __init__(self,pos):
        self.center = pos 
        self.radius = 7

    def show(self):
        pygame.draw.circle(screen,(0,255,0),self.center,self.radius,0)


class End:
    def __init__(self,pos):
        self.center = pos 
        self.radius = 7

    def show(self):
        pygame.draw.circle(screen,(255,0,0),self.center,self.radius,0)

def main(): 
    screen_color = (255,255,255)
    start = Start([300,550])
    end = End([300,50])
    pop = Population(start.center,end.center,end.radius)
    # global obstacles
    # obstacles = [Obstacle([50,200],400,30)]
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return  
        screen.fill(screen_color)
        
        start.show()
        end.show()

        # for obstacle in obstacles:
        #     obstacle.show()
        
        if pop.is_reached():
            print(colored("Goal Reached", "green"))
            return
        else: 
            if len(pop.dead_pop) == 0 and len(pop.population) == 0 :
                pop.generate()
            elif pop.all_dead():
                pop.calc_fitness()
                pop.select_parent() 
            else:
                pop.live()      

        pygame.display.flip()

if __name__ == "__main__":
    main()

