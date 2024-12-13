import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Ensure the file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_evaluations_file>")
    sys.exit(1)

file_path = sys.argv[1]

# Check if the file exists
if not os.path.isfile(file_path):
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)

try:
    # Load the data from the specified file
    data = np.load(file_path)
    timesteps = data['timesteps']
    results = data['results']
    ep_lengths = data['ep_lengths']

    # Filter evaluations every 200k timesteps
    filtered_indices = [i for i, t in enumerate(timesteps) if t % 200000 == 0]
    filtered_timesteps = [timesteps[i] for i in filtered_indices]
    filtered_results = [sum(results[i]) / len(results[i]) for i in filtered_indices]
    filtered_ep_lengths = [sum(ep_lengths[i]) / len(ep_lengths[i]) for i in filtered_indices]

    # Create the figure and first y-axis
    fig, ax1 = plt.subplots()

    # Plot the first line on ax1
    rline, = ax1.plot(
        [t for t in filtered_timesteps], 
        filtered_results, 
        'k-', 
        label='Reward'
    )  # Black line
    ax1.set_xlabel('Timesteps')
    ax1.set_ylabel('Reward', color='k')
    ax1.tick_params(axis='y', labelcolor='k')

    # Create a second y-axis sharing the same x-axis
    ax2 = ax1.twinx()

    # Plot the second line on ax2
    eline, = ax2.plot(
        [t for t in filtered_timesteps], 
        filtered_ep_lengths, 
        color='gray', 
        linestyle='--', 
        label='Episode Length'
    )  # Gray dashed line
    ax2.set_ylabel('Episode Length', color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')

    # Add title and legend
    plt.title('Episode Length and Results vs Timesteps')
    fig.tight_layout()
    plt.legend([rline, eline], [l.get_label() for l in [rline, eline]])

    # Save the figure
    fname = os.path.splitext(os.path.basename(file_path))[0] + "_graph.png"
    fig.savefig(fname)
    print(f"Graph saved as '{fname}'")

except Exception as e:
    print(f"Error processing file: {e}")
    sys.exit(1)
