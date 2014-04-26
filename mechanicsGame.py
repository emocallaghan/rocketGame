# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 13:42:13 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *
import random
import math
import time

class Drawable(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def draw(self,screen):
        pass
    @abstractmethod
    def translate(self,deltaPosition):
        pass
    
class body(Drawable):
    def __init__(mass, radius, position, velocity, color):
        self.mass = mass;
        self.radius = radius;
        self.position = position;
        self.velocity = velocity;
        self.color = color;
        self.acceleration = (0,0);
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0);
        
    def translate(self, deltaPosition):
        self.position(0) += deltaPosition(0);
        self.position(1) += deltaPosition(1);
        
    def calculateAcceleration(self, force):
        self.accelearation = [force[1]/self.mass, force[0]/self.mass];
        
    def deltaPosition(self,force, time):
        calculateAcceleration(force);
        deltaX = deltaPosition1D(self.acceleration(0),self.velocity(0), time);
        deltaY = deltaPosition1D(self.acceleration(1),self.velocity(1), time);
        return [deltaX, deltaY];
        
    def deltaPositon1D(self,accel,vel,time):
        return (vel*time + .5*accel*time**2);
        
class planet(body):
    def __init__(mass, radius, position, velocity, color):
        super(planet,self).__init__(mass, radius, position, velocity, color);
    
class thruster(Drawable):
    def __init__(self, radius, position, color):
        self.radius = radius;
        self.position = position;
        self.color = color;
        
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0);
        
    def translate(self, deltaPosition):
        self.position(0) += deltaPosition(0);
        self.position(1) += deltaPosition(1);

    def fire(self):
        return 123; #kJ of potential energy spent by emiting one fart of liquid hydrogen
        
class thrusterSet():
    def __init__(mass,radius, positions):
        self.mass = mass;
        self.thrusterList = [];
        for position in positions:
            self.thrusterList.append(thruster(mass, radius, position))
        
    def fireThruster(self,index):
        energyFired = self.thrusterList[index].fire();
        direction = 1;
        if(index == 2 or 3):
            direction = -1;
        return [direction, energyFired];


class rocketBody(body):
    def __init__(mass, radius, position, velocity, color = (72,209,204)):
        super(rocketBody, mass, radius, position, velocity, color);
        
class rocket():
    def __init__(bMass, bRadius, bPosition, tmass, tradius, velocity):
        self.body = rocketBody(bMass, bRadius, bPosition, velocity);
        x = bPosition(0);
        y = bPosition(1);
        self.thrusters = thrusterSet(tmass, tradius, (x,y-bRadius), (x+bRadius,y),(x,y+bRadius),(x-bRadius,y));
        
       
        