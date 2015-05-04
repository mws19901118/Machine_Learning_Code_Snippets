'''
Created on Feb 26, 2015
Modified on Apr 12, 2015
@summary: This program is implementation of  a single layer perceptron with sigmoid function algorithm for binary classification with all attributes have categorical and no-missing values.
@author: Michael.W a.k.a. Junsheng Wang
@version: 2.0
'''

import math

'''
@summary: The learning process of  perceptron
@param train: Training data set
@param rate: Learning rate
@param iteration: Number of iteration
@return: The weight vector of perceptron
'''
def learning(train,rate,iteration):
    weight=[]
    n=len(train)
    m=len(train[0])
    for i in range(m):
        weight.append(0)                                                                              #Initialize weights.
    for i in range(iteration):
        index=i%n
        sum=0
        for j in range(m-1):
            sum+=weight[j]*train[index][j]
        sum-=weight[-1]
        output=1/(1+math.exp(-sum))                                                     #Calculate the output.
        if output>=0.5:
            label=1
        else:
            label=0
        delta=rate*(train[index][-1]-output)*output*(1-output)       #Calculate delta.
        for j in range(m-1):
            weight[j]+=delta*train[index][j]                                              #Upgrade weights.
        weight[-1]+=delta*(-1)
    return weight
