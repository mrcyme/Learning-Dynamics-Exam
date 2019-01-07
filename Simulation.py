'''
Created on Jan 6, 2019

@author: simeo
'''
import numpy as np
from individual import*
import copy
class Simulation:
    def __init__(self,numberOfRounds,alpha,riskCurve,wealth = 100,populationSize=100,numberOfGamesByGenerations=1000,numberOfGenerations=10000,mu=0.03,sigma=0.15):
        self.numberOfRounds = numberOfRounds
        self.numberOfGamesByGenerations = numberOfGamesByGenerations
        self.numberOfGenerations = numberOfGenerations
        self.wealth = wealth 
        self.alpha = alpha
        self.riskCurve = riskCurve
        self.populationSize = populationSize
        #create the first population
        self.population = self.createRandomPopulation()
        self.mu = mu
        self.sigma = sigma
        
    def createRandomPopulation(self):
        #create the first population
        population = np.array([Individual(self.wealth,self.riskCurve,self.alpha,i,None) for i in range(self.populationSize)])
        for individual in population:
            #initialize the behaviour (lenght = numberofRounds)
            individual.generateRandomBehaviour(self.numberOfRounds)
        population[0].setBehaviour([[round(random.random(),2),0,0] for i in range(self.numberOfRounds)])
        return population
    
    
    def renewPopulation(self):
        fitness = np.array([individual.fitness for individual in self.population])
        fitprop = fitness/np.sum(fitness)
        numoffspring = np.random.multinomial(self.populationSize, fitprop)
        a = []
        for j in range(len(numoffspring)):
            for i in range(numoffspring[j]):
                b = [elem for elem in self.population[j].behaviour]
                #memory[counter+i] = b
                a.append(copy.deepcopy(b))
        return a
    

            
     
        
        
    
    def playGame(self,players):
        #play a game between two players (or more)
        Cr = 0 # initial public good 
        totalInitialWealth = np.sum([player.wealth for player in players])
        contributions=np.empty((len(players),self.numberOfRounds))
        for nround in range(self.numberOfRounds):
            #print('-----round ',nround)
            for i in range(len(players)):
                contributions[i,nround] = players[i].Step(Cr,nround)
            Cr += np.sum(contributions[:,nround])/totalInitialWealth
            for i in range(len(players)):
                newWealth = (1-self.alpha*risk(Cr,self.riskCurve))*(players[i].wealth-contributions[i,nround])
                players[i].setWealth(newWealth)
            
        for i in range(len(players)):
            players[i].contribution.append(np.sum(contributions[i])/players[i].initialWealth)
                  
        for player in players:
            player.addFinalWealthToHistory()
            player.resetRound()
            
        
    
    def playGeneration(self):
        #for a certain number of iteration 2 players are selected randomly and the play a game
        for i in range(self.numberOfGamesByGenerations):
            players = np.random.choice(self.population,2,replace=False)
            self.playGame(players)

    def wrightFisher(self): 
        #print('1---------',self.population)
        newBehaviours = self.renewPopulation()
        for behav in newBehaviours:
            a = np.random.rand()
            b = np.random.rand()
            if a<self.mu:
                for elem in behav:
                    elem[0] += round(np.random.normal(0,self.sigma),2)
                    elem[0] = max(0,elem[0])
                    elem[0] = min(1,elem[0])
            if b<self.mu:
                for elem in behav:
                    elem[1] = round(np.random.uniform(0,1),2)
                    elem[2] = round(np.random.uniform(0,1),2)
        self.population = [Individual(self.wealth,self.riskCurve,self.alpha,i,newBehaviours[i]) for i in range(self.populationSize)]
        #print('2---------',self.population)
        
    
    def runSim(self):
        averageResults = np.zeros(50)
        #lauch a simulation 
        for i in range(self.numberOfGenerations):
            self.playGeneration()
            contributionValues = np.zeros(self.populationSize)
            for j in range(self.populationSize):
                self.population[j].setFitnessValue()
                mean = np.mean(self.population[j].contribution)
                contributionValues[j]=mean
            if (self.numberOfGenerations-50<=i<self.numberOfGenerations):
                averageResults[i-self.numberOfGenerations+50] = np.mean(contributionValues)
            self.wrightFisher() 
        av = np.mean(averageResults)
        print('for omega = {},alpha = {}, riskurve : {}, c = {}'.format(self.numberOfRounds,self.alpha,self.riskCurve,av))
        return av
