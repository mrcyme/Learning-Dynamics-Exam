'''
Created on Jan 6, 2019

@author: simeo
'''
import random
import math
import numpy as np

class Individual:
    def __init__(self, initialWealth, riskCurve, alpha,index,behaviour):
        self.initialWealth = initialWealth #wealth
        self.wealth = initialWealth
        self.riskCurve = riskCurve 
        self.alpha = alpha #fraction lost during bad event
        self.behaviour = behaviour #Initialized randomly when a simulation is launched
        self.contribution = []
        self.finalWealthHistory = []
        self.index = index
        self.fitness = None
        
    def __repr__(self):
        #To output a string representaion of the object
        return ('Individual {}, behaviour : {}'.format(self.index,str(self.behaviour)))

 
    def generateRandomBehaviour(self,numberOfRounds):
        #instanciate a random behaviour
        self.behaviour = [[round(random.random(),2),round(random.random(),2),round(random.random(),2)] for i in range(numberOfRounds)]
        #self.behaviour = [[round(random.random(),2),i/numberOfRounds,i/numberOfRounds] for i in range(numberOfRounds)]
    def setBehaviour(self,behaviour):
        self.behaviour = behaviour
        
    def setFitnessValue(self):
        #to calculate the fitness value a the end of a generation (usefull to render new population)
        self.fitness =  np.exp(np.mean(self.finalWealthHistory))
        
    def Contribution(self, Cr,nround):
        beh= self.behaviour[nround]
        if(Cr<=beh[0]):
            return beh[1]
        else:
            return beh[2]
        
    
    def Step(self, Cr ,nround):
        #amount contributed to public good
        c = self.Contribution(Cr,nround)
        contribution = c*self.wealth
        #calculate what's left of wealth
        return contribution
    
    def addFinalWealthToHistory(self):
        #to add the ramaining wealth at the end of a game, the the mean is done to calculate the fitness at the end of a generation
        self.finalWealthHistory.append(self.wealth)
        
    def setWealth(self,newWealth):
        self.wealth = newWealth
        
    def resetRound(self):
        self.wealth = self.initialWealth
        
def addNoiseToTreshold(behav,sigma):
    for elem in behav:
        elem[0] += round(np.random.normal(0,sigma),2)
        elem[0] = max(0,elem[0])
        elem[0] = min(1,elem[0])



        
def risk(Cr,riskCurve):#chance of having bad event happening
    #this are not the right curve TODO!!
    p1 = lambda Cr :1 -Cr
    p2 = lambda Cr: 1-10*Cr if Cr<0.1 else 0
    p3 = lambda Cr : 1-math.pow(Cr,4)
    p4 = lambda Cr: 1/(math.exp(10*((Cr)-0.5))+1)
    dic = {'linear':p1,'piecewiseLinear':p2,'powerlaw':p3,'treshold':p4}
    if (random.random() < dic[riskCurve](Cr)):
        return 1
    return 0