import math

def distance(p1,p2):
    distance = math.sqrt(math.pow(p2[0]-p1[0]),2)+math.pow(p2[1]-p1[1])
    return int(distance)

def distance_violate(results):

    if len(results) >=2:
        centroid=[r[3] for r in results]
    
    outcome =[]
    for i in centroid:
        cen=[]
        for j in centroid:
            cen.append(distance(i,j))
        outcome.append(cen)
    violations=set()

    for i in range(0,len(outcome)-1):
        for j in range(i,len(outcome)-1):

            if outcome[i][j]<75:
                violations.add(i)
                violations.add(j)

    return violations
        