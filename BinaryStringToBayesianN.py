from operator import index
import networkx as nx
from pgmpy.models import BayesianNetwork
import SignificantEdgesToGraph as SEtG
import tools as tools
import ReadCSV as rcsv
from pgmpy.estimators import K2Score
import StructureLearningData as SLD

def MakeCandidateEdgeDictionary( filename ):
    dictionary = {}
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edgePair = []
    counter = 0
    for i in range( len(Lines) ):
        bounds = SEtG.GetVerticesFromString( Lines[i] )
        edgePair.append( ( bounds[0], bounds[1] ) )
        if ( i % 2 == 1 ):
            dictionary[ counter ] = [ edgePair[0], edgePair[1] ]
            edgePair = []
            counter += 1
    file1.close()
    return dictionary

def DictionaryToList( dictionary ):
    edges = []
    for index in dictionary:
        edges = edges + dictionary[ index ]
    return edges

def AllSignificantEdgesToList( filename ):
    edges = []
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    for i in range( len(Lines) ):
        bounds = SEtG.GetVerticesFromString( Lines[i] )
        edges.append( ( bounds[0], bounds[1] ) )
    file1.close()
    return edges


def RemoveRedundantEdges( liste, dictionary ):
    dictionary_list = DictionaryToList( dictionary )
    non_redundant_list = []
    for i in range( len( liste ) ):
        if ( liste[i] not in dictionary_list ):
            non_redundant_list.append( liste[i] )
    return non_redundant_list


def BuildGraphFromBinaryString( edgeList, candidate_dictionary, bin_string ):
    edges = []
    for i in range( len( edgeList ) ):
        edges.append( edgeList[i] )
    for j in range( len( bin_string ) ):
        edge_to_add = candidate_dictionary[j][ bin_string[j] ]
        edges.append( edge_to_add )
    return edges

def IncrementBinaryString( bin_string ):
    current = 0
    while( current < len( bin_string ) ):
        if ( ( bin_string[ current ] + 1 ) == 1 ):
            bin_string[ current ] += 1
            return
        else:
            bin_string[ current ] = 0
            current += 1
    if( bin_string == [0]*len( bin_string ) ):
        for i in range( len( bin_string ) ):
            bin_string[i] = 2


def score( network, dataframe ):
    bay_network = SEtG.SignificantEdgeListToBayesianNetwork( network )
    score = K2Score( dataframe ).score( bay_network )
    return score

def temp_score( network ):
    return len( network )

def GetBestBinaryNetworks(  edgeList, candidate_dictionary, dataframe ):
    scores = {}
    current = [0]*len( candidate_dictionary )
    while( current != [2]*len( candidate_dictionary ) ):
        print( current )
        edges = BuildGraphFromBinaryString( edgeList, candidate_dictionary, current )
        print( current )
        edges = SEtG.RemoveSelfEdges( edges ) #will be able to remove this line after when using the file without any self edges
        print( current )
        scores[ current ] = score( edges, dataframe )
        print( current )
        IncrementBinaryString( current )
    return scores

def NetworkTo2dMatrix( network, vertex_to_index ):
    size = len( vertex_to_index )
    network_as_edges = list( network.edges )
    matrix = tools.CreateAdjMatrix( size, size )
    for i in range( len( network_as_edges ) ):
        index1 = vertex_to_index[ network_as_edges[i][0] ]
        index2 = vertex_to_index[ network_as_edges[i][1] ]
        matrix[index1][index2] = 1
    return matrix

def RemoveSelfEdges( edges ):
    new_set = []
    for i in range( len( edges ) ):
        if ( edges[i][0] != edges[i][1] ):
            new_set.append( edges[i] )
    return new_set

def MatrixToNetwork( matrix, index_to_vertex ):
    network = []
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1):
                vertex1 = index_to_vertex[i]
                vertex2 = index_to_vertex[j]
                network.append( ( vertex1, vertex2 ) )
    return nx.DiGraph( network )

def Execution( sig_edges_filename, candidate_filename ):
    sig_edges = AllSignificantEdgesToList( sig_edges_filename )
    candidate_dictionary = MakeCandidateEdgeDictionary( candidate_filename )
    vertices = SEtG.SignificantEdgesToVertices( sig_edges_filename )
    non_redundant = RemoveRedundantEdges( sig_edges, candidate_dictionary )

    data = rcsv.CreateDataframe("CleanedFinalData11.csv")
    cleaned_dataframe = SEtG.NewDataFrameFromCols( data, vertices )
    cleaned_dataframe.to_csv( "DebugCsvTest.csv" )

    best_networks = GetBestBinaryNetworks( non_redundant, candidate_dictionary, cleaned_dataframe )
    return best_networks


if __name__ == "__main__":
    #networks = Execution( "notcorrectedSorted11005.txt", "Candidates.txt" )
    #print( networks )

    vertices = SEtG.SignificantEdgesToVertices( "notcorrectedSorted11005.txt" )
    dataframe = rcsv.CreateDataframe( "CleanedFinalData11.csv" )
    SLD.GetStructureLearningDF( dataframe, vertices )
    