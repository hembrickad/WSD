'''
Adrienne Hembrick
April 8, 2021

Problem:Through the use of a training file the code tries to use context to find whether
the word "line" is referencing a phone or a product.

Description:The wsd code first takes in both files that the user gives through the terminal and capitolizes the words
The listTrain() splits the training list text between a phone list and a product list depending on whether the answer
tag says "phone" or "product". concatTrain() and sep() splits the list and forms a better seperated
list. splitTrain() and tot() forms four default dictionaries out of the list -- two for each association (before the word
and after the word). listTest() starts to prepare the answers by locating the id of all of the test data and places the words
assoicated into a test-list. splitTest() seperates to words based on whether or not the word came before or after the
the term "line" or "lines". Associate predicts whether or not a word is associated with "phone" or "product" based on
the popularity of words before and after line for each association. format() finishes formatting the answer by
placing the associationg and combo() makes the list into a string.

Instructions: In the terminal after compiling the file place the test file along with a
'>' character and the file you want the information to be moved to.

    python tagger.py pos-test.txt pos-train.txt > pos-test-train.txt

        Input:
        
        <corpus lang="en">
        <lexelt item="line-n">
        <instance id="line-n.w8_059:8174:">
        <context>
        <s> Advanced Micro Devices Inc., Sunnyvale, Calif., and Siemens
        AG of West Germany said they agreed to jointly develop, manufacture
        and market microchips for data communications and telecommunications
        with an emphasis on the integrated services digital network. </s> <@> </p> <@>
        <p> <@> <s> The integrated services digital network, or ISDN, is an international
        standard used to transmit voice, data, graphics and video images over telephone
        <head>lines</head> . </s> 
        </context>

        Output:
        
        <answer instance="line-n.w8_059:8174:" senseid="phone"/>

Results:

Baseline:80.16%

	Phone	Product	
Phone	68	21
Product	4	33

'''

###### IMPORTS ######
import sys
import re
import random
from collections import defaultdict

###### GLOBAL VARIABLES ######
mainList = list()
phDList = list()
prDList = list()
prBe = defaultdict(int)
prAf = defaultdict(int)
phBe = defaultdict(int)
phAf = defaultdict(int)

answTest = list()
testwordsBe = list()
testwordsAf = list()

###### METHODS ######
# Input for training data
def inputTrain(args):
    sent = " "
    g = open(args, 'r')
    sent += g.read()
    sent = sent.upper()
    return sent

#Make input file a list of words
def listTrain(values):
    new = re.split("\n",values)
    for x in range(len(new)):
        if re.search('<ANSWER INSTANCE=',new[x]):
            if bool(re.search("PHONE", new[x])):
                phDList.append(new[x+2])
            else:
                prDList.append(new[x+2])

#seperates words and '/' for the test file
#also takes out dashes since they mess up the default dictionary
def sep(sent):
    sent = sent.replace("-", "")
    l = re.split(" |  ",sent)
    while '' in l:
       l.remove('')
    return l  
        
#Divides the training data into seperate lists
def concatTrain(l):
    n = " "
    return sep(n.join(l))

#Creates Default Dictionaries 
def tot(l):
    tol = defaultdict(int)
    for x in l:
        tol[x] += 1
    return tol 

#Makes defaultdict with words before and after the word line
def splitTrain():
    ph1 = list()
    ph2 = list()
    pr1 = list()
    pr2 = list()
    global prBe, prAf, phBe, phAf
    
    for x in range(len(phDList)):
        if (phDList[x] == '<HEAD>LINE</HEAD>' or phDList[x] == '<HEAD>LINES</HEAD>'):
            ph1.append([phDList[x-2],phDList[x-1]])
            ph2.append([phDList[x+1], phDList[x+2]])
    for x in range(len(prDList)):
        if (prDList[x] == '<HEAD>LINE</HEAD>' or prDList[x] == '<HEAD>LINES</HEAD>'):
            pr1.append([prDList[x-2],prDList[x-1]])
            pr2.append([prDList[x+1], prDList[x+2]])
    prBe = tot(pr1)
    prAf = tot(pr2)
    phBe = tot(ph1)
    phAf = tot(ph2)

# Input for testing data a prepares answer list for solutions
def listTest(values):
    new = re.split("\n", values)
    words = list()
    global answTest
    for x in range(len(new)):
        if bool(re.search('<INSTANCE ID',new[x])):
            new[x] = new[x].replace('<INSTANCE ID','')
            new[x] = new[x].replace('>','')
            new[x] = new[x].lower()
            words.append(new[x+2])
            answTest.append('<answer instance' + new[x] + " senseid=" )
    words = concatTrain(words)
    splitTest(words)

#Seperates the words for the test file
def splitTest(l):
    global testwordsBe,testwordsAf
    for x in range(len(l)):
        if (l[x] == '<HEAD>LINE</HEAD>' or l[x] == '<HEAD>LINES</HEAD>'):
            testwordsBe.append([l[x-2],l[x-1])
            testwordsAf.append(l[x+1])  
    
# Finds the most likely word assiciation point for the test document
def associate():
    ph = 0
    pr = 0
    pl = 0
    global testwordsBe,testwordsAf
    for x in range(len(testwordsBe)):
        ph = phBe.get(testwordsBe[x], 0)
        pr = prBe.get(testwordsBe[x], 0)
        if(ph > pr):
            format(pl, "\"phone\"")
            pl += 1
        elif(ph < pr):
            format(pl, "\"product\"")
            pl += 1
        else:
            ph = phAf.get(testwordsAf[x], 0)
            pr = prAf.get(testwordsAf[x], 0)
            if(ph > pr):
                format(pl, "\"phone\"")
                pl += 1
            elif(ph < pr):
                format(pl, "\"product\"")
                pl += 1
            else:
                format(pl, "\"phone\"")
                pl += 1
        
#completes answers in the answer list for output           
def format(pl, answ):
    answTest[pl] += answ + '/>\n'

#combines the words into text
def combo():
    global answTest
    comb = ' '
    return (comb.join(answTest))

    

###### MAIN PROCESS ######
train = sys.argv[1]
test = sys.argv[2]
listTrain(inputTrain(train))
listTest(inputTrain(test))

phDList = concatTrain(phDList)
prDList = concatTrain(prDList)

splitTrain()
associate()

f = combo()
print(f)




