import pygame
from math import ceil
from math import trunc

class Button:
    def __init__(self, position, radius, title):
        self.position = position
        self.radius = radius
        self.title = title
        self.color = (255, 0, 0)
        self.on = False
    
    def draw(self, screen, font):
        text = font.render(self.title, False, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.position[0], self.position[1] - 20)
        pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.radius)
        screen.blit(text, textRect)

    def click(self, pos):
        if pos[0] < self.position[0] + self.radius and pos[0] > self.position[0] - self.radius and pos[1] < self.position[1] + self.radius and pos[1] > self.position[1] - self.radius:
            if self.on:
                self.on = False
                self.color = (255, 0, 0)
                return False
            else:
                self.on = True
                self.color = (0, 255, 0)
                return True
        return None




class Slider:
    def __init__(self, position, width, radius, title, scale = (0, 1), round = False):
        self.position = position
        self.width = width
        self.radius = radius
        self.ballX = self.position[0]
        self.clicked = False
        self.title = title
        self.scale = scale
        self.round = round

    def draw(self, screen, font):
        body = pygame.Rect(self.position[0], self.position[1], self.width, 1)

        text = font.render(self.title, False, (0, 0, 0))
        textRect = text.get_rect()

        zero = font.render(str(self.scale[0]), False, (0, 0, 0))
        one = font.render(str(self.scale[1]), False,  (0, 0, 0))

        zeroRect = zero.get_rect()
        oneRect = one.get_rect()

        zeroRect.center = (self.position[0], self.position[1] + 20)
        oneRect.center = (self.position[0] + self.width, self.position[1] + 20)
        textRect.center = (self.position[0] + self.width / 2, self.position[1] - 20)

        screen.blit(zero, zeroRect)
        screen.blit(one, oneRect)
        screen.blit(text, textRect)

        pygame.draw.rect(screen, (0, 0, 0), body)
        pygame.draw.circle(screen, (0, 0, 255), (self.ballX, self.position[1]), self.radius)


    def mouseOnball(self, x, y):
        if x > self.ballX - self.radius and x < self.ballX + self.radius and y < self.position[1] + self.radius and y > self.position[1] - self.radius:
            self.clicked = True
            return True
        return False

    def update(self, x):
        if self.clicked == False:
            return None 

        if x >= self.position[0] + self.width:
            self.ballX = self.position[0] + self.width
            return self.scale[1]
        
        if x <= self.position[0]:
            self.ballX = self.position[0]
            return self.scale[0]
        
        self.ballX = x
        value = ((x - self.position[0])/(self.width))*self.scale[1] + self.scale[0]
        if self.round:
            value = trunc(value)
        return value

        

