import pandas as pd
import matplotlib.pyplot as plt

data_path = "../data/analysis_data/2025plus_data.csv"

# Load the data
data = pd.read_csv(data_path)

# Count delays by station
station_counts = data['Station'].value_counts().reset_index()
station_counts.columns = ['Station', 'Record Count']

# Handle any None or NaN values
station_counts = station_counts.fillna({'Station': 'Unknown'})

# Sort by Record Count in descending order
station_counts = station_counts.sort_values('Record Count', ascending=False)

# Display the top 15 stations with most delays
top_stations = station_counts.head(15)[['Station', 'Record Count']].copy()

# Make a rank column
top_stations.insert(0, '#', range(1, len(top_stations) + 1))

# Set up the figure and plot
plt.figure(figsize=(12, 8))

# Create table with no cells
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# Create the table
table = plt.table(
    cellText=top_stations.values,
    colLabels=['#', 'Station', 'Record Count'],
    cellLoc='center',
    loc='center',
    colWidths=[0.1, 0.6, 0.3]
    # Adjusted widths for the wider station column
)

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.5)

# Color the header row
for i, key in enumerate(table._cells):
    if key[0] == 0:  # Header row
        cell = table._cells[key]
        cell.set_facecolor('#f0f0f0')
        cell.set_text_props(weight='bold')
    # Add gray background to record count column for non-header cells
    elif key[1] == 2 and key[0] > 0:  # Record Count column, non-header
        cell = table._cells[key]
        cell.set_facecolor('#f0f0f0')

# Add title
plt.title('Stations with the highest number of delays:', fontsize=14,
          pad=20)

# Add pagination indicator at the bottom
total_records = len(station_counts)
plt.figtext(0.5, 0.05, f'1 - 15 / {total_records}', ha='center')

# Save the figure
save_path = "../outputs/06-delay_stations.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)

# Print output
print(f"Saved station delays chart to {save_path}")
plt.close()

# Show the first few rows of the data for confirmation
print("\nTop 5 stations with most delays:")
print(top_stations.head())
