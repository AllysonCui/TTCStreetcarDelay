"""
TTC Station Delay Analysis Script

This script identifies the stations with the highest number of transit delays
and creates a tabular visualization ranking them by frequency.
"""

import polars as pl
import matplotlib.pyplot as plt

data_path = "../data/analysis_data/2025plus_data.csv"
data = pl.read_csv(data_path)

# Count delays by station
station_counts = (
    data.group_by("Station")
    .len()
    .rename({"len": "Record Count"})
    .sort("Record Count", descending=True)
)

# Select top 15 stations with most delays
top_stations = station_counts.head(15)
top_stations = top_stations.with_row_index(name="#", offset=1)

# Convert to pandas for matplotlib table
top_stations_pd = top_stations.to_pandas()

# Create the visualization
plt.figure(figsize=(12, 8))
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# Create and style the table
table = plt.table(
    cellText=top_stations_pd.values,
    colLabels=['#', 'Station', 'Record Count'],
    cellLoc='center',
    loc='center',
    colWidths=[0.1, 0.6, 0.3]
)

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.5)

# Style the table cells
for i, key in enumerate(table._cells):
    if key[0] == 0:  # Header row
        cell = table._cells[key]
        cell.set_facecolor('#f0f0f0')
        cell.set_text_props(weight='bold')
    elif key[1] == 2 and key[0] > 0:  # Record Count column, non-header
        cell = table._cells[key]
        cell.set_facecolor('#f0f0f0')

# Add title and pagination
plt.title('Stations with the highest number of delays:', fontsize=14, pad=20)
total_records = len(station_counts)
plt.figtext(0.5, 0.05, f'1 - 15 / {total_records}', ha='center')

# Save the figure
save_path = "../outputs/06-delay_stations.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)
plt.close()
