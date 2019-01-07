'''
Created on Jan 6, 2019

@author: simeo
'''
import numpy as np
from Simulation import*
import pandas as pd
import matplotlib.pyplot as plt
alpha = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

riskCurve = ['piecewiseLinear','linear','treshold','powerlaw']
omega = [1,2,4]


results = np.zeros((len(omega),len(riskCurve),len(alpha)))
for i in range(len(omega)):
    for j in range(len(riskCurve)):
        for l in range(len(alpha)):
            sim = Simulation(omega[i],alpha[l],riskCurve[j],numberOfGenerations = 1000)
            results[i,j,l] = sim.runSim() 


plt.figure(figsize = (10,22))          
plt.subplot(3,1,1)
plt.title('$\Omega = 1$')
plt.plot(alpha,results[0,0,:],'r',marker='o')
plt.plot(alpha,results[0,1,:],'b',marker='o')
plt.plot(alpha,results[0,2,:],'g',marker='o')
plt.plot(alpha,results[0,3,:],'y',marker='o')

plt.ylabel('contribution')
plt.legend(('Piecewise Linear', 'Linear','Treshold','Power law'),
           loc='upper left')
plt.subplot(3,1,2)
plt.title('$\Omega = 2$')
plt.plot(alpha,results[1,0,:],'r',marker='o')
plt.plot(alpha,results[1,1,:],'b',marker='o')
plt.plot(alpha,results[1,2,:],'g',marker='o')
plt.plot(alpha,results[1,3,:],'y',marker='o')

plt.ylabel('contribution')
plt.legend(('Piecewise Linear', 'Linear','Treshold','Power law'),
           loc='upper left')
plt.subplot(3,1,3)
plt.title('$\Omega = 2$')
plt.plot(alpha,results[2,0,:],'r',marker='o')
plt.plot(alpha,results[2,1,:],'b',marker='o')
plt.plot(alpha,results[2,2,:],'g',marker='o')
plt.plot(alpha,results[2,3,:],'y',marker='o')
plt.xlabel('Alpha')
plt.ylabel('contribution')
plt.legend(('Piecewise Linear', 'Linear','Treshold','Power law'),
           loc='upper left')

plt.show()