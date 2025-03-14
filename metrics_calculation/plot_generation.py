import os
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt

def generate_plots(city: str, G_with_bearings, bearings, plots_directory: str = 'results/plots'):
    plot_path = f'{plots_directory}/{city}.png'
    manual_plot_path = f'{plots_directory}/{city}_manual.png'
    aligned_plot_path = f'{plots_directory}/{city}_aligned.png'
    shifted_plot_path = f'{plots_directory}/{city}_shifted.png'
    aligned_shifted_plot_path = f'{plots_directory}/{city}_aligned_shifted.png'


    os.makedirs(plots_directory, exist_ok=True)
    
    # First plot
    fig, ax = ox.plot_orientation(G_with_bearings, title=f'{city}')
    plt.savefig(plot_path)
    plt.close()

    # Second plot
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

    # Third plot (aligned)
    max_bin_index = np.argmax(n)
    rotation_angle = bins[max_bin_index]
    aligned_bearings = (np.deg2rad(bearings) - rotation_angle) % (2 * np.pi)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    n_aligned, bins_aligned, patches_aligned = ax.hist(aligned_bearings, bins=bins, alpha=0.75, color='green')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(f'Aligned Polar Histogram of Bearings for {city}')
    ax.set_ylim(0, n_aligned.max())
    plt.savefig(aligned_plot_path)
    plt.close(fig)

    # Fourth plot (shifted outward)
    max_height = n.max()
    R = 0.7 * max_height
    total_radius = R + max_height

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    n_shifted, bins_shifted, patches_shifted = ax.hist(np.deg2rad(bearings), bins=bins, alpha=0.75, color='red', bottom=R, align='mid')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(f'Shifted Polar Histogram of Bearings for {city}')

    ax.set_ylim(0, total_radius)
    ax.yaxis.set_visible(False)

    plt.savefig(shifted_plot_path)
    plt.close(fig)

    # Fifth plot (aligned and shifted outward)
    max_height_aligned = n_aligned.max()
    R_aligned = 0.7 * max_height_aligned
    total_radius_aligned = R_aligned + max_height_aligned

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    n_aligned_shifted, bins_aligned_shifted, patches_aligned_shifted = ax.hist(aligned_bearings, bins=bins, alpha=0.75, color='purple', bottom=R_aligned, align='mid')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(f'Aligned and Shifted Polar Histogram of Bearings for {city}')

    ax.set_ylim(0, total_radius_aligned)
    ax.yaxis.set_visible(False)

    plt.savefig(aligned_shifted_plot_path)
    plt.close(fig)