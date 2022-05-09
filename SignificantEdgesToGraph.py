import networkx as nx
from pgmpy.models import BayesianNetwork
import matplotlib.pyplot as plt
from pgmpy.estimators import K2Score,BDsScore
import pandas as pd
import tools as tools
import DisplayGraph as dg
import ReadCSV as rcsv
import pgmpy
import timeit
import copy    
import pickle
import GeneticAlgorithm as GA
import TwoDMatrixIterator as TMI
import BinaryStringToBayesianN as BSTB

def InitializeVarToIndexDictionary( IndexToVarListe ):
    var_to_index = {}
    for i in range( len( IndexToVarListe ) ):
        var_to_index[ IndexToVarListe[i] ] = i
    return var_to_index

def SignificantEdgeListToBayesianNetwork( edges_list ):
    return BayesianNetwork( edges_list )

def SignificantEdgesToBayesianNetwork( filename ):
    edges = []
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        edges.append( (bounds[0], bounds[1]) )
    file1.close()
    edges = RemoveSelfEdges( edges )
    bn = BayesianNetwork( edges )
    return bn

def SignificantEdgesToVertices( filename ):
    vertices = set()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        vertices.add( bounds[0] )
        vertices.add( bounds[1] )
    return list( vertices )
    

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
    pre_strings = string.split( ";;;" )
    strings = pre_strings[0].split( "--- ")
    last_colon = FindLastColon( strings[1] )
    strings[1] = strings[ 1 ][ 0:last_colon ]
    return strings

def FindLastColon( string ):
    size = len( string )
    for i in range( size ):
        if ( string[ size -1 -i ] == ":"):
            return size-1-i
    return 0

def RemoveSelfEdges( edges ):
    new_set = []
    for i in range( len( edges ) ):
        if ( edges[i][0] != edges[i][1] ):
            new_set.append( edges[i] )
    return new_set

def GetDataFromDataframe( dataframe, cols ):
    data = []
    for col in cols:
        one_col = tools.ConvertToVector( dataframe[col], col )
        tools.SetNaNOnCol( one_col )
        data.append( one_col )
    return data

def CreateNewDataFrame( data, cols ):
    dataframe_dict = {}
    for i in range( len( cols ) ):
        dataframe_dict[ cols[i] ] = data[i]
    return pd.DataFrame( dataframe_dict )

def NewDataFrameFromCols( dataframe, cols ):
    data = GetDataFromDataframe( dataframe, cols )
    new_dataframe = CreateNewDataFrame( data, cols )
    return new_dataframe

def ScoreGraph(g, method = 'k2', data=None):
    if type(data) == type(None):
        data=pd.read_csv('ScoringDataframe.csv')
    if method == 'k2':
        grader = pgmpy.estimators.K2Score(data,complete_samples_only=False)
    elif method == 'bd':
        grader = pgmpy.estimators.BDsScore(data,complete_samples_only=False)
    severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
    graphscore = 0
    for node in g.nodes:
        if node == severity:
            continue
        parents = list(g.predecessors(node))
        edgescore = grader.local_score(node,parents)
        graphscore += edgescore
    return graphscore


def Score( adjMatrix, index_to_vertex ,method = 'bd'):
    graph =  BSTB.MatrixToNetwork( adjMatrix, index_to_vertex )
    if ( nx.is_directed_acyclic_graph( graph ) == False ):
        return -99999
    else:
        return ScoreGraph( graph, method = method )
    

def btog(b,es,g1):
    # binary representation to graph
    # b: binary string
    # es: list of bidirectional edges
    #     each element is a list of 2 edges
    #     each edge is a tuple of 2 nodes
    #     (list of lists of tuples)
    # g: the intial graph with bidirectional edges
    
    to_rm = []
    g2=copy.deepcopy(g1)
    for j in range(13):  # remove 13 out of 26 edges
        if b[j] == '0':
            to_rm.append(es[j][0])
        else:
            to_rm.append(es[j][1])
    for e in to_rm:
        g2.remove_edge(e[0],e[1])
    return g2

def bidirectional_edges():
    f= open('e.txt')
    lines = f.readlines()
    bie=[]
    for l in lines:
        #print(l)
        n1=l.split('---')[0]
        n2=l.split('---')[1][:-1]
        bie.append((n1,n2))
    
    es=[]
    for i in range(13):
        es.append([bie[2*i],bie[2*i+1]])
    return es

def WriteEdgesToTxt( matrix, index_to_vertex ):
    #f = open( "NonRandomFinalGraph.txt", "w" )
    f = open( "Final_structure.txt", "w" )
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1 ):
                v1 = index_to_vertex[i]
                v2 = index_to_vertex[j]
                f.write( v1 + "---" + v2 )
                f.write( "\n" )
    f.close()

def ToCytoscape( matrix, index_to_vertex , name = 'aaaaa.csv' ):
    f = open( name, "w" )
    f.write( ",Left,Right\n" )
    cnt=0
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1 ):
                v1 = index_to_vertex[i]
                v2 = index_to_vertex[j]
                f.write( str(cnt) + "," +  v1 + "," + v2 )
                f.write( "\n" )
                cnt+=1
    f.close()


if __name__ == "__main__":
    g = SignificantEdgesToGraph( "notcorrectedSorted11005.txt")
    #nx.relabel_nodes(g, {"If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?":"severity"}, copy=False)
    index_to_var_liste = list( g.nodes )
    var_to_index_dict = InitializeVarToIndexDictionary( index_to_var_liste )

    data=pd.read_csv('ScoringDataframe.csv')
    '''
    CHecking scoring function
    
    s=timeit.default_timer()
    ScoreGraph(g,'k2',data)
    e=timeit.default_timer()
    '''
    
    '''getting bidirectional edges'''
    es = bidirectional_edges()
        
    '''build a dictionary
    keys are network binary representations
    values are total k2 scores
    '''
    #TAKES ABOUT 1H20MIN TO RUN
    #NO NEED TO RUN IF SCORING HAS BEEN FINISHED
    '''
    scoredic={}
    for i in range(2**13):
        representation = format(i, '#015b')[2:]
        to_rm = []
        g2=copy.deepcopy(g)
        for j in range(13):
            if representation[j] == '0':
                to_rm.append(es[j][0])
            else:
                to_rm.append(es[j][1])
        for e in to_rm:
            g2.remove_edge(e[0],e[1])
        graphscore = ScoreGraph(g2,'bd',data)
        scoredic[representation]=graphscore
        
    pickle.dump(scoredic,open('networkBDscores.pickle','wb'))
    
    '''
    scoredic = pickle.load(open('networkBDscores.pickle','rb'))
    
    
    '''select top k candidates'''
    k=10
    firstnet = format(0, '#015b')[2:]
    firstscore = scoredic[firstnet]
    topk_b=[]
    topk_scores=[]
    for i in range(k):
        topk_b.append(firstnet)
        topk_scores.append(firstscore)
    for representation in scoredic.keys():
        score = scoredic[representation]
        for i in range(k):
            if (topk_scores[i] < score):
                topk_scores[i] = score
                topk_b[i] = representation
                break
    
    
    ''' get topk graphs and adjacency matrices'''
    topk_g=[]
    adjs=[]
    for b in topk_b:
        candidate = btog(b,es,g)
        if nx.is_directed_acyclic_graph(candidate)==False:
            print('not DAG!')
        topk_g.append(candidate)
        adj = BSTB.NetworkTo2dMatrix( candidate, var_to_index_dict )
        adjs.append(adj)
    
    
    
    #start_parents, end_thresh, mutate_numb, best_cand_num, bad_reprod_accept, mutate_perc, index_to_vertex 
    children = GA.GeneticRun(   start_parents = adjs, 
                                end_thresh = 1e-6,
                                mutate_numb = 200,  # this number of 1-edge mutations 
                                                    #and same amount of 2-edge mutations
                                best_cand_num = 10,  #10,
                                bad_reprod_accept = 1, #3,
                                index_to_vertex = index_to_var_liste ,
                                method = 'k2',
                                max_itr = 20,
                                )
    
    bestDescendant = children.list[0]
    graph = BSTB.MatrixToNetwork( bestDescendant, index_to_var_liste )
    print(1)
    ug = graph.to_undirected()
    #print(nx.number_connected_components(ug))
   #print(nx.number_strongly_connected_components(g))
   #print(nx.number_weakly_connected_components(g))
    print(0)
    #WriteEdgesToTxt( bestDescendant, index_to_var_liste )
    ToCytoscape( bestDescendant, index_to_var_liste, name = 'aaasenitycheck.csv' )  # name = "Final_structure.csv"