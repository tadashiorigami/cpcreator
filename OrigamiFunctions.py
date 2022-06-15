import OrigamiClasses as oc
from math import atan2, degrees, radians

def cptoorigami(filename):
    filename = open(filename, 'r')
    ori = oc.Origami()
    line = filename.readline()
    # print(line)
    while line:
        coordinates = line.split()
        point1 = (round(float(coordinates[1]),8), round(float(coordinates[2]),8))
        point2 = (round(float(coordinates[3]),8), round(float(coordinates[4]),8))
        if abs(point1[0]) <= 200 and abs(point1[1]) <= 200 and abs(point2[0]) <= 200 and abs(point2[1]) <= 200:
            if point1 not in ori.points:
                ori.points.append(point1)
            if point2 not in ori.points:
                ori.points.append(point2)
            ori.lines.append((point1,point2))
        line = filename.readline()
        # print(line)
    # print(ori.lines)
    return ori

#Function to take an origami class and export as a .CP file
def exportCP(origami, filename):
    with open(filename, 'w') as f:
        for line in origami.lines:
            linetype = "2 "
            if line[0][0] == -200 and line[1][0] == -200:
                    linetype = "1 "
            elif line[0][1] == -200 and line[1][1] == -200:
                    linetype = "1 "
            elif line[0][0] == 200 and line[1][0] == 200:
                    linetype = "1 "
            elif line[0][1] == 200 and line[1][1] == 200:
                    linetype = "1 "                      
            f.write(linetype + str(line[0][0]) + " " + str(line[0][1]) + " " + str(line[1][0]) + " " + str(line[1][1]) + '\n')

#Function to get angle between two points
def get_angle(point_1, point_2): #These can also be four parameters instead of two arrays
    angle = atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])
    
    #Optional
    angle = degrees(angle) + 180
    
    return angle

def testAngles(origami):
    
    #Select the angle to calculate deviation from
    # deviationAngle = 11.25

    middlePoints = []
    excessAngles = 0 #Sums the excess angles - CP must be 0
    excessAngleCounter = 0 #counts to make the average of sums
    
    # Lists middle points
    for point in origami.points:
        if point[0] != -200 and point[0] != 200 and point[1] != -200 and point[1] != 200:
            middlePoints.append(point)
    
    for point in middlePoints:
        
        connectedpoints = []
        angles = []
        excessAngleInPoint = 0
        for line in origami.lines:
           if point in line:
                connectedpoints.append(line[line.index(point)-1])
       
        
        # if connection == 1:
            # print(point)
        for cpoint in connectedpoints:
            angles.append(get_angle(point, cpoint))
        angles.sort()
        excessAngleInPoint = 360-angles[-1]+angles[0] 
        for i in range(1, len(angles)):
            excessAngleInPoint =  excessAngleInPoint + (angles[i]-angles[i-1])*pow(-1,i)
        excessAngleInPoint = abs(round(excessAngleInPoint,6))
        excessAngles = (excessAngles*excessAngleCounter + excessAngleInPoint)/(excessAngleCounter+1)
        excessAngleCounter = excessAngleCounter + 1
        # print(excessAngles)
    excessoutput = (-1)*(excessAngles/90*2-1)
    # print(excessoutput)

    return excessoutput

def testEven(origami):
    
    middlePoints = []
    
    # Lists middle points
    for point in origami.points:
        if point[0] != -200 and point[0] != 200 and point[1] != -200 and point[1] != 200:
            middlePoints.append(point)
    
    
    connections = [0]*17 # The index indicates the number of connections in each point
    
    for point in middlePoints:
        connection = 0
        for line in origami.lines:
           if point in line:
                connection = connection + 1
        if connection < 17:
            connections[connection] = connections[connection]+1
        
    # Append only the sum of evens and sum of odds with high bias
    # print("Connections %s = " % (connections))
    evenconections = 0
    oddconnections = 0
    for i in range(len(connections)):
        if i % 2 == 0:
            evenconections = evenconections + connections[i]
        else:
            oddconnections = oddconnections + connections[i]
        
    if (evenconections+oddconnections) == 0:
        evenconections = 1

    return evenconections/(evenconections+oddconnections)
