import sys
import pygame

from scripts.entities import physicsEntity
from scripts.utils import load_image

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ninja game")
        self.screen = pygame.display.set_mode((640,480))

        self.clock = pygame.time.Clock()

        '''self.img = pygame.image.load('data/images/clouds/cloud.png')
        self.img.set_colorkey((0,0,0))

        self.img_pos = [160,260]

        self.collision_area = pygame.Rect(50,50,300,50)'''

        self.movement = [False,False]

        self.assets= {
            'player':load_image('entities/player/player.png')
        }

        self.player = physicsEntity(self,'player',(50,50),(8,15))
    
    def run(self):
        while True:
            self.screen.fill((14,255,144))
            '''
            #if you want to move the object under the rectangular area uncomment below lines.
            #self.img_pos[1] += (self.movement[1]-self.movement[0])*5
            #self.screen.blit(self.img, self.img_pos)

            #img_r  = pygame.Rect(self.img_pos[0],self.img_pos[1],self.img.get_height(),self.img.get_width())
            img_r = pygame.Rect(*self.img_pos,*self.img.get_size())

            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen,(0,100,255),self.collision_area)
            else:
                pygame.draw.rect(self.screen,(0,100,155),self.collision_area)

            #this section let the cloud area to move on the rectangular area
            self.img_pos[1] += (self.movement[1]-self.movement[0])*5
            self.screen.blit(self.img, self.img_pos)
            '''

            self.player.update((self.movement[1]-self.movement[0],0))
            self.player.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #keyboard movements    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()