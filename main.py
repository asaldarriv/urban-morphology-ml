import os
import time
import osmnx as ox
import pandas as pd

from error_handling.error_logging import log_error

from data_collection_and_processing.data_collection import collect_data
from data_collection_and_processing.data_processing import process_data

from metrics_calculation.plot_generation import generate_plots
from metrics_calculation.metrics_calculation import calculate_metrics

def main():
    # Initialize directories and file lists

    base_directoty_results = 'results'
    os.makedirs(base_directoty_results, exist_ok=True)

    boeing_results_dataframe = pd.read_excel('input/boeing_results.xlsx')
    cities = boeing_results_dataframe['City'].str.lower().str.replace(" ", "_").tolist()

    local_graphs_directory = f'{base_directoty_results}/local_graphs'
    local_graphs_files = [os.path.splitext(filename)[0] for filename in os.listdir(local_graphs_directory) if filename.endswith('.graphml')]

    metrics_directory = f'{base_directoty_results}/metrics'
    metrics_files = [os.path.splitext(filename)[0] for filename in os.listdir(metrics_directory) if filename.endswith('.xlsx')]
    
    plots_directory = f'{base_directoty_results}/plots'
    # plots_files = [os.path.splitext(filename)[0] for filename in os.listdir(plots_directory) if filename.endswith('.png')]

    error_logs_directory = f'{base_directoty_results}/error_logs'
    error_files = [os.path.splitext(filename)[0] for filename in os.listdir(error_logs_directory) if filename.endswith('_error.txt')]

    while len(metrics_files) <= len(cities):

        for city in cities:
            try:
                print(f'Processing {city}...')
                if city in error_files:
                    os.remove(os.path.join(error_logs_directory, f'{city}_error.txt'))
                elif city in local_graphs_files:
                    G_with_bearings = ox.load_graphml(f'{local_graphs_directory}/{city}.graphml')
                else:
                    G_with_bearings = collect_data(city, local_graphs_directory)
                bearings = process_data(G_with_bearings)
                calculate_metrics(city, G_with_bearings, metrics_directory)
                generate_plots(city, G_with_bearings, bearings, plots_directory)
            except Exception as e:
                # TO-DO: How to handle with OpenStreetMap API rate limit exceeded?
                print(f'Error processing {city}: {e}')
                time.sleep(300)
                log_error(city, str(e))
                continue

if __name__ == "__main__":
    main()