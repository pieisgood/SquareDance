import os, sys
import weakref
import pygame
from pygame.locals import *
#These are different kinds of events, this list will grow with time

class Event:

    def __init__(self):
        self.name = "Gen Event"

class GameOverEvent(Event):

    def __init__(self):
        self.name = "Game Over Event"

class StateEvent(Event):

    def __init__(self, state):
        self.name = "State change Event"
        self.state = state

class PauseEvent(Event):

    def __init__(self):
        self.name = "Pause Event"

class MoveEvent(Event):

    def __init__(self):
        self.name = "Move Event"

class QuitEvent(Event):

    def __init__(self):
        self.name = "Quit Event"

class TickEvent(Event):

    def __init__(self):
        self.name = "Tick Event"

class BeatEvent(Event):

    def __init__(self):
        self.name = "Beat Event"

class GroupMoveEvent(Event):

    def __init__(self, direction):
        self.name = "Move Request Event"
        self.direction = direction
		
class DelayTickEvent(Event):
	
    def __init__(self):
	self.name = "Delay Tick Event"

class RotateEvent(Event):

    def __init__(self, direction):
        self.name = "Rotate Event"
        self.direction = direction

class DeleteSquaresEvent(Event):

    def __init__(self):
        self.name = "Delete Squares Event"

class MoveEvent(Event):

    def __init__(self):
        self.name = "Move Event"

class MenuEvent(Event):

    def __init__(self):
        self.name = "Menu Event"

#This is an event manager class, this will be the framework for events.
class SquareEventManager:

    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        self.listeners[ listener ] = 1

    def UnregisterListener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]

    def Post(self, event):
        for listener in self.listeners.keys():
            listener.Notify(event)

#Unique event managers are below, for beat events and other things
