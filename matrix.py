import math

# some useful acessory functions

def vectorAddition(v1,v2):
    if len(v1) == len(v2):
        newV = [0]*len(v2)
        for i in range(len(v1)):
            newV[i] = v1[i] + v2[i]
        return tuple(e for e in newV)

def matrixMultiply (M, v):
    if isinstance(v, tuple) and len(v) == len(M[0]):
        newV = [0]*len(v)
        rows = len(M)
        cols = len(M[0])

        for row in range(rows):
            for col in range(cols):
                newV[row] += v[col]*M[row][col]
        
        return tuple(e for e in newV)
    
def getProjection(x, z, n):
    return n*x/(z+n)

def rotate(v,t,i):  
    M = None
    # ROTATE X
    if i == 1:
        M = [[1,        0,               0],
            [0, math.cos(t), -math.sin(t)],
            [0, math.sin(t),  math.cos(t)]
            ]
        
    # ROTATE Y
    elif i == 2:
        M = [[math.cos(t),0,-math.sin(t)   ],
         [0,        1,      0         ],
         [math.sin(t), 0, math.cos(t)]
         ]
        
    # ROTATE Z
    elif i == 3:
        M = [
        [math.cos(t), -math.sin(t), 0],
         [math.sin(t), math.cos(t),  0],
         [0, 0, 1]
         ]
    return matrixMultiply(M,v)



