import os, sys
import pygame
from pygame.locals import *
from SquareEventManager import *

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class SquareController:
	
	def __init__(self, evManager, style, screen, aMap, state, score):
                self.evManager = evManager
                self.evManager.RegisterListener( self )
                self.styleList = style
		self.view = self.styleList.get_current_style()
		self.model = aMap
		self.score = score
		self.bar_tick = 0
		self.screen = screen
		self.state = state
		self.combo = self.model.get_combo()
		self.delete_tick = pygame.time.get_ticks()
		self.delay_tick = pygame.time.get_ticks()
		self.move_tick = pygame.time.get_ticks()
		self.current_tick = pygame.time.get_ticks()
		self.is_first = 0
		self.is_paused = 0
                self.width = self.model.get_width()
                self.height = self.model.get_height()
		self.fadeSurface = pygame.Surface((self.width, self.height))
		self.alphaFade = 255
		self.fade = False

	def Notify(self, event):
                if isinstance( event, TickEvent ):
                        if self.is_first == 0:
                                self.view.play_background_music()
                                self.is_first = 1
                        if self.is_paused == 1:
                                self.view.continue_background_music()
                                self.is_paused = 0
                        self.current_tick = pygame.time.get_ticks()
                        msBar = self.current_tick - self.bar_tick 
                        self.bar_tick += msBar
                        self.bar_tick = self.bar_tick%10000
                        if self.current_tick - self.move_tick > 30:
                                move_event = MoveEvent()
                                self.evManager.Post( move_event )
                                self.move_tick = self.current_tick
                        if self.current_tick - self.delay_tick > 1000:
                                delay_event = DelayTickEvent()
                                self.evManager.Post( delay_event )
                                self.delay_tick = self.current_tick
                        self.model.get_bar().new_position(self.bar_tick)
                        self.model.smooth_drop(msBar)
                        self.model.drop_blocks()
                        self.model.find_squares()
                        self.model.square_highlights_check()
                        if self.model.delete_sequential(self.score):
                                self.view.play_delete_sound()
                        if not(self.model.game_check()):
                                self.state.set_state("GameOver")
                                self.view.stop_background_music()
                                self.view.play_gameover_sound()
                        if self.styleList.is_transition(msBar):
                                self.view.fade_background_music()
                                self.view = self.styleList.get_next_style()
                                self.view.play_background_music()
                                self.fadeSurface = self.styleList.get_fade_surface(self.model)
                                self.view.set_surface(self.screen)
                                self.fade= True
                                
                        highlights = self.model.get_highlights()
                        sequential = self.model.get_sequential()
                        pMap = self.model.get_position_map()
                        self.view.render_background()
                        self.view.render_map(self.model)
                        self.view.render_highlights(highlights)
                        self.view.render_sequential_highlights(sequential, pMap)
                        self.view.render_bar(self.model.get_bar(), self.combo)
                        self.view.render_fps(msBar)
                        self.view.render_score(self.score.get_scoreStr())
                        if self.fade:
                                self.fadeSurface.set_alpha(self.alphaFade)
                                self.alphaFade -= 2
                                if self.alphaFade < 0:
                                        self.fade = False
                                        self.alphaFade = 255
                                        self.fadeSurface = pygame.Surface((self.width, self.height))
                                self.view.render_fade(self.fadeSurface)
                                
                        self.bar_tick = pygame.time.get_ticks()
                        pygame.display.flip()
                elif isinstance( event, GroupMoveEvent):
			self.model.try_move(event.direction)
			self.view.play_move_sound()
		elif isinstance( event, DelayTickEvent):
                        self.model.try_move(DOWN)
                        #self.model.drop_blocks()
                        self.combo = self.model.get_combo()
                elif isinstance( event, RotateEvent):
                        self.model.rotate_group( event.direction)
                        self.view.play_move_sound()
                elif isinstance( event, DeleteSquaresEvent):
                        self.model.delete_squares()
                if isinstance( event, PauseEvent):
                        highlights = self.model.get_highlights()
                        sequential = self.model.get_sequential()
                        pMap = self.model.get_position_map()
                        self.is_paused = 1
                        self.view.stop_background_music()
                        self.view.render_background()
                        self.view.render_map(self.model)
                        self.view.render_highlights(highlights)
                        self.view.render_sequential_highlights(sequential, pMap)
                        self.view.render_pause()

                        pygame.display.flip()

                if isinstance(event, GameOverEvent):
                        #print "got to drawing"
                        highlights = self.model.get_highlights()
                        sequential = self.model.get_sequential()
                        pMap = self.model.get_position_map()
                        self.view.render_background()
                        self.view.render_map(self.model)
                        self.view.render_highlights(highlights)
                        self.view.render_sequential_highlights(sequential, pMap)
                        #self.view.render_bar(self.model.get_bar(), self.combo)
                        self.view.render_gameOver()

                        pygame.display.flip()
                        
                                        
                                
		

class SquareKeyBoardController:

        def __init__(self, evManager, state):
                #stuff goes here
                self.evManager = evManager
                self.evManager.RegisterListener( self )
                self.state = state
                

        def Notify(self, event):
                if isinstance( event, TickEvent ):                                
                        #handle inputs
			for event in pygame.event.get():
				ev = None
				if event.type == QUIT:
					ev = QuitEvent()
				elif event.type == KEYDOWN \
				     and event.key == K_ESCAPE:
					ev = QuitEvent()
				elif event.type == KEYDOWN \
                                        and event.key == K_p :
                                                ev = PauseEvent()
                                                self.state.set_state("Pause")
				elif event.type == KEYDOWN \
				     and event.key == K_UP:
					direction = UP
					ev = GroupMoveEvent(direction)
				elif event.type == KEYDOWN \
                                     and event.key == pygame.K_d:
                                        direction = pygame.K_d
                                        ev = RotateEvent(direction)
				elif event.type == KEYDOWN \
                                     and event.key == pygame.K_a:
                                        direction = pygame.K_a
                                        ev = RotateEvent(direction)
                                if ev:
                                        self.evManager.Post( ev )
                if isinstance( event, MoveEvent ):
                        tKey = pygame.key.get_pressed()
                        if tKey[pygame.K_DOWN]:
                                direction = DOWN
                                ev = GroupMoveEvent(direction)
                                self.evManager.Post( ev )
                        if tKey[pygame.K_LEFT]:
                                direction = LEFT
                                ev = GroupMoveEvent(direction)
                                self.evManager.Post( ev )
                        if tKey[pygame.K_RIGHT]:
                                direction = RIGHT
                                ev = GroupMoveEvent(direction)
                                self.evManager.Post( ev )
                if isinstance( event, PauseEvent):
                        for event in pygame.event.get():
                                if event.type == KEYDOWN \
                                        and event.key == K_p:
                                                #print "got here"
                                                self.state.set_state("Start")

                if isinstance( event, GameOverEvent):
                        for event in pygame.event.get():
                                ev = None
                                if event.type == KEYDOWN \
                                        and event.key == K_r:
                                        self.state.set_state("Start")
                                elif event.type == KEYDOWN \
                                        and event.key == K_ESCAPE:
					ev = QuitEvent()

				if ev:
                                        self.evManager.Post( ev )

class SquareMenuController:

        def __init__(self, evManager, squareDanceState, squareDanceMenu):
                self.evManager = evManager
                self.evManager.RegisterListener( self )
                self.state = squareDanceState
                self.menu = squareDanceMenu

        def Notify(self, event):
                if isinstance( event, MenuEvent ):
                        position = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                                if event.type == MOUSEBUTTONDOWN:
                                        position = event.pos
                                        newState = self.menu.check_menu(position[0], position[1])
                                        if newState :
                                                self.state.set_state(newState)
                        self.menu.check_highlight(position[0], position[1])
                        self.menu.render_menu()
                        pygame.display.flip()                
                        
                        
                                
#Control the tick of the game, Finished
class SquareCPUController:

        def __init__(self, evManager, squareDanceState):
                #stuff goes here
                self.evManager = evManager
                self.evManager.RegisterListener( self )
                self.keepGoing = True
                self.state = squareDanceState
                self.state.set_state("Menu")
                self.fps = 0

        def Run(self):

                while self.keepGoing:
                        currentState = self.state.get_state()

                        if currentState == "Start":
                                event = TickEvent()
                                self.evManager.Post( event )
                        elif currentState == "Menu":
                                event = MenuEvent()
                                self.evManager.Post( event )
                        elif currentState == "Pause":
                                event = PauseEvent()
                                self.evManager.Post( event )
                        elif currentState == "GameOver":
                                event = GameOverEvent()
                                self.evManager.Post( event )
                        elif currentState == "Quit":
                                event = QuitEvent()
                                self.evManager.Post( event )
                        elif currentState == "Create Playlist":
                                #stuff
                                event = QuitEvent()
                                self.evManager.Post( event )
                        elif currentState == "Create Style":
                                #stuff
                                event = QuitEvent()
                                self.evManager.Post( event )
                        #print "fps = " + str(1000/(temptwo - tempone))

        def Notify(self, event):
                if isinstance( event, QuitEvent):
                        self.keepGoing = False
                        pygame.quit()
                        
                        
#class SquareRythmController:

 #       def __init__(self):
                #stuff goes here
		
