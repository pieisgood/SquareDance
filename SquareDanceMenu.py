import os, sys
import pygame

#this will control the menu of SquareDance
class SquareDanceMenu:

    def __init__(self, state, screen):
        self.currentFunction = ''
        self.state = state
        self.screen = screen
        self.menuItems = []
        self.width = 0
        self.height = 0

    def add_menu_item(self, menuI, width, height):
        self.width = width
        self.height = height
        count = len(self.menuItems)
        menuI.set_width(int(width/4))
        menuI.set_height(int(height/15))
        menuI.set_position(int(width/2), int(height/2) + (count)*menuI.get_height())
        self.menuItems.append(menuI)
        return True

    def check_menu(self, x,y):

        for item in self.menuItems:
            if item.got_clicked(x,y):
                return item.get_state()

        return False

    def check_highlight(self, x,y):

        for item in self.menuItems:
            if item.is_over(x,y):
                item.set_highlight(True)
            else:
                item.set_highlight(False)
        return False
    
    def render_menu(self):

        count = 0

        for item in self.menuItems:
            surf = pygame.Surface((item.get_width(), item.get_height()))
            text = pygame.font.Font(None, 20)
            text = text.render(item.get_state(), 1, (255,255,255))
            surf.set_alpha(100)
            if item.get_highlight():
                surf.fill((100,200,100), None)
            else:
                surf.fill((100,200,200), None)
            place = item.get_pos()
            self.screen.blit(surf, (place[0], place[1] + 6*count) )
            self.screen.blit(text, (place[0] + int(item.get_width()/2), place[1] + int(item.get_height()/2)))
            count += 1


    def run_menu(self):
        grey = pygame.Surface((self.width, self.height))
        grey.set_alpha(100)
        grey.fill((100,100,100), None)
        
        self.Screen.blit(grey, (0,0))
        pText = pygame.font.Font(None, 40)
        pRender = pText.render("Paused", 1, (255,255,255))
        self.Screen.blit(pRender, (int(self.width/2),int(self.height/2)))
        

class MenuItem:

    def __init__(self, state, position, width, height):
        self.state = state
        self.position = position
        self.width = width
        self.height = height
        self.highlight = False;

    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_pos(self):
        return self.position
    def get_highlight(self):
        return self.highlight
    def set_highlight(self, highlight):
        self.highlight = highlight
        return True
    def set_width(self, width):
        self.width = width
        return True
    def set_height(self, height):
        self.height = height
        return True
    def set_position(self, x,y):
        self.position = [x,y]
        return True

    def is_over(self, x,y):
        if x < (self.position[0] + self.width) and \
           x > self.position[0] and y < (self.position[1] + self.height) and \
           y > self.position[1]:
            return True
        else:
            return False

    def got_clicked(self, x, y):
        if x < (self.position[0] + self.width) and \
           x > self.position[0] and y < (self.position[1] + self.height) and \
           y > self.position[1]:
            return True
        else:
            return False
            
    def get_state(self):
        return self.state
