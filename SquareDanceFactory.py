import os, sys
import pygame
import json
from json import JSONDecoder
from pygame.locals import *
from SquareDanceView import Style
from SquareDanceBlock import *
from SquareDanceMap import *
from SquareDanceController import *
from SquareDanceSList import *
from SquareDanceMenu import *
from SquareDanceScore import *
#A class to handle creation of all our classes
class SquareFactory:

    def __init__(self, init_file):
        self.stylename = 'none'
        self.playlistname = 'none'
        self.json_data = open(init_file.strip(), 'r')
        self.data = json.load(self.json_data)
        

    def createMap(self, width, height):

        newMap = SquareDanceMap(width, height)

        return newMap

    def newBlock(self,color):
        rBlock = Block(color)
        return rBlock

    def newScore(self):
        return SquareDanceScore()

    def newStyle(self,style_name, screen, width, height):
        inStyle = open(style_name.strip(), 'r')
        image_items = json.load(inStyle)

        rStyle = Style(screen, width, height)
        rStyle.set_image_one(image_items["block_one"])
        rStyle.set_image_two(image_items["block_two"])
	rStyle.set_image_map(image_items["map_image"])
	rStyle.set_image_background(image_items["background"])
	rStyle.set_image_bar(image_items["bar_image"])
	rStyle.set_highlight_image_one(image_items["highlight_one"])
	rStyle.set_highlight_image_two(image_items["highlight_two"])
	rStyle.set_sequential_highlight_image(image_items["small_highlight"])
	rStyle.set_pause_background(image_items["Pause_Background"])
	rStyle.set_image_top(image_items["top_row"])
	rStyle.set_background_music(image_items["background_music"])
	rStyle.set_move_sound(image_items["move_sound"])
	rStyle.set_delete_sound(image_items["delete_sound"])
	rStyle.set_gameover_sound(image_items["gameover_sound"])

        return rStyle

    def newStyleList(self, screen, width, height):
        
        StyleList = SquareDanceSList()

        for style in self.data["Styles"]:
            StyleList.add_style(self.newStyle(style["Style_Name"], screen, width, height))
        return StyleList

    def newSquareController(self, evManager , style, screen, aMap, state, score):
        return SquareController(evManager, style, screen, aMap, state, score)

    def newSquareMenu(self, state, screen, width, height):
        Menu = SquareDanceMenu(state, screen)
        startItem = MenuItem("Start", '', '', '')
        createPlaylistItem = MenuItem("Create Playlist", '','','')
        createNewStyle = MenuItem("Create Style", '', '', '')
        optionsItem = MenuItem("Options", '', '', '')
        exitItem = MenuItem("Quit",  '' , '', '')
        Menu.add_menu_item(startItem, width, height)
        Menu.add_menu_item(createPlaylistItem, width, height)
        Menu.add_menu_item(createNewStyle, width, height)
        Menu.add_menu_item(optionsItem, width, height)
        Menu.add_menu_item(exitItem, width, height)
       
        
        return Menu
        
		
