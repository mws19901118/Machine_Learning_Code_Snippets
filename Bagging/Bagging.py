'''
Created on Apr 12, 2015
@summary: This program is implementation of  bagging.
@input: 4 command_line arguments which should be .dat files in the same directory with this python source code. The first argument indicates the name of train data file while the second argument indicates the name of test data file. The headers of both data should be exactly the same.
@output: Print the structure of decision tree as well as accuracy to the command line. 
@author: Michael.W a.k.a. Junsheng Wang
@version: 1.0
'''
import sys
import os
import math
import random
from perceptron import learning
'''
@summary: Deal with command line input.
@return: True, if the input file is opened successfully; False, on the contrary.
'''
def Init():
    l=len(sys.argv)
    if l!=6:
        print "Wrong number of arguments!"
        return False
    else:
        if not os.path.isfile(sys.argv[1]):
            print "Train data file does not exist!"
            return False
        elif not os.path.isfile(sys.argv[2]):
            print "Test data file does not exist!"
            return False
        else:
            if int(sys.argv[3])<=0:
                    print "The number of Bootstrap sample set should be greater than 0!"
                    return False
            else:
                if float(sys.argv[4])<=0 or float(sys.argv[4])>1:
                    print "Learning rate is invalid!"
                    return False
                else:
                    if int(sys.argv[5])<=0:
                        print "The number of iteration should be greater than 0!"
                        return False
    return True
'''
@summary: Read and preprocess the data.
@param path: The path of data file
@return: The data read from data file
'''
def readfile(path):
    datafile=file(path)
    firstline=datafile.readline()                                                               #Read and split the header.
    data=[]                                                                                                     #Record the data matrix.
    while True:
        line=datafile.readline()
        temp=line.split()
        if temp==[]:                                                                                        #If reach the end of file, break.
            break
        t=[]
        for i in temp:
            t.append(int(i))
        data.append(t)
    datafile.close()
    return data                                                                                             #Return data

'''
@summary: Perceptron learning for each bootstrap sample.
@param train: The whole train data set
@param k: Number of bootstrap samples.
@param rate: Learning rate.
@param itration: Number of iteration
@return: Perceptron weight vector of  each bootstrap sample
'''
def bagging(train,k,rate,iteration):
    n=len(train)
    bootstrap=[]                                                                                                          #Bootstrap perceptron
    for i in range(k):
        ctrain=[]
        for j in range(n):
            ctrain.append(train[random.randint(0,n-1)])
        bootstrap.append(learning(ctrain,rate,iteration))
    return bootstrap
'''
@summary: Calculate output of perceptron on certain data.
@param data: Data vector
@param weight: Weight vector
@return: The label of  certain data
'''
def check(data,weight):
    sum=0
    m=len(data)
    for j in range(m-1):
        sum+=weight[j]*data[j]
    sum-=weight[-1]
    output=1/(1+math.exp(-sum))
    if output>=0.5:
        label=1
    else:
        label=0
    return label

'''
@summary: Calculate the accuracy of test data on bootstrap perceptron.
@param test: Test data set
@param bp: Perceptron weight vector of  each bootstrap sample
@return: The accuracy of test data on bootstrap perceptron.
'''
def evaluate(test,bootstrap):
    l=len(test)
    n=len(bootstrap)
    total=0
    for i in range(l):
        sum=0
        for j in range(n):
            sum+=check(test[i], bootstrap[j])
        if sum>n/2:
            label=1
        else:
            label=0
        if label==test[i][-1]:
            total+=1
    return total*1.0/l

if __name__ == '__main__':
    if Init():                                                                                                      #Initialize and deal with command line input.
        train=readfile(sys.argv[1])                                                              #Read training set.
        test=readfile(sys.argv[2])                                                               #Read test set
        k=int(sys.argv[3])                                                             #Number of Bootstrap sample sets.
        rate=float(sys.argv[4])
        iteration=int(sys.argv[5])
    else:
        sys.exit()
    
    bootstrap=bagging(train,k,rate,iteration)
    print evaluate(test, bootstrap)
        