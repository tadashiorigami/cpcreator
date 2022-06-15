import OrigamiCreator as oc
import NNTraining as nnt
import numpy as np
import random
import OrigamiFunctions as of


## Choosing GA parameters
generations = 100
weights = "firsttest.h5"
mutationProb = 0.1
smallMutationProb = 0.1

# Random mutation parameters
printcomments = 0
create1pointline = 0.1
create2pointline = 0.1
randomPoint = 0.5
connect2points = 0.2
instructionsLines = 10
maintainTop = 0
forceSmallEvo = 0
minimumlines = 20
nudgedivisor = 10000
divisor = 1

#Neural Network parameters
arraySize = 8

#Function to create a population of instructions
def randomInstructionsPop(amount):
    instructionsPop = []
    for i in range(0,amount):
        instructionsPop.append(oc.randomCPInstructions(instructionsLines))
    return instructionsPop

def showScores(instructionsPopulation):
    cpPopulation = []
    for instruction in instructionsPopulation:
        cpPopulation.append(oc.createFromInstructions(instruction))
    resultsNP = nnt.testCPs(cpPopulation, weights)
    results = []
    for i in range(len(resultsNP)):
        results.append(resultsNP[i][1])
    print(results)

def evolveInstructions(instructionsPopulation , mutationType = 0, scores = None):
    cpPopulation = []
    populationSize = len(instructionsPopulation)
    
    
        
    if scores == None:
        for instruction in instructionsPopulation:
            cpPopulation.append(oc.createFromInstructions(instruction))
        scores = []
        resultsNP = nnt.testCPs(cpPopulation, weights)
        for i in range(0,populationSize):
            scores.append(resultsNP[i][1]*100)

    # print(scores)
    
    # Create next population
    new_parents = selectInstructionsPopulation(instructionsPopulation, scores, 2)
    # print("Selection #1 = " + str(instructionsPopulation.index(new_parents[0])))
    # print("Selection #2 = " + str(instructionsPopulation.index(new_parents[1])))
    
    nextPop = []
    nextPop.append(new_parents[0])
    nextPop.append(new_parents[1])
    # max_score = max(scores)
    # Nextpop #0 is the highest score
    # print("Max score index = " + str(scores.index(max(scores))))
    if maintainTop == 1:
        nextPop[0] = instructionsPopulation[scores.index(max(scores))]
    

    for i in range(1, int(populationSize/2)):
        # print("testing top scorer 1 " + str(cpdisc.testCP(oc.convertToNumpyArray(oc.createFromInstructions(nextPop[0])), weights)[0][1]))
        # print("Making crossover")
        offspring = singlePointCrossover(new_parents[0],new_parents[1])
        offspring_1 = offspring[0][:]
        offspring_2 = offspring[1][:]
        # print("testing top scorer 1 " + str(cpdisc.testCP(oc.convertToNumpyArray(oc.createFromInstructions(nextPop[0])), weights)[0][1]))
        # print("Mutating ")
        nextPop.append(mutateInstruction(offspring_1, mutationProb, mutationType))
        nextPop.append(mutateInstruction(offspring_2, mutationProb, mutationType))
    
    
    for instruction in nextPop:
        cpPopulation.append(oc.createFromInstructions(instruction))
    scores = []
    resultsNP = nnt.testCPs(cpPopulation, weights)
    for i in range(0,populationSize):
        scores.append(resultsNP[i][1]*100)
        
            
    max_score = max(scores)
    if max_score < 1e-20:
        for i in range(0,populationSize):
            scores[i] = 1
    # print(scores)
    # print("Max score = " + str(max_score))
    topcontender = instructionsPopulation[scores.index(max(scores))]
    
    return nextPop, topcontender, max_score, scores

def nudgeInstructions(instructionsPopulation , mutationType = 2, scores = None, divisor = 5):
    cpPopulation = []
    populationSize = len(instructionsPopulation)
    
    
        
    if scores == None:
        for instruction in instructionsPopulation:
            cpPopulation.append(oc.createFromInstructions(instruction))
        scores = []
        for i in range(0,populationSize):
            scores.append(of.testAngles(cpPopulation[i]))

    # print(scores)
    
    # Create next population
    new_parents = selectInstructionsPopulation(instructionsPopulation, scores, 2)
    # print("Selection #1 = " + str(instructionsPopulation.index(new_parents[0])))
    # print("Selection #2 = " + str(instructionsPopulation.index(new_parents[1])))
    
    nextPop = []
    nextPop.append(new_parents[0])
    nextPop.append(new_parents[1])
    max_score = max(scores)

    # Nextpop #0 is the highest score
    # print("Max score index = " + str(scores.index(max(scores))))
    nextPop[0] = instructionsPopulation[scores.index(max(scores))]
    

    for i in range(1, int(populationSize/2)):
        # print("testing top scorer 1 " + str(cpdisc.testCP(oc.convertToNumpyArray(oc.createFromInstructions(nextPop[0])), weights)[0][1]))
        # print("Making crossover")
        offspring = singlePointCrossover(new_parents[0],new_parents[1])
        offspring_1 = offspring[0][:]
        offspring_2 = offspring[1][:]
        # print("testing top scorer 1 " + str(cpdisc.testCP(oc.convertToNumpyArray(oc.createFromInstructions(nextPop[0])), weights)[0][1]))
        # print("Mutating ")
        nextPop.append(mutateInstruction(offspring_1, mutationProb, mutationType, divisor))
        nextPop.append(mutateInstruction(offspring_2, mutationProb, mutationType, divisor))
            
    # newCPs = []
    # for person in nextPop:
    #     newCPs.append(oc.createFromInstructions(instruction))
    
    cpPopulation = []
    populationSize = len(instructionsPopulation)
    for instruction in nextPop:
        cpPopulation.append(oc.createFromInstructions(instruction))
        
    scores = []
    for i in range(0,populationSize):
        scores.append(of.testAngles(cpPopulation[i]))
             
    max_score = max(scores)
    # print(scores)
    # print("Max score = " + str(max_score))
    topcontender = instructionsPopulation[scores.index(max(scores))]
    
    return nextPop, topcontender, max_score, scores

def helpEvenInstructions(instructionsPopulation , mutationType = 2, scores = None):
    cpPopulation = []
    populationSize = len(instructionsPopulation)
    
    if scores == None:
        for instruction in instructionsPopulation:
            cpPopulation.append(oc.createFromInstructions(instruction))
        scores = []
        for i in range(0,populationSize):
            scores.append(of.testEven(cpPopulation[i]))

    # print(scores)
    
    # Create next population
    new_parents = selectInstructionsPopulation(instructionsPopulation, scores, 2)
    # print("Selection #1 = " + str(instructionsPopulation.index(new_parents[0])))
    # print("Selection #2 = " + str(instructionsPopulation.index(new_parents[1])))
    
    nextPop = []
    nextPop.append(new_parents[0])
    nextPop.append(new_parents[1])
    max_score = max(scores)
    # Nextpop #0 is the highest score
    # print("Max score index = " + str(scores.index(max(scores))))
    nextPop[0] = instructionsPopulation[scores.index(max(scores))]
    

    for i in range(1, int(populationSize/2)):
        # print("testing top scorer 1 " + str(cpdisc.testCP(oc.convertToNumpyArray(oc.createFromInstructions(nextPop[0])), weights)[0][1]))
        # print("Making crossover")
        offspring = singlePointCrossover(new_parents[0],new_parents[1])
        offspring_1 = offspring[0][:]
        offspring_2 = offspring[1][:]
        # print("testing top scorer 1 " + str(cpdisc.testCP(oc.convertToNumpyArray(oc.createFromInstructions(nextPop[0])), weights)[0][1]))
        # print("Mutating ")
        nextPop.append(mutateInstruction(offspring_1, mutationProb, 0))
        nextPop.append(mutateInstruction(offspring_2, mutationProb, 0))
            
    # newCPs = []
    # for person in nextPop:
    #     newCPs.append(oc.createFromInstructions(instruction))
    
    cpPopulation = []
    populationSize = len(instructionsPopulation)
    for instruction in nextPop:
        cpPopulation.append(oc.createFromInstructions(instruction))
        
    scores = []
    for i in range(0,populationSize):
        scores.append(of.testEven(cpPopulation[i]))
             
    max_score = max(scores)
    # print(scores)
    # print("Max score = " + str(max_score))
    topcontender = instructionsPopulation[scores.index(max(scores))]
    
    return nextPop, topcontender, max_score, scores

def selectInstructionsPopulation(populationchoices, scores, k=2): 
    #first selection
    population = populationchoices[:]
    scoresSum = 0.0
    selection = []
    for score in scores:
        scoresSum = scoresSum + score
    
    #for random first
    firstSelection = random.random()*scoresSum
    counter = 0.0
    for i in range(0,len(scores)):
        counter = counter + scores[i]
        if counter > firstSelection:
            selection.append(population[i])
            scores = np.delete(scores,i,0)
            population.pop(i)
            break
      
    #second selection
    scoresSum = 0.0
    for score in scores:
        scoresSum = scoresSum + score
    firstSelection = random.random()*scoresSum
    counter = 0.0
    for i in range(0,len(scores)):
        counter = counter + scores[i]
        if counter > firstSelection:
            selection.append(population[i])
            break
        
    return selection

def singlePointCrossover(genomeA, genomeB): 

    length = len(genomeA)
    cut = random.randint(1, length-1)
    # print("offspring cut at " + str(cut))
    offspringA = []
    offspringB = []
    for i in range(0,length):
        if i < cut:
            offspringA.append(genomeA[i])
            offspringB.append(genomeB[i])
        else:
            offspringA.append(genomeB[i])
            offspringB.append(genomeA[i])

    return [offspringA,offspringB]

def mutateInstruction(genome , p, type=0, divisor=1):
    newgenome = []
    linecount = 0
    eraser = 0
    for gene in genome:
        if gene[1] != 0:
             linecount = linecount+1
        if gene[7] != 0:
             linecount = linecount+1
        if gene[11] != 0:
             linecount = linecount+1
    if linecount >= minimumlines:
        eraser = 1
    for gg in range(0,len(genome)):
        if p < random.random():
            newgenome.append(genome[gg])
        else:
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
            # 0  a = area index for the first new points
            # 1  b = new points in area (0, 1, 2)
            # 2  c = index of line to make first point (0 to 100, make mod len(lines in area))
            # 3  d = index of line number 2 different from line 1. If there's no line 2, index of point to make the line
            # 4  e = percentage of line 1
            # 5  f = percentage of line 2
            # 6  g = point to connect to if 1
            # 7  h = create random point yes or no
            # 8  i = xRAND
            # 9  j = yRAND
            # 10 k = index of triangle to connect to (mod number of triangles the point is inside)
            # 11 l = if 1 connect two points in an area with more than 4 points
            # 12 m = Index of area to connect
            # 13 n = Index of first point
            # 14 o = Index of second point
            
            if type == 0:
                a = random.randint(0,gg)

                b = random.random()
                if b < create1pointline:
                    b = 1
                elif b < create1pointline + create2pointline:
                    b = 2
                elif eraser:
                    b = 0
                else:
                    b = genome[gg][1]
               
                c = random.randint(0,100)
                d = random.randint(0,100)
                e = random.random()
                f = random.random()
                g = random.randint(0,100) 
                h = random.random()
                if h < randomPoint:
                    h = 1
                elif eraser:
                    h = 0
                else:
                    h = genome[gg][7]
                i = random.random()*1.96- 0.98
                j = random.random()*1.96- 0.98
                k = random.randint(0,20)

                l = random.random()
                if l < connect2points:
                    l = 1
                elif eraser:
                    l = 0
                else:
                    l = genome[gg][11]
                m = random.randint(0,gg)
                n = random.randint(0,100)
                o = random.randint(0,100)
                
            elif type == 1: #Small mutations
                a = genome[gg][0]
                b = genome[gg][1]
                c = genome[gg][2]
                d = genome[gg][3]
                e = (genome[gg][4]-0.02 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                f = (genome[gg][5]-0.02 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                g = genome[gg][6]
                h = genome[gg][7]
                i = (genome[gg][8]-0.02 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                j = (genome[gg][9]-0.02 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                k = genome[gg][10]
                l = genome[gg][11]
                m = genome[gg][12]
                n = (genome[gg][13] + int(random.random()*2-0.5))%100
                o = (genome[gg][14] + int(random.random()*2-0.5))%100
                
            elif type == 2: #only nudge points
                a = genome[gg][0]
                b = genome[gg][1]
                c = genome[gg][2]
                d = genome[gg][3]
                e = (genome[gg][4]-0.01 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                f = (genome[gg][5]-0.01 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                g = genome[gg][6]
                h = genome[gg][7]
                i = (genome[gg][8]-0.02 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                j = (genome[gg][9]-0.02 + (random.random()/50-0.01)/divisor)%0.96 + 0.02
                k = genome[gg][10]
                l = genome[gg][11]
                m = genome[gg][12]
                n = genome[gg][13]
                o = genome[gg][14]
                
            newgenome.append((a,b,c,d,e,f,g,h,i,j,k,l,m,n,o))
            
        gg = gg+1
    return newgenome

def FullProcessRandomGA(popAmount, threshold1 = 50, output=None):
    initialPop = randomInstructionsPop(popAmount)
    initialPop = evolveInstructions(initialPop)
    gen = 0
    evenornot = 0
    print("Initial population best fit score = " + str(initialPop[2]))
    # print("Scores = " + str(initialPop[3]))
    # if output != None:
    #     output = str(output)
    #     of.exportCP(oc.createFromInstructions(initialPop[1]), output+"Gen00000.cp")
    lastscore=initialPop[2]
    gen = 0
    while gen < 10000:
        evolutionType = 0 + int((gen%5)/4)
        initialPop = evolveInstructions(initialPop[0], evolutionType, initialPop[3])
        print("Best fit score = " + str(initialPop[2]) + "\n\n")
        lastscore=initialPop[2]
        # print(lastscore)
        # print(threshold1)
        gen = gen + 1
        if lastscore>threshold1:
            evenornot = of.testEven((oc.createFromInstructions(initialPop[1])))
            if lastscore > 90:
                gen = 10000
            if evenornot == 1:
                gen = 10000
    
    
    # Refine even/odd connections 
    while evenornot<1:
        initialPop = helpEvenInstructions(initialPop[0] ,2, initialPop[3])
        evenornot = initialPop[2]
        print("Best fit even/odd score = " + str(initialPop[2]) + "\n\n")
        
    
    # Start the refining step
    refinement = 0
    refinementcount = 0
    countDifference = 0
    lastscore = 0
    divisor = 1
    difference = 1
    while refinement < 0.9999999: 
        initialPop = nudgeInstructions(initialPop[0] ,2, initialPop[3], divisor)
        refinement = initialPop[2]
        countDifference = (countDifference + 1)%100
        if countDifference == 0:
            difference = (refinement-lastscore)/(1-lastscore)
            lastscore = refinement
            if difference == 0:
                divisor = divisor*10
                if divisor > 100000:
                    divisor = 100000
            elif difference < 1/1000:
                divisor = divisor/10
                if divisor < 1:
                    divisor = 1
        print("Best fit refinement score = " + str(initialPop[2]) + "\n\n")
        refinementcount = refinementcount + 1
        if refinementcount > 20000:
            print("Refinement failed")
            break

        
    
    
    of.exportCP(oc.createFromInstructions(initialPop[1]),output)
    
    return initialPop