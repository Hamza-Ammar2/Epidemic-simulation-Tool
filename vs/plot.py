import pygame

class Plot:
    def __init__(self, times, susciptible, infected, recovered, position, width, height):
        self.times = times
        self.susciptible = susciptible
        self.infected = infected
        self.recovered = recovered
        self.population = self.susciptible[0] + self.infected[0] + self.recovered[0]
        self.height = (height)
        self.width = (width)
        self.position = position
        self.ratioH = self.height/(self.susciptible[0] + self.infected[0] + self.recovered[0])

    def drawLegend(self, screen, font):
        s = font.render('Susciptible', False, (0, 0, 0))
        sRect = s.get_rect()

        i = font.render('Infected', False, (0, 0, 0))
        iRect = i.get_rect()

        r = font.render('Recovered', False, (0, 0, 0))
        rRect = r.get_rect()

        blue = pygame.Rect(self.position[0] + self.width + 40, self.position[1] + 30, 20, 20)
        red = pygame.Rect(self.position[0] + self.width + 40, self.position[1] + 70, 20, 20)
        black = pygame.Rect(self.position[0] + self.width + 40, self.position[1] + 110, 20, 20)

        sRect.center = (self.position[0] + self.width + 50, self.position[1] + 20)
        iRect.center = (self.position[0] + self.width + 50, self.position[1] + 60)
        rRect.center = (self.position[0] + self.width + 50, self.position[1] + 100)

        pygame.draw.rect(screen, (0, 0, 255), blue)
        screen.blit(s, sRect)

        pygame.draw.rect(screen, (255, 0, 0), red)
        screen.blit(i, iRect)

        pygame.draw.rect(screen, (0, 0, 0), black)
        screen.blit(r, rRect)

    
    def draw(self, screen, font):
        self.drawLegend(screen, font)
        rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 255), rect)
        
        width = (self.width/(max(len(self.recovered), len(self.infected))))

        for i in range(0, len(self.infected)):
            x = self.position[0] + self.width - (len(self.infected) - i)*width
            y = self.position[1] + self.height - self.infected[i]*self.ratioH

            valueRect = pygame.Rect(x, y, width, self.infected[i]*self.ratioH)
            pygame.draw.rect(screen, (255, 0, 0), valueRect)
        
        for i in range(0, len(self.recovered)):
            x = self.position[0] + self.width - (len(self.recovered) - i)*width
            y = self.position[1]

            valueRect = pygame.Rect(x, y, width, self.recovered[i]*self.ratioH)
            pygame.draw.rect(screen, (0, 0, 0), valueRect)
        
    def update(self, times, susciptible, infected, recovered):
        self.times.append(times)
        self.susciptible.append(susciptible)

        if infected != self.infected[len(self.infected) - 1]:
            self.infected.append(infected)
        if recovered != self.recovered[len(self.recovered) - 1]:
            self.recovered.append(recovered)