import pygame
import random
import sys
import cv2
import time
from gaze_tracking import GazeTracking

pygame.init()
fps=30
fpsclock=pygame.time.Clock()
cadre_x = 1920
cadre_y = 1080
screen=pygame.display.set_mode((cadre_x, cadre_y))
pygame.display.set_caption("Keyboard_Input")

#couleur
blanc=(255,255,255)
noir=(0,0,0)
vert=(0,255,0)

#pas auquel le joueur se deplace
step = 0


#ennemi
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
        self.x = 100
        self.y = 335
        self.img_joueur = pygame.image.load('img/perso.jpg')
        self.nvlle_img_joueur = pygame.transform.scale(self.img_joueur, (50, 50)) 
        self.rect_joueur = self.nvlle_img_joueur.get_rect()
        self.rect_joueur.topleft = (self.x, self.y)
        self.nbr_vies = 3
        self.img_vie = pygame.image.load('img/coeur.png')

compteur = 1

def jeu():
    fin = False
    ennemi = Ennemi()
    joueur = Joueur()
    compteur = 1
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    t1 = True
    left_pupil_t2 = (0,0)
    right_pupil_t2 = (0,0)
    calibration_pos = (0,0)
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
        
        if gaze.is_blinking():
            print("WINK")
        
        elif ((left_pupil_t1 != None) and (right_pupil_t1!= None) and (left_pupil_t2 != None) and (right_pupil_t2 != None)):
            position = (((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100)
            joueur.x -= 100* position

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
        
        print(position)

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
    
