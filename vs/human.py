import numpy as np
import math

class Human:
    def rotate(self, angle, vector):
        theta = np.deg2rad(angle)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        return np.dot(rot, vector)

    def __init__(self, walls, speed, timeStep, radius = 1, infectionProbability = 0.1, cutoff = 10, wSD = 0):
        self.walls = walls
        self.status = "s"
        self.infectedTime = None
        if np.random.rand() < infectionProbability:
            self.status = "i"
            self.infectedTime = 0
        
        self.angle = np.random.rand()*360
        self.speed = speed #* np.random.rand()
        self.velocity = self.rotate(self.angle, np.array([speed, 0]))
        self.position = np.array([
            self.walls["width"]*np.random.rand() + self.walls["x"],
            self.walls["height"]*np.random.rand() + self.walls["y"]
        ])
        self.radius = radius
        self.timeStep = timeStep
        self.travelling = False
        self.destination = None
        # constants of Lennard Jones Potential
        self.eps = 15.0
        self.sig = 20.0
        self.force = np.array([0.0, 0.0])
        self.oldForce = np.array([0.0, 0.0])
        self.cutoff = cutoff
        # will Social Distance
        self.wSD = False
        if np.random.rand() < wSD:
            self.wSD = True
        self.oldPos = None
        self.shoppingTime = None
        self.isShopping = False
        self.shoppingDuration = 3.0
        self.oldWalls = None
        # end Shopping
        self.endSh = None
        # asymptomatic
        self.asym = None
        # q for quarintined
        self.q = False
        # a for asymptomatic
        self.a = ""
    
    # Sets destination to Shopping center
    def goShopping(self, walls):
        if self.isShopping or self.travelling:
            return
        self.travelling = True
        self.oldPos = self.position
        self.oldWalls = self.walls
        self.destination = walls
        center = np.array([walls["x"] + walls["width"]/2, walls["y"] + walls["height"]/2])
        pointer = center - self.position
        self.velocity = pointer*self.speed*10
        self.shoppingTime = False
        self.isShopping = True

    # Ends Shopping and sets destination to back where human was before shopping
    def endShopping(self):
        self.travelling = True
        self.destination = {
            "x": self.oldPos[0] - self.radius*2,
            "y": self.oldPos[1] - self.radius*2,
            "width": self.radius*4,
            "height": self.radius*4
        }
        self.endSh = True

    # Sets up travelling destination
    def setUpDest(self, walls):
        if self.travelling or self.isShopping:
            return
        self.travelling = True
        self.destination = walls
        center = np.array([walls["x"] + walls["width"]/2, walls["y"] + walls["height"]/2])
        pointer = center - self.position
        self.velocity = pointer

    # Updates Position while travelling or going shopping
    def travel(self):
        # Checks if destination is reached
        if self.position[0] + self.radius <= self.destination["x"] + self.destination["width"] and self.position[0] - self.radius >= self.destination["x"] and self.position[1] + self.radius <= self.destination["y"] + self.destination["height"] and self.position[1] - self.radius >= self.destination["y"]:
            self.travelling = False
            self.walls = self.destination
            self.destination = None
            # Checks that destination was Shopping and not Another City
            if self.shoppingTime != None:
                self.shoppingTime = self.shoppingDuration
                self.isShopping = True
            
            # Checks if destination was Back to where human was after shopping 
            if self.endSh:
                self.walls = self.oldWalls
                self.oldWalls = None
                self.oldPos = None
                self.isShopping = False
                self.endSh = None
            return
        # Updates position
        self.position = self.position + self.timeStep*self.velocity 
    
    def addForce(self, vector):
        # IF NO SOCIAL DISTANCING NO FORCE
        if not self.wSD or self.travelling or self.isShopping:
            return
        direction = self.position - vector
        # Shifting minimum of Potential to cutoff point
        dist = np.linalg.norm(direction) - (self.cutoff - self.sig*(2.0**(1.0/6.0)))

        # APPLYING LENNARD JONES FORCE
        magnitude = self.eps*(((48.0*self.sig**14.0)/(dist**14.0)) - ((24.0*self.sig**8.0)/(dist**8.0)))
        a = direction *magnitude
        self.force += a

    def updateVelocity(self):
        # Updates Velocity when travelling according to "almost" a spring force law
        if self.travelling:
            center = np.array([self.destination["x"] + self.destination["width"]/2, self.destination["y"] + self.destination["height"]/2])
            pointer = center - self.position
            self.velocity = pointer
            return
        # RANDOM WALK IN CASE OF NO SOCIAL DISTANCING
        if not self.wSD or self.isShopping:
            if np.random.rand() < 0.01:
                theta = np.random.rand()*180
                self.velocity = self.rotate(theta, self.velocity)
            return
        
        # UPDATING VELOCITY ACCORDING TO VERLET ALGORITHM
        self.velocity += (self.timeStep/2)*(self.force + self.oldForce)
        self.force = np.array([0.0, 0.0])
        self.oldForce = np.array([0.0, 0.0])

    # Updates position
    def update(self):
        # Checks if human is shopping
        if self.shoppingTime != None and self.shoppingTime != False:
            # Checks for time spent shopping
            if self.shoppingTime > 0:
                self.shoppingTime -= self.timeStep
            # If time is longer than what is allowed return 
            else:
                self.shoppingTime = None
                self.endShopping()
    
        # Travel if Travelling
        if self.travelling:
            self.travel()
            return

        # WALL COLLISION DETECTION
        if self.position[0] + self.radius >= self.walls["x"] + self.walls["width"] or self.position[0] - self.radius <= self.walls["x"]:
            self.velocity[0] = -1*self.velocity[0]

            if self.position[0] + self.radius >= self.walls["x"] + self.walls["width"]:
                self.position[0] = self.walls["x"] + self.walls["width"] - self.radius
            if self.position[0] - self.radius <= self.walls["x"]:
                self.position[0] = self.walls["x"] + self.radius
        
        if self.position[1] + self.radius >= self.walls["y"] + self.walls["height"] or self.position[1] - self.radius <= self.walls["y"]:
            self.velocity[1] = -1*self.velocity[1]

            if self.position[1] + self.radius >= self.walls["y"] + self.walls["height"]:
                self.position[1] = self.walls["y"] + self.walls["height"] - self.radius
            if self.position[1] - self.radius <= self.walls["y"]:
                self.position[1] = self.walls["y"] + self.radius

        # NORMALIZING VELOCITY AND FORCE
        if np.dot(self.velocity, self.velocity) > self.speed*25.0*self.speed or np.dot(self.force, self.force) > self.speed*25.0*self.speed:
            if np.dot(self.force, self.force) != 0:    
                self.force = self.force*(self.speed*5.0/np.linalg.norm(self.force))
            self.velocity = self.velocity*(self.speed/np.linalg.norm(self.velocity))
        
        # UPDATING THE POSITION ACCORDING TO VERLET ALGORITHM
        self.position += self.velocity*self.timeStep + self.force*(self.timeStep**2)/2
        self.oldForce = self.force
        self.force = np.array([0.0, 0.0])

    def isInProximity(self, vector, IR):
        if np.dot(self.position - vector, self.position - vector) <= IR**2:
            return True
        return False

    def getInfected(self, time, asym):
        if self.travelling or self.status == "r" or self.status == "i":
            return False
        self.status = "i"
        self.infectedTime = time

        # a for asymptomatic
        if np.random.rand() < asym:
            self.asym = True
            self.a = "a"
        else:
            self.asym = False
        return True

    def recover(self, recoveryTime, time):
        if self.status != "i":
            return False
        if time - self.infectedTime >= recoveryTime:
            self.status = "r"
            self.asym = None
            return True
        return False  