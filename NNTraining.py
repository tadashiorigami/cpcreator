import OrigamiClasses as oc
import OrigamiFunctions as of
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import os,glob

n_foldable_training = 100
n_unfoldable_training = 1126
n_foldable_testing = 22
n_unfoldable_testing = 218

arraySize = 36
setEpochs = 100
weights = "firsttest.h5"

model = Sequential([
  Dense(64, activation='relu', input_shape=(arraySize,)),
  Dense(64, activation='sigmoid'),
  Dense(64, activation='sigmoid'),
  Dense(1, activation='sigmoid'),
])


# Function to get the origami class and filter the most relevant data.
# The output is a numpy array to prepare for the neural network test
def filterOrigami(origami):
    
    #Select the angle to calculate deviation from
    # deviationAngle = 11.25

    points = origami.countp()
    middlePoints = []
    below10 = 0
    
    # Lists middle points
    for point in origami.points:
        if point[0] != -200 and point[0] != 200 and point[1] != -200 and point[1] != 200:
            middlePoints.append(point)
    
    # Count how many connections each point in middle has, from 0 to 16 or more
    # Also counts the angle between connected points
    connections = [0]*17 # The index indicates the number of connections in each point
    excessAngles = 0 #Sums the excess angles - CP must be 0
    excessAngleCounter = 0 #counts to make the average of sums
    # deviation = 0
    # deviationCounter = 0
    for point in middlePoints:
        connection = 0
        connectedpoints = []
        angles = []
        excessAngleInPoint = 0
        for line in origami.lines:
           if point in line:
                connection = connection + 1
                connectedpoints.append(line[line.index(point)-1])
        if connection < 17:
            connections[connection] = connections[connection]+1
        
        # if connection == 1:
            # print(point)
        for cpoint in connectedpoints:
            angles.append(of.get_angle(point, cpoint))
        angles.sort()
        excessAngleInPoint = 360-angles[-1]+angles[0] 
        # deviation = (deviation*deviationCounter + ((360-angles[-1]+angles[0])+deviationAngle/2)%deviationAngle - deviationAngle/2)/(deviationCounter+1)
        # deviationCounter = deviationCounter+1
        # print(((360-angles[-1]+angles[0])+deviationAngle/2)%deviationAngle - deviationAngle/2)
        for i in range(1, len(angles)):
            excessAngleInPoint =  excessAngleInPoint + (angles[i]-angles[i-1])*pow(-1,i)
            # deviation = (deviation*deviationCounter + ((angles[i]-angles[i-1])+ deviationAngle/2)%deviationAngle- deviationAngle/2)/(deviationCounter+1)
            # deviationCounter = deviationCounter+1
        excessAngleInPoint = abs(round(excessAngleInPoint,5))
        excessAngles = (excessAngles*excessAngleCounter + excessAngleInPoint)/(excessAngleCounter+1)
        excessAngleCounter = excessAngleCounter + 1
        # print(excessAngles)
    
    # print(excessAngles)
    # deviation = round(deviation,5)
    # print(deviation)
    # Count how many points in each section, divided in 16 parts (4x4)
    divisions = 4
    sectionPoints = [[0 for col in range(divisions)] for row in range(divisions)]
    for i in range(0, divisions):
        for j in range(0, divisions):
            leftmargin = i*(400/divisions)-200
            rightmargin = (i+1)*(400/divisions)-200
            bottommargin = j*(400/divisions)-200
            topmargin = (j+1)*(400/divisions)-200
            
            for point in origami.points:
                if point[0] >= leftmargin and point[0] <= rightmargin and point[1] >= bottommargin and point[1] <= topmargin:
                    sectionPoints[i][j] = sectionPoints[i][j]+1
    flatSectionPoints = []     
    for section in sectionPoints:
        for subs in section:
            flatSectionPoints.append(subs)
    # print(flatSectionPoints)
    
    # Count how many angles below 10 degrees (not good)
    for point in origami.points:
        connectedpoints = []
        angles = []
        angledifference = 0
        for line in origami.lines:
           if point in line:
                connectedpoints.append(line[line.index(point)-1])
        for cpoint in connectedpoints:
            angles.append(of.get_angle(point, cpoint))
        angles.sort()
        for i in range(0, len(angles)):
            if i == 0:
                angledifference = 360-angles[i-1] + angles[i]
            else:
                angledifference = (angles[i]-angles[i-1])
            if angledifference < 10:
                below10 = below10 + 1
    
    output = []
    output.append(len(middlePoints)/points*2-1)
    # print("Percentage of middle points %s = " % (len(middlePoints)/points))
    
    
    excessoutput = (-1)*(excessAngles/90*2-1)
    if excessoutput < -1:
        excessoutput = -1
    output.append(excessoutput)
    # print("Excess alternating sum %s = " % (excessAngles/90))
    # print(output[-1])
    
    
    maxamount = max(connections)
    if maxamount == 0:
        maxamount = 1
        
    # Append only the sum of evens and sum of odds with high bias
    # print("Connections %s = " % (connections))
    # evenconections = 0
    # oddconnections = 0
    # for i in range(len(connections)):
    #     if i % 2 == 0:
    #         evenconections = evenconections + connections[i]
    #     else:
    #         oddconnections = oddconnections + connections[i]
        
    # if (evenconections+oddconnections) == 0:
    #     evenconections = 1
    
    # output.append(2*evenconection s/(evenconections+oddconnections)-1 - (1-(1/(1+oddconnections))))
    
    
    # Append all the connections
    maxconnections = max(connections)
    if maxconnections == 0:
        maxconnections = 1
    for connection in connections:
        output.append(connection/maxconnections)
    
    # print(str(output[-2]) + " " + str(output[-1]))
    # print(" ")
    for section in flatSectionPoints:
        output.append(section/points *2-1)
    # print("Points in section %s = " % (flatSectionPoints))
        
    output.append(below10/points)
    # print("Percentage of angles below 10 %s = " % (below10/points*2-1))
    
    # print(output)
    npOutput = np.zeros([len(output),])
    for i in range(len(output)):
        npOutput[i] = output[i]
    return npOutput
        

#Function to perform a neural network training. Saves the weights in the output
def neuralTest(outputname=None):
    #### POPULATING TRAINING SETS
    # opening training CPs
    train_cps = np.zeros([n_foldable_training + n_unfoldable_training,arraySize])
    train_labels = np.array([], dtype="int32")

    # Populate train labels with 100 1s and 1100 0s
    for i in range (0,n_foldable_training):
        train_labels = np.append(train_labels,[1])
    for i in range (0,n_unfoldable_training):
        train_labels = np.append(train_labels,[0])
        
    foldable_training_path = './training/foldable'
    unfoldable_training_path = './training/unfoldable'
    x = 0

    # Populate foldable training cps on np arrays
    for filename in glob.glob(os.path.join(foldable_training_path, '*.cp')):
        origami = of.cptoorigami(filename)
        train_cps[x] = filterOrigami(origami)
        x = x+1
            
    # Populate unfoldable training cps on np arrays
    for filename in glob.glob(os.path.join(unfoldable_training_path, '*.cp')):
        origami = of.cptoorigami(filename)
        train_cps[x] = filterOrigami(origami)
        x = x+1
            
    #### POPULATING TESTING SETS
    # opening testing CPs
    test_cps = np.zeros([n_foldable_testing + n_unfoldable_testing,arraySize])
    test_labels = np.array([], dtype="int32")

    # Populate test labels with 22 1s and 22 0s
    for i in range (0,n_foldable_testing):
        test_labels = np.append(test_labels,[1])
    for i in range (0,n_unfoldable_testing):
        test_labels = np.append(test_labels,[0])
        
    foldable_testing_path = './testing/foldable'
    unfoldable_testing_path = './testing/unfoldable'
    x = 0

    for filename in glob.glob(os.path.join(foldable_testing_path, '*.cp')):
        origami = of.cptoorigami(filename)
        test_cps[x] = filterOrigami(origami)
        x = x+1
            
    for filename in glob.glob(os.path.join(unfoldable_testing_path, '*.cp')):
    
        origami = of.cptoorigami(filename)
        test_cps[x] = filterOrigami(origami)
        x = x+1

    
    # Compile the model.
    model.compile(
      optimizer='adam',
      loss='categorical_crossentropy',
      metrics=['accuracy'],
    )

    # Train the model.
    # model.load_weights('model.h5')
    model.fit(
      train_cps,
      to_categorical(train_labels),
      epochs=setEpochs,
      batch_size=32,
    )
    print("---Training done---")

    # Evaluate the model.
    print("")
    print("---Testing prediction ---")
    model.evaluate(
      test_cps,
      to_categorical(test_labels)
    )
    # # Save the model to disk later using:
    if outputname != None:
        model.save_weights(outputname)
        
def showPredictions(weights):
    #### POPULATING TESTING SETS
    # opening testing CPs
    test_cps = np.zeros([n_foldable_testing + n_unfoldable_testing,arraySize])
    test_labels = np.array([], dtype="int32")

    # Populate test labels with 22 1s and 219 0s
    for i in range (0,n_foldable_testing):
        test_labels = np.append(test_labels,[1])
    for i in range (0,n_unfoldable_testing):
        test_labels = np.append(test_labels,[0])
        
    foldable_testing_path = './testing/foldable'
    unfoldable_testing_path = './testing/unfoldable'
    x = 0
    filenamesList = []

    for filename in glob.glob(os.path.join(foldable_testing_path, '*.cp')):
        filenamesList.append(filename)
        origami = of.cptoorigami(filename)
        test_cps[x] = filterOrigami(origami)
        x = x+1
            
    for filename in glob.glob(os.path.join(unfoldable_testing_path, '*.cp')):
        filenamesList.append(filename)
        origami = of.cptoorigami(filename)
        test_cps[x] = filterOrigami(origami)
        x = x+1
    
    # # Load the model from disk:
    model.load_weights(weights)
    
    # # Predict on the first 5 test images.
    predictions = model.predict(test_cps[:(n_foldable_testing + n_unfoldable_testing)])
    # Print our model's predictions.
    print(np.argmax(predictions[:20], axis=1))
    print(np.argmax(predictions[20:40], axis=1))
    print(np.argmax(predictions[40:60], axis=1))
    print(np.argmax(predictions[60:80], axis=1))
    print(np.argmax(predictions[80:100], axis=1))
    print(np.argmax(predictions[100:120], axis=1))
    print(np.argmax(predictions[120:140], axis=1))
    print(np.argmax(predictions[140:160], axis=1))
    print(np.argmax(predictions[160:180], axis=1))
    print(np.argmax(predictions[180:200], axis=1))
    print("------------")
    for i in range(0,len(predictions)):
        print(filenamesList[i] + ": " + str(round(predictions[i][1]*100,1)))
    
def testCPs(creasepatterns, weights):
    # print(weights)
    amount = len(creasepatterns)
    filtered = np.zeros([amount,arraySize])
    for i in range(0,amount):
        filtered[i] = filterOrigami(creasepatterns[i])
    
    model.load_weights(weights)
    predictions = model.predict(filtered[:amount])
    return predictions