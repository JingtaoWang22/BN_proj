import InitializeGraph as ig
import random
import tools as tools
import ArraySaver as As
import ExpEdgeVisitTracker as ET

def GetProbabilityArray(start, num_nodes, prob_matrix):
    probability = []
    summation = 0
    for i in range(num_nodes):
        prob = prob_matrix[start][i]
        summation += prob
        probability.append(summation)
    return probability

#If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?
#for all random walks

def OneWalk(graph, start, steps, prob_matrix, edgeTracker):
    current = start
    num_nodes = len(graph.vs)
    path = []
    path.append(current)

    end_string = "If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?"

    increment_vector = tools.CreateArrayOfZeros( len( graph.es ) )
    AB_increment_vector = tools.CreateArrayOfZeros( len( graph.es ) )
    BA_increment_vector = tools.CreateArrayOfZeros( len( graph.es ) )

    for i in range(steps):
        prob_array = GetProbabilityArray(current, num_nodes, prob_matrix)
        next_step = tools.RollRandom(prob_array)
        edge_ID = graph.get_eid(current, next_step)
        increment_vector[edge_ID] += 1
        if ( current < next_step ):
            AB_increment_vector[ edge_ID ] += 1
        else:
            BA_increment_vector[ edge_ID ] += 1
        current = next_step
        path.append(current)

    if (graph.vs[current]["clinic_vars"] == end_string):
        edgeTracker.IncrementTrackerFromList( increment_vector )
        edgeTracker.IncrementABVisitsFromList( AB_increment_vector )
        edgeTracker.IncrementBAVisitsFromList( BA_increment_vector )

    return path

       
def TheWalks(g, times, steps, prob_matrix):
    ExpTracker = ET.EdgeVisitTracker( len( g.es ) )
    set_of_paths = []
    for i in range(times):
        start = random.randint(0, len(g.vs)-1)
        path = OneWalk(g, start, steps, prob_matrix, ExpTracker)
        set_of_paths.append(path)
    ExpTracker.PassDataToGraph( g )

    return set_of_paths

def ShowEdges( g , times ):
    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            ID = g.get_eid(h,i)
            if ( g.es[ID]["Time_Visited"] != ([0]*times)):
                print( g.vs[h]["clinic_vars"], end = "--- " )
                print( g.vs[i]["clinic_vars"], end = ": ")
                print( g.es[ID]["Time_Visited"] )


def RunExperiments( g, npy_filename, times, numb_walks, numb_steps, showEdges = False ):
    mutual_Info_Matrix = As.LoadArrayFromFile( npy_filename)
    end_string = "If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?"
    tools.SetNextToItself(end_string, g, mutual_Info_Matrix)

    prob_matrix = ig.InitializeProbabilityMatrix( mutual_Info_Matrix )

    for i in range(times):
        TheWalks( g, numb_walks, numb_steps, prob_matrix )
        print(i)

    if ( ShowEdges ):
        ShowEdges( g, times )


def RunRandomExperiments( g, npy_filename, times, numb_walks, numb_steps, showEdges = False ):
    end_string = "If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?"
    mutual_Info_Matrix = As.LoadArrayFromFile( npy_filename )
    tools.Shuffle2DMatrix( mutual_Info_Matrix )
    tools.SetNextToItself(end_string, g, mutual_Info_Matrix)

    prob_matrix = ig.InitializeProbabilityMatrix( mutual_Info_Matrix )
    for i in range(times):
        TheWalks( g, numb_walks, numb_steps, prob_matrix )
        print(i)
    
    if ( ShowEdges ):
        ShowEdges( g, times )

if __name__ == "__main__":
    g = ig.InitializeGraphFast('CleanedFinalData11.csv')
    RunRandomExperiments( g, "MutualInfoSave11.npy", 10, 1000000, 7)
    

    #RunRandomExperiments( g, "MutualInfoSave1.npy", 20 )