from numpy import size

class EdgeVisitTracker( object ):

    def __init__ ( self, size ):
        self.edgesTotalVisits = [0]*size
        self.edgesABVisits = [0] * size
        self.edgesBAVisits = [0] * size
        self.size = size
    
    def reset( self ):
        self.edges = [0]*self.size

    def IncrementTrackerFromList( self, liste ):
        for i in range( len( liste ) ):
            self.edgesTotalVisits[i] += liste[i]
    
    def IncrementABVisitsFromList( self, liste ):
        for i in range( len( liste ) ):
            self.edgesABVisits[i] += liste[i]

    def IncrementBAVisitsFromList( self, liste ):
        for i in range( len( liste ) ):
            self.edgesBAVisits[i] += liste[i]
    
    def PassDataToGraph( self, g ):
        for i in range( len( self.edgesTotalVisits ) ):
            g.es[i]["Time_Visited"].append( self.edgesTotalVisits[i] )
            g.es[i]["AB"].append( self.edgesABVisits[i] )
            g.es[i]["BA"].append( self.edgesBAVisits[i] )
 