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
cadre_x = 1900
cadre_y = 1000
screen=pygame.display.set_mode((cadre_x, cadre_y))
pygame.display.set_caption("Keyboard_Input")

#couleur
blanc=(255,255,255)
noir=(0,0,0)
vert=(0,255,0)

#pas auquel le joueur se deplace
step = 0


#ennemi
class Tir:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('img/ball-ray.png')
        self.new_img = pygame.transform.scale(self.img, (30, 100)) 
        self.rect = self.new_img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def dep(self):
        self.y -= 50

class Ennemi:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.img_ennemi = pygame.image.load('img/square.png')
        self.nvlle_img_ennemi = pygame.transform.scale(self.img_ennemi, (50, 50)) 
        self.rect_ennemi = self.nvlle_img_ennemi.get_rect()
        self.rect_ennemi.topleft = (self.x, self.y)

#joueur/fusee
class Joueur:
    def __init__(self):
        self.x = (cadre_x  / 2) - 60
        self.y = cadre_y - 300
        self.img_joueur = pygame.image.load('img/perso.jpg')
        self.nvlle_img_joueur = pygame.transform.scale(self.img_joueur, (50, 50)) 
        self.rect_joueur = self.nvlle_img_joueur.get_rect()
        self.rect_joueur.topleft = (self.x, self.y)
        self.nbr_vies = 3
        self.img_vie = pygame.image.load('img/coeur.png')
        self.cooldown = 0


compteur = 1

def jeu():
    fin = False
    is_blinking = True
    ennemi = Ennemi()    
    joueur = Joueur()
    mixer.music.load("space.wav")
    mixer.music.play(-1)
    compteur = 1
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    t1 = True
    left_pupil_t2 = (0,0)
    right_pupil_t2 = (0,0)
    calibration_pos = (0,0)
    tirs = []
    compteur_tir = 0
    while not fin:
        screen.fill(noir)
        

        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        if compteur%2 != 0 :
            screen.blit(joueur.nvlle_img_joueur, (joueur.x,joueur.y))
            joueur.rect_joueur.topleft = (joueur.x, joueur.y)
        else :
            screen.fill(noir)
        
        compteur = compteur - 1
        if compteur < 1 :
            compteur = 1

        for i in range(joueur.nbr_vies) :
            screen.blit(joueur.img_vie, (10 + i * 40, 10))

        screen.blit(ennemi.nvlle_img_ennemi, (ennemi.x,ennemi.y))
        ennemi.rect_ennemi.topleft = (ennemi.x, ennemi.y)

        for tir in tirs:
            if tir.y < 0:
                tirs.remove(tir)
                print(len(tirs))
            tir.dep()
            screen.blit(tir.new_img, (tir.x,tir.y))
            tir.rect.topleft = (tir.x, tir.y)

        if len(tirs) != 0:
            joueur.cooldown +=1
            if joueur.cooldown  == 7:
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
        
        

        """key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_SPACE]:
            if joueur.cooldown == 0:
                tirs.append(Tir(joueur.x,joueur.y))"""
        if gaze.is_blinking() :
            if joueur.cooldown == 0 :
                tirs.append(Tir(joueur.x,joueur.y))
                firing_shot = mixer.Sound("shoot.wav")
                firing_shot.play()

        
        elif ((left_pupil_t1 != None) and (right_pupil_t1!= None) and (left_pupil_t2 != None) and (right_pupil_t2 != None)):
            position = (((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100)
            if position < -0.20 or position > 0.20:
                joueur.x -= 40* position

        if joueur.x > cadre_x-joueur.nvlle_img_joueur.get_size()[0] :
            joueur.x = cadre_x-joueur.nvlle_img_joueur.get_size()[0]
        
        if joueur.x < 0 :
            joueur.x = 0

        if ennemi.rect_ennemi.colliderect(joueur.rect_joueur) :
            ennemi.x = random.randrange(0, 600)
            ennemi.y = random.randrange(0, 400)
            compteur = 9
            
            joueur.nbr_vies = joueur.nbr_vies - 1
            if joueur.nbr_vies == 0 :
                fin = True
        

        pygame.display.update()
        fpsclock.tick(fps)

def main():
    while True:
        jeu()
        screen.fill(vert)
        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
    
