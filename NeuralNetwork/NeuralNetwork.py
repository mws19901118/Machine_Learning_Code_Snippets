'''
Created on Feb 26, 2015
@summary: This program is implementation of  a single layer perceptron with sigmoid function algorithm for binary classification with all attributes have categorical and no-missing values.
@input: 4 command_line arguments which should be .dat files in the same directory with this python source code. The first argument indicates the name of train data file while the second argument indicates the name of test data file. The headers of both data should be exactly the same.
@output: Print the structure of decision tree as well as accuracy to the command line. 
@author: Michael.W a.k.a. Junsheng Wang
@version: 1.0
'''
import sys
import os
import math

'''
@summary: Deal with command line input.
@return: True, if the input file is opened successfully; False, on the contrary.
'''
def Init():
    l=len(sys.argv)
    if l!=5:
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
            if float(sys.argv[3])<=0 or float(sys.argv[3])>1:
                print "Learning rate is invalid!"
                return False
            else:
                if int(sys.argv[4])<=0:
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
@summary: Calculate the accuracy on certain data set.
@param data: data set
@param weight: weight vector
@return: the accuracy on certain data set
'''
def check(data,weight):
    count=0
    for i in data:
        sum=0
        for j in range(m-1):
            sum+=weight[j]*i[j]
        sum-=weight[-1]
        output=1/(1+math.exp(-sum))
        if output>=0.5:
            label=1
        else:
            label=0
        if label==i[-1]:
            count+=1
    return count*100.0/len(data)

if __name__ == '__main__':
    if Init():                                                                                                      #Initialize and deal with command line input.
        train=readfile(sys.argv[1])                                                              #Read training set.
        test=readfile(sys.argv[2])                                                               #Read test set
        rate=float(sys.argv[3])
        iteration=int(sys.argv[4])
    else:
        sys.exit()
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
    print "Accuracy on training set ("+str(n)+"instances): "+str(check(train, weight))+"%"
    print "Accuracy on test set ("+str(len(test))+"instances): "+str(check(test, weight))+"%"
    
