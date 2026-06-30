import json

notebook_path = 'Revisi_code_agriculture.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find cell 2
cell2 = nb['cells'][2]
source = cell2['source']

# Find the split index
split_idx = -1
for i, line in enumerate(source):
    if '# TAHAP 3: SYNTHETIC ANOMALY INJECTION' in line:
        split_idx = i
        break

if split_idx != -1:
    part1 = source[:split_idx]
    part2 = source[split_idx:]
    
    # We will modify cell 2 to be just part 1
    cell2['source'] = part1
    
    # The plot code
    plot_code = [
        "# Visualize Raw vs Smoothed Data (Moving Average)\n",
        "import matplotlib.pyplot as plt\n",
        "import matplotlib.dates as mdates\n",
        "\n",
        "fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)\n",
        "colors = ['green', 'red', 'purple', 'saddlebrown']\n",
        "labels = ['Green (D35)', 'Red (D34)', 'Purple (D33)', 'Brown (D32)']\n",
        "\n",
        "for i, (sensor, color, label) in enumerate(zip(english_sensor_names, colors, labels)):\n",
        "    axes[i].plot(df_final.index, df_final[f'raw_{sensor}'], color='lightgray', label='Raw (Interpolated)', linewidth=1.5)\n",
        "    axes[i].plot(df_final.index, df_final[f'smooth_{sensor}'], color=color, label='Smoothed (MA Window=5)', linewidth=1.5)\n",
        "    axes[i].set_ylabel(label, fontsize=10)\n",
        "    axes[i].legend(loc='upper right')\n",
        "    axes[i].grid(True, alpha=0.3)\n",
        "\n",
        "axes[0].set_title('Raw vs Smoothed Data (Moving Average)', fontsize=14, fontweight='bold')\n",
        "axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%b %H:%M'))\n",
        "fig.tight_layout()\n",
        "plt.show()\n"
    ]
    
    plot_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": plot_code
    }
    
    markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["### Synthetic Anomaly Injection\n"]
    }
    
    part2_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": part2
    }
    
    # Insert new cells after cell 2
    nb['cells'].insert(3, plot_cell)
    nb['cells'].insert(4, markdown_cell)
    nb['cells'].insert(5, part2_cell)
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Notebook modified successfully.")
else:
    print("Split point not found in cell 2.")
