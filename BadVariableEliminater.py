import matplotlib.pyplot as plt
import ReadCSV as Rcsv

def CountNonMissingValuesInList( liste ):
    counter = 0
    for i in range( len( liste ) ):
        if ( str( liste[i] ) != "-999" and str( liste[i] ) != "-999.0"):
            counter += 1
    return counter


def GetListNumberOfVarsPatient( dataframe ):
    liste = []
    for index, row in dataframe.iterrows():
        current = list( row )
        liste.append( CountNonMissingValuesInList( current ) )
    return liste

def GetNumberSmallerThan( liste, x ):
    counter = 0
    for i in range( len( liste ) ):
        if ( liste[i] >= x ):
            counter += 1
    return counter

def Plot( dataframe ):
    data = GetListNumberOfVarsPatient( dataframe )
    y_values = []
    bins = [ 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400 ]
    for i in range( len( bins ) ):
        y_values.append( GetNumberSmallerThan( data, bins[i] ) )
    plt.bar( bins, y_values, width = 20 )
    plt.xlabel( 'x: # variables' )
    plt.ylabel( 'y: #patients having at least x variables' ) 
    plt.show()

def GetBadVariablesTup( dataframe, threshhold ):
    bad_vars = []
    for var in dataframe.columns:
        values = dataframe[ var ]
        filled_values = CountNonMissingValuesInList( values )
        if ( filled_values < threshhold ):
            bad_vars.append( (var, filled_values ) )
    
    return bad_vars

def GetBadVarsString( dataframe, threshhold ):
    bad_vars = []
    for var in dataframe.columns:
        values = dataframe[ var ]
        filled_values = CountNonMissingValuesInList( values )
        if ( filled_values < threshhold ):
            bad_vars.append( var )
    
    return bad_vars


def DropBadVars( dataframe, to_file_name , threshhold ):
    to_remove = GetBadVarsString( dataframe, threshhold )
    dataframe.drop( to_remove, inplace = True, axis = 1 )
    dataframe.to_csv( to_file_name )


if __name__ == "__main__":
    dataframe = Rcsv.InitializeData( "CleanedFinalData1.csv" )
    print( len(dataframe.columns) )
    DropBadVars( dataframe, "CleanedFinalData11.csv", 1000 )
    print( len( dataframe.columns ) )
    #bad_vars = GetBadVariables( dataframe, 6000 )
    #print( len( bad_vars ) )
    #f = open( "bad_vars.txt", "w" )
    #for tup in bad_vars:
        #f.write( str( tup ) )
        #f.write('\n')
    #f.close()
