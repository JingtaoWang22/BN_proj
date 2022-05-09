import matplotlib.pyplot as plt
import networkx as nx


def ShowGraph( graph ):
    G = graph.to_networkx()
    nx.draw( G, node_size = 50 )
    plt.show()

def ShowGraphNX( graph ):
    nx.draw( graph, node_size = 50 )
    plt.show()
