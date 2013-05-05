import os, sys
import pygame
from pygame.locals import *
from SquareDanceBlock import *
from SquareDanceMap import *
#A class meant to handle the current style being displayed by the game
class Style:

    def __init__(self, screen, width, height):
        pygame.mixer.init()
        self.color_one = 'one'
        self.color_two = 'two'
        self.color_one_image = ''
        self.color_two_image = ''
        self.highlight_one_image = ''
        self.highlight_two_image = ''
        self.color_one_square = ''
        self.color_two_square = ''
        self.bar_image = ''
        self.map_image = ''
        self.background_image = ''
        self.Sounds = ''
        self.sequential_highlight_image = ''
        self.top_image = ''
        self.pauseBackground = ''
        self.move_sound = ''
        self.background_music = ''
        self.gameover_sound = ''
        self.delete_sound = ''
        self.channel_handler = [ pygame.mixer.Channel(i) for i in range(5) ]
        self.Screen = screen
        self.width = width
        self.height = height

    def render_fade(self, surface):
        self.Screen.blit(surface, (0,0))
        return True

    def set_surface(self, surface):
        self.Screen = surface
        return True

    def render_bar(self, bar, combo):
        #rendering bar code goes here
        #print bar.get_position().get_x()
        self.Screen.blit(self.bar_image, (bar.get_position().get_x(),bar.get_position().get_y()))
        self.render_text(combo, bar.get_position().get_x(), bar.get_position().get_y())
        return True

    def render_nextSquares(self, sMap):
        
        return True

    def render_pause(self):
        grey = pygame.Surface((self.width, self.height))
        grey.set_alpha(100)
        grey.fill((100,100,100), None, BLEND_MULT)
        
        self.Screen.blit(grey, (0,0))
        pText = pygame.font.Font(None, 40)
        pRender = pText.render("Paused", 1, (255,255,255))
        self.Screen.blit(pRender, (int(self.width/2),int(self.height/2)))

    def render_gameOver(self):
        grey = pygame.Surface((self.width, self.height))
        grey.set_alpha(100)
        grey.fill((100,100,100), None, BLEND_MULT)
        
        self.Screen.blit(grey, (0,0))
        pText = pygame.font.Font(None, 40)
        pRender = pText.render("Game Over", 1, (255,255,255))
        self.Screen.blit(pRender, (int(self.width/2),int(self.height/2)))

        

    def render_highlights(self, highlights):
        for x in range(16):
            for y in range(12):
                if highlights[x][y] != None:
                    if highlights[x][y].get_color() == 'one':
                        location = highlights[x][y].get_currPosition()
                        self.Screen.blit(self.highlight_one_image, (location.get_x(), location.get_y()))
                    if highlights[x][y].get_color() == 'two':
                        location = highlights[x][y].get_currPosition()
                        self.Screen.blit(self.highlight_two_image, (location.get_x(), location.get_y()))

        return True

    def render_sequential_highlights(self, sequential, pMap):
        for x in range(16):
            for y in range(12):
                if sequential[x][y]:
                    location = pMap.get_coords(x,y)
                    self.Screen.blit(self.sequential_highlight_image, (location.get_x(),location.get_y()))
    
    def render_text(self, text, x, y):
        #code to render text on screen :) easy peasy
        font = ''
        font = pygame.font.Font(None, 12)
        tRender = font.render(text, 1, (10, 10, 10))
        self.Screen.blit(tRender, (x,y))
        return True

    def render_fps(self, msDelta):
        font = pygame.font.Font(None, 20)
        #tRender = font.render(str(1000/(msDelta)), 1, (10,10,10))
        #self.Screen.blit(tRender, (0,0))
    
    def render_block(self,block, x, y):
        #rendering block code goes here
        if block.get_color() == 'one':
            self.Screen.blit(self.color_one_image , (x, y))              
        elif block.get_color() == 'two':
            self.Screen.blit(self.color_two_image , (x, y))
        return True

    def render_map(self, sMap):
        #rendering field code goes here
        the_positions = sMap.get_position_map()
        for x in xrange(12):
            for y in xrange(16):
                if x == 0 or x == 1:
                    tempP = the_positions.get_coords(y,x)
                    self.Screen.blit(self.top_image, (tempP.get_x(), tempP.get_y()))
                else:
                    tempP = the_positions.get_coords(y,x)
                    self.Screen.blit(self.map_image, (tempP.get_x(), tempP.get_y()))
        #self.Screen.blit(self.map_image, 0.1*width + 0.04*height*x, 0.1*height + 0.04*height*y)
	this_field = sMap.get_field()
	#f = 0
	for y in xrange(12):
		for x in xrange(16):
			if isinstance(this_field[x][y], Block):
                            #print "should be rendering boxes!"
                            tempBb = this_field[x][y]
                            #f += 1
                            #location = tempBb.get_place()
                            #location = the_positions.get_coords(location[0], location[1])
                            location = tempBb.get_currPosition()
			    self.render_block(tempBb, location.get_x(), location.get_y() )
	#print f
        tempG = sMap.get_active_group()
	for x in xrange(4):
            tempB = tempG.get_block(x)
            location = tempB.get_place()
            #print location[0]
            #print location[1]
            location = the_positions.get_coords(location[0], location[1])
            self.render_block(tempB, location.get_x(), location.get_y() )
        return True
                              
    def render_background(self):
        #rendering background code goes here
        self.Screen.blit(self.background_image, (0,0))
        return True
    
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

    def set_image_one(self,image_name):
        #image assignment goes here
        self.color_one_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.color_one_image = self.scale_block(self.color_one_image)
        return True
    def set_image_two(self,image_name):
        #image assignment goes here
        self.color_two_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.color_two_image = self.scale_block(self.color_two_image)
        return True

    def set_image_map(self,image_name):
        #image assignment goes here
        self.map_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert_alpha()
        self.map_image = self.scale_block(self.map_image)
        return True
    
    def set_image_top(self,image_name):
        #image assignment goes here
        self.top_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert_alpha()
        self.top_image = self.scale_block(self.top_image)
        return True
    
    def set_image_background(self,image_name):
        #image assignment goes here
        self.background_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.width,self.height))
        return True

    def set_image_bar(self, image_name):
        self.bar_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.bar_image = pygame.transform.scale(self.bar_image, (int(0.004*self.height), int(12*0.05*self.height)))
        return True

    def set_highlight_image_one(self, image_name):
        self.highlight_one_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.highlight_one_image = pygame.transform.scale(self.highlight_one_image, (int(0.1*self.height),int(0.1*self.height)))
        self.highlight_one_image.set_alpha(100)

    def set_highlight_image_two(self, image_name):
        self.highlight_two_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.highlight_two_image = pygame.transform.scale(self.highlight_two_image, (int(0.1*self.height),int(0.1*self.height)))
        self.highlight_two_image.set_alpha(100)

    def set_sequential_highlight_image(self, image_name):
        self.sequential_highlight_image = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.sequential_highlight_image = self.scale_block(self.sequential_highlight_image)

    def set_pause_background(self, image_name):
        self.pauseBackground = pygame.image.load(os.path.join('data',image_name.strip() )).convert()
        self.pauseBackground = pygame.transform.scale(self.pauseBackground, (self.height,self.height))
        self.pauseBackground.set_alpha(100)

    def scale_block(self, image):
        image = pygame.transform.scale(image, (int(0.05*self.height),int(0.05*self.height)))
        return image

    def set_move_sound(self, sound_name):
        self.move_sound = pygame.mixer.Sound(os.path.join('data',sound_name.strip() ))
        self.move_sound.set_volume(0.1)
        return True

    def set_background_music(self, sound_name):
        self.background_music = pygame.mixer.Sound(os.path.join('data',sound_name.strip() ))
        return True

    def set_delete_sound(self, sound_name):
        self.delete_sound = pygame.mixer.Sound(os.path.join('data',sound_name.strip() ))
        self.delete_sound.set_volume(0.2)
        return True

    def set_gameover_sound(self, sound_name):
        self.gameover_sound = pygame.mixer.Sound(os.path.join('data',sound_name.strip() ))
        return True

    def play_move_sound(self):
        self.channel_handler[0].play(self.move_sound)

    def play_background_music(self):
        self.channel_handler[1].play(self.background_music)

    def play_delete_sound(self):
        self.channel_handler[2].play(self.delete_sound)

    def play_gameover_sound(self):
        self.channel_handler[3].play(self.gameover_sound, 2)

    def stop_background_music(self):
        self.channel_handler[1].pause()

    def continue_background_music(self):
        self.channel_handler[1].unpause()
        
    def fade_background_music(self):
        self.channel_handler[1].fadeout(3000)
