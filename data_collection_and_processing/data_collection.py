import os
import osmnx as ox

def collect_data(city: str, local_graphs_directory: str = 'results/local_graphs'):
    """
    Obtain the graph of the city from OpenStreetMap, as an undirected graph with all its bearings.
    If the graph has already been downloaded, load it from disk.
    Else, download the graph, convert it to an undirected graph, add edge bearings, and save it to disk.

    Parameters:
    - city: the name of the city to download the graph for
    Output:
    - G_with_bearings: the graph of the city with edge bearings
    - File saved to disk: the graph of the city with edge bearings saved to disk
    """
    graphml_path = f'{local_graphs_directory}/{city}.graphml'
    
    if os.path.exists(graphml_path):
        G_with_bearings = ox.load_graphml(graphml_path)
    else:
        G_from_place = ox.graph.graph_from_place(city, network_type="drive")
        G_undirected = ox.convert.to_undirected(G_from_place)
        G_with_bearings = ox.bearing.add_edge_bearings(G_undirected)
        ox.save_graphml(G_with_bearings, filepath=graphml_path)
    
    return G_with_bearings