from human import Human
import numpy as np
import pygame


class Arena:
    def st2rgb(self, status):
        if status == "s":
            return (0, 0, 255)
        elif status == "i":
            return (255, 0, 0)
        elif status == "ia":
            return (0, 255, 0)
        else:
            return(0, 0, 0)

    def __init__(self, walls, population, radius, timeStep, speed, cutoff = 10, wSD = 0):
        self.population = []
        self.walls = walls
        self.shoppingCenter = {
                    "x": self.walls["x"] + self.walls["width"]/2 - 5,
                    "y": self.walls["y"] + self.walls["height"]/2 - 5,
                    "width": 10,
                    "height": 10
                }
        self.radius = radius
        self.time = 0
        for i in range(population):
            human = Human(self.walls, speed, timeStep, self.radius, cutoff = cutoff, wSD = wSD, infectionProbability=0)
            self.population.append(human)
        
        self.susciptible = population 
        self.infected = 0
        self.recovered = 0
        self.IR = cutoff
        self.allowShopping = False
        self.allowQuarantine = False
    
    def drawBorder(self, screen):
        arenaBorder = pygame.Rect(self.walls["x"], self.walls["y"], self.walls["width"], self.walls["height"])
        pygame.draw.rect(screen, (0, 0, 0), arenaBorder, 2)

        if self.allowShopping:
            shoppingBorder = pygame.Rect(self.shoppingCenter["x"], self.shoppingCenter["y"], self.shoppingCenter["width"], self.shoppingCenter["height"])
            pygame.draw.rect(screen, (0, 0, 0), shoppingBorder, 2)
    
    def update(self, screen, IP, RecoveryTime, timeStep, quarantine, shoppingProbability, asym):
        # The Borders of the City
        self.drawBorder(screen)
        self.time += timeStep
        count = 0
        for human in self.population:
            # Check if Human is infected and should recover
            if human.recover(RecoveryTime, self.time):
                self.infected -= 1
                self.recovered += 1
            
            # Stops loop from overreaching as we reach the last person
            if count + 1 > len(self.population) - 1:
                # Last person already had interacted with everyone
                human.update()

                # Shop if possible
                if self.allowShopping:
                    if np.random.rand() < shoppingProbability:
                        human.goShopping(self.shoppingCenter)
                # Draw the last Person
                pygame.draw.circle(screen, self.st2rgb(human.status + human.a), (human.position[0], human.position[1]), human.radius)
                break

            # Human-Human Interactions
            for i in range(count + 1, len(self.population)):
               if human.isInProximity(self.population[i].position, self.IR):
                    # Social Distancing Forces
                    human.addForce(self.population[i].position)
                    self.population[i].addForce(human.position)
                    
                    # Infection spread between Humans
                    if human.status == "i" or self.population[i].status == "i":
                        if np.random.rand() < IP and human.isInProximity(self.population[i].position, 0.915*self.IR):  
                            if self.population[i].getInfected(self.time, asym):
                                self.infected += 1
                                self.susciptible -= 1
                            if human.getInfected(self.time, asym):
                                self.susciptible -= 1
                                self.infected += 1
            # Updates position after getting all Forces
            human.update()
            
            # If there's Quarantine and human is not asymptomatic/ a "day" after infection he can be quarentined
            if self.allowQuarantine and human.q == False and human.asym == False and self.time - human.infectedTime >= 2:
                human.setUpDest(quarantine)
                human.wSD = False
                human.q = True
            # if there's a Market place human has a Chance to go Shopping
            if self.allowShopping:
                if np.random.rand() < shoppingProbability:
                    human.goShopping(self.shoppingCenter)
            # Draws the Human
            pygame.draw.circle(screen, self.st2rgb(human.status + human.a), (human.position[0], human.position[1]), human.radius)
            count += 1
        
        
######### Second Loop to Update Velocity after positions have been updated #########
        count = 0
        for human in self.population:
            # Prevents loop from overreaching last human
            if count + 1 > len(self.population) - 1:
                human.updateVelocity()
                break
            # Social Distancing forces in new Positions
            for i in range(count + 1, len(self.population)):
                if human.isInProximity(self.population[i].position, self.IR):
                    human.addForce(self.population[i].position)
                    self.population[i].addForce(human.position)
            # Updates Velocity After getting all forces
            human.updateVelocity()
            count += 1

    # Human exits City
    def exportHuman(self, walls):
        i = np.random.choice([i for i in range(len(self.population))])
        # Make sure randomely chose person isn't travelling or shopping
        if self.population[i].travelling or self.population[i].isShopping:
            return None
        
        traveller = self.population[i]
        self.population.remove(traveller)
        traveller.setUpDest(walls)
        return traveller
