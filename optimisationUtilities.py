import sys
import numpy as np

''' what is allowed:
    1. Change order of lines;
    2. Change direction of lines.
    
    assumptions: 
    1. infinite acceleration (x=vt).
    2. No mark delays.
    
'''

# INPUT FOR  SCRIPT DEBUGGING
#| Xs | Ys | Xf | Yf |
#| 0. | 1. | 2. | 3. |

inputVectors = np.array([[  0. ,  10., 100.,   20.],
                         [  0.,  50., 100., 50.],
                         [  0., 100. ,100., 200.],
                         [  0., 240. ,100., 240.],
                         [  1., 1. ,5., 5.],
                         [  -5., -5. ,-1., 0.],
                         ])

# inputVectors = np.array([[  0. ,  0., 10.,   0.],
#                          [  0., 10. , 10.,  10.]])
#
#

inputVectors = np.array([[  0.1 ,  0.1, 5.,   5.],
                          [  5., 5. , 10.,  10.],
                          [  -5., -5. , 10.,  10.],
                          [  5., 10. , -5.,  10.],
                          [  0., 10. , -5.,  10.]]
                        )


inputVectors = np.array([[  0.1,  2., 10.,   1.],
                         [  3., 10. , 10.,  10.]])


inputVectors = np.array([[  0,  0, 0,   1],
                         [  0,  0.5, 0,   1],
                         [  0,  0.5, 0,   1],
                         ])


inputVectors = np.array([[  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0, 0,   1],
                         [  0,  0.5, 0,   1],
                         ])



def swapVectorDirection(vector):
    vectorOut = np.empty_like(vector)
    vectorOut = [vector[2], vector[3], vector[0], vector[1]]
    return vectorOut

def calculateMarkTimes(markSpeed, vectorArray):
    totalLength = 0
    for vector in vectorArray:
        xStart = vector[0]; yStart = vector[1]
        xEnd = vector[2];   yEnd = vector[3]
        dx = xEnd - xStart
        dy = yEnd - yStart
        lineLength = np.sqrt(dx**2 + dy**2)
        totalLength += lineLength
    totalTime = totalLength/markSpeed

    return [totalTime]
#
# def calculateJumpTimes(jumpSpeed, vectorArray):
#     totalLength = 0
#     for i in range(len(vectorArray)-1):
#         vector = vectorArray[i]
#         nextVector = vectorArray[i+1]
#         xStart = vector[2]    # starts where the first line finished
#         xEnd = nextVector[0]  # ends where the next line starts
#         yStart = vector[3]
#         yEnd = nextVector[1]
#         dx = xEnd - xStart
#         dy = yEnd - yStart
#         lineLength = np.sqrt(dx**2 + dy**2)
#         totalLength += lineLength
#     totalTime = totalLength/jumpSpeed
#     return [totalTime]

def findStartCoordinates(vector4):
    startCoordinates = vector4[0:2]
    return startCoordinates

def findEndCoordinates(vector4):
    endCoordinates = vector4[2:4]
    return endCoordinates

def calculateJumpTimes(jumpSpeed, vectorArray):
    totalLength = 0
    for i in range(len(vectorArray)-1):
        vector = vectorArray[i]
        nextVector = vectorArray[i+1]
        # xStart = vector[2]    # starts where the first line finished
        # yStart = vector[3]
        [xStart, yStart] = findEndCoordinates(vector)
        [xEnd, yEnd] = findStartCoordinates(nextVector)   # ends where the next line starts

        dx = xEnd - xStart
        dy = yEnd - yStart

        lineLength = np.sqrt(dx**2 + dy**2)
        totalLength += lineLength
    totalTime = totalLength/jumpSpeed
    return [totalTime]

def calculateHypotenuse(vector2):
    return np.sqrt(vector2[0]**2+vector2[1]**2)


def findClosestVectorToOrigin(vectorArrayModified):
    indexXYdirect = np.argmin(
        np.abs(np.array(vectorArrayModified[:,0]) - 0)+np.abs(np.array(vectorArrayModified[:,1]) - 0))  # min XY strart
    indexXYreversed = np.argmin(
        np.abs(np.array(vectorArrayModified[:, 2]) - 0) + np.abs(np.array(vectorArrayModified[:, 3]) - 0))

    pivotVectorDirect = (findStartCoordinates(vectorArrayModified[indexXYdirect]))
    pivotVectorReverse = (findEndCoordinates(vectorArrayModified[indexXYreversed]))

    distanceFromOriginDirect = calculateHypotenuse(pivotVectorDirect)
    distanceFromOriginReverse = calculateHypotenuse(pivotVectorReverse)

    if distanceFromOriginReverse>distanceFromOriginDirect:
        indexOfFirstVector = indexXYdirect
    else:
        indexOfFirstVector = indexXYreversed
        vectorArrayModified[indexOfFirstVector] = swapVectorDirection(vectorArrayModified[indexOfFirstVector])
    print("first vector is: ", vectorArrayModified[indexOfFirstVector])


def optimiseOrderOfVectors(vectorArrayInput):
    print("Jump time before optimisation: ", calculateJumpTimes(1, vectorArrayInput))
    vectorArray = vectorArrayInput.copy()

    print("vectorArray:\n", vectorArray)
    sortedArray = np.zeros(shape=np.shape(vectorArray))

    # 0th column: dist. from end point to end; 1st: from dist. from end point to start
    distanceArray = np.zeros([len(vectorArray), 2])
    sortedArray[0, :] = vectorArray[0, :]  #
    indexArray=np.zeros([len(vectorArray)], dtype=int)
    indexArray[0] = 0

    for i in range(1, len(vectorArray)-1):
        endCoordinates = findEndCoordinates(sortedArray[i-1,:])
        print("endCoordinates: \n", endCoordinates)
        '''end to start of new vector distance'''
        distanceArray[:, 0] = np.sqrt((vectorArray[:, 0] - endCoordinates[0])**2 + (vectorArray[:, 1] - endCoordinates[1])**2)
        '''end to end of new vector distance'''
        distanceArray[:, 1] = np.sqrt((vectorArray[:, 2] - endCoordinates[0])**2 + (vectorArray[:, 3] - endCoordinates[1])**2)

        print("distanceArray:\n", distanceArray)
        '''minimum of distances except current:'''
        minDirect = min(distanceArray[i:, 0])
        minInverse = min(distanceArray[i:, 1])
        print("minDirect:   :", minDirect)
        print("minInversed  :", minInverse)

        if minInverse >= minDirect:
            itemindex = np.argmin(distanceArray[i:, 0]) + i
            nextVector = (vectorArray[itemindex, :])
            indexArray[i] = itemindex
            print("itemindex: ", itemindex)
        else:
            # swap direction of the min vector.
            itemindex = np.argmin(distanceArray[i:, 1]) + i
            nextVector = swapVectorDirection(vectorArray[itemindex, :])
            indexArray[i] = itemindex
            print("itemindex: ", itemindex)
            print("swap!")
        sortedArray[i, :] = nextVector
        print("sortedArray:\n", sortedArray)
        print("indexArray:\n", indexArray)

    setIndexArray = set(indexArray.flatten())
    setEnumerate = set(range(len(vectorArray)))
    uniqueIndexSet = setEnumerate - setIndexArray
    uniqueIndex = uniqueIndexSet.pop()
    # print("setEnumerate:\n", type(setEnumerate))
    # print("setEnumerate:\n", (setEnumerate))
    # print("setIndexArray:\n", type(setIndexArray))
    # print("setIndexArray:\n", (setIndexArray))
    # print("uniqueIndex:\n", (uniqueIndex))


    print("*"*10)
    print("sortedArray[len(sortedArray), :]:\n", sortedArray[-1, :])
    print("vectorArray[uniqueIndex,:]  \n", vectorArray[uniqueIndex,:])

    sortedArray[-1, :] = vectorArray[uniqueIndex,:]
    print("*"*10)
    print("*"*10)
    print("sortedArray:\n", sortedArray)
    print("Jump time after optimisation: ", calculateJumpTimes(1, sortedArray))
    return sortedArray


def optimiseDirectionsNeighbouringVectors(vectorArray):
    #print("Mark time before optimisation: ", calculateMarkTimes(1, inputVectors))
    print("Jump time before optimisation: ", calculateJumpTimes(1, inputVectors))

    vectorArrayModified = vectorArray.copy()
    for i in range(1, len(vectorArrayModified[:, 0])):
        dxDirect = vectorArrayModified[i, 2] - vectorArrayModified[i - 1, 0]
        dyDirect = vectorArrayModified[i, 3] - vectorArrayModified[i - 1, 1]
        dxInverse = vectorArrayModified[i, 2] - vectorArrayModified[i - 1, 2]  # swap beginning of the next line to start position of the previous line
        dyInverse = vectorArrayModified[i, 2] - vectorArrayModified[i - 1, 2]
        travelDirect = np.sqrt(dxDirect**2 + dyDirect**2)
        travelInverse = np.sqrt(dxInverse ** 2 + dyInverse ** 2)
        if travelInverse < travelDirect:
            vectorArrayModified[i, :] = swapVectorDirection(vectorArrayModified[i, :])

        #print("Mark time after optimisation: ", calculateMarkTimes(1, inputVectors))
        print("Jump time after optimisation: ", calculateJumpTimes(1, vectorArrayModified))
    return vectorArrayModified


