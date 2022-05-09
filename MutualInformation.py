import numpy as np
import InitializeGraph as Init
from pyitlib import discrete_random_variable as drv
import random
import tools as tools

def GenerateGraphVectorMatrix(g):
    matrix = []
    for i in range(len(g.vs)):
        matrix.append(g.vs[i]["Vector"])
    return np.array(matrix)

def ComputeMutualInformation( array ):
    size = len( array )
    mutual_info_matrix = tools.CreateAdjMatrix(size, size)
    for i in range( len( array ) ):
        current_var = array[i]
        for j in range( len( array ) ):
            inner_var = array[j]
            mask = ( current_var != -999 ) * ( inner_var != -999 )
            x1 = current_var[ mask ]
            x2 = inner_var[ mask ]

            if ( len(x1) == 0 ):
                mutual_info_matrix[i][j] = 0
            else:
                mutual = drv.information_mutual( x1, x2 )
                mutual_info_matrix[i][j] = mutual
            
    return mutual_info_matrix

def ManualNaNRemove(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if ( str(matrix[i][j]) == str(np.nan) ):
                matrix[i][j] = 0

def SumMatrix(matrix):
    summed = []
    for i in range(len(matrix)):
        total = 0
        for j in range(len(matrix[i])):
            if (str(matrix[i][j]!=str(np.nan))):
                total += matrix[i][j]
        summed.append(total)
    return summed

def InitializeMutualInfoMatrix(g):
    matrix = GenerateGraphVectorMatrix(g)
    matrix = ComputeMutualInformation(matrix)
    return matrix

def ShuffleMutualInfo(MutualInfoMatrix):
    size = len(MutualInfoMatrix)
    for i in range(size):
        for j in range(size):
            randi = random.randint(0, size-1)
            randj = random.randint(0, size-1)

            temp = MutualInfoMatrix[i][j]

            MutualInfoMatrix[i][j] = MutualInfoMatrix[randi][randj]
            MutualInfoMatrix[j][i] = MutualInfoMatrix[randi][randj]

            MutualInfoMatrix[randi][randj] = temp
            MutualInfoMatrix[randj][randi] = temp

if __name__ == "__main__":
    g = Init.InitializeGraph('CompletedTestData.csv')
    matrix = GenerateGraphVectorMatrix(g)

    # there are nan in the mutual information matrix dont really know why
    matrix = ComputeMutualInformation(matrix)
    print( matrix )
