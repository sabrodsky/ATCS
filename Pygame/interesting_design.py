# you will need to install pygame of course
import pygame, random

#launch the pygame module
pygame.init()

# Set up the drawing window (every aspect changes dynamically so you can easily change window size)
window_x, window_y = 500,500
screen = pygame.display.set_mode((window_x,window_y))

# Run until the user asks to quit
running = True
snow_count = 0
color_count = 0

# Colors (r,g,b)
colors = {'white': (255,255,255), 'black': (0,0,0), 'red': (255,0,0), 'green': (0,255,0), 'pine': (50, 125, 50), 'blue': (0,0,255), 'yellow': (255,255,0), 'magenta': (255,0,255), 'cyan': (0,255,255), 'brown': (120,60,30), 'orange': (255,150,0)}
ornament_list = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta']

# Ratio (it's 500 by 500 because that was the window size that I had originally used to calculate everything)
x_ratio, y_ratio = (window_x/500), (window_y/500)

# snow setup
class Snowflake:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.change_x = random.randint(1,4)
        self.change_y = random.randint(1,5)
    def move_snowflake(self):
        self.change_x *= -1
        self.pos_x += self.change_x
        self.pos_y += self.change_y
    def draw_snowflake(self, x,y):
        pygame.draw.circle(screen, colors['white'], (x,y), 1)
snowflakes_behind = []
snowflakes_front = []

while running:
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(colors['black'])

    #add snowflakes to list
    if snow_count%7 == 0:
        snowflakes_behind.append(Snowflake(random.randint(5, (window_x-5)),0))
        snowflakes_front.append(Snowflake(random.randint(5, (window_x-5)),0))
    #move and draw snowflakes
    for snowflake in snowflakes_behind:
        snowflake.move_snowflake()
        if snowflake.pos_y >= (window_y + 5):
            snowflakes_behind.remove(snowflake)
        else:
            snowflake.draw_snowflake(snowflake.pos_x, snowflake.pos_y)

    # Drawing Tree
    pygame.draw.rect(screen, colors['brown'], [230*x_ratio, 450*y_ratio, 40*x_ratio, 50*y_ratio])
    for x in range(5):
        pygame.draw.polygon(screen, colors['pine'], [(250*x_ratio, (50*y_ratio)+(x*50*y_ratio)),((150*x_ratio)-(x*25*x_ratio),(150*y_ratio)+(x*75*y_ratio)),((350*x_ratio)+(x*25*x_ratio),(150*y_ratio)+(x*75*y_ratio))])

    # Draw Star
    pygame.draw.polygon(screen, colors['yellow'], [(250*x_ratio,15*y_ratio),(260*x_ratio,35*y_ratio),(285*x_ratio,35*y_ratio),(265*x_ratio,50*y_ratio),(275*x_ratio,75*y_ratio),(250*x_ratio,60*y_ratio),(225*x_ratio,75*y_ratio),(235*x_ratio,50*y_ratio),(215*x_ratio,35*y_ratio),(240*x_ratio,35*y_ratio)])

    # Draw Ornaments
    for x in range(5): #top row
        pygame.draw.circle(screen, colors[ornament_list[(color_count+x+12)%len(ornament_list)]], ((180*x_ratio)+(x*(25*x_ratio)),(138*y_ratio)-(x*(10*y_ratio))), 10)
    for x in range(9): #mid row
        pygame.draw.circle(screen, colors[ornament_list[(color_count+x+5)%len(ornament_list)]], ((135*x_ratio)+(x*(25*x_ratio)),(285*y_ratio)-(x*(10*y_ratio))), 10)
    for x in range(12): #bottom row
        pygame.draw.circle(screen, colors[ornament_list[(color_count+x+5)%len(ornament_list)]], ((80*x_ratio)+(x*(25*x_ratio)),(438*y_ratio)-(x*(10*y_ratio))), 10)

    #move and draw snowflakes
    for snowflake in snowflakes_front:
        snowflake.move_snowflake()
        if snowflake.pos_y >= (window_y + 5):
            snowflakes_front.remove(snowflake)
        else:
            snowflake.draw_snowflake(snowflake.pos_x, snowflake.pos_y)

    # Pause
    pygame.display.flip()
    pygame.time.wait(100)

    # Increase count
    snow_count += 1
    if snow_count%5 == 0:
        color_count += 1

# Done! Time to quit.
pygame.quit()