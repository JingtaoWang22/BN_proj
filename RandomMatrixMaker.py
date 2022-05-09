import random
import TwoDMatrixIterator as TMI
import tools
import BinaryStringToBayesianN as BSTB
import GeneticAlgorithm as GA
import SignificantEdgesToGraph as SEG
import networkx as nx

def MakeRandomMatrix( num_edges, index_to_vertex ):
    size = len( index_to_vertex )
    matrix = tools.CreateAdjMatrix( size, size )
    flat_size = TMI.GetSize( matrix )
    for i in range( num_edges ):
        rand_ind = random.randint( 0, flat_size - 1 )
        TMI.SetAtIndex( matrix, rand_ind, 1 )
        if ( not TMI.IsDAG( matrix, index_to_vertex ) ):
            TMI.SetAtIndex( matrix, rand_ind, 0 )
    return matrix

def WriteEdgesToTxt( matrix, index_to_vertex ):
    f = open( "RandomFinalGraph.txt", "w" )
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1 ):
                v1 = index_to_vertex[i]
                v2 = index_to_vertex[j]
                f.write( v1 + "---" + v2 )
    f.close()

if __name__ == "__main__":
    candidates = []
    g = SEG.SignificantEdgesToGraph( "notcorrectedSorted11005.txt")
    index_to_vertex = list( g.nodes )
    for i in range( 10 ):
        candidates.append( MakeRandomMatrix( 200, index_to_vertex ) )
    children = GA.GeneticRun( candidates, 0.005, 5, 10, 4, 0.05, index_to_vertex )
    bestDescendant = children.list[0]
    graph = BSTB.MatrixToNetwork( bestDescendant, index_to_vertex )
    WriteEdgesToTxt( bestDescendant, index_to_vertex )
