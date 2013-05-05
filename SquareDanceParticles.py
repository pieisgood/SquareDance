import os, sys
import pygame
from pygame.locals import *
import random

class Particle:

    def __init__(self, pImage, position, velocity, angle, angularVelocity, size, TTL):
        self.pImage = pImage
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.anglularV = angularVelocity
        self.size = size
        self.TTL = TTL

    def Update(self):
        self.TTL = self.TTL - 1
        self.position = self.position + self.velocity
        self.angle = self.angle + self.angleV
        return True

    def Draw(self, Screen):
        Screen.blit(self.pImage, position)
        return True

class HighlightParticle:

    def __init__(self, pImage):
        self.pImage = pImage

class ParticleEngine:

    def __init__(self, textures, location):
        self.EmitterLocation = location
        self.textures = textures
        self.particles = []
        self.random = random()

    def GenerateNewParticle(self):
        texture = self.textures[random.randint(0, self.textures.size() -1)]
        position = EmitterLocation
        velocity = new Vector2(1.0 * random.random()*2 - 1, 1.0 * random.random()*2 - 1)
        angle = 0
        angularV = 0.1*random.random()*2 - 1
        size = random.random()
        TTL = 20 + random.randint(0,40)

        return Particle(texture, position, velocity, angle, angularV, size, TTL)

    def Draw(self, particles, Screen):
        for item in particles:
            item.Draw(Screen)

    
        
