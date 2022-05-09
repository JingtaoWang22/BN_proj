import InitializeGraph as ig
import MutualInformation as MInf
import RandomWalk as RW
import tools as tools
import SignificantEdgesToGraph as SEG

def main(times, steps):
    g = ig.InitializeGraph('preliminary_hospitalized.csv')
    MutualInfoMatrix = MInf.InitializeMutualInfoMatrix(g)
    prob_matrix = ig.InitializeProbabilityMatrix(MutualInfoMatrix)
    end_string = "If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?"
    tools.SetNextToItself(end_string, g, prob_matrix)

    RW.TheWalks(g, times, steps, prob_matrix)

    MInf.ShuffleMutualInfo(MutualInfoMatrix)
    prob_matrix = ig.InitializeProbabilityMatrix(MutualInfoMatrix)
    tools.SetNextToItself

    RW.TheWalks(g, times, steps, prob_matrix)

if __name__ == "__main__":
    #main(10, 10)
     g = SEG.SignificantEdgesToGraph( "notcorrectedSorted11005.txt")
     print( g.edges )
     print( type( g.nodes ) )
