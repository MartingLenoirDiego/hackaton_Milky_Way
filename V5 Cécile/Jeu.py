
import pygame
import sys
import random

pygame.init()


black = [0, 0, 0]
white = [255, 255, 255]
size = [600, 400]

x_gene = 1920
y_gene = 1080

attaque = 10
vitesse_max = 5




pygame.display.set_caption("spaceA")
screen = pygame.display.set_mode((x_gene,y_gene))

background_terre = pygame.image.load("ressources/terre3.jpg")
background_terre.convert()

background_traverse = pygame.image.load("ressources/espace4.jpg")
background_traverse.convert()
new_terrestre = pygame.transform.scale(background_traverse, (1920,1080))
background_mars = pygame.image.load("ressources/mars.jpg")
background_mars.convert()

snow_list = []

comete = pygame.image.load("ressources/monstre5.png")
nouvelle_comete= pygame.transform.scale(comete, (80,80))

navette = pygame.image.load("ressources/monstre7.png")
nouvelle_navette = pygame.transform.scale(navette, (80,80))

aste = pygame.image.load("ressources/monstre6.png")
nouvel_aste = pygame.transform.scale(aste, (80,80))


tableau = [nouvelle_comete, nouvelle_navette, nouvel_aste]

liste_comete = []

for i in range (1) :
    x = random.randrange(0, x_gene)
    y = random.randrange(-400,0)

    liste_comete.append([x,y,tableau[random.randrange(0,len(tableau))]])

for i in range(50):
    x = random.randrange(0, x_gene)
    y = random.randrange(0, y_gene)
    snow_list.append([x, y])

clock = pygame.time.Clock()

done = True

y_background = 0 
i = 0 

x_j = random.randrange(0, 600)
y_j = 0
remplir_liste = 0 
while done:
    
    

    #nombre_attaque = random.randrange(1,attaque)
    vitesse_attaque = random.randrange(1,vitesse_max)

    screen.blit(new_terrestre ,(0,0))

    y_background += 0.5


    if remplir_liste%20 == 0 :
        liste_comete.append([random.randrange(0, x_gene), random.randrange(-400,0), tableau[random.randrange(0,len(tableau))]])

    if y_background < y_gene :
        screen.blit(new_terrestre , (0,y_background))
        screen.blit(new_terrestre , (0,y_background-y_gene))


    else :
        y_background = 0
        screen.blit(new_terrestre ,(0,y_background))
        

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = False

    for i in range(len(snow_list)):
        pygame.draw.circle(screen, white, snow_list[i], 2)
        snow_list[i][1] += 1

        if snow_list[i][1] > y_gene :
            y = random.randrange(-50, -10)
            snow_list[i][1] = y
            x = random.randrange(0, x_gene)
            snow_list[i][0] = x

    for i in range(len(liste_comete)):
        screen.blit(liste_comete[i][2], (liste_comete[i][0],liste_comete[i][1]))
        liste_comete[i][1] += vitesse_attaque

        if liste_comete[i][1] > y_gene :
            y = random.randrange(-50, -10)
            liste_comete[i][1] = y
            x = random.randrange(0, x_gene)
            liste_comete[i][0] = x

    remplir_liste +=1
    #screen.blit(nouvelle_comete,(x_j,y_j))
    #y_j += 1
    clock.tick(60)
    pygame.display.flip()

    
pygame.quit()



