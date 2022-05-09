import numpy as np
import sys

#Compute the average of non nan values of the list, will do this for now in the place of imputation

def NonNanAverage(liste):
    total = 0
    counter = 0
    for i in range(len(liste)):
        if (str(liste[i]) != "-999"):
            total += float(liste[i])
            counter += 1
    return total/counter

# Temporarily "imputes" the nan, this won't be necessary after because of inputation

def CleanMissingValues(liste):
    average = NonNanAverage(liste)
    newlist = []
    for i in range(len(liste)):
        element = liste[i]
        if (str(element) == "-999"):
            element = average
        newlist.append(element)
    return newlist

def NonMissingValuesIndices( liste ):
    indices = []
    for i in range( len( liste ) ):
        if ( liste[i] != -999 ):
            indices.append( i )
    return indices

def GetCompleteValuesFromIndices( liste, indices ):
    values = []
    for i in range( len( indices ) ):
        values.append( liste[ indices[i] ] )
    return values

# this creates the bins necessary for discretizing

def BuildBins( start, end, num_bins ):
    increment = (end - start)/num_bins
    current = start
    bins = []
    while ( current <= end ):
        bins.append( current )
        current += increment
    return bins

# Generate the list of real variables

def IsRealVar( array ):
    for i in range(len(array)):
        if ( type( array[i] ) == float ) and ( array[i] != -999 ):
            return True
    return False


def UpdateDataEntries( liste, indices, completeValues ):
    for i in range( len( completeValues ) ):
        liste[indices[i]] = completeValues[i]

# Generate a list of arrays of discretized known real random variables.

def Discretize( dataEntries, var ):
    discretized = []

    NonNanIndices = NonMissingValuesIndices( dataEntries )
    CompleteValues = GetCompleteValuesFromIndices( dataEntries, NonNanIndices )

    xmax = int( max( CompleteValues ) ) + 1
    xmin = int( min( CompleteValues ) )
    if (var == "Age at arrival:"):
        xmax = 100
        xmin = 0
    bins = BuildBins( xmin, xmax, 10)
    discretized = list( np.digitize( CompleteValues, bins ) )

    UpdateDataEntries( dataEntries, NonNanIndices, discretized )

    return dataEntries

# Check how many possible forms in data in the column of a variable

def CheckHowManyPossibilities(dataframe, variable):
    uniques = set()
    liste = list(dataframe[variable])
    for i in range(len(liste)):
        uniques.add(liste[i])
    return uniques

if __name__ == "__main__":
    print( sys.path)
