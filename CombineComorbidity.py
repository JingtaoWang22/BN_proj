import pandas as pd
import ReadCSV as r

def GetCommorbidityCols( dataframe ):
    commorbidities = []
    to_remove = []
    for col in dataframe:
        if ( ("Other comorbidity") in col or ( "Other comorbodity") in col ):
            to_remove.append( col )
            commorbidities.append( list( dataframe[col] ) )
    dataframe.drop( to_remove, inplace = True, axis = 1 )

    return commorbidities

def MergeCommorbidities( commorbidities ):
    combined = []
    for i in range( len( commorbidities[0] ) ):
        total = 0
        for j in range( len( commorbidities ) ):
            if ( str(commorbidities[j][i]) != "-999" ):
                total += 1
        combined.append( total )
    return combined

def CombineCommorbidities( dataframe ):
    to_merge = GetCommorbidityCols( dataframe )
    merged = MergeCommorbidities( to_merge )
    dataframe[ "Number of comorbidities: "] = merged


def MergeInCSV( file , end_file_name ):
    dataframe = r.CreateDataframe( file )
    CombineCommorbidities( dataframe )
    dataframe.to_csv( end_file_name )

if __name__ == "__main__":
    MergeInCSV( "CleanedFinalData.csv", "CleanedFinalData.csv" )