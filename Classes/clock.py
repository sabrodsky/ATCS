#for this project, i'm making a clock that displays correct time
#for now, the hour hand is broken and i'm working on making the movement more fluid

#you will need to install pygame of course
import pygame, math, datetime

#launch the pygame module
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
    def __init__(self, x, y, hours):
        self.x = x
        self.y = y
        self.pos = hours
    def move(self, seconds):
        if int(seconds - 60-current_time.second)%60 == 0:
            self.pos += 1/60
    def show(self, seconds):
        self.move(seconds)
        pygame.draw.line(screen, (0,0,255), (self.x, self.y), (self.x+125*math.cos(2*math.pi*(self.pos/360)), self.y+125*math.sin(2*math.pi*(self.pos/360))), 5)
hour_hand = Hour(window_x/2, window_y/2, (current_time.hour + (-5))%12)

#minute hand
class Minute:
    def __init__(self, x, y, minutes):
        self.x = x
        self.y = y
        self.pos = minutes - 15
        self.offset = 59 - current_time.second #makes sure the minute hand only updates when second hand is at 12
    def move(self, seconds):
        if int(seconds - self.offset)%60 == 0: #only happens if second hand is at 12
            self.pos += 1
    def show(self, seconds):
        self.move(seconds)
        pygame.draw.line(screen, (0,255,0), (self.x, self.y), (self.x+175*math.cos(2*math.pi*(self.pos/60)), self.y+175*math.sin(2*math.pi*(self.pos/60))), 5)
minute_hand = Minute(window_x/2, window_y/2, current_time.minute)

#second hand
class Second:
    def __init__(self, x, y, seconds):
        self.x = x
        self.y = y
        self.pos = seconds - 15
    def move(self):
        self.pos += 1
    def show(self):
        self.move()
        # pygame.draw.circle(screen, (0,255,255), (self.x + 200*math.cos(2*math.pi*(self.pos/60)), self.y + 200*math.sin(2*math.pi*(self.pos/60))), 5)
        pygame.draw.line(screen, (255,0,0), (self.x, self.y), (self.x+190*math.cos(2*math.pi*(self.pos/60)), self.y+190*math.sin(2*math.pi*(self.pos/60))), 5)
second_hand = Second(window_x/2, window_y/2, current_time.second)

while running:
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # if seconds >= 60:
    #     running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # dots for the numbers on the clock (couldn't figure out text)
    for x in range(60):
        if x%5 == 0:
            pygame.draw.line(screen, (0,0,0), (250 + 160*math.cos(2*math.pi*(x/60)), 250 + 160*math.sin(2*math.pi*(x/60))), (250 + 180*math.cos(2*math.pi*(x/60)), 250 + 180*math.sin(2*math.pi*(x/60))), 6)
        else:
            pygame.draw.circle(screen, (0,0,0), (250 + 180*math.cos(2*math.pi*(x/60)), 250 + 180*math.sin(2*math.pi*(x/60))), 3)

    # Draw outline of clock
    pygame.draw.circle(screen, (0,0,0), (window_x/2, window_y/2), 200, 5)
    pygame.draw.circle(screen, (0,0,0), (window_x/2,window_y/2), 5)

    hour_hand.show(seconds)
    minute_hand.show(seconds)
    second_hand.show()

    # Flip the display
    pygame.display.flip()

    #small increments to make motion more fluid
    pygame.time.delay(1000)
    seconds += 1

# Done! Time to quit.
pygame.quit()