from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter

def createExamples():
    numberArrayExamples = open("numArEx.txt","a")
    numbersWeHave = range(0,4) #originally (0,10)
    versionsWeHave = range(1,10) #originally (1,10)

    for eachFace in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = "images/data/" + str(eachFace) + "." + str(eachVer) + ".jpg"
            ei = Image.open(imgFilePath)
            eiar = threshold(np.array(ei))
            #eiar = np.array(ei)
            eiar1 = str(eiar.tolist())

            lineToWrite = str(eachFace) + "::" + eiar1 + "\n"
            numberArrayExamples.write(lineToWrite)

def threshold(imageArray):
    balanceAr = []
    total = 0
    newAr = imageArray

    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = (eachPix[0]+eachPix[1]+eachPix[2])/3
            balanceAr.append(avgNum)
    for n in balanceAr:
        total+=n
    balance=total/len(balanceAr)
    
    for eachRow in newAr:
        for eachPix in eachRow:
            avgNum = (eachPix[0]+eachPix[1]+eachPix[2])/3
            if avgNum > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                #eachPix[3] = 255

            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                #eachPix[3] = 255
                
    return newAr

def whatNumIsThis(filePath):
    matchedAr = []
    loadExamples = open("numArEx.txt","r").read()
    loadExamples = loadExamples.split("\n")

    i = Image.open(filePath)
    iar = threshold(np.array(i))
    #iar = np.array(i)
    iarl = iar.tolist()

    inQuestion = str(iarl)

    for eachExample in loadExamples:
        if len(eachExample) > 3:
            splitEx = eachExample.split("::")
            currentNum = splitEx[0]
            currentAr = splitEx[1]

            eachPixEx = currentAr.split("],")
            eachPixInQ = inQuestion.split("],")

            x = 0
            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))

                x += 1

    x = Counter(matchedAr)
    print(x)
    k = str(x)[9:10]
    f = open("names.txt","r")
    r = f.readlines()
    r = [s.strip("\n") for s in r]
    a = ""
    for i in range(0,len(r)):
        if r[i] == str(k) and r[i-1] == "":
            a += str(r[i+1])
    print(a)
    f.close()
    
    graphX= []
    graphY = []

    for eachThing in x:
        graphX.append(eachThing)
        graphY.append(x[eachThing])

    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4),(1,0), rowspan=1, colspan=4)

    ax1.imshow(iar)
    ax2.bar(graphX,graphY, align="center")
    plt.ylim(400)

    xloc = plt.MaxNLocator(12)

    ax2.xaxis.set_major_locator(xloc)
    #plt.show()

createExamples()
whatNumIsThis("images/test" + input("Which photo?: ") + ".jpg")
time.sleep(10)
