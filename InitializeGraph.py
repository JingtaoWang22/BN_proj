from igraph import*
import ReadCSV
import pandas as pd
import tools as tools
import random
import numpy as np

def CreateVector( variable, dataframe ):
    DataEntries = dataframe[variable].tolist()
    return tools.ConvertToVector( DataEntries, variable )


def AttachVectors( variables, dataframe, g ):
    liste = []
    for var in variables:
        liste.append( CreateVector( var, dataframe ) )
    g.vs["Vector"] = liste


def CreateEdges( g ):
    added = set()
    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            if (not((h,i) in added or (i,h) in added)):
                g.add_edges([(h, i)])
                ID = g.get_eid(h,i)
                g.es[ID]["Time_Visited"] = []
                g.es[ID]["AB"] = []
                g.es[ID]["BA"] = []
                added.add((h,i))


def InitializeMutualInfoMatrix(g):
    added = set()
    MutualInfoMatrix = tools.CreateAdjMatrix(len(g.vs), len(g.vs))

    for i in range(len(g.vs)):
        constantVector = g.vs[i]["Vector"]
        for j in range(len(g.vs)):
            if (not((j,i) in added or (i,j) in added)):
                currentVector = g.vs[j]["Vector"]
                mutual = tools.ComputeMutualInfo(constantVector, currentVector)
                MutualInfoMatrix[i][j] = mutual
                MutualInfoMatrix[j][i] = mutual
                added.add((i,j))

    return MutualInfoMatrix

def InitializeProbabilityMatrix(MutualInfoMatrix):
    Mutual = np.array(MutualInfoMatrix)
    totals = Mutual.sum(axis = 1)
    
    size = len(MutualInfoMatrix)
    prob_matrix = tools.CreateAdjMatrix(size, size)
    for i in range(size):
        for j in range(size):
            if ( totals[i] == 0 ):
                prob_matrix[i][j] = 0
            else:
                prob_matrix[i][j] = MutualInfoMatrix[i][j]/totals[i]
    return prob_matrix


def InitializeGraph( file ):
    g = Graph()
    patient_data = ReadCSV.CreateDataframe( file )

    clinic_vars = list( patient_data.columns )

    g.add_vertices( len( clinic_vars[ 3: ] ) )
    g.vs[ "clinic_vars" ] = clinic_vars[ 3: ]

    AttachVectors( clinic_vars[ 3: ], patient_data, g )

    CreateEdges(g)

    return g


def InitializeGraphFast( file ):
    g = Graph()
    patient_data = ReadCSV.CreateDataframe( file )

    clinic_vars = list( patient_data.columns )

    g.add_vertices( len( clinic_vars[ 3: ] ) )
    g.vs[ "clinic_vars" ] = clinic_vars[ 3: ]

    CreateEdges(g)

    return g


if __name__ == "__main__":
    g = InitializeGraph('CompletedTestData.csv')
    #for i in range( len( g.vs ) ):
        #print(g.vs[i]["clinic_vars"])
    print(g.vs[-1]["Vector"])
    #print(len(g.vs))
    #liste = list(patient_data["Temperature:"])
    #print(str(liste[-1]) == str(liste[-1]))
    #liste = CleanList(liste)
    #print(liste)
    #for i in range(len(liste)):
        #print(liste[i])
    #for col in patient_data:
        #print(col)
        #print(CleanList(list(patient_data[col])))





    
    
