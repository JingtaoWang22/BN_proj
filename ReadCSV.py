import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Discretization as dis

def InitializeData(data_file):
    patient_data = pd.read_csv(data_file)
    return patient_data

def CreateDataframe( data_file ):
    df = InitializeData( data_file )
    return df

def IncompleteData( row ):
    for i in range( len( row ) ):
        if ( row[i] == -999 ):
            return True
    return False

def CompleteRows( dataframe ):
    id_tracker = {}
    cols  = dataframe.columns

    for index, row in dataframe.iterrows():
        id = dataframe.loc[ index, 'BQC ID' ]
        if ( id not in id_tracker ):
            id_tracker[id] = index
        else:
            original_index = id_tracker[id]
            for col in cols:
                if ( dataframe.loc[ index, col ] == -999 ):
                    dataframe.loc[ index, col ] = dataframe.loc[original_index, col]
        print( index )

def GetToRemoveRows( dataframe ):
    to_remove_rows = []
    for index, row in dataframe.iterrows():
        if ( dataframe["Final COVID status:"].iloc[index] != "Positive" ):
            to_remove_rows.append( index )

    return to_remove_rows


def CompleteData( dataframe, name ):
    CompleteRows( dataframe )
    dataframe.to_csv( name )

def CleanNegativePatients( dataframe, newname ):
    to_remove = GetToRemoveRows( dataframe )
    dataframe.drop( to_remove, inplace=True )
    dataframe.to_csv(newname)

def CleanColumn(liste):
    newlist = []
    for i in range(len(liste)):
        if (str(liste[i]) != str(np.nan)):
            newlist.append(liste[i])
    return newlist

def PlotReals(dataframe):
    age = "Age at arrival:"
    temperature = "Temperature:"
    systolic = "Systolic BP:"
    diastolic = "Diastolic BP:"
    respiratory = "Respiratory rate (associated with BP above):"
    heartRate = "Heart rate (associated with BP above):"

    real_list = [age, temperature, systolic, diastolic, respiratory, heartRate]

    for i in range(len(real_list)):
        currentList = list(dataframe[real_list[i]])
        currentList = CleanColumn(currentList)
        xmax = int(max(currentList)) + 1
        if (i == 0):
            xmax = 100
        xmin = int(min(currentList))
        plt.title(real_list[i])
        plt.hist(currentList, bins = 100, range = [xmin, xmax])
        plt.show()

if __name__ == "__main__":
    data = CreateDataframe("CleanedFinalData1.csv")
    CompleteData( data, "CleanedFinalData1.csv" )

    #CompleteData( data )
    #CleanNegativePatients( data, "CleanedFinalData.csv" )
    #print( " Done ")

    #print( dis.Discretize( data ) )
    #PlotReals(data)
    #PlotReals(data)
    #print(data.head())
    #print(data.shape)

#return (list(patient_data.columns))
#print("bob")
#print(patient_data.loc[1:5])
#InitializeData()
