#
# Pygame full camera example
# Part of the pygame_examples library
#  -- github.com/rik-cross/pygame_examples
#
# Image credit - Cup Nooble
#  -- cupnooble.itch.io/sprout-lands-asset-pack
#

#
# Features:
#  -- Zoom
#  -- Lazy follow
#  -- Clamp to map
#

import pygame
import os

# initialise Pygame
pygame.init()

screen_size = (680, 460)

# setup screen to required size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Full camera example with controls')
clock = pygame.time.Clock()

# create a player character to move and track
character = pygame.sprite.Sprite()
character.image = pygame.image.load(os.path.join('images', 'character.png'))
character.position = (50, 50)
character.size = (36, 48)

map = pygame.image.load(os.path.join('images', 'grass.png'))
mapPosition = (0, 0)
mapSize = (256, 256)

cameraPosition = (50, 50)
cameraSize = (360, 360)
# the camera center = the position + half the size
cameraCenter = (cameraPosition[0] + cameraSize[0] / 2,
                cameraPosition[1] + cameraSize[1] / 2)
cameraZoom = 3
# set a minimim zoom, based on the largest map dimension
if mapSize[0] > mapSize[1]:
    minZoom = cameraSize[0] / mapSize[0]
else:
    minZoom = cameraSize[1] / mapSize[1]

# the target for the camera
cameraWorldTarget = (character.position[0] + character.size[0] / 2,
                     character.position[1] + character.size[1] / 2)

# the current calculated target (for lazy follow)
currentTarget = cameraWorldTarget

# game loop
running = True
while running:

    # advance clock at 60 FPS
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # arrow keys to move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.position = (character.position[0] - 1, character.position[1])
    if keys[pygame.K_RIGHT]:
        character.position = (character.position[0] + 1, character.position[1])
    if keys[pygame.K_UP]:
        character.position = (character.position[0], character.position[1] - 1)
    if keys[pygame.K_DOWN]:
        character.position = (character.position[0], character.position[1] + 1)

    # z and x to zoom
    if keys[pygame.K_z]:
        # don't go below minimum zoom level
        cameraZoom = max(cameraZoom - 0.05, minZoom)
    if keys[pygame.K_x]:
        cameraZoom += 0.05

    # 'cameraWorldTarget' is the point in the game world
    # that the camera is focused on.
    # In this case, the center of the camera is focused
    # on the center of the player
    cameraWorldTarget = (character.position[0] + character.size[0] / 2,
                         character.position[1] + character.size[1] / 2)

    # the current position is calculated as 95% of the current position
    # and just 5% movement towards the target position (per frame)
    # this results in a 'lazy follow'
    currentTarget = (currentTarget[0] * 0.95 + cameraWorldTarget[0] * 0.05,
                     currentTarget[1] * 0.95 + cameraWorldTarget[1] * 0.05)

    # the camera target needs to be adjusted
    # to account for the zoom factor
    adjustedTarget = (currentTarget[0] * cameraZoom,
                      currentTarget[1] * cameraZoom)

    # clamp the camera to the bounds of the map
    adjustedTarget = (
        max(min(adjustedTarget[0], mapSize[0] * cameraZoom-cameraSize[0]/2), mapPosition[0] * cameraZoom + cameraSize[0]/2),
        max(min(adjustedTarget[1], mapSize[1] * cameraZoom-cameraSize[1]/2), mapPosition[1] * cameraZoom + cameraSize[1]/2)
    )

    # the overall offset for each game object is
    # the camera screen center point - the adjusted target
    cameraScreenOffset = (cameraCenter[0] - adjustedTarget[0],
                          cameraCenter[1] - adjustedTarget[1])

    # the character also needs to be adjusted
    # to account for the camera zoom
    adjustedChar = (character.position[0] * cameraZoom,
                    character.position[1] * cameraZoom)

    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')

    # clip the drawing area to the camera
    screen.set_clip((cameraPosition[0], cameraPosition[1],
                     cameraSize[0], cameraSize[1]))

    # draw camera background
    # (no need to worry about the camera size as the drawing area is clipped)
    screen.fill('gray10')

    # draw a map
    screen.blit(
        # scale the image
        pygame.transform.scale(map, (mapSize[0] * cameraZoom,
                                     mapSize[1] * cameraZoom)), 
        # position the image
        (cameraScreenOffset[0] + mapPosition[0] * cameraZoom,
         cameraScreenOffset[1] + mapPosition[1] * cameraZoom))

    # draw the character
    screen.blit(
        # scale the image
        pygame.transform.scale(character.image, (character.size[0] * cameraZoom,
                                                 character.size[1] * cameraZoom)), 
        # position the image
        (cameraScreenOffset[0] + adjustedChar[0],
         cameraScreenOffset[1] + adjustedChar[1]))

    # reset screen clip
    screen.set_clip()

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
