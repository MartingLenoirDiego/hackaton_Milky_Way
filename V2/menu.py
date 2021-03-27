import pygame
#from game import Game
 
def begin():
 
    pseudo = input("Enter a pseudoname: ")
 
    pygame.init()
 
    pygame.display.set_caption("Space Mars! ")
    screen = pygame.display.set_mode((1080, 620))
    background = pygame.image.load("im\marsim.jpg")
    over = pygame.image.load("im\go.jpg")
 
    img_but_play = pygame.image.load('im\pngegg.png')
    but_play = pygame.transform.scale(img_but_play, (600, 750))
    but_play_rect = but_play.get_rect()
    but_play_rect.x = but_play.get_width() / 5
    but_play_rect.x = but_play.get_height() / 0.5
 
 
    replay = pygame.image.load('im\pngegg.png')
    replay = pygame.transform.scale(but_play, (400, 150))
    replay_rect = replay.get_rect()
    replay_rect.x = replay.get_width() / 5
    replay_rect.x = replay.get_height() / 0.5
 
    game = Game()
 
    running = True
    while running:
        screen.blit(background, (0, -400))
        if game.is_playing and game.is_playing != "over":
            game.update (screen)
 
        elif game.is_playing == "over":
            screen.blit(over, (0, -400))
            #screen.blit(replay, replay_rect)
        
        else:
            screen.blit(but_play, but_play_rect)
        
        pygame.display.flip()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("See you soon " + pseudo)
 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if but_play_rect.collidepoint(event.pos) and not game.is_playing:
                    game.start_game()
                    #game.is_playing = True
                if replay_rect.collidepoint(event.pos) and game.is_playing =="over":
                    game.start_game()
 
    
begin()
