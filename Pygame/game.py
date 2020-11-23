
#you will need to install pygame of course

import pygame

#launch the pygame module

pygame.init()

# Set up the drawing window

size = (500,500)
screen = pygame.display.set_mode(size)

# Run until the user asks to quit

running = True

while running:

# Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    # Fill the background with white

    screen.fill((255, 255, 255))


    # Draw a solid blue circle in the center

    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)


    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()
