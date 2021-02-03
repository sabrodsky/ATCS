#you will need to install pygame of course
import pygame, random, colorsys

#launch the pygame module
pygame.init()

# Set up the drawing window
window_x, window_y = 1000,700
screen = pygame.display.set_mode((window_x,window_y))

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

class Ball:
    def __init__(self, r,g,b):
        self.pos_x = 10
        self.pos_y = 10
        # self.change_x = random.randint(1, 10)
        # self.change_y = random.randint(1, 10)
        self.change_x = 0.5
        self.change_y = 0.5
        self.radius = 10
        self.color = hsv2rgb(r,g,b)
    def move(self):
        self.pos_x += self.change_x
        self.pos_y += self.change_y
        if self.pos_x + self.radius >= window_x or self.pos_x - self.radius <= 0: self.change_x *= -1
        if self.pos_y + self.radius >= window_y or self.pos_y - self.radius <= 0: self.change_y *= -1
    # def color(self):

    def show(self):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)
balls = []

# Run until the user asks to quit
running = True
count = 0

while running:
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    if count%10 == 0:
        balls.append(Ball(count/200,1,1))
    for ball in balls:
        ball.move()
        ball.show()
    
    # if len(balls) >= 300:
    #     balls.pop(0)

    # Flip the display
    pygame.display.flip()
    # pygame.time.wait(5)
    count += 1

# Done! Time to quit.
pygame.quit()