import math

#To find to euclidean distance between two centroids
def distance(p1,p2):

    distance = math.sqrt(math.pow(p2[0]-p1[0],2)+math.pow(p2[1]-p1[1],2))
    #Returns distance  between two objects in pixels
    return int(distance)


def breachsocialdistance(results,violatedistance=75):

    #Makes a seperate list of all centroids of detected objects
    centroid = [r[3] for r in results]
    
    #Intializing a list to store the indexes of violating objects
    outcome = []

    #Loop over each centroid
    for i in centroid:
        
        #Make a layer for each centroid
        cen = []

        #To compare each centroid with the others
        for j in centroid:
            
            #Appends the distance of each centroid with the others
            cen.append(distance(i,j))
        
        #Stores each each to form a Distance matrix
        outcome.append(cen)
    
    #Initialize a set to store Non repeating indexes of the violating objects
    violations = set()

    #loop through each element in the outcome distance matrix
    for i in range(0,len(outcome)):
        for j in range(i+1,len(outcome)):

            #Checks if the distance in pixels is lesser than the safe distance
            if outcome[i][j]<violatedistance:
                violations.add(i)
                violations.add(j)

    return violations
        