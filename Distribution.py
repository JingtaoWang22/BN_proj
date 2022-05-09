import ArraySaver as AS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from scipy.stats import nbinom
import statsmodels.api as sm
import InitializeGraph as ig
import RandomWalk as RW
import PlotRandomDistribution as PRD
import tools as tools
import copy
import DisplayGraph as DG


def GetDistributionParameters( filename ):
    data = AS.LoadArrayFromFile( filename )
    X = np.ones_like( data )
    res = sm.NegativeBinomial( data, X ).fit( start_params = [ 1,1 ])
    p = 1/( 1 + np.exp( res.params[0] )*res.params[1] )
    n = np.exp( res.params[0] )*p/( 1-p )
    return ( n, p )

def GetDistributionParametersDir( filename ):
    pre_data = AS.LoadArrayFromFile( filename )
    data = tools.TwoDArrayToOneDArray( pre_data )
    X = np.ones_like( data )
    res = sm.NegativeBinomial( data, X ).fit( start_params = [ 1,1 ])
    p = 1/( 1 + np.exp( res.params[0] )*res.params[1] )
    n = np.exp( res.params[0] )*p/( 1-p )
    return ( n, p )


def PlotFil( filename ):
    data = AS.LoadArrayFromFile( filename )
    n, p = GetDistributionParameters( filename )
    x_plot = np.linspace( 0, 50 )
    sns.set_theme()
    ax = sns.distplot( data, kde = False, norm_hist = True, label = "Real Values")
    ax.plot( x_plot, nbinom.pmf( x_plot, n, p ), 'g-', lw=2, label = 'Fitted NB')
    plt.title( "Real vs Fitted NB Distributions" )
    plt.show()


def AddEdgeToSortedArray( edgeTup, edgeTupList ):
    for i in range( len( edgeTupList ) ):
        if ( edgeTup[1] < edgeTupList[i][1] ):
            edgeTupList.insert( i, edgeTup )
            return
    edgeTupList.append( edgeTup )

def WriteEdgeTuplistToTxt( edgeTupList, filename ):
    f = open( filename, "w" )
    for i in range( len( edgeTupList ) ):
        f.write( edgeTupList[i][0] )

    f.close()


def SignificantEdgesToTxt( g, p_values, threshold, out_filename ):
    edgeTups = []
    
    visited = set()
    for h in range( len( g.vs ) ):
        for i in range( len( g.vs ) ):
            ID = g.get_eid( h,i )

            if ( ID in visited ):
                continue
            visited.add( ID )

            if ( p_values[ID][0] < threshold ):
                string = ""
                string += g.vs[h]["clinic_vars"]
                string += "--- "
                string += g.vs[i]["clinic_vars"]
                string += ": "
                string += str( p_values[ID][0] )
                string += ";;;TimesVisited: "
                string += str(g.es[ID]["AB"][0])
                string += "\n"

                to_add = ( string, p_values[ID][0] )
                AddEdgeToSortedArray( to_add, edgeTups )

            if ( p_values[ID][1] < threshold ):
                string = ""
                string += g.vs[i]["clinic_vars"]
                string += "--- "
                string += g.vs[h]["clinic_vars"]
                string += ": "
                string += str( p_values[ID][1] )
                string += ";;;TimesVisited: "
                string += str(g.es[ID]["BA"][0])
                string += "\n"

                to_add = ( string, p_values[ID][1] )
                AddEdgeToSortedArray( to_add, edgeTups )
    WriteEdgeTuplistToTxt( edgeTups, out_filename )


def GetPValues( g, n, p ):
    #p_values = tools.CreateArrayOfZeros( len( g.es ) )
    p_values = []
    for m in range( len( g.es ) ):
        p_values.append( [ 0, 0 ] )

    visited = set()

    for h in range( len( g.vs ) ):
        for i in range( len( g.vs ) ):
            ID = g.get_eid( h,i )

            if ( ID in visited ):
                continue

            p_value1 = 1 - nbinom.cdf( g.es[ID]["AB"][0] , n, p )
            p_value2 = 1 - nbinom.cdf( g.es[ID]["BA"][0] , n, p )

            p_values[ID][0] = p_value1
            p_values[ID][1] = p_value2

    return np.array( p_values )


def FDRCorrection( array, alpha ):
    return sm.stats.multipletests( array, alpha= alpha, method= 'fdr_bh' )

def BonferroniCorrection( array, alpha ):
    return sm.stats.multipletests( array, alpha= alpha, method= 'bonferroni' )



if __name__ == "__main__":
    g = ig.InitializeGraphFast('CleanedFinalData11.csv')
    
    RW.RunExperiments( g, "MutualInfoSave11.npy", 1, 1000000, 7 )

    #DG.ShowGraph()
    
    ( n, p ) = GetDistributionParametersDir( "RandomDirectedData11.npy" )

    p_values = GetPValues( g, n, p )

    bonf_input005 = copy.deepcopy( p_values )
    not_input005 = copy.deepcopy( p_values )

    bonf_input001 = copy.deepcopy( p_values )
    not_input001 = copy.deepcopy( p_values )

    SignificantEdgesToTxt( g, bonf_input005,  0.05/len(g.es), "bonfcorrectedSorted11005.txt")
    SignificantEdgesToTxt( g, not_input005, 0.05, "notcorrectedSorted11005.txt")

    SignificantEdgesToTxt( g, bonf_input001,  0.01/len(g.es), "bonfcorrectedSorted11001.txt")
    SignificantEdgesToTxt( g, not_input001, 0.01, "notcorrectedSorted11001.txt")