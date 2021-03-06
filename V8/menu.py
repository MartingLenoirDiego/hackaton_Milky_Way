
import pygame
import sys
import random

pygame.init()

fps=30
fpsclock=pygame.time.Clock()

black = [0, 0, 0]
white = [255, 255, 255]
blanc=(255,255,255)
noir=(0,0,0)
vert=(0,255,0)

step=10

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



class Ennemi:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        #self.img = "ressources/monstre5.png"
        self.img_ennemi = pygame.image.load(img)
        self.nvlle_img_ennemi = pygame.transform.scale(self.img_ennemi, (80, 80)) 
        self.rect_ennemi = self.nvlle_img_ennemi.get_rect()
        self.rect_ennemi.topleft = (self.x, self.y)



class Joueur:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.img_joueur = pygame.image.load('ressources/perso.jpg')
        self.nvlle_img_joueur = pygame.transform.scale(self.img_joueur, (50, 50)) 
        self.rect_joueur = self.nvlle_img_joueur.get_rect()
        self.rect_joueur.topleft = (self.x, self.y)
        self.nbr_vies = 3
        self.img_vie = pygame.image.load('ressources/vie.png')
        self.nvlle_img_vie = pygame.transform.scale(self.img_vie, (30, 30)) 


    
def jeu():
    fin = False
    # = Ennemi()
    joueur = Joueur()
    compteur = 1

    snow_list = []

    img_comete = "ressources/monstre5.png"
    #comete = pygame.image.load("ressources/monstre5.png")
    #nouvelle_comete= pygame.transform.scale(comete, (80,80))

    img_navette = "ressources/monstre7.png"
    #navette = pygame.image.load("ressources/monstre7.png")
    #nouvelle_navette = pygame.transform.scale(navette, (80,80))

    img_aste = "ressources/monstre6.png"
    #aste = pygame.image.load("ressources/monstre6.png")
    #nouvel_aste = pygame.transform.scale(aste, (80,80))

    tableau = [img_comete, img_navette, img_aste]
    #tableau = [nouvelle_comete, nouvelle_navette, nouvel_aste]

    liste_comete = []

    for i in range (1) :
        x = random.randrange(0, x_gene)
        y = random.randrange(-400,0)
        image = tableau[random.randrange(0,len(tableau))]

        enn = Ennemi(x, y, image)

        #print("x : ", enn.x, " y : ", enn.y, " joueur : ", joueur.y, " joueur diff : ", joueur.y - enn.y) 

        liste_comete.append(enn)

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

        vitesse_attaque = random.randrange(1,vitesse_max)

        screen.blit(new_terrestre ,(0,0))

        y_background += 0.5


        if remplir_liste%20 == 0 :
            enn = Ennemi(random.randrange(0, x_gene), random.randrange(-400,0), tableau[random.randrange(0,len(tableau))])
            liste_comete.append(enn)

        if y_background < y_gene :
            screen.blit(new_terrestre , (0,y_background))
            screen.blit(new_terrestre , (0,y_background-y_gene))


        else :
            y_background = 0
            screen.blit(new_terrestre ,(0,y_background))
            

        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()


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

        if compteur%2 != 0 :
            screen.blit(joueur.nvlle_img_joueur, (joueur.x,joueur.y))
            joueur.rect_joueur.topleft = (joueur.x, joueur.y)
        else :
            screen.fill(blanc)
        
        compteur = compteur - 1
        if compteur < 1 :
            compteur = 1


        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT]:
            joueur.x -= step
        if key_input[pygame.K_RIGHT]:
            joueur.x += step

        #limite du cadre pour le joueur
        if joueur.x > x_gene - joueur.nvlle_img_joueur.get_size()[0] :
            joueur.x = x_gene - joueur.nvlle_img_joueur.get_size()[0]
        if joueur.x < 0 :
            joueur.x = 0

        
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

        
        for i in range(joueur.nbr_vies) :
            screen.blit(joueur.nvlle_img_vie, (5 + i * 30, 5))

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
    

    
  




