import polars as pl
import matplotlib.pyplot as plt

data_path = "../data/analysis_data/2025plus_data.csv"

# Load the data with polars
data = pl.read_csv(data_path)

# Count delays by station
station_counts = (
    data.group_by("Station")
    .len()  # Use len() instead of count() which is deprecated
    .rename({"len": "Record Count"})  # Updated column name
    .sort("Record Count", descending=True)
)

# Handle any None or NaN values
station_counts = station_counts.with_columns(
    pl.when(pl.col("Station").is_null())
    .then(pl.lit("Unknown"))
    .otherwise(pl.col("Station"))
    .alias("Station")
)

# Display the top 15 stations with most delays
top_stations = station_counts.head(15)

# Create a rank column
top_stations = top_stations.with_row_index(name="#", offset=1)

# Convert to pandas for matplotlib table
top_stations_pd = top_stations.to_pandas()

# Set up the figure and plot
plt.figure(figsize=(12, 8))

# Create table with no cells
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# Create the table
table = plt.table(
    cellText=top_stations_pd.values,
    colLabels=['#', 'Station', 'Record Count'],
    cellLoc='center',
    loc='center',
    colWidths=[0.1, 0.6, 0.3]
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
plt.title('Stations with the highest number of delays:', fontsize=14, pad=20)

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
print(top_stations.head(5))
