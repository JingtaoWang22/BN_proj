import matplotlib.pyplot as plt
import RandomWalk as RW
import InitializeGraph as ig
import numpy as np
import ArraySaver as AS
import tools as tools

def GetPlotDataFromGraph( g ):
    data = []
    for e in g.es:
        data.append( tools.AverageListValue( e["Time_Visited"] ) )
    AS.ArrayToFile( np.array( data ), "RandomExpData" )
    return data


def GetDirectedDataFromGraph( g, to_filename ):
    data = []
    for e in g.es:
        data.append( [ tools.AverageListValue( e["AB"] ), tools.AverageListValue( e["BA"] ) ] )
    AS.ArrayToFile( np.array( data ), to_filename )
    return data


def PlotEdgeVisits( g , max_val ):
    data = GetPlotDataFromGraph( g )
    plt.hist( data, bins = 100, range = [0, max_val] )
    plt.show()


def PlotEdgeVisitsFromFile( data_file, max_val ):
    data = AS.LoadArrayFromFile( "RandomExpData.npy" )
    plt.hist( data, bins = 100, range = [0, max_val] )
    plt.show()

if __name__ == "__main__":
    g = ig.InitializeGraphFast("CleanedFinalData11.csv")
    RW.RunRandomExperiments( g, "MutualInfoSave11.npy", 10, 1000000, 7 )
    GetDirectedDataFromGraph( g, "RandomDirectedData11" )

    #PlotEdgeVisits( g, 100 )

    #PlotEdgeVisitsFromFile( "RandomExpData.npy", 10 )