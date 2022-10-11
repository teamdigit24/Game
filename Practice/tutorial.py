# import the pygame module, so you can use it
import pygame
import time

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("UK_logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Game Test")
     
    # create a surface on screen that has the size of 1600 x 900
    screen = pygame.display.set_mode((1500, 800))

    title_screen(screen)

    # Filling the background with a solid color
    #screen.fill('blue')

    # Setting background image
    bg = pygame.image.load("circuit_bg.png")
    screen.blit(bg, (0, 0))

    # Loading image     
    image = pygame.image.load("DIGIT_logo.png")
    # Setting image transparency
    image.set_alpha(128)

    # Drawing the image (surface object) onto the screen (surface object)
    screen.blit(image, (50, 50))

    # Update full display surface
    pygame.display.flip()

    # define a variable to control the main loop
    running = True
    
    # define the position of the image
    xpos = 50
    ypos = 50
    # how many pixels we move our image each frame
    step_x = 2
    step_y = 2

    # main loop
    while running:

        # check if the image is still on screen, if not change direction
        if xpos>1500-200 or xpos<0:
            step_x = -step_x
        if ypos>800-200 or ypos<0:
            step_y = -step_y
        # update the position of the image
        xpos += step_x # move it to the right
        ypos += step_y # move it down

        # first erase the screen 
        #(just blit the background over anything on screen)
        screen.blit(bg, (0,0))
        # now blit the smiley on screen
        screen.blit(image, (xpos, ypos))
        # and update the screen (don't forget that!)
        pygame.display.flip()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     

def title_screen(screen):
    
    # Filling the background with a solid color
    screen.fill('blue')
    
    # Updating the full display surface
    pygame.display.flip()

    for i in range(5):
        time.sleep(1)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()