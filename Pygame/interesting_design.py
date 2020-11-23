#you will need to install pygame of course
import pygame, random

#launch the pygame module
pygame.init()

# Set up the drawing window
size = (500,500)
screen = pygame.display.set_mode(size)

# Run until the user asks to quit
running = True
snow_count = 0
color_count = 0

# Colors (r,g,b)
colors = {'white': (255,255,255), 'black': (0,0,0), 'red': (255,0,0), 'green': (0,255,0), 'pine': (50, 125, 50), 'blue': (0,0,255), 'yellow': (255,255,0), 'magenta': (255,0,255), 'cyan': (0,255,255), 'brown': (120,60,30), 'orange': (255,150,0)}
ornament_list = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta']

# Tree setup
tree_triangles = [[(250,50),(150,150),(350,150)],[(250,100),(125,225),(375,225)],[(250,150),(100,300),(400,300)],[(250,200),(75,375),(425,375)],[(250,250),(50,450),(450,450)]]
ornament_centers_bottom = [[(80,440),0],[(105, 430),1],[(130,420),2],[(155,410),3],[(180,400),4],[(205,390),5],[(230,380),6],[(255,370),7],[(280,360),8],[(305,350),9],[(330,340),10],[(355,330),11]]
ornament_centers_mid = [[(135,285),7],[(160, 275),8],[(185,265),9],[(210,255),10],[(235,245),11],[(260,235),12],[(285,225),13],[(310,215),14],[(335,205),15]]
ornament_centers_top = [[(180,140),1],[(205, 130),2],[(230,120),3],[(255,110),4],[(280,100),5]]

# snow setup
class Snowflake:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.change_x = random.randint(1,4)
        self.change_y = random.randint(1,3)
    def move_snowflake(self):
        self.change_x *= -1
        self.pos_x += self.change_x
        self.pos_y += self.change_y
    def draw_snowflake(self, x,y):
        pygame.draw.circle(screen, colors['white'], (x,y), 1)
snowflakes = []

while running:
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    # screen.fill((225,245,255))
    screen.fill(colors['black'])

    if snow_count%10 == 0:
        snowflakes.append(Snowflake(((snow_count * 19)%500),0))
    for snowflake in snowflakes:
        snowflake.move_snowflake()
        snowflake.draw_snowflake(snowflake.pos_x, snowflake.pos_y)

    # Drawing Tree
    pygame.draw.rect(screen, colors['brown'], [230, 450, 40, 50])
    for triangle in tree_triangles:
        pygame.draw.polygon(screen, colors['pine'], triangle)

    # Draw Star
    pygame.draw.polygon(screen, colors['yellow'], [(250,15),(260,35),(285,35),(265,50),(275,75),(250,60),(225,75),(235,50),(215,35),(240,35)])

    # Draw Ornaments
    for center in ornament_centers_bottom:
        pygame.draw.circle(screen, colors[ornament_list[(color_count+center[1])%len(ornament_list)]], center[0], 10)
    for center in ornament_centers_mid:
        pygame.draw.circle(screen, colors[ornament_list[(color_count+center[1])%len(ornament_list)]], center[0], 10)
    for center in ornament_centers_top:
        pygame.draw.circle(screen, colors[ornament_list[(color_count+center[1])%len(ornament_list)]], center[0], 10)

    # Pause
    pygame.display.flip()
    pygame.time.wait(100)

    # Increase count
    snow_count += 1
    if snow_count%5 == 0:
        color_count += 1

# Done! Time to quit.
pygame.quit()