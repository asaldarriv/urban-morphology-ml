import os
import osmnx as ox
import pandas as pd

def calculate_metrics(city: str, G_with_bearings, metrics_directory: str = 'results/metrics'):
    """"
    Calculate the metrics for the city and save them to disk.
    """

    metrics_path = f'{metrics_directory}/{city}.xlsx'
    
    basic_stats = ox.stats.basic_stats(G_with_bearings)
    unweighted_entropy = ox.bearing.orientation_entropy(G_with_bearings, weight=None)
    weighted_entropy = ox.bearing.orientation_entropy(G_with_bearings, weight='length')
    normalized_orientation_order = 1-((unweighted_entropy-1.386)/(3.584-1.386))**2
    average_circuity = basic_stats['circuity_avg']
    mean_street_segment_length = basic_stats['edge_length_avg']
    average_node_degree = basic_stats['k_avg']
    proportion_of_dead_ends_nodes = basic_stats['streets_per_node_proportions'][1]
    proportion_of_4_w_nodes = basic_stats['streets_per_node_proportions'][4]

    metrics_df = pd.DataFrame({
        'φ': [normalized_orientation_order],
        'Ηo': [unweighted_entropy],
        'Ηw': [weighted_entropy],
        'ĩ': [mean_street_segment_length],
        'ς': [average_circuity],
        'k̅': [average_node_degree],
        'Pde': [proportion_of_dead_ends_nodes],
        'P4w': [proportion_of_4_w_nodes]
    })

    os.makedirs(metrics_directory, exist_ok=True)
    metrics_df.to_excel(metrics_path, index=False)
    
    return metrics_df