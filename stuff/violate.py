import math

def distance(point1,point2):
    distance = math.sqrt(math.pow(point2[0]-point1[0],2)+math.pow(point2[1]-point1[1],2))
    return int(distance)

def breachsocialdistance(final,violatedistance=75):

    centroids = [r[3] for r in final]
    n = len(centroids)
    rows,cols= (n,n)
    results = []
    for i in centroids:
        col = []
        for j in centroids:
            col.append(distance(i,j))
        results.append(col)

    violates = set()

    for i in range(0,len(results)):
        for j in range(i + 1 ,len(results)):
            if results[i][j] < violatedistance:
                violates.add(i)
                violates.add(j)

    return violates