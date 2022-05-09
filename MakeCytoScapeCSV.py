import pandas as pd
import networkx as nx

def SignificantEdgesToGraph( filename ):
    g = nx.DiGraph()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edges = []
    for line in Lines:
        bounds = GetVerticesFromString( line )
        g.add_edge( bounds[0], bounds[1] )
        edges.append( (bounds[0], bounds[1]) )
    file1.close()
    return g

def GetVerticesFromString( string ):
    strings = string.split( "---" )
    return strings

def MakeCytoScapeCSV( filename, out_filename ):
    g = SignificantEdgesToGraph( filename )
    leftVertices = []
    rightVertices = []
    for edge in list( g.edges ):
        leftVertices.append( edge[0] )
        rightVertices.append( edge[1] )
    data = { "Left": leftVertices, "Right": rightVertices }
    df = pd.DataFrame( data )
    df.to_csv( out_filename )

if __name__ == "__main__":
    #MakeCytoScapeCSV( "RandomFinalGraph.txt", "CytoScapePlotRandom.csv" )
    MakeCytoScapeCSV( "NonRandomFinalGraph.txt", "CytoScapePlotNonRandom.csv" )
