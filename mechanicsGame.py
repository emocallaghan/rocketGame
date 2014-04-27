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

"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
                                Model
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
"""--------------------------------Drawable----------------------------------"""

class Drawable(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def draw(self,screen):
        pass
    @abstractmethod
    def translate(self,deltaPosition):
        pass
    
   
"""--------------------------------Body and Planent----------------------------------"""
    
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
        
    def update(self, force, time):
        deltaPos = self.deltaPosition(force, time);
        self.translate(deltaPos);
   
class planet(body):
    def __init__(mass, radius, position, velocity, color):
        super(planet,self).__init__(mass, radius, position, velocity, color);
        
"""--------------------------------dependantBody, rocketBody, thruster----------------------------------"""
        
class dependantBody(Drawable):
    def __init__(mass, radius, position, color):
        self.mass = mass;
        self.radius = radius;
        self.position = position;
        self.color = color;
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0);
        
    def translate(self, deltaPosition):
        self.position(0) += deltaPosition(0);
        self.position(1) += deltaPosition(1);
     

class rocketBody(dependantBody):
    def __init__(mass, radius, position, color = (72,209,204)):
        super(rocketBody,self).__init__( mass, radius, position, color);
        
        
class thruster(dependantBody):
    def __init__(self, radius, position, color = (255,54,54)):
        super(rocketBody,self).__init__( mass, radius, position, color);

    def fire(self):
        return 123; #kJ of potential energy spent by emiting one fart of liquid hydrogen

"""--------------------------------thrusterSet----------------------------------"""
   
class thrusterSet():
    def __init__(mass,radius, positions):
        self.mass = mass;
        self.thrusterList = [];
        for position in positions:
            self.thrusterList.append(thruster(mass, radius, position))
        
    def fireThruster(self,index):
        energyFired = self.thrusterList[index].fire();
        direction = [0,0];
        if (index == 0):
            direction = [0 , 1];
        elif(index == 1):
            direction = [-1 , 0];
        elif(index == 2 ):
            direction = [0 , -1];
        elif(index == 3):
            direction = [1 , 0];
        return [direction, energyFired];

    def translate(self, deltaPosition):
        for thruster in self.thrusterList:
            thruster.translate(deltaPosition);
    
    def draw(self,screen):
        for thruster in self.thrusterList:
            thruster.draw(screen);

"""--------------------------------Rocket----------------------------------"""
        
class rocket():
    def __init__(bMass, bRadius, bPosition, tmass, tradius, velocity):
        self.body = rocketBody(bMass, bRadius, bPosition, velocity);
        x = bPosition(0);
        y = bPosition(1);
        self.acceleration = [0,0]
        self.thrusters = thrusterSet(tmass, tradius, (x,y-bRadius), (x+bRadius,y),(x,y+bRadius),(x-bRadius,y));
        
    def fireThruster(self, index):
        poof = self.thruster.fireThruster(index);
        energy = poof[1];
        directinon = poof[0];
        force = energy/self.body.radius;
        directionalForce = [force*direction[0], force*direction[1]];
        return directionalForce;
        
    def calculateAcceleration(self, force):
        mass = bMass + self.thrusters.mass;
        self.acceleration = [force[0]/mass, force[1]/mass];
        return self.acceleration;
    
    def deltaPosition(self,force, time):
        self.calculateAcceleration(force);
        deltaX = deltaPosition1D(self.acceleration(0),self.velocity(0), time);
        deltaY = deltaPosition1D(self.acceleration(1),self.velocity(1), time);
        return [deltaX, deltaY];
        
    def deltaPositon1D(self,accel,vel,time):
        return (vel*time + .5*accel*time**2);
    
    def translate(self,deltaPosition):
        self.body.translate(deltaPosition);
        self.thrusters.translate(deltaPosition);
        
    def update(self, force, time):
        deltaPos = self.deltaPosition(force, time);
        self.translate(deltaPos);

    def draw(self, screen):
        self.body.draw(screen);
        self.thrusters.draw(screen);
        
class model():
    def __init__(rbMass, rbRadius, position, tmass, tradius):
        self.planentsList = []
        self.myRocket = rocket(rbMass, rbRadius, position, tmass, tradius, [0,0]);
        self.generatePlanets(1);
        
    def generatePlanets(self,numPlanets):
        pass
    
    def update(self, planetForces, rocketForce, time):
        for i in range(len(planetForces)):
            self.planetsList[i].update(planetForces[i], time);
        self.rocket.update(rocketForce, time);
        
    def fireRocket(self, index):
        self.myRocket.fireThruster(index);
    
    def objectsInWorld(self):
        return [self.myRocket, self.planentsList];
    
    def draw(self,screen):
        for planet in self.planetList:
            planet.draw(screen);
        self.myRocket.draw(screen);
    
            
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
                                View
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
class view():
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    def draweverything(self):
        self.model.draw(self.screen);
        
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
                                Controller
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """