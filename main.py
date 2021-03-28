import pygame
import random
import sys
import cv2
import time
from pygame import mixer
from gaze_tracking import GazeTracking

pygame.init()
fps=60
fpsclock=pygame.time.Clock()

black = [0, 0, 0]
white = [255, 255, 255]
blanc=(255,255,255)
noir=(0,0,0)
vert=(0,255,0)

step=10

x_gene = 1850
y_gene = 1000

attaque = 10
vitesse_max = 20

pygame.display.set_caption("spaceA")
screen = pygame.display.set_mode((x_gene,y_gene))

background_terre = pygame.image.load("ressources/terre3.jpg")
background_terre.convert()

background_traverse = pygame.image.load("ressources/espace4.jpg")
background_traverse.convert()
new_terrestre = pygame.transform.scale(background_traverse, (1920,1080))
background_mars = pygame.image.load("ressources/mars.jpg")
background_mars.convert()

class Tir:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('ressources/ball-ray.png')
        self.new_img = pygame.transform.scale(self.img, (30, 100)) 
        self.rect = self.new_img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def dep(self):
        self.y -= 50

class Ennemi:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.img_ennemi = pygame.image.load(img)
        self.nvlle_img_ennemi = pygame.transform.scale(self.img_ennemi, (80, 80)) 
        self.rect_ennemi = self.nvlle_img_ennemi.get_rect()
        self.rect_ennemi.topleft = (self.x, self.y)



class Joueur:
    def __init__(self):
        self.x = x_gene /2
        self.y = y_gene - 100
        self.img_joueur = pygame.image.load('ressources/navette.png')
        self.nvlle_img_joueur = pygame.transform.scale(self.img_joueur, (100, 100)) 
        self.rect_joueur = self.nvlle_img_joueur.get_rect()
        self.rect_joueur.topleft = (self.x, self.y)
        self.nbr_vies = 3
        self.img_vie = pygame.image.load('ressources/vie.png')
        self.nvlle_img_vie = pygame.transform.scale(self.img_vie, (30, 30)) 


    
def jeu():
    fin = False
    is_blinking = True
    joueur = Joueur()
    compteur = 1
    mixer.music.load("ressources/space.wav")
    mixer.music.play(-1)
    compteur = 1
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    t1 = True
    left_pupil_t2 = (0,0)
    right_pupil_t2 = (0,0)
    calibration_pos = (0,0)
    tirs = []
    #différents monstres possible
    img_comete = "ressources/monstre5.png"
    img_navette = "ressources/monstre7.png"
    img_aste = "ressources/monstre6.png"
    tableau = [img_comete, img_navette, img_aste]

    liste_comete = []
    for i in range (1) :
        x = random.randrange(0, x_gene)
        y = random.randrange(-400,0)
        image = tableau[random.randrange(0,len(tableau))]

        enn = Ennemi(x, y, image)

        liste_comete.append(enn)

    snow_list = []
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

    while not fin:

        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Affichage + déroulement fond écran
        screen.blit(new_terrestre ,(0,0))
        y_background += 0.5
        if y_background < y_gene :
            screen.blit(new_terrestre , (0,y_background))
            screen.blit(new_terrestre , (0,y_background-y_gene))
        else :
            y_background = 0
            screen.blit(new_terrestre ,(0,y_background))

        #petites boules blanches décoration
        for i in range(len(snow_list)):
            pygame.draw.circle(screen, white, snow_list[i], 2)
            snow_list[i][1] += 1

            if snow_list[i][1] > y_gene :
                y = random.randrange(-50, -10)
                snow_list[i][1] = y
                x = random.randrange(0, x_gene)
                snow_list[i][0] = x


        remplir_liste +=1
        clock.tick(60)

        #Faire un flash si perd une vie
        if compteur%2 != 0 :
            screen.blit(joueur.nvlle_img_joueur, (joueur.x,joueur.y))
            joueur.rect_joueur.topleft = (joueur.x, joueur.y)
        else :
            screen.fill(blanc)
        compteur = compteur - 1
        if compteur < 1 :
            compteur = 1

        

        #limite du cadre pour le joueur
        if joueur.x > x_gene - joueur.nvlle_img_joueur.get_size()[0]  :
            joueur.x = x_gene - joueur.nvlle_img_joueur.get_size()[0] -10
        if joueur.x < 10 :
            joueur.x = 10

        #fréquence pour l'augmentation +1 de la qtité des monstres
        if remplir_liste%20 == 0 :
            enn = Ennemi(random.randrange(0, x_gene), random.randrange(-400,0), tableau[random.randrange(0,len(tableau))])
            liste_comete.append(enn)

        #affichage + vérification collision des monstres
        vitesse_attaque = random.randrange(1,vitesse_max)
        for i in range(len(liste_comete)):            
            screen.blit(liste_comete[i].nvlle_img_ennemi, (liste_comete[i].x, liste_comete[i].y))
            liste_comete[i].rect_ennemi.topleft = (liste_comete[i].x, liste_comete[i].y)

            liste_comete[i].y += vitesse_attaque

            if liste_comete[i].y > y_gene :
                y = random.randrange(-50, -10)
                liste_comete[i].y = y
                x = random.randrange(0, x_gene)
                liste_comete[i].x = x
            
            if liste_comete[i].rect_ennemi.colliderect(joueur.rect_joueur) :
                liste_comete[i].x = 2000
                liste_comete[i].y = 2000
                compteur = 9
                
                joueur.nbr_vies = joueur.nbr_vies - 1
                if joueur.nbr_vies == 0 :
                    fin = True

        #affichage vies
        for i in range(joueur.nbr_vies) :
            screen.blit(joueur.nvlle_img_vie, (5 + i * 30, 5))

        for tir in tirs:
            for comete in liste_comete:
                if tir.rect.colliderect(comete.rect_ennemi) :
                    tir.x=2000
                    comete.x = 2000
                    tirs.remove(tir)
            if tir.y < 0:
                tirs.remove(tir)
            tir.dep()
            screen.blit(tir.new_img, (tir.x,tir.y))
            tir.rect.topleft = (tir.x, tir.y)

        if len(tirs) != 0:
            joueur.cooldown +=1
            if joueur.cooldown  == 15:
                joueur.cooldown = 0
        elif len(tirs) == 0:
            joueur.cooldown = 0

        _, frame = webcam.read()


        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""
        
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        if (calibration_pos == (0,0) and left_pupil != None)  :
            time.sleep(2)
            calibration_pos = gaze.pupil_left_coords()
            print(calibration_pos)

        if t1 :
            left_pupil_t1 = gaze.pupil_left_coords()
            right_pupil_t1 = gaze.pupil_right_coords()
            left_pupil_t2 = (0,0)
            right_pupil_t2 = (0,0)
            t1 = False
        elif t1 == False :
            left_pupil_t2 = gaze.pupil_left_coords()
            right_pupil_t2 = gaze.pupil_right_coords()
            t1 = True
        
        
        if gaze.is_blinking() :
            if joueur.cooldown == 0 :
                tirs.append(Tir(joueur.x,joueur.y))
                firing_shot = mixer.Sound("ressources/shoot.wav")
                firing_shot.play()

        
        elif ((left_pupil_t1 != None) and (right_pupil_t1!= None) and (left_pupil_t2 != None) and (right_pupil_t2 != None)):
            position = (((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100)
            if position < -0.20 or position > 0.20:
                joueur.x -= 30* position
                
        #rafraichissement
        pygame.display.update()
        fpsclock.tick(fps)

def main():
    jeu()
    print('fin')
    while True :
        screen.fill(vert)
        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
    

    
  




