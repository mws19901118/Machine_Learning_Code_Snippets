'''
Created on Jan 25, 2015
@summary: This program is implementation of  binary classification ID3 algorithm with all attributes have categorical and no-missing values.
@input: 2 command_line arguments which should be .dat files in the same directory with this python source code. The first argument indicates the name of train data file while the second argument indicates the name of test data file. The headers of both data should be exactly the same.
@output: Print the structure of decision tree as well as accuracy to the command line. 
@author: Michael.W a.k.a. Junsheng Wang
@version: 1.0
'''
import sys
import os
import math
'''
@summary: The ID3 Tree Node
class0: The amount of  class 0
class1: The amount of class 1
entropy: The entropy of current node
label: If current node is a leaf node, label means which class current node belongs to; If current node is not a leaf node, label means the index of attribute of current node.
 child: The list of child of  current node
 calentropy(): Calculate the entropy of current node.
'''
class ID3TreeNode:
    def __init__(self,class0,class1):
        self.class0=class0
        self.class1=class1
        self.entropy = 0
        self.label = -1
        self.child=[]
    def calentropy(self):
        if self.class0==0 or self.class1==0:
            self.entropy=0
        else:
            p0=self.class0*1.0/(self.class0+self.class1)
            p1=self.class1*1.0/(self.class0+self.class1)
            self.entropy=-(p0*math.log(p0,2)+p1*math.log(p1,2))

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
            print "Train data file does not exist!"
            return False
        elif not os.path.isfile(sys.argv[2]):
            print "Test data file does not exist!"
            return False
    return True
'''
@summary: Read and preprocess the data.
@param path: The path of data file
@return: A tuple:0. data 1. attributes name 2.attributes value 3.class0 amount 4.class1 amount
'''
def readfile(path):
    datafile=file(path)
    firstline=datafile.readline().split()                                                   #Read and split the header.
    numofattr=len(firstline)/2                                                                 #Get the amount of attributes.
    header=[]                                                                                                #Record the name of attributes.
    for i in range(numofattr):
        header.append(firstline[2*i])
    data=[]                                                                                                     #Record the data matrix.
    attribute=[[] for i in range(numofattr)]
    class0=0
    class1=0
    while True:
        line=datafile.readline()
        temp=line.split()
        if temp==[]:                                                                                        #If reach the end of file, break.
            break
        data.append(temp)
        for i in range(numofattr+1):
            if i<numofattr:
                if not temp[i] in attribute[i]:                                                 #Record the values of each attribute.
                    attribute[i].append(temp[i]) 
            else:                                                                                                  #Count the amount of each class.
                if temp[i]=='0':
                    class0+=1
                else:
                    class1+=1
    datafile.close()
    return (data,header,attribute,class0,class1)                            #Return a tuple.

'''
@summary: Generate the ID3 tree from training data.
@param root: The root node of the tree
@param index: The unclassified data belonging to current node
@param attribute: The remaining attribute of current node
'''
def generatetree(root,index,attribute):
    global traindata
    global header
    if root.class0==0:                                                                                                                           #If there is no class0, set label of current node to 1.
        root.label=1
        return
    elif root.class1==0:                                                                                                                        #If there is no class1, set label of current node to 0.
        root.label=0
        return
    same=True
    for i in index:
        if traindata[i][0:len(attribute)]!=traindata[index[0]][0:len(attribute)]:                   #Check if all the examples of data are of same value.
            same=False
            break
    if same==True:                                                                                                                              #If all the examples of data are of same value, set the label of current node to the greater one of class0 and class1.
        if root.class0>=root.class1:
            root.label=0
        else:
            root.label=1
        return
    
    IG=0
    nextlevel=[]                                                                                                                                    #Record children of current node.
    maxindex=0                                                                                                                                  #Record the index of attribute which has the maximum IG.
    maxdistribute=[]                                                                                                                          #Record the data distribution according to current selection of attribute.  
    for i in range(len(attribute)):                                                                                                    #Traverse all the remaining attributes to find the maximum IG.
        if attribute[i]==[]:
            continue
        sumh=0                                                                                                                                       #Record the entropy of current attribute selection.
        num=len(attribute[i])
        distribute=[[] for k in range(num)]                                                                                     #Record the data distribution in current attribute selection.
        countclass=[[0,0] for k in range(num)]                                                                              #Record the amount of each class in current attribute selection.
        temp=[]                                                                                                                                        #Record the children of current node in current attribute selection. 
        for j in index:
            for k in range(num):
                if traindata[j][i]==attribute[i][k]:
                    distribute[k].append(j)                                                                                                 
                    if traindata[j][-1]=='0':                                                                                                  #Count each class.
                        countclass[k][0]+=1
                    else:
                        countclass[k][1]+=1
        for k in range(num):
            temp.append(ID3TreeNode(countclass[k][0],countclass[k][1]))                         #Construct temporary children.
            temp[k].calentropy()                                                                                                          #Calculate entropy of temporary children and add it to the entropy of current attribute selection.
            sumh+=temp[k].entropy*(temp[k].class0+temp[k].class1)/(root.class0+root.class1)
        if root.entropy-sumh>IG:                                                                                                    #If IG of current attribute selection is greater than maximum IG, update maximum IG and other variables.
            IG=root.entropy-sumh
            nextlevel=temp
            maxindex=i
            maxdistribute=distribute
    root.label=maxindex                                                                                                                 #If current node is not a leaf node, let label be the index of attribute of current node.
    root.child=nextlevel
    restattribute=[a for a in attribute]                                                                                        #Copy the attributes and delete the attribute of current node.
    restattribute[maxindex]=[]
    for i in range(len(root.child)):
        generatetree(root.child[i], maxdistribute[i],restattribute)                                     #Recursively deal with the children of current node.

'''
@summary:  Print the ID3 tree to the screen.
@param root: Current node
@param level: Current tree level(begin with 0)
@return: The string should be printed of current node.
'''
def printtree(root,level):
    global header
    global attribute
    output="\n"                                                                                                                  #Add a line break to end current line.
    if root.child!=[]:                                                                                                            #If current node is not leaf node, do the following steps.
        for i in range(len(attribute[root.label])):                                                         #Traverse all the value of current attribute of node.
            for j in range(level):
                output+="| "                                                                                                     #The number of '| ' in the front of each line equals to the level of current node.
            output+=header[root.label]+" = "+attribute[root.label][i]+" :"            #Add the  header name and values to output string.
            output+= printtree(root.child[i],level+1)                                                     #Add the output strings of the children of current node to output string.
        return output
    else:                                                                                                                                 #If current node is leaf node, return its label and a line break.
        return " "+str(root.label)+'\n'

'''
@summary: Classify inout data according to the ID3 Tree.
@param root: The root node of ID3 Tree
@param data: The unclassified data
@return: True, if the classification is correct; False, on the contrary.
'''
def classify(root,data):
    while root.child!=[]:
        i=attribute[root.label].index(data[root.label])         #While haven't reach leaf node, find the next node in the children of current node according to the value of corresponding attribute of data.
        root=root.child[i]
    if root.label==int(data[-1]):                                                   #Return true, if the classification is correct; return false, on the contrary.
        return True
    else:
        return False

if __name__ == '__main__':
    if Init():                                                                                        #Initialize and deal with command line input.
        train=readfile(sys.argv[1])                                                #Read training set.
        test=readfile(sys.argv[2])                                                  #Read test set
        traindata=train[0]                                                               #Record data matrix for training.
        header=train[1]                                                                   #Record the header of data.
        attribute=train[2]                                                                #Record the value for each attribute.
    else:
        sys.exit()
    total=train[3]+train[4]                                                           #Total amount of data equals the amount of class0 plus the amount of class1.
    index=[i for i in range(total)]                                               #Record all the index of data in the whole data matrix.
    root=ID3TreeNode(train[3],train[4])                                #Construct the root node of the ID3 tree.
    root.calentropy()                                                                    #Calculate the entropy of root.
    generatetree(root,index,attribute)                                  #Generate the ID3 tree.
    count=0                                                                                     #Calculate the accuracy on training set.
    for i in traindata:
        if classify(root, i)==True:
            count+=1
    print "Accuracy on training set ("+str(total)+"instances): "+str(count*100.0/total)+"%"
    count=0                                                                                     #Calculate the accuracy on test set.
    for i in test[0]:
        if classify(root, i)==True:
            count+=1
    print "Accuracy on test set ("+str(test[3]+test[4])+"instances): "+str(count*100.0/(test[3]+test[4]))+"%"
    print printtree(root,0)