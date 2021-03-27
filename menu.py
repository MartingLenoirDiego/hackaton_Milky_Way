
import pygame
import random
pygame.init()
black = [0, 0, 0]
white = [255, 255, 255]
size = [600, 400]
scr = pygame.display.set_mode(size)
pygame.display.set_caption("Snow Animation")
dImg = pygame.image.load('space.png')
snow_list = []
for i in range(50):
    x = random.randrange(0, 700)
    y = random.randrange(0, 600)
    snow_list.append([x, y])
clock = pygame.time.Clock()
done = False
while not done:
    scr.blit(dImg,(0,0))
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = True  
    for i in range(len(snow_list)):
        pygame.draw.circle(scr, white, snow_list[i], 2)
        snow_list[i][1] += 1
        if snow_list[i][1] > 400:
            y = random.randrange(-50, -10)
            snow_list[i][1] = y
            x = random.randrange(0, 400)
            snow_list[i][0] = x
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
"""


import pygame
import sys
pygame.init()
fps=30
fpsclock=pygame.time.Clock()
sur_obj=pygame.display.set_mode((400,300))
pygame.display.set_caption("Keyboard_Input")
White=(255,255,255)
p1=10
p2=10
step=5
while True:
    sur_obj.fill(White)
    pygame.draw.rect(sur_obj, (255,0,0), (p1, p2, 70, 65))
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    key_input = pygame.key.get_pressed()   
    if key_input[pygame.K_LEFT]:
        p1 -= step
    if key_input[pygame.K_UP]:
        p2 -= step
    if key_input[pygame.K_RIGHT]:
        p1 += step
    if key_input[pygame.K_DOWN]:
        p2 += step
    pygame.display.update()
    fpsclock.tick(fps)
    """

"""
Sources des codes : 
https://pythonguides.com/python-pygame-tutorial/
https://www.codespeedy.com/movement-of-object-when-arrow-keys-are-pressed-in-pygame/

"""
