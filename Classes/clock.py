#for this project, i'm making a clock

#you will need to install pygame of course
import pygame, math

#launch the pygame module
pygame.init()

# Set up the drawing window
window_x, window_y = 500,500
screen = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption('Clock Program')

# Run until the user asks to quit
running = True
seconds = 45 #the second hand starts at the top

#hour hand
class Hour:
    def __init__(self):
        pass
    def move(self):
        pass
    def show(self):
        self.move()
        pass
hour_hand = Hour()

#minute hand
class Minute:
    def __init__(self):
        pass
    def move(self):
        pass
    def show(self):
        self.move()
        pass
minute_hand = Minute()

#second hand
class Second:
    def __init__(self, x, y, seconds):
        self.x = x
        self.y = y
        self.pos = seconds%60
        self.change = 0.05
    def move(self):
        self.pos += self.change
    def show(self):
        self.move()
        # pygame.draw.circle(screen, (0,255,255), (self.x + 200*math.cos(2*math.pi*(self.pos/60)), self.y + 200*math.sin(2*math.pi*(self.pos/60))), 5)
        pygame.draw.line(screen, (255,0,0), (self.x, self.y), (self.x+200*math.cos(2*math.pi*(self.pos/60)), self.y+200*math.sin(2*math.pi*(self.pos/60))), 5)
second_hand = Second(window_x/2, window_y/2, seconds)

while running:
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if seconds >= 60:
        running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw outline of clock
    pygame.draw.circle(screen, (0,0,0), (window_x/2, window_y/2), 200, 5)
    pygame.draw.circle(screen, (0,0,0), (window_x/2,window_y/2), 5)

    # hour_hand.show()
    # minute_hand.show()
    second_hand.show()

#just some calculations
# in radians
# x = originx + r * cos(a)
# y = originy + r * sin(a)

    # Flip the display
    pygame.display.flip()

    #small increments to make motion more fluid
    pygame.time.delay(50)
    seconds += 0.05

# Done! Time to quit.
pygame.quit()