from arena import Arena
from plot import Plot
import pygame
import numpy as np
from slider import Slider
from slider import Button

########################################## CONSTANTS ################################################

cityPopulation = 25
cities = []
numOfCities = 1
# Quarantine Exists or not
allowQuarantine = False
# Probability of travel
travellingProbability = 0
# Shopping Probabiltiy
shoppingProbability = 0.001
# Interval between each frame/update
timeStep = 0.045
# Percentage of social distancers
socialDistancing = 0 
# Infection probability
IP = 0.1      
# Infection radius       
IR = 20.0
# Time to recover (or die) after being infected
RecoveryTime = 10.0
# intertial speed of humans
speed = 10
# probability of being asymptomatic i.e : quarantine
asym = 0
# allows shopping
allowShop = False
cityWidth = 150
cityHeight = 150
qWidth = 50
qHeight = 50

########################################## HELPFUL FUNCTIONS #############################################

def updateShopping(state):
    global cities

    for city in cities:
        city.allowShopping = state

def updateQuarantine(state):
    global cities

    for city in cities:
        city.allowQuarantine = state

def updateSocialDest():
    global socialDistancing
    global cities

    for city in cities:
        for human in city.population:
            human.wSD = False
            if np.random.rand() < socialDistancing:
                human.wSD = True
           
def updateSpeed():
    global cities

    for city in cities:
        for human in city.population:
            human.speed = speed


def interCityTravel():
    global cities
    global travellingProbability
    global numOfCities
    global quarantine


    if numOfCities > 1 and np.random.rand() < travellingProbability:
        indices = [i for i in range(numOfCities)]
        depIndex = np.random.choice(indices)
        indices.remove(depIndex)
        destIndex = np.random.choice(indices)

        traveller = cities[depIndex].exportHuman(cities[destIndex].walls)
        if traveller != None:
            cities[destIndex].population.append(traveller)
            

def createCities():
    global cities
    global windowHeight 
    global windowWidth
    global cityHeight
    global cityWidth
    global gap
    global margin
    global numOfCities
    global plot
    global time
    global allowShop
    global allowQuarantine

    if numOfCities == 1:
        gap = 0
    else:
        gap = (windowHeight - 2*margin - numOfCities*cityHeight)/(numOfCities - 1)
    cities = []
    for i in range(0, numOfCities):
        y = i*(cityHeight + gap) + margin
        edges = {
            "x": windowWidth - cityWidth - margin,
            "y": y,
            "width": cityWidth,
            "height": cityHeight
        }

        city = Arena(edges, cityPopulation, 3, timeStep, speed, cutoff=IR, wSD = socialDistancing)
        if allowQuarantine:
            city.allowQuarantine = True
        if allowShop:
            city.allowShopping = True
        cities.append(city)
    plot = Plot([0], [numOfCities*cityPopulation - 1], [1], [0], [margin, margin], 300, 200)
    i = np.random.choice([x for x in range(numOfCities)])
    cities[i].population[0].getInfected(0, asym)
    time = 0


########################################## INITIALIZATIONS OF PYGAME #############################################
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)
pygame.display.set_caption('Epidemic Simulation')
logo = pygame.image.load('assets/virus.jpg')
pygame.display.set_icon(logo)

done = False
screen = pygame.display.set_mode((700, 700))
windowHeight = screen.get_height()
windowWidth = screen.get_width()
margin = 50
gap = 0

# Walls/location of quarintine area
quarantine = {
    "x": windowWidth - cityWidth - 2*margin - qWidth,
    "y": windowHeight - margin - qHeight,
    "width": qWidth,
    "height": qHeight
}

Quar = pygame.Rect(quarantine["x"], quarantine["y"], quarantine["width"], quarantine["height"])

# Create the cities
createCities()
slideWidth = 100

######################################### SLIDERS ######################################################

plot = Plot([0], [numOfCities*cityPopulation - 1], [1], [0], [margin, margin], 300, 200)
IPSlider = Slider([margin, 300], slideWidth, 8, "Infection Probability", (0.1, 1.0))
sdSlider = Slider([3*margin + slideWidth, 300], slideWidth, 8, "Social Distance Index")
asymSlider = Slider([margin, 400], slideWidth, 8, "Asymptotic Probability")
RTSlider = Slider([3*margin + slideWidth, 400], slideWidth, 8, "Recovery Time", (5.0, 10.0))
CTSlider = Slider([margin, 500], slideWidth, 8, "City Travel Index", (0, 0.1))
SpeedSlider = Slider([3*margin + slideWidth, 500], slideWidth, 8, "Speed/Temperature", (10.0, 20.0))
cityPopSlider = Slider([margin, 600], slideWidth, 8, "City Population", (25, 100), True)
NOCSlider = Slider([3*margin + slideWidth, 600], slideWidth, 8, "Number of cities", (1, 4), True)

########################################### BUTTONS ######################################################

allowShoppingButton = Button([2*margin, 680], 8, 'Allows Shopping')
quarantineButton = Button([2*margin + 180, 680], 8, 'Allows Quarentine')
resetButton = Button([2*margin + 350, 680], 8, 'Reset Simulation')




########################################## SIMULATION LOOP #####################################################

time = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            IPSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            sdSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            asymSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            RTSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            CTSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            SpeedSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            cityPopSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            NOCSlider.mouseOnball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            if allowShoppingButton.click(pygame.mouse.get_pos()) != None:
                allowShop = allowShoppingButton.on
                updateShopping(allowShoppingButton.on)

            if quarantineButton.click(pygame.mouse.get_pos()) != None:
                allowQuarantine = quarantineButton.on
                updateQuarantine(quarantineButton.on)
            if resetButton.click(pygame.mouse.get_pos()) != None:
                createCities()
        
        if event.type == pygame.MOUSEBUTTONUP:
            IPSlider.clicked = False
            sdSlider.clicked = False
            asymSlider.clicked = False
            RTSlider.clicked = False
            CTSlider.clicked = False
            SpeedSlider.clicked = False
            cityPopSlider.clicked = False
            NOCSlider.clicked = False
    
    screen.fill((255, 255, 255))
    susciptible = 0
    infected = 0
    recovered = 0
    for city in cities:
        city.update(screen, IP, RecoveryTime, timeStep, quarantine, shoppingProbability, asym)
        susciptible += city.susciptible
        infected += city.infected
        recovered += city.recovered
    time += timeStep

    if allowQuarantine:
        pygame.draw.rect(screen, (0, 0, 0), Quar, 2)
    # DRAW SLIDERS
    plot.update(time, susciptible, infected, recovered)
    plot.draw(screen, font)
    IPSlider.draw(screen, font)
    sdSlider.draw(screen, font)
    asymSlider.draw(screen, font)
    RTSlider.draw(screen, font)
    CTSlider.draw(screen, font)
    SpeedSlider.draw(screen, font)
    cityPopSlider.draw(screen, font)
    NOCSlider.draw(screen, font)

    # DRAW BUTTONS
    allowShoppingButton.draw(screen, font)
    quarantineButton.draw(screen, font)
    resetButton.draw(screen, font)

    # UPDATE SLIDERS AND CORRESPONDING VALUES
    if IPSlider.update(pygame.mouse.get_pos()[0]) != None:
        IP = IPSlider.update(pygame.mouse.get_pos()[0])

    if sdSlider.update(pygame.mouse.get_pos()[0]) != None:
        socialDistancing = sdSlider.update(pygame.mouse.get_pos()[0])
        updateSocialDest()

    if asymSlider.update(pygame.mouse.get_pos()[0]) != None:
        asym = asymSlider.update(pygame.mouse.get_pos()[0])

    if RTSlider.update(pygame.mouse.get_pos()[0]) != None:
        RecoveryTime = RTSlider.update(pygame.mouse.get_pos()[0])

    if CTSlider.update(pygame.mouse.get_pos()[0]) != None:
        travellingProbability = CTSlider.update(pygame.mouse.get_pos()[0])
    
    if SpeedSlider.update(pygame.mouse.get_pos()[0]) != None:
        speed = SpeedSlider.update(pygame.mouse.get_pos()[0])
    
    if cityPopSlider.update(pygame.mouse.get_pos()[0]) != None:
        cityPopulation = cityPopSlider.update(pygame.mouse.get_pos()[0])
        createCities()
    
    if NOCSlider.update(pygame.mouse.get_pos()[0]) != None:
        numOfCities = NOCSlider.update(pygame.mouse.get_pos()[0])
        createCities()

    interCityTravel()
    pygame.display.update()
pygame.quit()