from operator import index
import random
import tools as tools
import copy
import networkx as nx


def GetSize( matrix ):
    size = 0
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i]) ):
            size += 1
    return size

def GetAtIndex( matrix, index ):
    matrixLength = len( matrix )
    x = int(index/matrixLength)
    y = index%( matrixLength )
    return matrix[x][y]

def SetAtIndex( matrix, index, element ):
    matrixLength = len( matrix )
    x = int(index/matrixLength)
    y = index%( matrixLength )
    matrix[x][y] = element

def MatrixToNetwork( matrix, index_to_vertex ):
    network = []
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1 ):
                vertex1 = index_to_vertex[i]
                vertex2 = index_to_vertex[j]
                network.append( ( vertex1, vertex2 ) )
    return nx.DiGraph( network )

def IsDAG( matrix, index_to_vertex ):
    network = MatrixToNetwork( matrix, index_to_vertex )
    return nx.is_directed_acyclic_graph( network )

def Mate( matrix1, matrix2, index_to_vertex ):
    matrix_size = len( matrix1 )
    flat_matrix_size = GetSize(matrix1)
    split_point = random.randint( 0, flat_matrix_size-1 )
    child1 = tools.CreateAdjMatrix( matrix_size, matrix_size )
    child2 = tools.CreateAdjMatrix( matrix_size, matrix_size )
    
    i = 0
    while( i <= split_point ):
        toSet1 = GetAtIndex( matrix1, i )
        toSet2 = GetAtIndex( matrix2, i )
        SetAtIndex( child1, i, toSet1 )
        SetAtIndex( child2, i, toSet2 )

        if ( toSet1 == 1 ):
            if ( not IsDAG( child1, index_to_vertex ) ):
                SetAtIndex( child1, i, 0 )
        if ( toSet2 == 1):
            if ( not IsDAG( child2, index_to_vertex ) ):
                SetAtIndex( child2, i, 0 )
        i += 1

    while( i < flat_matrix_size ):
        toSet1 = GetAtIndex(matrix2, i ) 
        toSet2 = GetAtIndex(matrix1, i )
        SetAtIndex( child1, i, toSet1 )
        SetAtIndex( child2, i, toSet2 )
        if ( toSet1 == 1 ):
            if ( not IsDAG( child1, index_to_vertex ) ):
                SetAtIndex( child1, i, 0 )
        if ( toSet2 == 1):
            if ( not IsDAG( child2, index_to_vertex ) ):
                SetAtIndex( child2, i, 0 )
        i += 1

    return [ child1, child2 ]
       

def flattenMatrix( matrix ):
    flattened = []
    for i in range( len( matrix ) ):
        flattened += matrix[i]
    return flattened


def MutateMatrix( matrix, index_to_vertex,edges ): # edges: #edges to mutate
    matrix_copy = copy.deepcopy( matrix )
    total_size = GetSize( matrix )

    i = 0
    
    fkind = 'fail' # 0: remove, 1: flip, 2: add
    
    '''TO DO
    
    adding flipping an edge
    do edges == 1 and edges == 2 seperately
    
    '''
    
    
    while i <  edges:
        i += 1
        outer = len( matrix ) - 1
        inner = len( matrix[0] ) - 1

        j = random.randint( 0, outer )
        k = random.randint( 0, inner )
        while( j == k ):
            k = random.randint( 0, inner )

        if ( matrix_copy[j][k] == 1 ):
            #print('in 1')
            coin = random.randint(0,1)
            coin==0
            if coin == 0: # remove an edge
                matrix_copy[j][k] = 0
                fkind = 'remove'
                #print('remove')
            #else: # flip an edge
            #    matrix_copy[j][k] = 0
            #    matrix_copy[k][j] = 1
            #    fkind = 'flip'
            #    #print('flip')
        else:
            #print('in 0 ')
            matrix_copy[j][k] = 1
            fkind='add'
            #print('add')
            if ( not IsDAG( matrix_copy, index_to_vertex ) ):
                matrix_copy[j][k] = 0
                #i -= 1
                fkind = 'fail'
                
    #print()
    #print(len(matrix_copy))

    #print()
    #print(fkind,matrix_copy[j][k],index_to_vertex[j],index_to_vertex[k])
    

    
    return matrix_copy


if __name__ == "__main__":
    matrix1 = [[1,1,1], [2,2,2], [3,3,3]]
    matrix2 = [ [0,0,0], [0,0,0], [0,0,0]]
    
    #children = Mate( matrix1, matrix2 )
    #print( flattenMatrix( children[0]) )
    #print( flattenMatrix( children[1]) )

    MutateMatrix( matrix2, 0.5 )
    print( matrix2 )
    






