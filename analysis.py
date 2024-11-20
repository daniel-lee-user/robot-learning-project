import matplotlib.pyplot as plt
import numpy as np
import os

cleanup_content = """#!/bin/bash
echo Cleaning up...\n"""
count=0
curr_dir = os.getcwd()
for item in os.listdir(curr_dir):
    if os.path.isdir(os.path.join(curr_dir, item)) and 'eval_' in item:
        count += 1
        data = np.load(item+'/evaluations.npz')
        lst = data.files
        # time, results, ep_length = [], [], []
        # TIME, RESULTS, EP_LENGTH = 0, 1, 2
        

        # Create the figure and first y-axis
        fig, ax1 = plt.subplots()

        # Plot the first line on ax1
        rline, = ax1.plot([t/10000 for t in data['timesteps']], [sum(r)/len(r) for r in data['results']], 'k-', label='Reward')  # Green line
        ax1.set_xlabel('Time (ms)')
        ax1.set_ylabel('Reward', color='k')
        ax1.tick_params(axis='y', labelcolor='k')

        # Create a second y-axis sharing the same x-axis
        ax2 = ax1.twinx()

        # Plot the second line on ax2
        eline, = ax2.plot([t/10000 for t in data['timesteps']], [sum(d)/len(d) for d in data['ep_lengths']], color='gray', linestyle='--', label='Episode Length')  # Blue dashed line
        ax2.set_ylabel('Episode Length', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')


        plt.title('Episode Length and Results vs Time (ms)')
        fig.tight_layout()
        plt.legend([rline, eline], [l.get_label() for l in [rline, eline]])
        fname = f"Graph_{item}"
        fig.savefig(fname)
        cleanup_content += """rm -rf """+fname+""".png\necho """+fname+""" cleared...\n"""

        for d in lst:
            print(f"{fname}: {len(data[d])} {d}")
            print(data[d])
cleanup_content += """echo Done. Goodbye!\nrm -- "$0\""""
with open('cleanup', 'w') as file:
    file.write(cleanup_content)
os.chmod('cleanup', 0o755)