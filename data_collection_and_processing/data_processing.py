def process_data(G_with_bearings):
    """
    Return the bearings of the edges of the graph.
    """
    
    bearings = [data['bearing'] for u, v, key, data in G_with_bearings.edges(keys=True, data=True) if 'bearing' in data]
    
    return bearings