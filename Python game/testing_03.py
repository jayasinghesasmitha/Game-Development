import sys
import pygame
import random
import math

from scripts.clouds import Clouds
from scripts.entities import physicsEntity,Player
from scripts.utils import load_image,load_images,Animation
from scripts.tilemap import Tilemap
from scripts.particle import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ninja game")

        self.screen = pygame.display.set_mode((640,480))

        self.display = pygame.Surface((320,240))

        self.clock = pygame.time.Clock()

        '''self.img = pygame.image.load('data/images/clouds/cloud.png')
        self.img.set_colorkey((0,0,0))

        self.img_pos = [160,260]

        self.collision_area = pygame.Rect(50,50,300,50)'''

        self.movement = [False,False]

        self.assets= {
            'decor':load_images('tiles/decor'),
            'grass':load_images('tiles/grass'),
            'large_decor':load_images('tiles/large_decor'),
            'stone':load_images('tiles/stone'),
            'player':load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds':load_images('clouds'),
            'player/idle' : Animation(load_images('entities/player/idle'),img_dur= 6),
            'player/run' : Animation(load_images('entities/player/run'),img_dur = 4),
            'player/jump' : Animation(load_images('entities/player/jump')),
            'player/slide' : Animation(load_images('entities/player/slide')),
            'player/wall_slide' : Animation(load_images('entities/player/wall_slide')),
            'particle/leaf' : Animation(load_images('particles/leaf'),img_dur=20,loop=False),
        }
        
        #print(self.assets)
        self.clouds = Clouds(self.assets['clouds'],count=16)
        self.player = Player(self,(50,50),(8,15))
        self.tilemap = Tilemap(self,tile_size=16)

        self.tilemap.load('map.json')
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor',2)],keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1],23,13))

        self.particles = []
        self.scroll = [0,0]

    def run(self):
        while True:
            
            #for the whole area
            #self.screen.fill((14,255,144))

            #for the selected area
            #self.display.fill((14,255,144))

            self.display.blit(self.assets['background'],(0,0))
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

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])/30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])/30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #this section spawn the particles
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf' ,pos ,velocity=[-0.1,0.3], frame=random.randint(0,20)))
                    
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            self.player.update(self.tilemap,(self.movement[1]-self.movement[0],0))

            #self.player.render(self.screen)
            self.player.render(self.display, offset = render_scroll)

            #to check the collision
            #print(self.tilemap.physics_rects_around(self.player.pos))

            #this section manages the particles
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display,offset = render_scroll)
                if particle.type == 'leaf' :
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

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

                    #the jump condition
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()