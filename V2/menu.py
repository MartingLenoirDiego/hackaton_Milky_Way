
import pygame
import random
import sys
pygame.init()
fps=30
fpsclock=pygame.time.Clock()
cadre_x = 600
cadre_y = 400
screen=pygame.display.set_mode((cadre_x, cadre_y))
pygame.display.set_caption("Keyboard_Input")

#couleur
blanc=(255,255,255)
noir=(0,0,0)
vert=(0,255,0)

#pas auquel le joueur se déplace
step=10

#ennemi
pos_x_ennemi = 200
pos_y_ennemi = 300
img_ennemi = pygame.image.load('square.png')
nvlle_img_ennemi = pygame.transform.scale(img_ennemi, (50, 50)) 
rect_ennemi = nvlle_img_ennemi.get_rect()
rect_ennemi.topleft = (pos_x_ennemi, pos_y_ennemi)

#joueur/fusée
pos_x_joueur = 100
pos_y_joueur = 335
img_joueur = pygame.image.load('perso.jpg')
nvlle_img_joueur = pygame.transform.scale(img_joueur, (50, 50)) 
rect_joueur = nvlle_img_joueur.get_rect()
rect_joueur.topleft = (pos_x_joueur, pos_y_joueur)

#vies
pos_x_vie = 10
pos_y_vie = 10
img_vie = pygame.image.load('coeur.png')
nbr_vies = 3


compteur = 1
fin = "non"

while True:
    
    if fin == "non" :
        screen.fill(noir)
        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        if compteur%2 != 0 :
            screen.blit(nvlle_img_joueur, (pos_x_joueur,pos_y_joueur))
            rect_joueur.topleft = (pos_x_joueur, pos_y_joueur)

        else :
            screen.fill(noir)
        
        compteur = compteur - 1

        if compteur < 1 :
            compteur = 1

        for i in range(nbr_vies) :
            screen.blit(img_vie, (pos_x_vie + i * 40, pos_y_vie))


        screen.blit(nvlle_img_ennemi, (pos_x_ennemi,pos_y_ennemi))
        rect_ennemi.topleft = (pos_x_ennemi, pos_y_ennemi)

        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT]:
            pos_x_joueur -= step
        #enlever les pos_y_joueur pour pas qu'il puisse avancer
        if key_input[pygame.K_UP]:
            pos_y_joueur -= step
        if key_input[pygame.K_RIGHT]:
            pos_x_joueur += step
        if key_input[pygame.K_DOWN]:
            pos_y_joueur += step

        if pos_x_joueur > cadre_x-nvlle_img_joueur.get_size()[0] :
            pos_x_joueur = cadre_x-nvlle_img_joueur.get_size()[0]
        
        if pos_x_joueur < 0 :
            pos_x_joueur = 0

        if rect_ennemi.colliderect(rect_joueur) :
            pos_x_ennemi = random.randrange(0, 600)
            pos_y_ennemi = random.randrange(0, 400)
            compteur = 9
            nbr_vies = nbr_vies - 1

            if nbr_vies == 0 :
                fin = "oui"
        
    else :
        screen.fill(vert)
        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()


    pygame.display.update()
    fpsclock.tick(fps)
    
