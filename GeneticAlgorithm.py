import TwoDMatrixIterator as mat
import random
import SortedList as SL
import timeit
import BinaryStringToBayesianN as BSTB
import networkx as nx
def Score( subject ):
    score = 0
    for i in range( len( subject ) ):
        for j in range( len( subject[i]) ):
            if ( subject[i][j] == 1 ):
                score += 1
    return score

def GetBestChildren( matrixListe, numb_to_keep, index_to_vertex , method = 'k2'):
    lList = SL.SortedList( numb_to_keep, index_to_vertex )
    for i in range( len( matrixListe ) ):
        lList.insert( matrixListe[i] , method = method)
    return lList

def MakeNextGen( matrixListe, mutate_numb, numb_to_keep, index_to_vertex,method='k2' ):
    i = 0
    allChildren = []
    for i in range( len( matrixListe )):
        for j in range( len( matrixListe )):
            
            children = mat.Mate( matrixListe[i], matrixListe[j], index_to_vertex )
            
            allChildren += children
            j += 1
        i += 1
    
    s=timeit.default_timer()
    
    mutated_children = []
    for k in range( mutate_numb ):
        flag = 0
        while flag == 0: # keeps mutating until a valid mutation is generated 
            rand = random.randint( 0, len( allChildren ) - 1 )
            mutated = mat.MutateMatrix( allChildren[rand], index_to_vertex, edges = 1 )
        
            graph = BSTB.MatrixToNetwork( mutated, index_to_vertex ).to_undirected()
            if len(list(nx.connected_components(graph))) == 1:
                flag = 1 # valid mutation (1 connected component) is found
                allChildren.append( mutated )
                mutated_children.append(mutated)

    for k in range( mutate_numb ):  # do the same for generating 2-edge mutations
        flag = 0
        while flag == 0: 
            rand = random.randint( 0, len( allChildren ) - 1 )
            mutated = mat.MutateMatrix( allChildren[rand], index_to_vertex, edges = 2)
        
            graph = BSTB.MatrixToNetwork( mutated, index_to_vertex ).to_undirected()
            if len(list(nx.connected_components(graph))) == 1:
                flag = 1 
                allChildren.append( mutated )
                mutated_children.append(mutated)

    
    nexgen = []
    for matrix in allChildren:
        ug = BSTB.MatrixToNetwork( matrix, index_to_vertex ).to_undirected()
        if len(list(nx.connected_components(ug))) == 1:
            nexgen.append(matrix)
            
    t=timeit.default_timer()
    #print(len(nexgen))
    mut_duration = str(t-s)
    #mutated_children
    return GetBestChildren( allChildren, numb_to_keep, index_to_vertex ,method = method),mut_duration

#start_parents are the start candidates
#end_thresh represents the minimum difference % from gen to gen for the algorithm to continue running
#mutate_numb is the number of children that we will mutate every gen
#best_cand_num is the number of best children that we will keep every generation
#mutatePerc is the number of children that we will mutate every generation
def GeneticRun( start_parents, end_thresh, mutate_numb, best_cand_num, bad_reprod_accept, index_to_vertex,method = 'k2',max_itr=100 ):
    f = open( "ScoreByIteration.txt", "w")
    
    difference = 1
    previous_gen_best = -999999.99
    current_bad_reprod = 0
    
    lastGen = GetBestChildren( start_parents, 10, index_to_vertex ,method=method)
    print( lastGen.GetBest() )
    next_Gen = None
    itr=0
    while( True ):
        if itr>max_itr:
            return next_Gen
        itr+=1
        print('start of itr'+str(itr))
        starttime = timeit.default_timer()
        next_Gen,mut_duration = MakeNextGen( lastGen.list, mutate_numb, best_cand_num, index_to_vertex,method=method )
        endtime =  timeit.default_timer()
        print('duration',str(endtime-starttime),'mutation duration',mut_duration)
        best = float(next_Gen.GetBest())
        f.write( str( best ) )
        f.write( "\n")
        print("best", best ,type(best))
        print("previous_gen_best", previous_gen_best, type(previous_gen_best))
        difference = float( best - previous_gen_best )#/previous_gen_best
        # if dont convert to float, the type will be "numpy.float64"
        
        lastGen = next_Gen
        previous_gen_best = best
        print("itr",itr)
        print('difference',difference,type(difference))
        print('end_thresh',end_thresh,type(end_thresh))
        print('current_bad_reprod',current_bad_reprod,type(current_bad_reprod))
        print('bad_reprod_accept',bad_reprod_accept,type(bad_reprod_accept))
        if ( ( difference <= end_thresh ) and (current_bad_reprod >= bad_reprod_accept ) ):
            print(3)
            f.close()
            print(2)
            return next_Gen
        elif ( ( difference <= end_thresh ) and (current_bad_reprod < bad_reprod_accept ) ):
            current_bad_reprod += 1
        else:
            current_bad_reprod = 0



    

    

