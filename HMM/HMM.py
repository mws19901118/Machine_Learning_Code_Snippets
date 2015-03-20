'''
Created on Mar 17, 2015
@summary: This program is implementation of  Viterbi Algorithm of Hidden Markov Model.
@input: 2 command_line arguments which should be .dat files in the same directory with this python source code. The first argument indicates the name of parameter data file while the second argument indicates the name of test data file containing a sequence of observations). 
@output: Print the sequence of hidden states to the command line. 
@author: Michael.W a.k.a. Junsheng Wang
@version: 1.0
'''
import sys
import os
import math
from symbol import parameters
'''
@summary: Deal with command line input.
@return: True, if the input file is opened successfully; False, on the contrary.
'''
def Init():
    l=len(sys.argv)
    if l!=3:
        print "Wrong number of arguments!"
        return False
    else:
        if not os.path.isfile(sys.argv[1]):
            print "Parameters data file does not exist!"
            return False
        elif not os.path.isfile(sys.argv[2]):
            print "Test data file does not exist!"
            return False
    return True
'''
@summary: Read the initial  parameters data.
@param path: The path of data file
@return: The parameters read from data file
'''
def readparameter(path):
    datafile=file(path)
    
    line=datafile.readline()
    N=int(line)                                                                                                                          #number of states
    
    line=datafile.readline()
    temp=line.split(" ")
    I=[]                                                                                                                                        #Initial state probabilities
    for i in range(N):
        I.append(float(temp[i]))
        
    line=datafile.readline()
    temp=line.split(" ")
    A=[[0 for i in range(N)] for j in range(N)]                                                                   #Transition probabilities
    for i in range(N):
        for j in range(N):
            A[i][j]=float(temp[i*N+j])
            
    line=datafile.readline()
    M=int(line)                                                                                                                         #Number of output symbols
    
    line=datafile.readline()
    line=line[:-1]
    temp=line.split(" ")
    S=[]                                                                                                                                       #Output alphabet
    for i in range(M):
        S.append(temp[i])
        
    line=datafile.readline()
    temp=line.split(" ")
    B=[[0 for i in range(M)] for j in range(N)]                                                                 #Output distributions
    for i in range(N):
        for j in range(M):
            B[i][j]=float(temp[i*M+j])

    datafile.close()
    return (N,I,A,M,S,B)

'''
@summary: Read the observation sequence data.
@param path: The path of data file
@return: The observation sequence read from data file
'''
def readtestdata(path):
    datafile=file(path)
    obsseq=[]                                                                                                                              #Observation sequence
    while True:
        line=datafile.readline()
        if len(line)==0:
            break
        line=line[:-1]
        seq=[]
        temp=line.split(" ")
        for i in temp:
            if i!="":
                seq.append(i)
        obsseq.append(seq)
    datafile.close()
    
    return obsseq

'''
@summary: Implementation of Viterbi algorithm.
@param parameter: The parameters of HMM
@param obsseq: The observation sequence
@return: The most likely state sequence for a given observation sequence.
'''
def viterbi(parameter,obsseq):
    N=parameter[0]
    I=parameter[1]
    A=parameter[2]
    M=parameter[3]
    S=parameter[4]
    B=parameter[5]
    dict={}                                                                                                                                 #Use dictionary to covert symbol character to its index quickly.
    for i in range(M):
        dict[S[i]]=i
    l=len(obsseq)
    V=[[0 for i in range(l)] for j in range(N)]
    b=[[0 for i in range(l)] for j in range(N)]
    for i in range(N):
        V[i][0]=I[i]*B[i][dict[obsseq[0]]]
        b[i][0]=0
    for i in range(1,l):
        for j in range(N):
            maxp=-1
            maxindex=0
            for k in range(N):
                if V[k][i-1]*A[k][j]>maxp:
                    maxp=V[k][i-1]*A[k][j]
                    maxindex=k
            V[j][i]=maxp*B[j][dict[obsseq[i]]]
            b[j][i]=maxindex
    maxp=-1
    maxindex=0
    for i in range(N):
        if V[i][l-1]>maxp:
            maxp=V[i][l-1]
            maxindex=i
    result=[maxindex]
    for i in range(1,l):
        result.append(b[maxindex][l-i])
        maxindex=b[maxindex][l-i]
    result.reverse()
    output=""
    for i in result:
        output+="S"+str(i+1)
    print output

if __name__ == '__main__':
    if Init():                                                                                                                                  #Initialize and deal with command line input.
        parameter=readparameter(sys.argv[1])                                                              #Read parameters.
        obsseq=readtestdata(sys.argv[2])
    else:
        sys.exit()
    for i in obsseq:
        viterbi(parameter, i)
        