import os
import pickle
import numpy as np
import osmnx as ox
import pandas as pd
import matplotlib.pyplot as plt

import time

local_metrics_dir = 'data-collection/local-metrics'
local_metrics_files = [os.path.splitext(filename)[0] for filename in os.listdir(local_metrics_dir) if filename.endswith('.xlsx')]

while len(local_metrics_files) < 100:

    boeing_results_dataframe = pd.read_excel('data-collection/reference-data/boeing_results.xlsx')

    cities: list[str] = boeing_results_dataframe['City'].tolist()

    error_logs_dir = 'data-collection/error-logs'
    error_files = [os.path.splitext(filename)[0] for filename in os.listdir(error_logs_dir) if filename.endswith('_error.txt')]

    local_graphs_dir = 'data-collection/local-graphs'
    local_graphs_files = [os.path.splitext(filename)[0] for filename in os.listdir(local_graphs_dir) if filename.endswith('.graphml')]

    local_metrics_dir = 'data-collection/local-metrics'
    local_metrics_files = [os.path.splitext(filename)[0] for filename in os.listdir(local_metrics_dir) if filename.endswith('.xlsx')]

    local_plots_dir = 'data-collection/local-plots'
    local_plots_files = [os.path.splitext(filename)[0] for filename in os.listdir(local_plots_dir) if filename.endswith('.png')]

    for city in cities:
        try:
            print(f'Processing {city}...')
            city_filename = city.lower().replace(" ", "_")

            graphml_path = f'data-collection/local-graphs/{city_filename}.graphml'
            bearings_path = f'data-collection/local-bearings/{city_filename}.pkl'
            metrics_path = f'data-collection/local-metrics/{city_filename}.xlsx'
            plot_path = f'data-collection/local-plots/{city_filename}.png'
            manual_plot_path = f'data-collection/local-plots/{city_filename}_manual.png'

            if city_filename in local_graphs_files and city_filename in local_metrics_files and city_filename in local_plots_files:
                continue

            G_from_place = ox.graph.graph_from_place(city, network_type="drive")
            G_undirected = ox.convert.to_undirected(G_from_place)
            G_with_bearings = ox.bearing.add_edge_bearings(G_undirected)
            ox.save_graphml(G_with_bearings, filepath=graphml_path)

            # Calculate the metrics
            basic_stats = ox.stats.basic_stats(G_with_bearings)
            unweighted_entropy = ox.bearing.orientation_entropy(G_with_bearings, weight=None)
            weighted_entropy = ox.bearing.orientation_entropy(G_with_bearings, weight='length')
            normalized_orientation_order = 1-((unweighted_entropy-1.386)/(3.584-1.386))**2
            average_circuity = basic_stats['circuity_avg']
            mean_street_segment_length = basic_stats['edge_length_avg']
            average_node_degree = basic_stats['k_avg']
            proportion_of_dead_ends_nodes = basic_stats['streets_per_node_proportions'][1]
            proportion_of_4_w_nodes = basic_stats['streets_per_node_proportions'][4]

            # Create a DataFrame with the metrics
            metrics_df = pd.DataFrame({
                'phi': [normalized_orientation_order],
                'M0': [unweighted_entropy],
                'Mw': [weighted_entropy],
                'i': [mean_street_segment_length],
                'c': [average_circuity],
                'k': [average_node_degree],
                'Pde': [proportion_of_dead_ends_nodes],
                'P4w': [proportion_of_4_w_nodes]
            })

            # Save the DataFrame as an Excel file
            os.makedirs('data-collection/local-metrics', exist_ok=True)
            metrics_df.to_excel(metrics_path, index=False)

            # Save the polar histogram plot
            os.makedirs('data-collection/local-plots', exist_ok=True)
            fig, ax = ox.plot_orientation(G_with_bearings, title=f'{city}')
            plt.savefig(plot_path)
            plt.close()

            # Creates a polar histogram of the bearings manually
            # Extract the bearings
            bearings = [data['bearing'] for u, v, key, data in G_with_bearings.edges(keys=True, data=True) if 'bearing' in data]
            # Generate the polar histogram and save it
            os.makedirs('data-collection/local-plots', exist_ok=True)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='polar')
            bins = np.linspace(0, 2 * np.pi, 36)
            n, bins, patches = ax.hist(np.deg2rad(bearings), bins=bins, alpha=0.75, color='blue')
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_title(f'Polar Histogram of Bearings for {city}')
            ax.set_ylim(0, n.max())
            plt.savefig(manual_plot_path)
            plt.close(fig)

            if f'{city_filename}_error' in error_files:
                os.remove(os.path.join(error_logs_dir, f'{city_filename}_error.txt'))

        except Exception as e:
            print(f'Error processing {city}: {e}')
            time.sleep(300)
            # Save the error to a text file
            error_log_path = f'data-collection/error-logs/{city_filename}_error.txt'
            os.makedirs('data-collection/error-logs', exist_ok=True)
            with open(error_log_path, 'w') as error_file:
                error_file.write(f'Error processing {city}: {e}\n')
            continue