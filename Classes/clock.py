#for this project, i'm making a clock that displays correct time

#note: sometimes the seconds are off because of delays in getting actual
#time and then showing the clock... so it may be incorrect by a second or two

import pygame, math, datetime
pygame.init()

# Set up the drawing window
window_x, window_y = 500,500
screen = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption('Clock Program')

# Run until the user asks to quit
running = True
seconds = 0
current_time = datetime.datetime.now() #get current time

#hour hand
class Hour:
    def __init__(self, x, y, hours, mins):
        self.x = x
        self.y = y
        self.pos = hours + (mins/60)
    def move(self, seconds):
        self.pos += 1/1440
    def show(self):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x + 100*math.cos(2*math.pi*(self.pos/12)), self.y + 100*math.sin(2*math.pi*(self.pos/12))), 5)

#minute hand
class Minute:
    def __init__(self, x, y, minutes):
        self.x = x
        self.y = y
        self.pos = minutes - 15
    def move(self, seconds):
        self.pos += 0.05
    def show(self):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x+150*math.cos(2*math.pi*(self.pos/60)), self.y+150*math.sin(2*math.pi*(self.pos/60))), 5)

#second hand
class Second:
    def __init__(self, x, y, seconds):
        self.x = x
        self.y = y
        self.pos = seconds - 15
    def move(self):
        self.pos += 0.05
    def show(self):
        self.move()
        # pygame.draw.circle(screen, (0,255,255), (self.x + 200*math.cos(2*math.pi*(self.pos/60)), self.y + 200*math.sin(2*math.pi*(self.pos/60))), 5)
        pygame.draw.line(screen, (255,0,0), (self.x, self.y), (self.x+190*math.cos(2*math.pi*(self.pos/60)), self.y+190*math.sin(2*math.pi*(self.pos/60))), 5)

class Clock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.second_hand = Second(window_x/2, window_y/2, current_time.second)
        self.minute_hand = Minute(window_x/2, window_y/2, current_time.minute)
        self.hour_hand = Hour(window_x/2, window_y/2, (current_time.hour - 3)%12, current_time.minute)
    def move(self, seconds):
        self.minute_hand.move(seconds)
        self.hour_hand.move(seconds)
    def show(self):
        #actual clock:
        for x in range(60):
            if x%5 == 0:
                pygame.draw.line(screen, (0,0,0), (250 + 160*math.cos(2*math.pi*(x/60)), 250 + 160*math.sin(2*math.pi*(x/60))), (250 + 180*math.cos(2*math.pi*(x/60)), 250 + 180*math.sin(2*math.pi*(x/60))), 5)
            else:
                pygame.draw.circle(screen, (0,0,0), (250 + 180*math.cos(2*math.pi*(x/60)), 250 + 180*math.sin(2*math.pi*(x/60))), 3)
        pygame.draw.circle(screen, (0,0,0), (window_x/2, window_y/2), 200, 5)
        pygame.draw.circle(screen, (0,0,0), (window_x/2,window_y/2), 5)
        #hour hand:
        self.hour_hand.show()
        #minute hand:
        self.minute_hand.show()
        #second hand:
        self.second_hand.show()
clock = Clock(window_x/2, window_y/2)

while running:
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    #display the clock
    if int(seconds)%60 == (59 - current_time.second):
        clock.move(seconds)
    clock.show()

    # Flip the display
    pygame.display.flip()

    #small increments to make motion more fluid
    pygame.time.delay(49) #hoped to fix the time error...
    seconds += 0.05

# Done! Time to quit.
pygame.quit()