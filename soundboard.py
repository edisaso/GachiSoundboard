import pygame
from pygame.locals import *

# variables
size = [500, 500]
rows = 4  # 10 max
spacing = int(size[0]/(1+2*rows))
fadein = 1000
fadeout = 3000
offset12 = spacing + 12
leftB = 1
rightB = 3

# colors
red = (237, 85, 101)
orange = (252, 110, 81)
yellow = (255, 206, 84)
yellow2 = (246, 187, 66)
green = (160, 212, 104)
green2 = (140, 193, 82)
turquoise = (72, 207, 173)
blue = (79, 193, 233)
purple = (93, 156, 236)
black = (0, 0, 0)
white = (255, 255, 255)
dark = (30, 30, 30)
grey = (150, 150, 150)
grey2 = (20, 20, 20)

# initialize game engine
pygame.mixer.pre_init(44100, -16, 2, 512)  # fixes delay in play
pygame.init()

# init channels
pygame.mixer.set_num_channels(rows**2)

# set screen width/height and caption
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption('GachiSoundBoard')

# init fonts
fontLogo = pygame.font.Font('res/Kathen.otf', int(spacing/2))
fontObj = pygame.font.Font('res/Hyperspace.otf', int(spacing/2.5))
fontnames = pygame.font.Font('res/pragmata.otf', 12)


def readpaths():
    '''read rows**2 lines from paths.txt file
    and create a list of paths'''
    paths = []
    with open("paths.txt") as myfile:
        paths = [next(myfile) for x in range(rows**2)]
    # remove white space
    paths = [line.rstrip('\n') for line in paths]
    return paths


def makebuttons():
    '''generate sound button objects according to the number of
    rows'''
    data = []
    n = 0
    for j in range(rows):
        for i in range(rows):
            data.append({
                'soundchannel': pygame.mixer.Channel(n),
                'soundobj': pygame.mixer.Sound(paths[n]),
                'coord': (spacing*(2*i+1), spacing*(2*j+1)),
                'size': (spacing, spacing),
                'path': paths[n],
                'rectobj': pygame.Rect(spacing*(2*i+1), spacing*(2*j+1), spacing, spacing),
                'textobj': fontObj.render(str(n+1), False, black),
                'textname': fontnames.render(paths[n][7:][:-4].upper(), True, white),
                'textcoords': (spacing*(2*i+1.3), spacing*(2*j+1.3)),
                'namecoords': (spacing*(2*i+1), spacing*(2*j+2.2)),
                'color': grey,
                'loop': False
            })
            n += 1
    return data


def makelogo():
    # draw logo according to the size of the buttons
    logo = fontLogo.render('GachiSoundboard', True, blue)
    logoRect = logo.get_rect()
    logoRect.midright = (spacing*(2*rows), spacing/2)
    return (logo, logoRect)


# make the initial set of objects
paths = readpaths()
data = makebuttons()
logo = makelogo()

# initialize clock. used later in the loop.
clock = pygame.time.Clock()

paused = False

# Loop until the user clicks close button
done = False
while done == False:
    # clear the screen before drawing
    screen.fill(black)
    # draw border
    pygame.draw.rect(screen, grey2, (0, 0, size[0], size[1]), 1)
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == K_f:
                pygame.mixer.fadeout(3000)
            elif event.key == K_p:
                if paused == False:
                    pygame.mixer.pause()
                    paused = True
                else:
                    pygame.mixer.unpause()
                    paused = False
            elif event.key == K_s:
                pygame.mixer.stop()
            elif event.key == K_r:
                paths = readpaths()
                data = makebuttons()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == leftB:
            pos = pygame.mouse.get_pos()
            for elem in data:
                if elem['rectobj'].collidepoint(pos):
                    if elem['soundchannel'].get_busy():
                        elem['soundchannel'].stop()
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, offset12, offset12), 5)
                    else:
                        elem['soundchannel'].play(elem['soundobj'])
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, offset12, offset12), 5)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == rightB:
            pos = pygame.mouse.get_pos()
            for elem in data:
                if elem['rectobj'].collidepoint(pos):
                    if elem['soundchannel'].get_busy():
                        elem['soundchannel'].fadeout(fadeout)
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, offset12, offset12), 5)
                    else:
                        elem['soundchannel'].play(
                            elem['soundobj'], fade_ms=fadein)
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, offset12, offset12), 5)
    # write game logic here
    pos = pygame.mouse.get_pos()
    for elem in data:
        if elem['soundchannel'].get_busy():
            elem['color'] = yellow
        else:
            if elem['path'] == 'sounds/fallback.wav':
                elem['color'] = grey
            else:
                elem['color'] = green
        if elem['rectobj'].collidepoint(pos):
            pygame.draw.rect(screen, orange, (elem['coord'][0]-6,
                                              elem['coord'][1]-6, offset12, offset12), 1)
    # write draw code here
    screen.blit(logo[0], logo[1])
    for elem in data:
        pygame.draw.rect(screen, elem['color'], elem['rectobj'])
        screen.blit(elem['textobj'], elem['textcoords'])
        screen.blit(elem['textname'], elem['namecoords'])

    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()
