import os, sys
import pygame

#this is a class that contains Styles and allows for transitions of
#styles throughout the game.
class SquareDanceSList:

    def __init__(self):

        self.styleList = []
        self.tillNextStyle = 10000
        self.fadeStyle = ''
        self.stylePlace = 0


    def add_style(self, style):

        self.styleList.append(style)
        return True

    def get_current_style(self):

        return self.styleList[self.stylePlace]

    def get_next_style(self):
        self.stylePlace += 1

        self.stylePlace = self.stylePlace%len(self.styleList)

        return self.styleList[self.stylePlace]

    def is_transition(self, msDelta):
        self.tillNextStyle -= msDelta

        if self.tillNextStyle < 0:
            self.tillNextStyle = 10000
            self.fadeStyle = self.styleList[self.stylePlace]
            return True
        else:
            return False

    def get_fade_surface(self, model):
        width = model.get_width()
        height = model.get_height()
        fadeSurface = pygame.Surface((width, height))
        self.fadeStyle.set_surface(fadeSurface)
        highlights = model.get_highlights()
        sequential = model.get_sequential()
        pMap = model.get_position_map()
        self.fadeStyle.render_background()
        self.fadeStyle.render_map(model)
        self.fadeStyle.render_highlights(highlights)
        self.fadeStyle.render_sequential_highlights(sequential, pMap)

        fadeSurface = pygame.transform.smoothscale(fadeSurface, (int(width*0.5),int(height*0.5)))
        fadeSurface = pygame.transform.smoothscale(fadeSurface, (width, height))

        

        return fadeSurface
