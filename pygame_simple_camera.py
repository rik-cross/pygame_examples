#
# Pygame simple camera example
# Part of the pygame_examples library
#  -- github.com/rik-cross/pygame_examples
#
# Image credit - Cup Nooble
#  -- cupnooble.itch.io/sprout-lands-asset-pack
#

#
# This simple example assumes that the camera is the
# full size of the screen. The 'full camera' example covers
# camera size, position, zoom, lazy follow and clamping
#

import pygame
import os

# initialise Pygame
pygame.init()

screen_size = (680, 460)

# setup screen to required size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Simple camera example')
clock = pygame.time.Clock()

character = pygame.sprite.Sprite()
character.image = pygame.image.load(os.path.join('images', 'character.png'))
character.position = (100, 100)
character.size = (36, 48)

# the center of the camera is the center of the screen
screenCenter = (screen_size[0] / 2, screen_size[1] / 2)

# game loop
running = True
while running:

    # advance clock at 60 FPS
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # camera is focused on the center of the player
    cameraTarget = (character.position[0] + character.size[0] / 2,
                    character.position[1] + character.size[1] / 2)

    # camera offset = camera center - camera target
    cameraOffset = (screenCenter[0] - cameraTarget[0],
                    screenCenter[1] - cameraTarget[1])
    
    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
    
    # player position doesn't change, instead the offset is added to the position
    screen.blit(character.image, (cameraOffset[0] + character.position[0], 
                                  cameraOffset[1] + character.position[1]))

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
