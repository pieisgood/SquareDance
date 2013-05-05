import os, sys
import pygame

#this will manage sounds, the idea being that
#multiple sounds need to be played at once
#but knowing when to stop and when to begin
#a sound can be difficult without a central
#manager. Events will trigger sounds which will
#be inserted into the Sound List to be iterated
#through each frame.
class SquareDanceSoundManager:

    def __init__(self):

        self.soundList = []



    def play_sounds(self):
        for sound in self.soundList :
            sound.play()
        return True

    def add_sound(self, new_sound):
        self.soundList.append(new_sound)
        return True
