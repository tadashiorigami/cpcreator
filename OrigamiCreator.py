import random
import itertools
import OrigamiClasses as oc

printcomments = 0
create1pointline = 0.2
create2pointline = 0.2
randomPoint = 0.5
connect2points = 0.2

def randomCPInstructions(loops):
    # Create corners
    # Create cycle:
    # Select area->
    # Select if create new points on line (0 1 or 2) -> 
    # if 0, skip, if 1, connect point to one existing edge, if 2, connect both points -> 
    # Ennumerate new areas ->
    # Select if create random point
    # - Case YES: Create random point, find the area it's in, find the area it's in, select one triangle (if inside) to connect the lines
    # Repeat
    
   
    #chances of creating each part
    
    
    # Instructions composed by cycles, each cycle on one line of the array.
    # Each instruction line will be as [a,b,c,d,e,f,g,h]
    # a = area index for the first new points
    # b = new points in area (0, 1, 2)
    # c = index of line to make first point (0 to 100, make mod len(lines in area))
    # d = index of line number 2 different from line 1. If there's no line 2, index of point to make the line
    # e = percentage of line 1
    # f = percentage of line 2
    # g = point to connect to if 1
    # h = create random point yes or no
    # i = xRAND
    # j = yRAND
    # k = index of triangle to connect to (mod number of triangles the point is inside)
    # l = if 1 connect two points in an area with more than 4 points
    # m = Index of area to connect
    # n = Index of first point
    # o = Index of second point
    
    instructions = []
    
    for loop in range(0,loops):
        
        a = random.randint(0,loop)
        b = random.random()
        if b < create1pointline:
            b = 1
        elif b < create1pointline + create2pointline:
            b = 2
        else:
            b = 0
        c = random.randint(0,100)
        d = random.randint(0,100)
        e = random.random()
        f = random.random()
        g = random.randint(0,100) 
        h = random.random()
        if h < randomPoint:
            h = 1
        else:
            h = 0
        i = random.random()*1.96- 0.98
        j = random.random()*1.96- 0.98
        k = random.randint(0,20)
        l = random.random()
        if l < connect2points:
            l = 1
        else:
            l = 0
        m = random.randint(0,loop)
        n = random.randint(0,100)
        o = random.randint(0,100)
        instructions.append((a,b,c,d,e,f,g,h,i,j,k,l,m,n,o))
        
    return instructions
        
#function to input instructions and output CP lines
def createFromInstructions(instructions):

    points = []
    areas = [] #sets of 3 or more lines
    lines = [] #sets of two points
    
    # Create corners
    points.append((-1,-1))
    points.append((-1,1))
    points.append((1,1))
    points.append((1,-1))
    lines.append((points[0],points[1]))
    lines.append((points[1],points[2]))
    lines.append((points[2],points[3]))
    lines.append((points[3],points[0]))
    areas.append([lines[0],lines[1],lines[2],lines[3]])
    
    for instr in instructions:
        # Check area index 
        areaIndex = instr[0]%len(areas)
        pointsType = instr[1]
        line1Index = instr[2]%len(areas[areaIndex])
        line2Index = instr[3]%len(areas[areaIndex])
        if line2Index == line1Index:
            line2Index = line2Index-1
        line1 = areas[areaIndex][line1Index]
        line2 = areas[areaIndex][line2Index]
        percentageL1 = instr[4]
        percentageL2 = instr[5]
        
        
        if pointsType == 1:
            if printcomments:
                print("Starting Division type 1")
            #select starting point
            startingpoint = findPointInLine(line1,percentageL1)
            lines.append((startingpoint, line1[0]))
            lines.append((startingpoint, line1[1]))
            lines.pop(lines.index(areas[areaIndex][line1Index]))
            
            # As there's only one point created, we take the second one from the list in areas[areaIndex]
            possiblepoints = []
            for possiblelines in areas[areaIndex]:
                possiblepoints.append(possiblelines[0])
                possiblepoints.append(possiblelines[1])
            selectedLine = areas[areaIndex][line1Index]
            while selectedLine[0] in possiblepoints:
                possiblepoints.pop(possiblepoints.index(selectedLine[0]))
            while selectedLine[1] in possiblepoints:
                possiblepoints.pop(possiblepoints.index(selectedLine[1]))
            
            # Select point from possible points
            endpoint = possiblepoints[instr[6]%len(possiblepoints)]
            
            # Appends the created line
            lines.append((startingpoint, endpoint))
            if printcomments:
                print("Done creating line" + str(lines[-1]))
            
            # find new area 1
            areas[areaIndex].pop(areas[areaIndex].index(line1))
            newArea = []
            nextPoint = line1[0]
            if printcomments:
                print("Finding first area division type 1")
            while nextPoint != endpoint:
                for i in range(0,len(areas[areaIndex])):
                    if nextPoint in areas[areaIndex][i]:
                        if printcomments:
                            print("next point = " + str(nextPoint))
                            print("Found in: " + str(areas[areaIndex][i]))
                            print("Final point = " + str(endpoint))
                        newArea.append(areas[areaIndex][i])
                        nextPoint = areas[areaIndex][i][areas[areaIndex][i].index(nextPoint)-1]
                        areas[areaIndex].pop(i)
                        break
            newArea.append((startingpoint, endpoint))
            newArea.append((startingpoint, line1[0]))
            areas.append(newArea)
            if printcomments:
                print("Done creating area" + str(newArea))
            
            #find new area 2
            if printcomments:
                print("Finding Second area division type 1")
            newArea = []
            nextPoint = line1[1]
            while nextPoint != endpoint:
                for i in range(0,len(areas[areaIndex])):
                    if nextPoint in areas[areaIndex][i]:
                        if printcomments:
                            print("next point = " + str(nextPoint))
                            print("Found in: " + str(areas[areaIndex][i]))
                            print("Final point = " + str(endpoint))
                        newArea.append(areas[areaIndex][i])
                        nextPoint = areas[areaIndex][i][areas[areaIndex][i].index(nextPoint)-1]
                        areas[areaIndex].pop(i)
                        break
            newArea.append((startingpoint, endpoint))
            newArea.append((startingpoint, line1[1]))
            areas.append(newArea)
            if printcomments:
                print("Done creating area" + str(newArea))
            
            # remove area (now divided)
            areas.pop(areaIndex)
            
            
            if printcomments:
                print("Division done, Starting areas correction")
            #correct areas with previous line
            for area in areas:
                if line1 in area:
                    areas[areas.index(area)].append((startingpoint, line1[0]))
                    areas[areas.index(area)].append((startingpoint, line1[1]))
                    areas[areas.index(area)].pop(areas[areas.index(area)].index(line1))
            # print("Correction done")
            
            
        #case 2: two points in lines
        if pointsType == 2:
            if printcomments:
                print("Creating division type 2")
            startingpoint = findPointInLine(line1,percentageL1)
            lines.append((startingpoint, line1[0]))
            lines.append((startingpoint, line1[1]))
            lines.pop(lines.index(line1))
            
            endpoint = findPointInLine(line2,percentageL2)
            lines.append((endpoint, line2[0]))
            lines.append((endpoint, line2[1]))
            lines.pop(lines.index(line2))
            
            lines.append((startingpoint, endpoint))
            if printcomments:
                print("Done creating line" + str(lines[-1]))
        #     # Find new areas

            areas[areaIndex].pop(areas[areaIndex].index(line1))
            areas[areaIndex].pop(areas[areaIndex].index(line2))
            areas[areaIndex].append((endpoint, line2[0]))
            areas[areaIndex].append((endpoint, line2[1]))
            
            #     # Find area 1
            newArea = []
            
            nextPoint = line1[0]
            if printcomments:
                print("Finding first area divisions type 2")
                print("First point = " + str(nextPoint))
            while nextPoint != line2[0] and nextPoint != line2[1]:
                for i in range(0,len(areas[areaIndex])):
                    if nextPoint in areas[areaIndex][i]:
                        if printcomments:
                            print("next point = " + str(nextPoint))
                            print("Found in: " + str(areas[areaIndex][i]))
                            print("Final point = " + str(endpoint))
                        newArea.append(areas[areaIndex][i])
                        nextPoint = areas[areaIndex][i][areas[areaIndex][i].index(nextPoint)-1]
                        areas[areaIndex].pop(i)
                        break
            newArea.append((endpoint, nextPoint))
            newArea.append((startingpoint, endpoint))
            newArea.append((startingpoint, line1[0]))
            areas.append(newArea)
            if printcomments:
                print("Done creating area" + str(newArea))
            
        #     #Find area 2
            newArea = []
            nextPoint = line1[1]
            if printcomments:
                print("Finding Second area division type 2")
            while nextPoint != line2[0] and nextPoint != line2[1]:
                for i in range(0,len(areas[areaIndex])):
                    if nextPoint in areas[areaIndex][i]:
                        if printcomments:
                            print("next point = " + str(nextPoint))
                            print("Found in: " + str(areas[areaIndex][i]))
                            print("Final point = " + str(endpoint))
                        newArea.append(areas[areaIndex][i])
                        nextPoint = areas[areaIndex][i][areas[areaIndex][i].index(nextPoint)-1]
                        areas[areaIndex].pop(i)
                        break
            newArea.append((endpoint, nextPoint))
            newArea.append((startingpoint, endpoint))
            newArea.append((startingpoint, line1[1]))
            areas.append(newArea)
            if printcomments:
                print("Done creating area" + str(newArea))
            
            #remove area (now divided)
            areas.pop(areaIndex)
            if printcomments:
                print("Division done, Starting areas correction")
            
        #     correct areas with previous line
            for area in areas:
                if line1 in area:
                    areas[areas.index(area)].append((startingpoint, line1[0]))
                    areas[areas.index(area)].append((startingpoint, line1[1]))
                    areas[areas.index(area)].pop(areas[areas.index(area)].index(line1))
                if line2 in area:
                    areas[areas.index(area)].append((endpoint, line2[0]))
                    areas[areas.index(area)].append((endpoint, line2[1]))
                    areas[areas.index(area)].pop(areas[areas.index(area)].index(line2))

        
        ## Now check if create random point in CP
        create = instr[7]
        if create == 1:
            xNew = instr[8]
            yNew = instr[9]
            triangIndex = instr[10]
            selectedArea = None
            # Find which area the point is in
            for area in areas:
                count = 0
                possibleLine = []
                for line in area:
                    #count if 0 or 2 lines has xNew in the middle
                    if line[0][0] < xNew and line[1][0] > xNew:
                        possibleLine.append(line)
                        count = count + 1
                        if count == 2:
                            break
                    if line[0][0] > xNew and line[1][0] < xNew:
                        possibleLine.append(line)
                        count = count + 1
                        if count == 2:
                            break
                
                #test if point is inside one of triangles formed by possibleline 1 and 2
                if count == 2:
                    if printcomments:
                        print("Found two lines. Checking if in area")
                    if pointInTriangle((xNew, yNew), possibleLine[0][0], possibleLine[0][1], possibleLine[1][0]) or pointInTriangle((xNew, yNew), possibleLine[1][0], possibleLine[1][1], possibleLine[0][1]):
                            selectedArea = area
                            if printcomments:
                                print("Area OK")
                            break
            if selectedArea != None:
                # Find the selected triangle
                # first get all points
                areaPoints = []
    
                for line in selectedArea:
                    if line[0] not in areaPoints:
                        areaPoints.append(line[0])
                    if line[1] not in areaPoints:
                        areaPoints.append(line[1])    
                
                # Test all 3 points possibilities
                triangles = []
                len(areaPoints)
                for comb in itertools.combinations(areaPoints, 3):
                    if pointInTriangle((xNew,yNew), comb[0], comb[1], comb[2]):
                        triangles.append(comb)
                if printcomments:
                    print("Random Point: " + str(xNew) + " " + str(yNew))
                    print("Selected area points:" + str(areaPoints))
                # print("Possible Triangles" + str(triangles))
                
                
                #Select one triangle
                triangIndex = triangIndex%len(triangles)
                if printcomments:
                    print("Selected triangle = " + str(triangles[triangIndex]))
                
                # Add three new lines to lines set
                lines.append(((xNew,yNew),triangles[triangIndex][0]))
                lines.append(((xNew,yNew),triangles[triangIndex][1]))
                lines.append(((xNew,yNew),triangles[triangIndex][2]))
                
                
                # Remove selected area
                areas.pop(areas.index(selectedArea))
                
                # Add three new areas
                nextPointIndex = 0
                for i in range(0,3):
                    nextPoint = triangles[triangIndex][nextPointIndex]
                    if printcomments:
                        print("Making area " + str(i+1))
                    newArea = []
                    newArea.append(((xNew,yNew), triangles[triangIndex][nextPointIndex]))
                    while nextPoint != triangles[triangIndex][nextPointIndex-1] and nextPoint != triangles[triangIndex][nextPointIndex-2]:
                        for j in range(0,len(selectedArea)):
                            if nextPoint in selectedArea[j]:
                                if printcomments:
                                    print("next point = " + str(nextPoint))
                                    print("Found in: " + str(selectedArea[j]))
                                    print("Final point = " + str(triangles[triangIndex][nextPointIndex-1]) + " or " + str(triangles[triangIndex][nextPointIndex-2]))
                                newArea.append(selectedArea[j])
                                nextPoint = selectedArea[j][selectedArea[j].index(nextPoint)-1]
                                selectedArea.pop(j)
                                break
                    nextPointIndex = triangles[triangIndex].index(nextPoint)
                    
                    newArea.append(((xNew,yNew), nextPoint))
                    areas.append(newArea)
                    if printcomments:
                        print("New area:")
                        print(newArea)
            
        ## Now check if make line between two points in an area with more than 3 points
        connect2 = instr[11]
        if connect2 == 1:
            if printcomments:
                print("Connecting two points")
            areaIndex = instr[12]
            point1Index = instr[13]
            point2Index = instr[14]
            
            #List possible areas
            possibleAreas = []
            
            for area in areas:
                if len(area) > 3:
                    possibleAreas.append(area.copy())
                    
            if printcomments:
                print("Possible areas: " + str(possibleAreas))
            
            # Check if any
            if len(possibleAreas) > 0:
                
                # Find the correct index for area among possibilities
                areaIndex = areaIndex%len(possibleAreas)
                selectedArea = possibleAreas[areaIndex].copy()
                
                if printcomments:
                    print("Area amount = " + str(len(areas)))
                    print("Selected area " + str(selectedArea))
                    
                selectedArea2 = selectedArea.copy()
                point1Index = point1Index%len(selectedArea)
                if printcomments:
                    print("Area Lenght = " + str(len(selectedArea)))
                    print("Point 1 index = " + str(point1Index))
                point2Index = point1Index - point2Index%(len(selectedArea)-3) - 2
                if printcomments:
                    print("Point 2 index = " + str(point2Index))
                generalAreaIndex = areas.index(selectedArea)
                possiblePoints = []
                
                # Append the points in correct order
                firstPoint = possibleAreas[areaIndex][0][0]
                nextPoint = firstPoint
                while 1:
                    for line in selectedArea:
                        if line[0] == nextPoint:
                            nextPoint = line[1]
                            possiblePoints.append(nextPoint)
                            selectedArea.pop(selectedArea.index(line))
                            break
                        if line[1] == nextPoint:
                            nextPoint = line[0]
                            possiblePoints.append(nextPoint)
                            selectedArea.pop(selectedArea.index(line))
                            break
                    if nextPoint == firstPoint:
                        break
                if printcomments:
                    print("Possible points = " + str(possiblePoints))
                point1 = possiblePoints[point1Index]
                point2 = possiblePoints[point2Index]
                if printcomments:
                    print("selected points = " + str(point1) + str(point2))
                # Use the selected points
                lines.append((point1,point2))
                nextPoint = point1
                # Make the two new areas
                newArea1 = []
                newArea2 = []
                while 1:
                    for line in selectedArea2:
                        if line[0] == nextPoint:
                            nextPoint = line[1]
                            newArea1.append(line)
                            selectedArea2.pop(selectedArea2.index(line))
                            break
                        if line[1] == nextPoint:
                            nextPoint = line[0]
                            newArea1.append(line)
                            selectedArea2.pop(selectedArea2.index(line))
                            break
                    if nextPoint == point2:
                        break
                newArea1.append((point1,point2))
                
                nextPoint = point1
                while 1:
                    for line in selectedArea2:

                        if line[0] == nextPoint:
                            nextPoint = line[1]
                            newArea2.append(line)
                            selectedArea2.pop(selectedArea2.index(line))
                            break
                        if line[1] == nextPoint:
                            nextPoint = line[0]
                            newArea2.append(line)
                            selectedArea2.pop(selectedArea2.index(line))
                            break
                    if nextPoint == point2:
                        break
                newArea2.append((point1,point2))
                areas.pop(generalAreaIndex)
                areas.append(newArea1)
                areas.append(newArea2)
                if printcomments:
                    print("Area amount = " + str(len(areas)))
                    print("Selected area " + str(selectedArea))
                    
        if printcomments:
            print("Instruction done \n\n")

    newOrigami = oc.Origami()
    for i in range(0,len(lines)):
        point1 = (round(lines[i][0][0]*200,8), round(lines[i][0][1]*200,8))
        point2 = (round(lines[i][1][0]*200,8), round(lines[i][1][1]*200,8))
        if abs(point1[0]) <= 200 and abs(point1[1]) <= 200 and abs(point2[0]) <= 200 and abs(point2[1]) <= 200:
            if point1 not in newOrigami.points:
                newOrigami.points.append(point1)
            if point2 not in newOrigami.points:
                newOrigami.points.append(point2)
            newOrigami.lines.append((point1,point2)) 
    
    if printcomments:
        print("----------- CP CREATED ----------\n\n\n\n")
    return newOrigami

def findPointInLine(line, cut):
    # case 1 Vertical line
    xcut = (line[1][0] - line[0][0])*cut + line[0][0]
    ycut = (line[1][1] - line[0][1])*cut + line[0][1]
    return (xcut,ycut)

def pointInTriangle(pt, v1, v2, v3):
    d1 = sign(pt, v1, v2);
    d2 = sign(pt, v2, v3);
    d3 = sign(pt, v3, v1);
    if d1<0 or d2<0 or d3<0:
        has_neg = 1
    else:
        has_neg = 0
    if d1>0 or d2>0 or d3>0:
        has_pos = 1
    else:
        has_pos = 0
    if has_neg and has_pos:
        return 0
    else:
        return 1
    
def sign(p1,p2,p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1]);
